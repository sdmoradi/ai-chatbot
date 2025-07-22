# 📚 Document-Based AI Chatbot with LangChain + FAISS + Ollama + FastAPI

This is a simple, fast, and lightweight **RAG (Retrieval-Augmented Generation)** chatbot that answers questions **only using your own documents** (PDF or TXT). It uses:

- 🧠 [Ollama](https://ollama.com) for local LLM and embeddings (`phi3`)
- 🔍 [FAISS](https://github.com/facebookresearch/faiss) for vector search
- ⚙️ [LangChain](https://www.langchain.com) for chaining logic
- 🚀 [FastAPI](https://fastapi.tiangolo.com) for RESTful API
- 🐳 Docker + Docker Compose for containerization

---

## 📁 Project Structure

```
├── app/
│   ├── app.py              # FastAPI app (query endpoint)
│   └── ingest.py           # Loads, chunks, embeds, and indexes documents
├── docs/                   # Place your .pdf or .txt files here
│   └── privacy.txt
├── faiss_index/            # FAISS vector index files
│   ├── index.faiss
│   └── index.pkl
├── Dockerfile              # Build image for chatbot
├── docker-compose.yml      # Run Ollama + chatbot together
├── requirements.txt        # Python dependencies
└── README.md               # You are here
```

---

## ⚙️ How It Works

1. `ingest.py` loads all `.pdf` and `.txt` files from `/docs`, splits them into chunks, and embeds them using `phi3` via Ollama.
2. Embeddings are stored in a FAISS vector index.
3. `app.py` runs a FastAPI server with an `/ask` endpoint.
4. Incoming questions are answered **only using the documents** — if the answer is not found, it says:

```
"I don't know based on the provided information."
```

---

## 🚀 Quick Start

### 1. 🧱 Requirements

- Docker
- Docker Compose

### 2. 📂 Add Your Documents

Place `.pdf` or `.txt` files inside the `docs/` folder:

```
docs/
├── privacy.txt
├── terms.pdf
```

### 3. 🐳 Run the App

```bash
docker compose up --build
```

- Ollama runs at `http://localhost:11434`
- Chatbot API runs at `http://localhost:8000`

---

## 📡 Example API Usage

### POST `/ask`

```bash
curl -X POST http://localhost:8000/ask      -H "Content-Type: application/json"      -d '{"question": "What does the privacy policy say about cookies?"}'
```

### Example Response:

```json
{
  "answer": "The privacy policy mentions that cookies are used to improve user experience..."
}
```

If not found:

```json
{
  "answer": "I don't know based on the provided information."
}
```

---

## ✅ Environment Variables

| Variable         | Default               | Description              |
|------------------|------------------------|--------------------------|
| `OLLAMA_BASE_URL`| `http://ollama:11434`  | Ollama backend URL       |

---
## ⚡️ GPU Support (optional)

If you have an NVIDIA GPU (e.g. 3090), you **must** use the `nvidia` runtime in Docker.

### 1. Install NVIDIA Docker Toolkit:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
---

## 📦 Build Notes

Dockerfile builds the app and runs:

```bash
python ingest.py && uvicorn app:app --host 0.0.0.0 --port 8000
```

Ingesting happens **on container startup**, ensuring the latest documents are always indexed.

---

## 📄 License

Apache-2.0 license
---

## ✨ Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Ollama](https://ollama.com)
- [FastAPI](https://fastapi.tiangolo.com)

---

## 🙋‍♂️ Author

Built with ❤️ by [Saeed Moradi]  
GitHub: [@sdmoradi](https://github.com/sdmoradi/)
