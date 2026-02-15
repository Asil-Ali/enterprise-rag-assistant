import streamlit as st
from agents.router_agent import route_question
from rag.loader import load_documents
from rag.vectorstore import build_vectorstore
from fpdf import FPDF  # لإنشاء PDF يدعم Unicode

# إعدادات الصفحة
st.set_page_config(
    page_title="Enterprise AI Assistant",
    layout="wide"
)

st.title("🏢 Enterprise AI Assistant")
st.caption(
    "An enterprise-ready AI assistant for intelligent document understanding, retrieval, and decision support."
)
st.divider()

# رفع الملفات
uploaded_files = st.file_uploader(
    "📂 Upload company documents (PDF, TXT, etc.)",
    accept_multiple_files=True
)

if uploaded_files:
    if "vectordb" not in st.session_state:
        with st.spinner("Processing and indexing documents..."):
            docs = load_documents(uploaded_files)
            st.session_state.vectordb = build_vectorstore(docs)
        st.success("✅ Documents processed and indexed successfully")

    st.divider()

    st.subheader("💬 Ask a question about your documents")
    question = st.text_input(
        "Type your question here",
        placeholder="Example: Summarize the key requirements in the document"
    )

    output_format = st.selectbox(
        "Output format",
        ["Readable", "JSON", "Portfolio"]
    )

    if question:
        with st.spinner("Generating answer..."):
            response = route_question(
                question,
                st.session_state.vectordb,
                output_format
            )

        st.divider()

        # عرض JSON
        if output_format == "JSON":
            st.subheader("📊 Structured Output")
            st.json(response)

        # عرض بشري احترافي أو Portfolio
        else:
            st.subheader("🤖 Assistant Answer")
            answer_text = response.get("answer", "No answer generated.")
            confidence = float(response.get("confidence") or 0)

            # كارد للإجابة
            st.markdown(
                f"""
                <div style="
                    background-color: #f4f6f8;
                    padding: 24px;
                    border-radius: 12px;
                    border-left: 6px solid #2c7be5;
                    color: #1a1a1a;
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    {answer_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            # Expander للمصادر والثقة
            with st.expander("📌 Sources and reliability details"):
                st.write(f"**Confidence level:** {confidence * 100:.0f}%")
                st.info(response.get("source_documents", "No source documents available."))

            # نص منسق للتحميل
            downloadable_text = f"""
Enterprise AI Assistant Report

Question:
{question}

----------------------------------------

Answer:
{answer_text}

----------------------------------------

Confidence Level:
{confidence * 100:.0f}%
"""

            # زر تحميل TXT
            st.download_button(
                label="📄 Download as TXT",
                data=downloadable_text,
                file_name="enterprise_ai_answer.txt",
                mime="text/plain"
            )

            # زر تحميل PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
            pdf.set_font("DejaVu", "", 14)
            pdf.multi_cell(0, 8, downloadable_text)
            pdf_output = "enterprise_ai_answer.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as f:
                st.download_button(
                    label="📄 Download as PDF",
                    data=f,
                    file_name="enterprise_ai_answer.pdf",
                    mime="application/pdf"
                )

else:
    st.info("⬆️ Upload documents to start using the Enterprise AI Assistant.")
