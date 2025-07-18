
from langchain.prompts import PromptTemplate

QUESTION_ANSWERING_PROMPT = """
You are a helpful assistant. Use the following context to answer the user's question.
Context:
{context}
Question:
{question}
Helpful Answer:
"""

SUMMARIZATION_PROMPT = """
Summarize the following academic paper into 3 concise bullet points.
Text:
{text}
Summary:
"""

ELI5_PROMPT = """
Explain the following text to me like I'm 5 years old.
Text:
{text}
Explanation:
"""

GENERATE_QUESTIONS_PROMPT = """
Based on the following text, generate 3 interesting questions that a user might want to ask.
Text:
{text}
Questions:
"""

ENTITY_EXTRACTION_PROMPT = """
Extract key entities (people, organizations, locations, and key concepts) from the following text. List each entity type separately.
Text:
{text}
Entities:
"""
