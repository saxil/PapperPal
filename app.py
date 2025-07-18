import streamlit as st
import os
import json
from dotenv import load_dotenv
from modules.file_loader import load_and_chunk_file
from modules.vectorstore import create_vectorstore
from modules.rag_chain import create_rag_chain
from modules.summarizer import summarize_document
from utils.llm_factory import get_llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.prompts import ELI5_PROMPT, GENERATE_QUESTIONS_PROMPT, ENTITY_EXTRACTION_PROMPT

load_dotenv()

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="PaperPal", page_icon="🤖")
st.title("PaperPal: Chat with your Documents")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "pptx", "docx"], accept_multiple_files=True)
    url_input = st.text_input("Or enter a URL to load from the web")
    llm_backend = st.selectbox("Choose LLM Backend", ["openai/gpt-3.5-turbo", "ollama/mistral", "openrouter/google/gemini-pro-1.5"])
    api_key = st.text_input("Enter API Key (if not using Ollama)", type="password")
    summarize_button = st.button("Summarize Document")
    clear_chat_button = st.button("Clear Chat")

    st.header("Export")
    st.download_button(
        label="Export Chat",
        data="\n".join([f"{message['role']}: {message['content']}" for message in st.session_state.messages]),
        file_name="chat_history.txt",
        mime="text/plain",
    )
    if "summary" in st.session_state:
        st.download_button(
            label="Export Summary",
            data=st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain",
        )

    st.header("Chat History")
    chat_history_name = st.text_input("Save chat history as:")
    save_chat_history_button = st.button("Save Chat History")
    load_chat_history_option = st.selectbox("Load chat history:", ["None"] + os.listdir("chat_histories") if os.path.exists("chat_histories") else ["None"])

    st.header("Smart Features")
    generate_questions_button = st.button("Generate Questions")
    extract_entities_button = st.button("Extract Entities")


if save_chat_history_button and chat_history_name:
    if not os.path.exists("chat_histories"):
        os.makedirs("chat_histories")
    with open(os.path.join("chat_histories", f"{chat_history_name}.json"), "w") as f:
        json.dump(st.session_state.messages, f)
    st.success(f"Chat history saved as {chat_history_name}.json")

if load_chat_history_option != "None":
    with open(os.path.join("chat_histories", load_chat_history_option), "r") as f:
        st.session_state.messages = json.load(f)
    st.success(f"Chat history loaded from {load_chat_history_option}")

# Main chat interface
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            if st.button("ELI5", key=f"eli5_{i}"):
                with st.spinner("Explaining..."):
                    eli5_prompt = PromptTemplate(template=ELI5_PROMPT, input_variables=["text"])
                    llm = get_llm(llm_backend, api_key)
                    chain = LLMChain(llm=llm, prompt=eli5_prompt)
                    explanation = chain.run(message["content"])
                    st.session_state.messages.append({"role": "assistant", "content": explanation})
                    with st.chat_message("assistant"):
                        st.markdown(explanation)

if uploaded_files or url_input:
    # Process the files
    if "vectorstore" not in st.session_state:
        with st.spinner("Processing Files..."):
            all_chunks = []
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Save the uploaded file to a temporary location
                    temp_dir = "temp"
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    chunks = load_and_chunk_file(file_path)
                    all_chunks.extend(chunks)
            elif url_input:
                chunks = load_and_chunk_file(url_input)
                all_chunks.extend(chunks)

            st.session_state.chunks = all_chunks
            st.session_state.vectorstore = create_vectorstore(all_chunks, llm_backend)
            st.success("Files processed successfully!")

    # Summarization
    if summarize_button:
        with st.spinner("Summarizing..."):
            summary = summarize_document(st.session_state.chunks, llm_backend, api_key)
            st.session_state.summary = summary
            st.session_state.messages.append({"role": "assistant", "content": summary})
            with st.chat_message("assistant"):
                st.markdown(summary)

    # Smart Features Logic
    if generate_questions_button and "chunks" in st.session_state:
        with st.spinner("Generating questions..."):
            questions_prompt = PromptTemplate(template=GENERATE_QUESTIONS_PROMPT, input_variables=["text"])
            llm = get_llm(llm_backend, api_key)
            chain = LLMChain(llm=llm, prompt=questions_prompt)
            questions = chain.run("\n".join([chunk.page_content for chunk in st.session_state.chunks]))
            st.session_state.messages.append({"role": "assistant", "content": questions})
            with st.chat_message("assistant"):
                st.markdown(questions)

    if extract_entities_button and "chunks" in st.session_state:
        with st.spinner("Extracting entities..."):
            entities_prompt = PromptTemplate(template=ENTITY_EXTRACTION_PROMPT, input_variables=["text"])
            llm = get_llm(llm_backend, api_key)
            chain = LLMChain(llm=llm, prompt=entities_prompt)
            entities = chain.run("\n".join([chunk.page_content for chunk in st.session_state.chunks]))
            st.session_state.messages.append({"role": "assistant", "content": entities})
            with st.chat_message("assistant"):
                st.markdown(entities)

    # Chat input
    if prompt := st.chat_input("Ask a question about the document"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            rag_chain = create_rag_chain(st.session_state.vectorstore, llm_backend, api_key)
            response = rag_chain({"query": prompt})
            answer = response["result"]
            source_documents = response["source_documents"]

            # Extract unique page numbers and format them
            page_numbers = set()
            for doc in source_documents:
                if "page_number" in doc.metadata:
                    page_numbers.add(str(doc.metadata["page_number"] + 1)) # +1 because page numbers are 0-indexed
            
            if page_numbers:
                sorted_page_numbers = sorted(list(page_numbers))
                if len(sorted_page_numbers) == 1:
                    answer += f" (Reference: Page {sorted_page_numbers[0]})"
                else:
                    answer += f" (Reference: Pages {', '.join(sorted_page_numbers)})"

            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

            with st.expander("Source Documents"):
                for doc in source_documents:
                    source = doc.metadata.get('source', 'Unknown')
                    page = doc.metadata.get('page_number')
                    if page is not None:
                        st.markdown(f"**Source:** {source}, **Page:** {page + 1}")
                    else:
                        st.markdown(f"**Source:** {source}")
                    st.markdown(doc.page_content)
