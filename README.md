# GroupMe Shift Assistant 

This project is a Python-based bot designed to help automate shift requests from GroupMe. By using GroupMe's API and integrating Google Gemini AI, this bot can monitor a GroupMe group for shift requests, analyze if the shift fits within the user's availability, and respond accordingly. This is especially useful for managing shift exchanges in a collaborative environment.

## Features
- **GroupMe Integration**: Monitors a GroupMe group for incoming shift requests.
- **AI-Powered Analysis**: Uses Google Gemini AI to determine if the shift aligns with your predefined schedule.
- **Automated Responses**: Automatically posts a response if the shift request fits your availability.
- **Human-Readable Scheduling**: Easily configure your availability in a clear, human-readable format.

## Requirements

To run this project, you will need the following:

- Python 3.6+
- GroupMe API access token
- Google Gemini API key
- `requests` Python library
- `google.generativeai` Python library

You can install the necessary libraries by running:

```sh
pip install requests google-generativeai
```

## Setup

### Step 1: Clone the Repository
First, clone the GitHub repository to your local machine:

```sh
git clone https://github.com/yourusername/shift-response-bot.git
cd shift-response-bot
```

### Step 2: Install Dependencies
Make sure you have Python 3.6+ installed. Install the required libraries using:

```sh
pip install requests google-generativeai
```

### Step 3: Configure API Keys and Schedule
Edit the Python script to add your API keys and availability schedule. Open `shift_response_bot.py` in a text editor and replace the placeholder values:

- **GroupMe Access Token**: Replace `'YOUR_GROUPME_API_KEY'` with your GroupMe API key.
- **Group ID**: Replace `'YOUR_GROUPME_GROUP_ID'` with the GroupMe group ID you want to monitor.
- **Gemini API Key**: Replace `'YOUR_GEMINI_API_KEY'` with your Gemini API key.

You also need to define your availability in the `YOUR_SCHEDULE` variable. This schedule is used by the AI to determine if you can take a shift.

### Step 4: Run the Bot
To start the bot, run the following command:

```sh
python shift_response_bot.py
```

The bot will continuously monitor the GroupMe group for shift requests and will respond based on your availability.

## How It Works

1. **Initial Setup**: The bot is configured to connect to both the GroupMe and Gemini APIs.
2. **Message Monitoring**: The bot continuously checks for new messages in the GroupMe group every 10 seconds.
3. **AI Analysis**: When a new shift request message is detected, it is passed to the Gemini AI model for analysis.
4. **Decision Making**: Based on your predefined availability, the AI will decide if the shift is possible for you to take.
5. **Responding**: If the AI determines that you are available, the bot will automatically respond to the GroupMe group, offering to take the shift.

## Functions Overview

### `get_est_now()`
Gets the current time in EST (UTC-5).

### `get_last_groupme_message(group_id, access_token)`
Retrieves the most recent message from the GroupMe group.

### `send_groupme_message(group_id, access_token, message_text)`
Sends a message to the GroupMe group.

### `extract_times_from_message(message_text)`
Uses regular expressions to extract the start and end times from a message.

### `analyze_message_with_gemini(message_text, schedule)`
Uses Google Gemini AI to analyze a shift request and determine if the shift fits within your availability.

### `main()`
The main function that continuously monitors the GroupMe group for shift requests and decides if the bot should respond.

## Running the Bot

To run the bot, execute the script using Python:

```sh
python shift_response_bot.py
```

The bot will continuously run, checking for new messages in the GroupMe group every 10 seconds.

### Environment Variables (Optional)
Instead of hardcoding the API keys and group ID, you can use environment variables for better security. You can set environment variables in your operating system and modify the script to use `os.getenv()` to retrieve them:

```python
ACCESS_TOKEN = os.getenv('GROUPME_API_KEY')
GROUP_ID = os.getenv('GROUPME_GROUP_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

## Notes
- **Time Zone Handling**: The bot uses EST as the time zone. Adjustments may be needed if your shifts are in a different time zone.
- **Debugging**: Debugging statements are provided throughout the code to help understand how the bot is making decisions. You can remove or comment them out as needed.

## Future Improvements
- **Advanced Availability Matching**: Enhance the Gemini AI prompt to handle more complex schedules, such as availability that changes week-to-week.
- **Error Handling**: Add more robust error handling for API requests to avoid the bot crashing due to network issues.
- **Improved Scheduling**: Allow for dynamic scheduling inputs, making it easier to update availability without modifying the code.
- **User Interface**: Develop a simple web or command-line interface to make it easier to configure the bot without editing the code.

## License
This project is open-source under the MIT License. Feel free to use, modify, and distribute it as needed.

## Contributing
If you wish to contribute, please open a pull request or file an issue with your suggestions or bug reports.

## Contact
If you have questions or need support, please open an issue on the GitHub repository.

