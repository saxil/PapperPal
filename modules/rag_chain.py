from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI, ChatOllama
from utils.prompts import QUESTION_ANSWERING_PROMPT

def create_rag_chain(vectorstore, llm_backend, api_key=None):
    """Creates the RAG chain for question answering."""
    prompt = PromptTemplate(
        template=QUESTION_ANSWERING_PROMPT,
        input_variables=["context", "question"]
    )

    if "openai" in llm_backend.lower():
        llm = ChatOpenAI(model_name=llm_backend, openai_api_key=api_key)
    elif "ollama" in llm_backend.lower():
        model_name = llm_backend.split('/')[-1]
        llm = ChatOllama(model=model_name)
    else:
        # Assuming OpenRouter format, which is compatible with OpenAI's API
        llm = ChatOpenAI(model_name=llm_backend, openai_api_base="https://openrouter.ai/api/v1", openai_api_key=api_key)


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain
