from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings, OllamaEmbeddings

def create_vectorstore(chunks, embedding_model_name, vectorstore_type="chroma"):
    """Creates a vector store from document chunks."""
    if "openai" in embedding_model_name.lower():
        embedding_function = OpenAIEmbeddings()
    elif "ollama" in embedding_model_name.lower():
        model_name = embedding_model_name.split('/')[-1]
        embedding_function = OllamaEmbeddings(model=model_name)
    else:
        embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model_name)

    if vectorstore_type.lower() == "chroma":
        vectorstore = Chroma.from_documents(chunks, embedding_function)
    elif vectorstore_type.lower() == "faiss":
        vectorstore = FAISS.from_documents(chunks, embedding_function)
    else:
        raise ValueError(f"Unsupported vectorstore type: {vectorstore_type}")

    return vectorstore
