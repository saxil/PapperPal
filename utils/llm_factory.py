from langchain.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain_ollama import OllamaEmbeddings

def get_llm(llm_backend, api_key=None):
    """Factory function to get the LLM instance."""
    if "openai" in llm_backend.lower():
        return ChatOpenAI(model_name=llm_backend, openai_api_key=api_key)
    elif "ollama" in llm_backend.lower():
        model_name = llm_backend.split('/')[-1]
        return ChatOllama(model=model_name)
    else:
        return ChatOpenAI(model_name=llm_backend, openai_api_base="https://openrouter.ai/api/v1", openai_api_key=api_key)

def get_embedding_function(embedding_model_name):
    """Factory function to get the embedding function."""
    if "openai" in embedding_model_name.lower():
        return OpenAIEmbeddings()
    elif "ollama" in embedding_model_name.lower():
        model_name = embedding_model_name.split('/')[-1]
        return OllamaEmbeddings(model=model_name)
    else:
        return SentenceTransformerEmbeddings(model_name=embedding_model_name)
