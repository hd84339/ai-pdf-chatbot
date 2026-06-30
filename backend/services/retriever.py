from .vector_store import similarity_search

def retrieve_context(query: str, top_k: int = 3) -> list:
    """Retrieve the most relevant chunk texts for a user query.

    Args:
        query: The user's question.
        top_k: Number of top chunks to return.
    Returns:
        A list of chunk strings ordered by relevance.
    """
    results = similarity_search(query, k=top_k)
    # Return only the text portion; ignore similarity scores for now.
    return [doc for doc, _ in results]
