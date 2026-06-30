from openai import OpenAI
from typing import List
from config import OPENAI_API_KEY, EMBEDDING_MODEL

# Configure OpenAI client to point to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY,
)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of strings using OpenRouter.

    Args:
        texts: List of text snippets (chunks).
    Returns:
        List of embedding vectors (list of floats) corresponding to each input.
    """
    # OpenRouter's embeddings API accepts a list of inputs
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
