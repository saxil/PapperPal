from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from utils.prompts import QUESTION_ANSWERING_PROMPT
from utils.llm_factory import get_llm

def create_rag_chain(vectorstore, llm_backend, api_key=None):
    """Creates the RAG chain for question answering."""
    prompt = PromptTemplate(
        template=QUESTION_ANSWERING_PROMPT,
        input_variables=["context", "question"]
    )

    llm = get_llm(llm_backend, api_key)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain
