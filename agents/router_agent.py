from agents.qa_agent import answer_with_rag
from agents.verify_agent import verify_answer
from agents.format_agent import format_output

def route_question(question, vectordb, output_format):
    # 1️⃣ استدعاء LLM عبر qa_agent
    result = answer_with_rag(question, vectordb)

    # 2️⃣ تحويل كل ما يتم إرجاعه إلى dict عادي لتجنب BaseModel issues
    if hasattr(result, "dict"):
        result = result.dict()  # pydantic BaseModel → dict

    # 3️⃣ التحقق من صحة الإجابة
    verified = verify_answer(result)

    # 4️⃣ تنسيق الإخراج حسب اختيار المستخدم
    final = format_output(verified, output_format)

    return final
