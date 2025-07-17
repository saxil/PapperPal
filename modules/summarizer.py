from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from utils.prompts import SUMMARIZATION_PROMPT
from utils.llm_factory import get_llm

def summarize_document(chunks, llm_backend, api_key=None):
    """Summarizes the document using a map-reduce chain."""
    prompt = PromptTemplate(
        template=SUMMARIZATION_PROMPT,
        input_variables=["text"]
    )

    llm = get_llm(llm_backend, api_key)

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=prompt,
        combine_prompt=prompt
    )

    summary = chain.run(chunks)
    return summary
