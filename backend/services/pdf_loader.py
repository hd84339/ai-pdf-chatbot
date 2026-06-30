import os
from pathlib import Path
from pypdf import PdfReader

def load_pdf(file_path: Path) -> str:
    """Read a PDF file and return its plain text.

    Args:
        file_path: Path to the uploaded PDF.
    Returns:
        Concatenated text of all pages.
    """
    if not file_path.suffix.lower() == ".pdf":
        raise ValueError("File must be a PDF")
    reader = PdfReader(str(file_path))
    # Extract text page by page, handling possible None values
    texts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texts.append(page_text)
    return "\n".join(texts)
