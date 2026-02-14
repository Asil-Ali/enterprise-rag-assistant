def format_output(result, output_format):
    if output_format == "JSON":
        return {
            "answer": result["answer"],
            "source_documents": result.get("context_used", ""),
            "verified": result.get("verified", False),
            "confidence": result.get("confidence", 0)
        }
    return result
