import streamlit as st
from agents.router_agent import route_question
from rag.loader import load_documents
from rag.vectorstore import build_vectorstore

st.set_page_config(page_title="Enterprise AI Assistant", layout="wide")

st.title("Enterprise AI Assistant")

# رفع الملفات
uploaded_files = st.file_uploader(
    "Upload company documents",
    accept_multiple_files=True
)

if uploaded_files:
    docs = load_documents(uploaded_files)
    vectordb = build_vectorstore(docs)
    st.success("✅ Documents processed and indexed")

    # إدخال السؤال
    question = st.text_input("Ask a question")
    output_format = st.selectbox("Output format", ["Readable", "JSON"])

    if question:
        response = route_question(question, vectordb, output_format)

        # Card للإجابة
        st.subheader("🤖 إجابة المساعد الذكي")
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;">
            {response['answer']}
        </div>
        """, unsafe_allow_html=True)

        # Expander للمصادر
        with st.expander("📌 المصادر المعتمدة (Source Documents)"):
            st.info(response.get("source_documents", ""))

        # Metrics للتحقق والثقة
        col1, col2 = st.columns(2)
        with col1:
            st.metric("دقة الإجابة", f"{response.get('confidence', 0)*100:.0f}%")
        with col2:
            status = "✅ تم التحقق" if response.get("verified", False) else "⚠️ غير مؤكد"
            st.write(f"**حالة الموثوقية:** {status}")

        # زر تحميل الخطاب
        st.download_button(
            label="📄 تحميل الإجابة كملف TXT",
            data=response['answer'],
            file_name="answer.txt",
            mime="text/plain"
        )
