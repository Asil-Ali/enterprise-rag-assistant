import os
from fpdf import FPDF

def build_pdf(answer, question, confidence):
    pdf = FPDF()
    pdf.add_page()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "..", "fonts", "DejaVuSansCondensed.ttf")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # معالجة الثقة سواء كانت رقم أو نص
    if isinstance(confidence, (int, float)):
        confidence_text = f"{confidence * 100:.0f}%"
    else:
        confidence_text = str(confidence)

    pdf.multi_cell(
        0,
        8,
        f"""Enterprise AI Assistant Report

Question:
{question}

----------------------------------------

Answer:
{answer}

----------------------------------------

Confidence Level:
{confidence_text}
"""
    )

    return pdf
