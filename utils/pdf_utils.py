import os
from fpdf import FPDF

def build_pdf(answer, question, confidence):
    pdf = FPDF()
    pdf.add_page()

    # تحديد مسار الخط بالنسبة لهذا الملف
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "..", "fonts", "DejaVuSansCondensed.ttf")

    # إضافة الخط مع دعم Unicode لجميع اللغات
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # معالجة الثقة سواء كانت رقم أو نص
    if isinstance(confidence, (int, float)):
        confidence_text = f"{confidence * 100:.0f}%"
    else:
        confidence_text = str(confidence)

    # إعداد النص الكامل
    text = (
        f"Enterprise AI Assistant Report\n\n"
        f"Question:\n{question}\n\n"
        f"----------------------------------------\n\n"
        f"Answer:\n{answer}\n\n"
        f"----------------------------------------\n\n"
        f"Confidence Level:\n{confidence_text}\n"
    )

    # استخدم multi_cell لتفادي أي مشاكل مع النصوص متعددة اللغات
    pdf.multi_cell(0, 8, text)

    return pdf
