# API Instructions

This document provides detailed instructions on how to obtain the required API keys for setting up the Shift Response Bot. You will need access to both the GroupMe API and the Google Gemini AI API.

## GroupMe API Setup

To get the GroupMe API access token, follow these steps:

### Step 1: Create a GroupMe Account
If you don't already have one, create an account on GroupMe:

- Visit [https://groupme.com](https://groupme.com)
- Click on **Sign Up** and follow the instructions to create your account.

### Step 2: Create a GroupMe Developer Account
Once you have a GroupMe account, you need to register as a developer to get an API access token:

1. Go to the [GroupMe Developer Portal](https://dev.groupme.com/).
2. Log in using your GroupMe credentials.
3. Click on **Access Token** on the upper right side of the page.
4. Copy the generated token. This token will be used as your `ACCESS_TOKEN` in the bot.

### Step 3: Create or Find Your Group ID
To get the `GROUP_ID` for the GroupMe group where shift requests will be posted:

1. Create a new group in the GroupMe app or use an existing one.
2. To find the group ID, you need to make an API call:
   - Use the following URL to get a list of your groups, replacing `ACCESS_TOKEN` with your actual token:
     ```
     https://api.groupme.com/v3/groups?token=ACCESS_TOKEN
     ```
   - You can use a tool like [Postman](https://www.postman.com/) or simply run a Python script to get the group information:
     ```python
     import requests

     ACCESS_TOKEN = 'YOUR_GROUPME_API_KEY'
     url = f'https://api.groupme.com/v3/groups?token={ACCESS_TOKEN}'
     response = requests.get(url)
     print(response.json())
     ```
   - Look for the group name in the response and note down the `group_id`.

## Google Gemini API Setup

To use the Google Gemini AI API, follow these steps:

### Step 1: Create a Google Cloud Account
If you don't already have one, create an account on Google Cloud:

- Visit [https://cloud.google.com](https://cloud.google.com)
- Click on **Get Started for Free** and follow the instructions to create your account.
- You may need to add billing information to activate your Google Cloud account.

### Step 2: Enable the Gemini API
Once your Google Cloud account is ready, you need to enable the Gemini API:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. From the **Navigation Menu**, select **APIs & Services** > **Library**.
3. Search for **Gemini API** and click on it.
4. Click **Enable** to enable the Gemini API for your project.

### Step 3: Create an API Key
After enabling the Gemini API, create an API key:

1. In the **APIs & Services** section of the Google Cloud Console, click on **Credentials**.
2. Click on **Create Credentials** and select **API Key**.
3. Copy the generated API key. This key will be used as your `GEMINI_API_KEY` in the bot.

### Step 4: Install Google Generative AI SDK
You need to install the Google Generative AI SDK to interact with the Gemini API:

```sh
pip install google-generativeai
```

## Summary of Configuration
After obtaining both API keys, you should have the following:

- **GroupMe Access Token** (`ACCESS_TOKEN`): Found in the GroupMe Developer Portal.
- **Group ID** (`GROUP_ID`): Retrieved using an API call.
- **Gemini API Key** (`GEMINI_API_KEY`): Created in the Google Cloud Console.

These keys should be added to the Python script `shift_response_bot.py` in the appropriate configuration section.

## Example Configuration
Below is an example of how to add the API keys to the script:

```python
# Configuration
ACCESS_TOKEN = 'YOUR_GROUPME_API_KEY'
GROUP_ID = 'YOUR_GROUPME_GROUP_ID'
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'
```

Make sure to replace the placeholder values with your actual keys.

For security reasons, consider using environment variables instead of hardcoding the API keys in your script, as described in the [README](shift_response_bot_readme.md).

## Troubleshooting
- **Invalid Access Token**: Ensure that you copied the correct token from the GroupMe Developer Portal.
- **API Key Restrictions**: Make sure that your Google Gemini API key is unrestricted or has the correct permissions to access the Gemini API.
- **Billing Issues**: Google Cloud may require valid billing information to use the Gemini API. Check your billing settings if you encounter any issues.

If you encounter any other issues, feel free to open an issue on the GitHub repository for help.

