import os
import PyPDF2
import faiss
from uuid import uuid4
from dotenv import load_dotenv
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

def process_pdf(uploaded_file):
    """Extract text from a PDF file and split it into manageable sections."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    
    return text

def embed_and_store(text):
    """Generate embeddings and store them in the FAISS vector database."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200)
    sections = text_splitter.split_text(text)
    
    embedded_sections = embeddings.embed_documents(sections)
    
    uuids = [str(uuid4()) for _ in range(len(sections))]
    documents = [Document(page_content=section) for section in sections]
    faiss_store.add_documents(documents=documents, ids=uuids)

def add_pdf_to_pokedex(pdf_file):
    """Complete process to add PDF content to the PokéDex."""
    text = process_pdf(pdf_file)
    embed_and_store(text)
    print("PDF has been successfully processed and stored in the PokéDex.")

def query_expertise(question, top_k=2):
    """Retrieve information from the stored expertise based on a query."""
    results = faiss_store.similarity_search(question, k=top_k)
    
    if results:
        print("Here are some insights based on the stored expertise:")
        for result in results:
            print(result.page_content)
    else:
        print("No relevant information found.")

if __name__ == "__main__":
    pdf_path = 'pokemon_stategy.pdf'
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            add_pdf_to_pokedex(pdf_file)
    
    query = 'What are the best strategies for Pokémon battles?'
    query_expertise(query)
    print("Query completed.")
