def format_output(result, output_format):
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

    if output_format == "Portfolio":
        return {
            "answer": answer,
            "confidence": f"{confidence * 100:.0f}%",
            "verified": "Verified" if verified else "Not verified",
            "preview_sources": context.split("\n")[:3] if isinstance(context, str) else []
        }

    # Readable (افتراضي)
    return {
        "answer": answer,
        "source_documents": context,
        "verified": verified,
        "confidence": confidence
    }
