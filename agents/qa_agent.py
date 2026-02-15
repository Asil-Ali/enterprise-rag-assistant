from langchain_openai import ChatOpenAI
from rag.retriever import retrieve_context
import os

def answer_with_rag(question, vectordb):
    context = retrieve_context(question, vectordb)

    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    prompt = f"""
Answer strictly from the context below.

Context:
{context}

Question:
{question}

Return a structured and clear answer.
"""

    answer = llm.invoke(prompt)

    

    return {"answer": answer, "context_used": context}
