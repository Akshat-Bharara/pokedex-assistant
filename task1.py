#Task 1
# 1. Set up access to Google’s Gemini API - DONE

# 2. Integrate the API in your development environment :-
# Set up the Google's Gemini Model in your environment
# Test the API connection by sending and receiving a simple response

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('API_KEY')

genai.configure(api_key=MY_ENV_VAR)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Tell me about pokemon in 2 lines")
print(response.text)

