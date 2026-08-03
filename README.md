# Contextify

Contextify is a browser-based Retrieval-Augmented Generation (RAG) application that lets users build a personal knowledge base from web pages and YouTube videos. It enables semantic search over indexed content and answers questions using retrieved context instead of relying solely on a large language model.

The project is designed with a modular architecture, making it easy to extend with additional knowledge sources and retrieval strategies.

---

## Features

- Index web pages directly from the browser
- Index YouTube videos using transcript extraction
- Semantic search over stored knowledge
- Context-aware question answering
- Source citations for generated responses
- Persistent vector storage with Qdrant Cloud
- Chrome Extension for quick interaction
- FastAPI backend exposing REST APIs
- Modular RAG pipeline for future extensibility

---

## Architecture

```
Chrome Extension
        │
        ▼
     FastAPI
        │
        ▼
   Knowledge Loader
        │
        ▼
     Chunking
        │
        ▼
    Embeddings
        │
        ▼
  Qdrant Vector DB
        │
        ▼
    Retriever
        │
        ▼
      Gemini
        │
        ▼
      Response
```

---

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain

### AI
- Gemini
- BGE-M3 Embeddings

### Vector Database
- Qdrant Cloud

### Frontend
- Chrome Extension
- JavaScript
- HTML
- CSS

---

## Project Structure

```
contextify/
│
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── extension/
│
├── docs/
│
├── scripts/
│
└── README.md
```

---

## Workflow

1. Select a supported knowledge source.
2. Extract textual content.
3. Split content into chunks.
4. Generate vector embeddings.
5. Store embeddings in Qdrant Cloud.
6. Retrieve relevant context for user queries.
7. Generate grounded responses using Gemini.
8. Display answers with source citations.

---

## Supported Knowledge Sources

- Web Pages
- YouTube Videos

The architecture is designed to support additional sources in the future with minimal changes.

---

## API Endpoints

```
POST /ingest
POST /query
GET  /health
```

---

## Future Improvements

- PDF support
- Markdown support
- GitHub repository indexing
- Documentation website crawling
- Hybrid search
- Reranking
- Conversation history
- Authentication
- Streaming responses

---

## Local Setup

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

```bash
cp .env.example .env
```

Run the backend

```bash
uvicorn app.main:app --reload
```

Load the Chrome Extension in Developer Mode and connect it to the backend.

---

## Design Goals

- Modular architecture
- Extensible ingestion pipeline
- Source-agnostic RAG workflow
- Production-oriented project structure
- Clean separation of concerns

---

## License

This project is licensed under the MIT License.