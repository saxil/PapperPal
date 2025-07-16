from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from utils.prompts import SUMMARIZATION_PROMPT

def summarize_document(chunks, llm_backend, api_key=None):
    """Summarizes the document using a map-reduce chain."""
    prompt = PromptTemplate(
        template=SUMMARIZATION_PROMPT,
        input_variables=["text"]
    )

    if "openai" in llm_backend.lower():
        llm = ChatOpenAI(model_name=llm_backend, openai_api_key=api_key)
    elif "ollama" in llm_backend.lower():
        model_name = llm_backend.split('/')[-1]
        llm = ChatOllama(model=model_name)
    else:
        llm = ChatOpenAI(model_name=llm_backend, openai_api_base="https://openrouter.ai/api/v1", openai_api_key=api_key)

    chain = load_summarize_chain(
        llm,
        chain_type="stuff",
        prompt=prompt
    )

    summary = chain.run(chunks)
    return summary
