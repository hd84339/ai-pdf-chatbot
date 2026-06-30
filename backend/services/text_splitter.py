from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Split the raw PDF text into overlapping chunks.

    Args:
        text: The full extracted text from a PDF.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap size to preserve context between chunks.
    Returns:
        A list of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " "],
    )
    return splitter.split_text(text)
