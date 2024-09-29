import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
from uuid import uuid4
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter


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

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
docstore = InMemoryDocstore()
faiss_store = FAISS(
    embedding_function=embeddings.embed_query,
    index=index,
    docstore=docstore,
    index_to_docstore_id={},
)

def get_gemini_response(image):
    """Generate a response based on the image using the Gemini model."""
    if image:
        response = model.generate_content([image])  
    else:
        response = model.generate_content([])  
    return response.text 

def process_pdf(uploaded_file):
    """Extract text from a PDF file and split it into manageable sections."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    
    return text

def embed_and_store(text):
    """Generate embeddings and store them in the FAISS vector database."""
    sections = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200).split_text(text)
    
    embedded_sections = embeddings.embed_documents(sections)
    
    uuids = [str(uuid4()) for _ in range(len(sections))]
    documents = [Document(page_content=section) for section in sections]
    faiss_store.add_documents(documents=documents, ids=uuids)

def fetch_web_content(url):
    """Fetch text content from a web page."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs if para.get_text()])
            return content
        else:
            st.error(f"Failed to retrieve content. Status code: {response.status_code}")
            return ""
    except requests.ConnectionError as e:
        st.error(f"Connection Error: {e}")
        return ""
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""


def embed_web_content(content):
    """Embed fetched web content and store it in the vector database."""
    sections = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200).split_text(content)
    
    embedded_sections = embeddings.embed_documents(sections)
    
    uuids = [str(uuid4()) for _ in range(len(sections))]
    documents = [Document(page_content=section) for section in sections]
    faiss_store.add_documents(documents=documents, ids=uuids)

st.title('AI Powered Pokedex Assistant for Pokedex Trainers')

tab1, tab2, tab3, tab4 = st.tabs(["Text", "Image", "PDF", "Website"])

with tab1:
    st.header("Pokedex chatbot")
    txt = st.text_input("Ask a question: ")
    if txt:
        full_prompt = pokedex_prompt + txt
        response = model.generate_content(full_prompt)
        st.write(response.text)

with tab2:
    st.header("Analyze Pokémon Images")
    image_file = st.file_uploader("Upload a Pokémon image", type=["jpg", "png"])
    if image_file:
        image = Image.open(image_file)
        result = get_gemini_response(image)
        if result:
            st.write(result)
        else:
            st.write("Sorry, there was an error processing your request.")

with tab3:
    st.header("Add Your Expertise to the PokéDex")
    pdf_file = st.file_uploader("Upload your research paper or battle strategy (PDF)", type=["pdf"])
    
    if pdf_file:
        text = process_pdf(pdf_file)
        embed_and_store(text)
        st.success("Your document has been processed and stored successfully!")

    query = st.text_input("Ask about your expertise (e.g., 'What is the best battle strategy for Charizard?')")
    if query:
        results = faiss_store.similarity_search(query, k=2)  
        if results:
            st.write("Here are some insights based on your expertise:")
            for result in results:
                st.write(result.page_content)  
        else:
            st.write("No relevant information found.")

with tab4:
    st.header("Enhance the PokéDex with Online Expertise")
    
    website_url = st.text_input("Provide a URL with Pokémon battle guides or strategies:")
    
    if website_url:
        web_content = fetch_web_content(website_url)
        
        if web_content:
            embed_web_content(web_content)
            st.success("The content has been successfully embedded into the PokéDex Assistant!")
        
    web_query = st.text_input("Ask about the battle strategy you added (e.g., 'How to train a Bulbasaur for competitive battles?')")
    
    if web_query:
        web_results = faiss_store.similarity_search(web_query, k=2)  
        
        if web_results:
            st.write("Based on the expertise from the website, here's what we've found:")
            for result in web_results:
                st.write(result.page_content) 
        else:
            st.write("No relevant information found.")
