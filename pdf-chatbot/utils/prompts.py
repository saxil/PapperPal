
QUESTION_ANSWERING_PROMPT = """
You are a helpful assistant. Use the following context to answer the user's question. Cite page and chunk when relevant.
Context:
{context}
Question:
{question}
Helpful Answer:
"""

SUMMARIZATION_PROMPT = """
Summarize the following academic paper into 3 concise bullet points.
Text:
{chunked_text}
Summary:
"""
