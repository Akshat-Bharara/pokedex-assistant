# AI-Powered PokéDex Assistant for Pokémon Trainers

Welcome to the AI-Powered PokéDex Assistant, an advanced, interactive, and intelligent chatbot designed to help Pokémon Trainers on their journey to becoming Pokémon Masters. Using Google's Gemini models and other AI tools, this Assistant can engage in natural conversations, recognize Pokémon images, process research PDFs, and even extract battle strategies from web links. Trainers can rely on this PokéDex to provide real-time insights, strategies, and personalized advice for competitive Pokémon battles.

## Demo video link
- https://drive.google.com/file/d/16dlEI3091-cot8n5CZ9rGBCDuiPKIPMy/view?usp=sharing

## Tasks Completed

1. Task 1: Use Google's Gemini models (free tier) to create the PokéDex Assistant (60 Points) 
    - Created a project and setup API Key in Google Cloud Console
    - Enabled the Generative Language API
    - Setted the Google's Gemini Model 
    - Tested the API connection by sending and receiving a simple response (task1.py)

2. Task 2: Engineer a system prompt to shape the Assistant’s behavior as a PokéDex (80 points)
    - Added a prompt to ensure the chatbot behaves as an intelligent, factual PokéDex resource
    - Ensured that the prompt focuses on delivering clear, concise explanations about Pokémon stats, types, evolutions, and other in-universe data.
    - Incorporated strict guidelines for the Assistant to ignore irrelevant or off-topic questions. For instance, the Assistant should refuse to answer non-Pokémon-related queries politely, such as “What’s the weather?” or “Tell me a joke,” while remaining professional and helpful.

3. Task 3: Add the ability to provide an image as input for the PokéDex Assistant (60 Points)
    - Ensured that the PokéDex Assistant can analyze Pokémon images, like recognizing a Pikachu from a Trainer’s photograph

4. Task 4: Allow Trainers to add their own expertise to the PokéDex via PDF uploads (100 Points)
    - Used Langchain for uploading and splitting Trainer research papers or battle strategies (20 points) 
    - Ensured PDFs can be split into manageable sections for detailed analysis.
    - Used Google’s embeddings API to generate embeddings from Trainer expertise (30 points) 
    - Made sure the PokéDex Assistant accurately represents the knowledge from uploaded documents
    - Stored the embeddings in a vector database - FAISS for future queries (20 points) 
    - Allowed the PokéDex Assistant to reference and access this expertise when Trainers ask related questions
    - Extracted the embeddings and use them to respond to queries (30 points)

5. Task 5: Allow Trainers to add their expertise through a website link (100 Points)
    - Used Langchain to retrieve and process Pokémon battle guides or strategy articles from the link provided by the Trainer (20 points)
    - Used Google’s embeddings API to generate embeddings from the fetched content (30 points) 
    - Ensured the PokéDex Assistant can analyze and store this knowledge for later use
    - Stored the embeddings in a vector database (20 points) 
    - Ensured the PokéDex Assistant can efficiently access and provide answers based on this new expertise
    - Extract and use the stored embeddings to respond to queries (30 points)

6. Task 6: Build a user-friendly front-end using Streamlit (80 points)
    - Designed a user-friendly interface for Trainers to interact with the PokéDex Assistant (50 points) 
    - Ensured the interface supports text, image, PDF, and website link inputs from Trainers
    - Tested the interface for usability, ensuring it’s intuitive for Trainers of all levels (30 points)
    
## Features

1. **Conversational AI**: Engage with the Assistant using natural language to inquire about Pokémon stats, evolutions, types, battle strategies, and more.
2. **Image Recognition**: Upload Pokémon images to identify the species and obtain detailed information.
3. **PDF Upload**: Add your own battle strategies or research papers, which are embedded and stored for personalized advice.
4. **Website Link Integration**: Retrieve and process Pokémon battle guides from website links provided by Trainers to expand the Assistant's knowledge.
5. **Responsive UI**: Built with Streamlit, the interface supports text, image, PDF, and website link inputs, making it user-friendly for Trainers of all experience levels.

## Tech Stack

- **Programming Language**: Python
- **AI/ML Tools**: Google’s Gemini Models, Langchain
- **Vector Database**: FAISS
- **Front-end**: Streamlit
- **Web Scraping**: BeautifulSoup
- **PDF Processing**: PyPDF2

## Requirements

- Python 3.8+
- Google Cloud API Key with access to Gemini and Generative Language APIs
- The following Python packages (listed in `requirements.txt`):


## Getting Started

### 1. Google Cloud Setup

1. Create a project on [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Generative Language API** for your project.
3. Generate an API Key and save it for later.

### 2. Environment Setup

1. Clone the repository:
 ```bash
git clone https://github.com/your-username/pokedex-assistant.git

cd pokedex-assistant

pip install -r requirements.txt

```

Create a .env file in the root directory and add your Google API key
```bash
API_KEY=your-google-api-key
GOOGLE_APPLICATION_CREDENTIALS = path-to-credentials-json
```

For running: 
```bash
streamlit run app.py
```
