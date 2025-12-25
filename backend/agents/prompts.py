from langchain_core.prompts import ChatPromptTemplate

qa_prompt = ChatPromptTemplate.from_template(
    """
You are a document-based question answering system.

RULES:
1. Use ONLY the provided context.
2. Do NOT infer or guess.
3. If the answer is missing, respond:
   "I don't know based on the provided context."

CONTEXT (may be partial):
{context}

QUESTION:
{question}

ANSWER (concise, factual):
"""
)
