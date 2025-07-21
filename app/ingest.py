import os
import logging
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

logging.basicConfig(level=logging.INFO)

docs_path = "/app/data"
documents = []

logging.info("Loading documents from /app/data")
for filename in os.listdir(docs_path):
    path = os.path.join(docs_path, filename)
    if filename.endswith(".pdf"):
        logging.info(f"Loading PDF: {filename}")
        documents.extend(PyPDFLoader(path).load())
    elif filename.endswith(".txt"):
        logging.info(f"Loading TXT: {filename}")
        documents.extend(TextLoader(path).load())

if not documents:
    raise ValueError("No documents found!")

logging.info("Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

logging.info("Generating embeddings with Ollama...")
embeddings = OllamaEmbeddings(
    model="phi3",
    base_url="http://ollama:11434"
)

db = FAISS.from_documents(chunks, embeddings)
db.save_local("faiss_index")
logging.info("FAISS index saved.")