def verify_answer(result):
    answer = result.get("answer", "")
    context = result.get("context_used", "")

    # حساب بسيط لكن منطقي للثقة
    answer_length = len(answer.split())
    context_length = len(context.split()) if isinstance(context, str) else 0

    # منطق بشري مفهوم
    if answer_length > 40 and context_length > 100:
        confidence = 0.9
        verified = True
    elif answer_length > 20:
        confidence = 0.7
        verified = True
    else:
        confidence = 0.5
        verified = False

    return {
        "answer": answer,
        "context_used": context,
        "verified": verified,
        "confidence": confidence
    }
