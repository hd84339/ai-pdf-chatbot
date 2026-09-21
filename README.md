# AI PDF Chatbot

A beginner-friendly Retrieval-Augmented Generation (RAG) PDF chatbot.

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer and npm
- An OpenAI API key

## How to Run (The Right Method)

To correctly run this application, you must run both the backend (Python FastAPI) and the frontend (React Vite) servers simultaneously in **two separate terminals**.

### Step 1: Configure and Start the Backend

1. Create a file named `.env` inside the `backend` folder and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
2. Open your **first terminal**, navigate to the backend directory, set up the Python virtual environment, and run the server:

   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

   *The backend API will start at `http://127.0.0.1:8000`*

### Step 2: Start the Frontend

1. Open a **second, new terminal** (leave the first one running) and navigate to the frontend directory.
2. Install the Node dependencies and run the development server:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

   *The frontend will start at `http://localhost:5173`*

### Step 3: Use the Application

1. Open your web browser and go to `http://localhost:5173`.
2. Select a PDF file and click **Upload & Index PDF**.
3. Once indexed, you can start asking questions about the document!

---

**Troubleshooting (Windows PowerShell):**
- If you get an error when running `.\.venv\Scripts\activate`, your system might be blocking scripts. Run this command as Administrator in PowerShell to fix it:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- To run the frontend in production mode, use `npm run build` and `npm run preview` in the frontend directory.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/upload-pdf` | Upload and index a PDF file |
| `POST` | `/ask` | Ask a question using `{"question": "..."}` |

FastAPI interactive documentation is available at `http://127.0.0.1:8000/docs` while the backend is running.

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
- Vite
- React
- Tailwind CSS

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
