import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama.llms import OllamaLLM  
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)
app = FastAPI()

class Query(BaseModel):
    question: str

logging.info("Starting FastAPI app...")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
logging.info(f"Connecting to Ollama at: {ollama_base_url}")

# Load LLM
llm = OllamaLLM(model="phi3", base_url=ollama_base_url)

# Load FAISS Vector DB
db = FAISS.load_local(
    "faiss_index",
    OllamaEmbeddings(model="phi3", base_url=ollama_base_url),
    allow_dangerous_deserialization=True
)

# Strict prompt: Only answer from the documents
prompt = PromptTemplate.from_template("""
You are an assistant that only answers questions based on the provided context.

If the answer is not contained in the context, respond:
"I don't know based on the provided information."

Context:
{context}

Question:
{question}
""")

# Create QA chain using the custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

@app.post("/ask")
async def ask_q(q: Query):
    logging.info(f"Received question: {q.question}")
    answer = qa_chain.run(q.question)
    return {"answer": answer}