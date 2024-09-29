import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('API_KEY')

genai.configure(api_key=MY_ENV_VAR)

model = genai.GenerativeModel("gemini-1.5-flash")

image_path = "pikachu.jpg"  

myfile = genai.upload_file(image_path)
print(f"{myfile=}")

content = [
    myfile, 
    "\n\n", 
    "Can you tell me about the pokemon in this photo?"
]

result = model.generate_content(content)
print(f"{result.text=}")


