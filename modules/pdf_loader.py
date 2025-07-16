import fitz as PyMuPDF
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(file_path, chunk_size=1000, chunk_overlap=200):
    """Loads a PDF, extracts text, and splits it into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    all_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                page_chunks = text_splitter.create_documents(
                    texts=[page_text],
                    metadatas=[{"source": file_path, "page_number": i}]
                )
                all_chunks.extend(page_chunks)
    
    chunks = all_chunks

    return chunks
