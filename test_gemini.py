import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("Please set the GOOGLE_GEMINI_API_KEY in your .env file")

# API endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Request headers
headers = {
    'Content-Type': 'application/json'
}

# Request payload
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works in a few words"
                }
            ]
        }
    ]
}

try:
    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an error for bad status codes
    
    # Print the response
    response_data = response.json()
    
    # Extract and print the generated text
    if 'candidates' in response_data and response_data['candidates']:
        text = response_data['candidates'][0]['content']['parts'][0]['text']
        print("\nResponse from Gemini:")
        print("-" * 50)
        print(text)
        print("-" * 50)
    else:
        print("No response content found. Full response:")
        print(json.dumps(response_data, indent=2))
        
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
