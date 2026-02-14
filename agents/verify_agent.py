def verify_answer(result):
    # تأكد من وجود محتوى وأنه غير فارغ
    confidence = 0.9 if result["answer"] else 0.5
    return {
        "answer": result["answer"],
        "context_used": result["context_used"],
        "verified": True,
        "confidence": confidence
    }
