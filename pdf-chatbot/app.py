import streamlit as st
import os
from dotenv import load_dotenv
from modules.pdf_loader import load_and_chunk_pdf
from modules.vectorstore import create_vectorstore
from modules.rag_chain import create_rag_chain
from modules.summarizer import summarize_document

load_dotenv()

st.set_page_config(page_title="PaperPal", page_icon="🤖")
st.title("PaperPal: Chat with your PDFs")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    llm_backend = st.selectbox("Choose LLM Backend", ["openai/gpt-3.5-turbo", "ollama/mistral", "openrouter/google/gemini-pro-1.5"])
    api_key = st.text_input("Enter API Key (if not using Ollama)", type="password")
    summarize_button = st.button("Summarize PDF")

# Main chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if uploaded_file is not None:
    # Process the file
    if "vectorstore" not in st.session_state:
        with st.spinner("Processing PDF..."):
            chunks = load_and_chunk_pdf(uploaded_file)
            st.session_state.vectorstore = create_vectorstore(chunks, llm_backend)
            st.success("PDF processed successfully!")

    # Summarization
    if summarize_button:
        with st.spinner("Summarizing..."):
            summary = summarize_document(st.session_state.vectorstore, llm_backend, api_key)
            st.session_state.messages.append({"role": "assistant", "content": summary})
            with st.chat_message("assistant"):
                st.markdown(summary)

    # Chat input
    if prompt := st.chat_input("Ask a question about the PDF"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            rag_chain = create_rag_chain(st.session_state.vectorstore, llm_backend, api_key)
            response = rag_chain({"query": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response["result"]})
            with st.chat_message("assistant"):
                st.markdown(response["result"])
