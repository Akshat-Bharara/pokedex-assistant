import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('API_KEY')

genai.configure(api_key=MY_ENV_VAR)

model = genai.GenerativeModel("gemini-1.5-flash")

pokedex_prompt = (
    "You are an intelligent and factual PokéDex AI. Your purpose is to provide accurate "
    "information related to Pokémon. Your primary goal is to provide clear and concise "
    "explanations about various Pokémon, including their stats, types, evolutions, abilities, "
    "and other in-universe data. Stay on-topic and politely refuse to answer unrelated questions. "
    "Now, please answer the following question:\n"
)

# Questions to test the PokéDex
questions = [
    # pokemon related questions
    "What is Pikachu's type and its abilities?",
    "What are the stats of Bulbasaur?",
    
    # non-pokemon related questions
    "What is the capital of France?",
    "Tell me a joke",

]

# Test the API connection by sending the prompt and questions
for question in questions:
    full_prompt = pokedex_prompt + question
    response = model.generate_content(full_prompt)
    print(f"Question: {question}\nResponse: {response.text}\n")
