from langchain_classic.prompts import PromptTemplate
STRICT_RAG_PROMPT_WITH_MEMORY = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template="""
You are an AI assistant answering questions strictly from the provided website content.

Conversation history (for context only):
{chat_history}

Rules:
- Use ONLY the information in the context.
- Do NOT use external knowledge.
- If the answer is not available in the website content, respond exactly with:
  "The answer is not available on the provided website."

Website Content:
{context}

Question:
{question}

Answer:
"""
)
