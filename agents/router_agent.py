from agents.qa_agent import answer_with_rag
from agents.verify_agent import verify_answer
from agents.format_agent import format_output

def route_question(question, vectordb, output_format):
    # استدعاء الـ QA Agent
    result = answer_with_rag(question, vectordb)

    # التعديل هنا: Pydantic v2 يستخدم model_dump بدلاً من dict
    if hasattr(result, "model_dump"):
        result = result.model_dump()
    elif hasattr(result, "dict"): # لدعم التوافق مع النسخ القديمة إذا وجدت
        result = result.dict()

    # التأكد من أن النتيجة تمر للمراحل التالية بشكل سليم
    verified = verify_answer(result)
    final = format_output(verified, output_format)

    return final
