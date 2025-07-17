import os
import hashlib
from langchain.vectorstores import Chroma, FAISS
from utils.llm_factory import get_embedding_function

def create_vectorstore(chunks, embedding_model_name, vectorstore_type="chroma", cache_dir="cache"):
    """Creates a vector store from document chunks, with caching."""
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Generate a unique cache folder name based on the document chunks and embedding model
    m = hashlib.sha256()
    for chunk in chunks:
        m.update(chunk.page_content.encode('utf-8'))
    m.update(embedding_model_name.encode('utf-8'))
    cache_key = m.hexdigest()
    cache_folder = os.path.join(cache_dir, cache_key)

    embedding_function = get_embedding_function(embedding_model_name)

    if os.path.exists(cache_folder):
        if vectorstore_type.lower() == "chroma":
            vectorstore = Chroma(persist_directory=cache_folder, embedding_function=embedding_function)
        elif vectorstore_type.lower() == "faiss":
            vectorstore = FAISS.load_local(cache_folder, embedding_function, allow_dangerous_deserialization=True)
        else:
            raise ValueError(f"Unsupported vectorstore type: {vectorstore_type}")
    else:
        if vectorstore_type.lower() == "chroma":
            vectorstore = Chroma.from_documents(chunks, embedding_function, persist_directory=cache_folder)
            vectorstore.persist()
        elif vectorstore_type.lower() == "faiss":
            vectorstore = FAISS.from_documents(chunks, embedding_function)
            vectorstore.save_local(cache_folder)
        else:
            raise ValueError(f"Unsupported vectorstore type: {vectorstore_type}")

    return vectorstore
