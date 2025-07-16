import streamlit as st
import os
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
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    llm_backend = st.selectbox("Choose LLM Backend", ["openai/gpt-3.5-turbo", "ollama/mistral", "openrouter/google/gemini-pro-1.5"])
    api_key = st.text_input("Enter API Key (if not using Ollama)", type="password")
    summarize_button = st.button("Summarize PDF")

# Main chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if uploaded_files:
    # Process the files
    if "vectorstore" not in st.session_state:
        with st.spinner("Processing PDFs..."):
            all_chunks = []
            for uploaded_file in uploaded_files:
                # Save the uploaded file to a temporary location
                temp_dir = "temp"
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                chunks = load_and_chunk_pdf(file_path)
                all_chunks.extend(chunks)

            st.session_state.chunks = all_chunks
            st.session_state.vectorstore = create_vectorstore(all_chunks, llm_backend)
            st.success("PDFs processed successfully!")

    # Summarization
    if summarize_button:
        with st.spinner("Summarizing..."):
            summary = summarize_document(st.session_state.chunks, llm_backend, api_key)
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
            answer = response["result"]
            source_documents = response["source_documents"]

            # Extract page numbers and format them
            page_numbers = []
            for doc in source_documents:
                if "page_number" in doc.metadata:
                    page_numbers.append(str(doc.metadata["page_number"] + 1)) # +1 because page numbers are 0-indexed
            
            if page_numbers:
                answer += f" (Reference: Page(s) {', '.join(page_numbers)})"

            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
