from fpdf import FPDF

def build_pdf(answer, question, confidence):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("DejaVu", "", "fonts/DejaVuSansCondensed.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0, 8, f"Question:\n{question}\n\nAnswer:\n{answer}\n\nConfidence: {confidence*100:.0f}%")

    return pdf
