import os
import requests
import faiss
from uuid import uuid4
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
docstore = InMemoryDocstore()
faiss_store = FAISS(
    embedding_function=embeddings.embed_query,
    index=index,
    docstore=docstore,
    index_to_docstore_id={},
)

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
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return ""
    except requests.ConnectionError as e:
        print(f"Connection Error: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def embed_and_store_web_content(content):
    """Generate embeddings for web content and store them in the FAISS vector database."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200)
    sections = text_splitter.split_text(content)
    
    embedded_sections = embeddings.embed_documents(sections)
    
    uuids = [str(uuid4()) for _ in range(len(sections))]
    documents = [Document(page_content=section) for section in sections]
    faiss_store.add_documents(documents=documents, ids=uuids)

def add_web_expertise_to_pokedex(url):
    """Complete process to add web content expertise to the PokéDex."""
    content = fetch_web_content(url)
    
    if content:
        embed_and_store_web_content(content)
        print("Website content has been successfully processed and stored in the PokéDex.")
    else:
        print("No content could be retrieved from the website.")

def query_web_expertise(question, top_k=2):
    """Retrieve information from the stored web expertise based on a query."""
    results = faiss_store.similarity_search(question, k=top_k)
    
    if results:
        print("Here are some insights based on the stored web expertise:")
        for result in results:
            print(result.page_content)
    else:
        print("No relevant information found.")

if __name__ == "__main__":
    website_url = 'https://gamerant.com/pokemon-common-competitive-strategies/'
    add_web_expertise_to_pokedex(website_url)
    
    query = 'Tell me about Bulky Offence'
    if query:
        query_web_expertise(query)
