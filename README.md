# AI PDF Chatbot

A beginner-friendly Retrieval-Augmented Generation (RAG) PDF chatbot.

## Project Structure

```text
ai-pdf-chatbot/
│
├── backend/
│   │
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── data/
│   │   └── uploaded_pdfs/
│   │
│   ├── chroma_db/
│   │
│   ├── services/
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── llm_service.py
│   │
│   └── utils/
│       └── helpers.py
│
├── frontend/
│   │
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│   │
│   ├── public/
│   └── package.json
│
└── README.md
```

## What Each File Does

### `pdf_loader.py`
**Responsibility:** PDF → Extract Text
**Contains:** `load_pdf()`
**Uses:** `PdfReader`

### `text_splitter.py`
**Responsibility:** Text → Chunks
**Contains:** `create_chunks()`
**Uses:** LangChain `RecursiveCharacterTextSplitter`

### `embeddings.py`
**Responsibility:** Chunk → Embedding
**Contains:** `get_embeddings()`
**Uses:** OpenAI Embeddings API

### `vector_store.py`
**Responsibility:** Embedding → Chroma DB
**Contains:** `add_documents()`, `similarity_search()`
**Uses:** Chroma

### `retriever.py`
**Responsibility:** User Question → Find Relevant Chunks
**Contains:** `retrieve_context()`

### `llm_service.py`
**Responsibility:** Context + Question → LLM → Answer
**Contains:** `generate_answer()`

### `app.py`
**Main entry point.**
**Flow:** Upload PDF → Index PDF → Ask Question → Get Answer

---

## Complete Flow

**When project runs:**
```text
User Uploads PDF
          ↓
pdf_loader.py (Extract Text)
          ↓
text_splitter.py (Chunks)
          ↓
embeddings.py (Vectors)
          ↓
vector_store.py (Chroma DB)
```

**Later:**
```text
User Question
          ↓
Embedding
          ↓
Retriever (Top 3 Chunks)
          ↓
LLM Service
          ↓
Final Answer
```

---

## Complete Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS
- Shadcn UI

### Backend
- Python
- FastAPI

### AI
- OpenAI
- LangChain

### Vector Database
- ChromaDB

### PDF Processing
- PyPDF

---

## How Big AI Companies Build Similar Systems

```text
User Upload PDF
        ↓
Next.js Frontend
        ↓
FastAPI Backend
        ↓
PyPDF
        ↓
LangChain Chunking
        ↓
OpenAI Embeddings
        ↓
ChromaDB

When user asks:

Question
    ↓
Embedding
    ↓
Chroma Search
    ↓
Top Chunks
    ↓
GPT
    ↓
Answer
```

---
