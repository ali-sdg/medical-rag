
A production-ready **Retrieval-Augmented Generation (RAG)** system for medical documents. Ask questions about clinical guidelines and medical papers get accurate, source-backed answers with zero hallucination.

---

## How It Works

```
PDF Documents → Chunks → Embeddings → Vector Store → Retriever → Prompt → LLM Answer
```

1. **Ingest** medical PDFs and split them into chunks
2. **Embed** each chunk using BioBERT (medical-specialized model)
3. **Store** embeddings in ChromaDB vector database
4. **Retrieve** the most relevant chunks for any question
5. **Generate** a grounded answer using a local LLM (Llama 3.2)

The LLM is instructed to answer **only** from retrieved context — if the answer isn't in the documents, it says so.

---

## Project Structure

```
medical-rag/
├── src/
│   ├── document_loader.py   # PDF ingestion
│   ├── chunker.py           # Text splitting
│   ├── embedder.py          # Embedding generation
│   ├── vector_store.py      # ChromaDB operations
│   ├── retriever.py         # Semantic search
│   ├── llm.py               # LLM prompt & inference
│   ├── evaluator.py         # RAG quality evaluation
│   └── api.py               # FastAPI REST API
├── data/                    # Place PDF files here
├── tests/                   # Automated tests
├── .github/workflows/       # CI/CD with GitHub Actions
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Ollama with `llama3.2:1b` model

### Run with Docker

```bash
# Clone the repository
git clone https://github.com/your-username/medical-rag.git
cd medical-rag

# Add your PDF files to the data/ folder
cp your-medical-papers.pdf data/

# Start all services
docker compose up -d

# Check it's running
curl http://localhost:8000/health
```

### Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the skin complications of diabetes?"}'
```

**Response:**
```json
{
  "question": "What are the skin complications of diabetes?",
  "answer": "Based on the provided documents, skin problems in diabetic patients include pruritus, xerosis, acrochordon, diabetic dermopathy, and acanthosis nigricans...",
  "sources": ["ARI-77-467.pdf"],
  "duration": 4.21
}
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| PDF Parsing | PyMuPDF |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | BioBERT (sentence-transformers) |
| Vector Database | ChromaDB |
| LLM | Llama 3.2 via Ollama |
| API | FastAPI + Uvicorn |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Evaluation | Custom faithfulness & relevancy metrics |

---

## API Reference

### `GET /health`
Check if the API is running.

```json
{"status": "ok", "message": "Medical RAG API is running!"}
```

### `POST /ask`
Ask a medical question.

**Request body:**
```json
{
  "question": "string",
  "n_results": 3
}
```

**Response:**
```json
{
  "question": "string",
  "answer": "string",
  "sources": ["filename.pdf"],
  "duration": 4.21
}
```

---

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

Tests cover: chunking logic, embedding generation, and prompt building.

---

## Local Development (without Docker)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama
ollama serve

# Run the API
uvicorn src.api:app --reload --port 8000
```

---

## Evaluation

The system evaluates answer quality on two metrics:

- **Faithfulness** — Is the answer grounded in the retrieved documents?
- **Relevancy** — Does the answer address the question?

```bash
python3 test_evaluation.py
```

---

## Design Decisions

- **No hallucination by design** — the prompt explicitly forbids answers outside the provided context
- **Local LLM** — no data leaves your machine; suitable for sensitive medical data
- **Modular pipeline** — each component is independently testable and replaceable

---
