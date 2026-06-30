"""Service for generating answers using OpenAI's ChatCompletion API.

The function ``generate_answer`` receives a user question and a list of
retrieved context chunks. It builds a prompt that instructs the model to
answer *only* based on the supplied context – if the answer cannot be
found, the model should explicitly say it does not know.

All configuration (API key and model name) is loaded from ``backend/config.py``.
"""

import openai
from openai import OpenAI
from typing import List
from config import OPENAI_API_KEY, LLM_MODEL

# Configure OpenAI client to point to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY,
)

def generate_answer(question: str, context_chunks: List[str]) -> str:
    """Generate a final answer for ``question`` using ``context_chunks``.

    Args:
        question: The user's natural‑language query.
        context_chunks: List of relevant document fragments.

    Returns:
        The assistant's answer as a plain string.
    """
    # Combine the retrieved chunks into a single context block.
    context_text = "\n\n".join(context_chunks)
    system_prompt = (
        "You are a helpful assistant that answers questions using ONLY the provided context. "
        "If the answer cannot be derived from the context, respond with "
        "'I don't know based on the given document.'"
    )
    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
