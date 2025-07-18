# PaperPal Documentation

Welcome to the official documentation for PaperPal, an intelligent document analysis tool.

## Overview

PaperPal is designed to help you quickly understand and extract key information from various document types. It streamlines the process of summarization, question-answering, and information retrieval from research papers, reports, and other text-heavy files.

## Features

*   **Intelligent Summarization:** Get concise summaries of lengthy documents.
*   **Contextual Q&A:** Ask questions about your documents and get accurate answers based on their content.
*   **Multi-document Support:** Analyze and query multiple documents simultaneously.
*   **User-Friendly Interface:** An intuitive web interface for easy interaction.

## Installation (Local)

To run PaperPal on your local machine, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://https://github.com/your-username/PaperPal.git
    cd PaperPal
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser.

## Usage

1.  Upload your document(s) using the interface.
2.  Choose to summarize the document or ask questions.
3.  Interact with the AI to get the information you need.

## Project Structure

```
PaperPal/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project README
├── docs/                  # Project documentation
├── modules/               # Core logic modules (file loading, RAG, summarization)
│   ├── file_loader.py
│   ├── rag_chain.py
│   ├── summarizer.py
│   └── vectorstore.py
├── utils/                 # Utility functions (LLM factory, prompts)
│   ├── llm_factory.py
│   └── prompts.py
├── chat_histories/        # Stores chat history
├── data/                  # Placeholder for data files
└── cache/                 # Cache directory
```