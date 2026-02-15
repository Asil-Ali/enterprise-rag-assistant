def format_output(result, output_format):
    # استخراج البيانات الأساسية لضمان عدم حدوث خطأ
    answer = result.get("answer", "No answer found.")
    context = result.get("context_used", "")
    verified = result.get("verified", False)
    confidence = result.get("confidence", 0)

    if output_format == "JSON":
        return {
            "status": "success",
            "data": {
                "answer": answer,
                "source_highlights": context.split("\n")[:5] if isinstance(context, str) else [],
                "metadata": {
                    "verified": verified,
                    "confidence_score": confidence
                }
            }
        }
    
    # تنسيق موحد للـ Readable
    return {
        "answer": answer,
        "source_documents": context,
        "verified": verified,
        "confidence": confidence
    }
