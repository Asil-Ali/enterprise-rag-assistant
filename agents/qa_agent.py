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

    # استدعاء LLM مباشرة
    answer_obj = llm(prompt)

    # التعامل مع جميع أنواع الإرجاع الممكنة
    try:
        # إذا كان كائن pydantic / AIMessage
        answer_text = answer_obj.content
    except AttributeError:
        try:
            # إذا كان dict (BaseModel يقدّم dict)
            answer_text = answer_obj.get("content", str(answer_obj))
        except Exception:
            # fallback لأي نوع آخر
            answer_text = str(answer_obj)

    return {"answer": answer_text, "context_used": context}
