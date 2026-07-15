import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Tuple
from config import CHROMA_DB_PATH, EMBEDDING_MODEL

# Initialise a persistent Chroma client. The DB will be stored in the path defined by CHROMA_DB_PATH.
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Use an OpenAI embedding function for consistency; however, we will supply explicit vectors when adding.
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=None,  # Not needed because we provide embeddings directly.
    model_name=EMBEDDING_MODEL,
)

def get_collection(name: str = "pdf_chunks"):
    """Retrieve or create a Chroma collection for PDF chunks.

    Args:
        name: Collection name (default "pdf_chunks").
    Returns:
        A Chroma collection object.
    """
    return client.get_or_create_collection(name=name, embedding_function=embedding_fn)

def add_documents(texts: List[str], embeddings: List[List[float]]) -> None:
    """Add chunk texts and their pre‑computed embeddings to the vector store.

    Args:
        texts: List of chunk strings.
        embeddings: Corresponding list of embedding vectors.
    """
    collection = get_collection()
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
    )

def similarity_search(query: str, k: int = 3) -> List[Tuple[str, float]]:
    """Search the collection for the *k* most similar chunks to the query.

    The function converts the query to an embedding using our custom
    get_embeddings function and lets Chroma compute cosine similarity internally.

    Returns:
        A list of (chunk_text, similarity_score) pairs, ordered by relevance.
    """
    from services.embeddings import get_embeddings
    collection = get_collection()
    query_embedding = get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    # Chroma returns parallel lists: documents and distances (where distance = 1 - cosine similarity).
    docs = results["documents"][0]
    distances = results["distances"][0]
    # Convert distance to similarity (higher is better).
    similarities = [1 - d for d in distances]
    return list(zip(docs, similarities))
