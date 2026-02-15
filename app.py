import streamlit as st
from agents.router_agent import route_question
from rag.loader import load_documents
from rag.vectorstore import build_vectorstore

# إعدادات الصفحة
st.set_page_config(
    page_title="Enterprise AI Assistant",
    layout="wide"
)

# العنوان والانطباع الأول
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
    # معالجة الملفات مرة واحدة فقط
    if "vectordb" not in st.session_state:
        with st.spinner("Processing and indexing documents..."):
            docs = load_documents(uploaded_files)
            st.session_state.vectordb = build_vectorstore(docs)
        st.success("✅ Documents processed and indexed successfully")

    st.divider()

    # إدخال السؤال
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

        # عرض بشري احترافي
        else:
            st.subheader("🤖 Assistant Answer")

            answer_text = response.get("answer", "No answer generated.")

            # كارد الإجابة
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

            # المصادر والثقة
            with st.expander("📌 Sources and reliability details"):
                confidence = response.get("confidence", 0)
                st.write(f"**Confidence level:** {confidence * 100:.0f}%")
                st.info(
                    response.get(
                        "source_documents",
                        "No source documents available."
                    )
                )

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

            # زر التحميل
            st.download_button(
                label="📄 Download answer as text file",
                data=downloadable_text,
                file_name="enterprise_ai_answer.txt",
                mime="text/plain"
            )

else:
    st.info(
        "⬆️ Upload documents to start using the Enterprise AI Assistant."
    )
