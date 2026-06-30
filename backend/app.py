"""Backend entry point defining FastAPI routes for PDF upload and question answering.

The API consists of two endpoints:
- ``/upload-pdf``: Accepts a PDF file, extracts text, chunks it, creates embeddings, and stores them in Chroma.
- ``/ask``: Takes a JSON body with a ``question`` field, retrieves the top‑k relevant chunks, and generates an answer via OpenAI.

All heavy‑lifting is delegated to the service modules under ``backend/services``.
"""

import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Import service functions (relative imports because ``backend`` is a package)
from services.pdf_loader import load_pdf
from services.text_splitter import create_chunks
from services.embeddings import get_embeddings
from services.vector_store import add_documents
from services.retriever import retrieve_context
from services.llm_service import generate_answer

app = FastAPI(title="PDF RAG Chatbot API")

# Enable CORS so the React frontend can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store uploaded PDFs
UPLOAD_DIR = Path(__file__).resolve().parent / "data" / "uploaded_pdfs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF upload and indexing.

    The uploaded file is saved to ``uploaded_pdfs`` and then processed:
    1. Extract raw text.
    2. Split into overlapping chunks.
    3. Generate embeddings for each chunk.
    4. Store both text and embeddings in Chroma.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    file_path = UPLOAD_DIR / file.filename
    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # Process the PDF
    raw_text = load_pdf(file_path)
    chunks = create_chunks(raw_text)
    embeddings = get_embeddings(chunks)
    add_documents(chunks, embeddings)
    return JSONResponse(content={"message": "PDF indexed successfully", "num_chunks": len(chunks)})

@app.post("/ask")
async def ask_question(payload: dict):
    """Answer a user query using retrieved context.

    Expected JSON payload: ``{"question": "Your question here"}``
    """
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="'question' field is required.")
    # Retrieve top‑k relevant chunks from Chroma
    context_chunks = retrieve_context(question, top_k=3)
    # Generate the final answer using the LLM
    answer = generate_answer(question, context_chunks)
    return JSONResponse(content={"answer": answer, "retrieved_chunks": context_chunks})

if __name__ == "__main__":
    # This allows you to run the server using `python app.py`
    print("Starting backend server...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
