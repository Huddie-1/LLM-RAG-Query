# 📦 RAGStack GPT — Intelligent Query Engine

> A production-grade Retrieval-Augmented Generation (RAG) system that lets you upload private documents and query them using a large language model — powered by Groq, LangChain, ChromaDB, and FastAPI.

🚀 **Live Demo:** [huddie-1-ragstack-gpt.hf.space](https://huggingface.co/spaces/Huddie-1/ragstack-gpt)

---

## 🎯 What This Project Does

RAGStack lets you upload your own documents (PDF, TXT, MD, CSV) and ask questions about them in natural language. Instead of relying solely on an LLM's training data, the system **retrieves relevant chunks from your documents** and uses them as context for the answer — this is called Retrieval-Augmented Generation (RAG).

## 🚀 Features

- 📄 **Document Upload** — Upload PDF, TXT, MD, and CSV files via a clean web UI
- 🔍 **Semantic Search** — Uses HuggingFace embeddings (`all-MiniLM-L6-v2`) to find the most relevant document chunks
- 🤖 **LLM-Powered Answers** — Queries answered by Llama 3.3 70B via Groq's free API
- 📊 **Source Attribution** — Every answer shows which document chunks were retrieved
- 📡 **Kafka Event Logging** — Query metadata published to a Kafka topic (`query-events`) for downstream analytics
- 🧩 **MCP Metadata** — Each query wrapped with structured metadata (request ID, user ID, timestamp, model version)
- ⚡ **Production-Ready API** — FastAPI backend with CORS, error handling, and a `/health` endpoint
- 🎨 **Custom Chat UI** — Dark blue chat interface served via HTTP, no framework needed

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq API — Llama 3.3 70B |
| RAG Orchestration | LangChain + LangChain Classic |
| Vector Database | ChromaDB (local) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (runs locally, free) |
| Web Framework | FastAPI + Uvicorn |
| Event Streaming | Apache Kafka (`kafka-python`) |
| PDF Parsing | PyPDF |
| Frontend | Vanilla HTML/CSS/JS (dark blue chat UI) |
| Environment | Python 3.13, virtualenv |

---

## 📁 Project Structure

```
LLM-RAG-Query-LoggerWithKafka/
├── main.py              # FastAPI app — /query, /upload, /health endpoints
├── rag_engine.py        # Full RAG pipeline — embeddings → retrieval → LLM
├── mcp.py               # Metadata Control Protocol — wraps each query
├── kafka_producer.py    # Publishes query events to Kafka topic
├── ingest.py            # One-time script to seed ChromaDB with sample docs
├── ragstack_ui.html     # Chat UI — served via Python HTTP server
├── requirements.txt     # All Python dependencies
├── .env.example         # Sample environment variables
└── README.md
```

---

## 🔬 How It Works — Query Flow

```
User types question
        ↓
FastAPI /query endpoint
        ↓
HuggingFace embeddings converts question → vector
        ↓
ChromaDB retrieves top-3 most similar document chunks
        ↓
LangChain assembles prompt: [context chunks] + [question]
        ↓
Groq API (Llama 3.3 70B) generates answer
        ↓
MCP packages metadata (request_id, doc_ids, model version)
        ↓
Kafka publishes event to query-events topic
        ↓
Answer + sources returned to UI
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/huddie-1/LLM-RAG-Query.git
cd LLM-RAG-Query
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
Get a free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Seed the vector database (first time only)
```bash
python ingest.py
```

### 6. Start the API server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Serve the UI (separate terminal)
```bash
python3 -m http.server 5500
```

### 8. Open in browser
```
http://localhost:5500/ragstack_ui.html
```

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/query` | Submit a question, get an answer + sources |
| `POST` | `/upload` | Upload a document (PDF, TXT, MD, CSV) |
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |

### Example `/query` request
```json
POST /query
{
  "question": "What is Retrieval-Augmented Generation?",
  "user_id": "demo"
}
```

### Example response
```json
{
  "answer": "RAG combines a retrieval system with a language model...",
  "sources": ["doc1", "doc2"],
  "metadata": {
    "request_id": "abc-123",
    "timestamp": "2026-06-07T10:33:00Z",
    "model_version": "llama-3.3-70b-versatile"
  }
}
```

---

## ⚠️ Portfolio Demo Note

This project is configured as a **local portfolio demonstration**. Documents uploaded during a session are stored in ChromaDB on disk and will persist between restarts locally. In a cloud deployment (e.g. Hugging Face Spaces), the vector store resets on each restart — this is expected behaviour for a stateless demo environment.

For production use with persistent document storage, replace ChromaDB with a managed vector database such as Pinecone or Weaviate.

---

## 🔮 Planned Improvements

- [x] Deploy to Hugging Face Spaces — [live here](https://huggingface.co/spaces/Huddie-1/ragstack-gpt)
- [ ] Replace ChromaDB with Pinecone for persistent cloud storage
- [ ] Add Prometheus + Grafana observability dashboard
- [ ] Add Loki for centralized log aggregation
- [ ] Support multi-user sessions
- [ ] Add streaming responses (SSE)
- [ ] OCR support for scanned PDFs

---

## 👨‍💻 Author

**Hudson Monanda**
- GitHub: [@huddie-1](https://github.com/huddie-1)
- Portfolio: [huddie-1.github.io/portifolio](https://huddie-1.github.io/portifolio)
- LinkedIn: [Hudson Monanda](https://linkedin.com/in/hudson-monanda)

---

## 📄 License

MIT License — free to use, modify, and distribute.