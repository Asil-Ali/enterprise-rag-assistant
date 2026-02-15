def format_output(result, output_format):
    if output_format == "JSON":
        return {
            "Response": {
                "Answer": result.get("answer", ""),
                "Source Highlights": result.get("context_used", "").split("\n")[:5],  # عرض أول 5 نقاط فقط
                "Verification": {
                    "Verified": result.get("verified", False),
                    "Confidence Score": result.get("confidence", 0)
                }
            }
        }
    return result
