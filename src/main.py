import time
import requests  # For making API calls to GroupMe
import uuid  # For generating unique identifiers for messages
import os  # To handle environment variables if needed
import google.generativeai as genai  # For accessing the Gemini API
from datetime import datetime, timedelta, timezone  # To handle time-related operations
import re  # For extracting times from text using regular expressions

# Configuration
ACCESS_TOKEN = 'INSERT API KEY'  # GroupMe API access token
GROUP_ID = 'INSERT GROUP ID'  # GroupMe group ID where shift requests are posted
GEMINI_API_KEY = 'INSERT API KEY'  # Gemini API key for AI model interaction

# Define your availability schedule in a human-readable format
YOUR_SCHEDULE = """
I am available to take shifts during the following times:
- Monday: 2pm to 10pm
- Tuesday: 6pm to 9pm
- Wednesday: 7pm to 9pm
- Thursday: 5pm to 10pm
- Friday: 4pm to 10pm
- Saturday: 10am to 10pm
- Sunday: 10am to 10pm
"""

# Initialize the Gemini API model using the provided API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get the current time in EST (Eastern Standard Time), which is UTC-5
def get_est_now():
    return datetime.now(timezone.utc) - timedelta(hours=5)

# Function to retrieve the most recent message from the GroupMe group
def get_last_groupme_message(group_id, access_token):
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages?token={access_token}&limit=1'
    response = requests.get(url)  # Make a GET request to GroupMe API to get the latest message
    messages = response.json()  # Parse the response as JSON
    if 'response' in messages and 'messages' in messages['response']:
        return messages['response']['messages'][0]  # Return the most recent message
    else:
        return None  # Return None if no message is found

# Function to send a message to the GroupMe group
def send_groupme_message(group_id, access_token, message_text):
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages?token={access_token}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "message": {
            "source_guid": str(uuid.uuid4()),  # Generate a unique identifier for each message
            "text": message_text  # The text of the message to send
        }
    }
    response = requests.post(url, json=data, headers=headers)  # Send the message using a POST request
    return response.json()

# Function to extract start and end times from a message using regular expressions
def extract_times_from_message(message_text):
    time_pattern = re.compile(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*to\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', re.IGNORECASE)
    match = time_pattern.search(message_text)
    if match:
        start_hour = int(match.group(1))
        start_minute = int(match.group(2)) if match.group(2) else 0
        start_period = match.group(3).lower() if match.group(3) else 'pm'
        end_hour = int(match.group(4))
        end_minute = int(match.group(5)) if match.group(5) else 0
        end_period = match.group(6).lower() if match.group(6) else 'pm'

        # Convert 12-hour format to 24-hour format
        if start_period == 'pm' and start_hour != 12:
            start_hour += 12
        if start_period == 'am' and start_hour == 12:
            start_hour = 0
        if end_period == 'pm' and end_hour != 12:
            end_hour += 12
        if end_period == 'am' and end_hour == 12:
            end_hour = 0

        return start_hour, start_minute, end_hour, end_minute
    return None, None, None, None  # Return None if no valid time is found

# Function to analyze a shift request message with the Gemini AI model
def analyze_message_with_gemini(message_text, schedule):
    est_now = get_est_now()  # Get the current EST time
    est_tomorrow = est_now + timedelta(days=1)  # Calculate tomorrow's date in EST

    # Generate a prompt for Gemini AI to decide if the shift request fits within your availability
    prompt = (
        f"A GroupMe message was received asking for someone to take a shift. "
        f"The message is: '{message_text}'.\n"
        f"Today is {est_now.strftime('%A')}. If the message references 'tomorrow', interpret it as the next day ({est_tomorrow.strftime('%A')}).\n"
        f"My availability is as follows:\n{schedule}\n"
        f"Can I take this shift based on my availability? Respond with 'Yes' or 'No' and provide a reason if necessary."
    )

    response = model.generate_content(prompt)  # Ask the Gemini model to analyze the message
    
    print("Full response from Gemini API:", response)  # Debugging: Print the full response for verification
    return response.text.strip() if response.text else "No response from Gemini API"

# Main function to continuously check GroupMe messages and respond to shift requests
def main():
    last_checked_message_id = None  # Store the ID of the last checked message
    last_checked_timestamp = get_est_now() - timedelta(seconds=60)  # Start checking from 60 seconds ago

    while True:
        last_message = get_last_groupme_message(GROUP_ID, ACCESS_TOKEN)  # Get the most recent message
        if last_message:
            # Convert the message timestamp to EST
            message_timestamp = datetime.fromtimestamp(last_message['created_at'], timezone.utc) - timedelta(hours=5)
            
            # Check if the message is new
            if last_message['id'] != last_checked_message_id and message_timestamp > last_checked_timestamp:
                print("Last message:", last_message['text'])

                # Use Gemini API to analyze the message and determine if you can take the shift
                decision = analyze_message_with_gemini(last_message['text'], YOUR_SCHEDULE)
                print("Decision from Gemini API:", decision)  # Debugging: Print the decision
                
                # If the AI decides you can take the shift
                if decision.lower().startswith('yes'):
                    # Extract shift times from the message
                    start_hour, start_minute, end_hour, end_minute = extract_times_from_message(last_message['text'])
                    if start_hour is not None and end_hour is not None:
                        start_time = message_timestamp.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
                        end_time = message_timestamp.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
                    
                        # Send a response to the GroupMe group saying you can take the shift
                        new_message_text = f"I can take it."
                        response = send_groupme_message(GROUP_ID, ACCESS_TOKEN, new_message_text)
                        print(response)
                    else:
                        print("Could not extract times from the message.")
                else:
                    print("The shift does not fit into your schedule or other reason.")

                # Update the last checked message ID and timestamp
                last_checked_message_id = last_message['id']
                last_checked_timestamp = message_timestamp

        # Sleep for 10 seconds before checking for new messages again
        time.sleep(10)

if __name__ == "__main__":
    main()
