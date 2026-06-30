import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve the project root (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env placed in the backend folder
ENV_PATH = BASE_DIR / "backend" / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Required OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in .env file")

# Optional configuration with sensible defaults for OpenRouter
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(BASE_DIR / "backend" / "chroma_db"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

# Ensure the Chroma DB directory exists
Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)

# Exported names for other modules
__all__ = [
    "OPENAI_API_KEY",
    "CHROMA_DB_PATH",
    "EMBEDDING_MODEL",
    "LLM_MODEL",
]
