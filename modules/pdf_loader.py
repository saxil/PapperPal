import fitz as PyMuPDF
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(file_path, chunk_size=1000, chunk_overlap=200):
    """Loads a PDF, extracts text, and splits it into chunks."""
    # Using pdfplumber for robust text extraction
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)

    # Using PyMuPDF for metadata (like page numbers)
    doc = PyMuPDF.open(file_path)
    pages = [page.get_text() for page in doc]
    doc.close()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.create_documents(
        texts=[text],
        metadatas=[{"source": file_path, "page_number": i} for i, page_text in enumerate(pages)]
    )

    return chunks
