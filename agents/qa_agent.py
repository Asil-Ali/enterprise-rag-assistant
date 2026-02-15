from langchain_openai import ChatOpenAI
from rag.retriever import retrieve_context
from langchain_core.messages import HumanMessage # إضافة مستحبة للتعامل السليم مع LangChain
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

    # --- التعديل هنا ---
    # استخدم .invoke() بدلاً من الاستدعاء المباشر
    answer_obj = llm.invoke(prompt) 

    # بما أن answer_obj الآن هو AIMessage، الوصول لمحتواه يكون بـ .content
    try:
        answer_text = answer_obj.content
    except AttributeError:
        answer_text = str(answer_obj)

    return {"answer": answer_text, "context_used": context}
