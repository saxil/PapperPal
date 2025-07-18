# PaperPal

PaperPal is an intelligent document analysis tool designed to help you quickly understand and extract key information from various document types. Whether you're dealing with research papers, reports, or any other text-heavy files, PaperPal streamlines the process of summarization, question-answering, and information retrieval.

## Features

- **Intelligent Summarization:** Get concise summaries of lengthy documents.
- **Contextual Q&A:** Ask questions about your documents and get accurate answers based on their content.
- **Multi-document Support:** Analyze and query multiple documents simultaneously.
- **User-Friendly Interface:** An intuitive web interface for easy interaction.

## Live Demo

Experience PaperPal live: [https://paperpal-bysahil.streamlit.app/](https://paperpal-bysahil.streamlit.app/)

## Documentation

For detailed information on how to use PaperPal, set it up locally, and understand its architecture, please refer to our documentation:

[PaperPal Documentation](./docs/)

## Installation (Local)

To run PaperPal on your local machine, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/PaperPal.git
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

## Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` (coming soon) for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

For any inquiries, please contact [your-email@example.com].
