import streamlit as st
from agents.router_agent import route_question
from rag.loader import load_documents
from rag.vectorstore import build_vectorstore

st.set_page_config(page_title="Enterprise AI Assistant", layout="wide")

st.title("🏢 Enterprise AI Assistant")

# رفع الملفات
uploaded_files = st.file_uploader(
    "Upload company documents",
    accept_multiple_files=True
)

if uploaded_files:
    # حفظ الـ vectordb في الجلسة عشان ما يعيد المعالجة كل شوية
    if 'vectordb' not in st.session_state:
        with st.spinner("Processing documents..."):
            docs = load_documents(uploaded_files)
            st.session_state.vectordb = build_vectorstore(docs)
            st.success("✅ Documents processed and indexed")

    # إدخال السؤال
    question = st.text_input("💬 Ask a question about your documents")
    output_format = st.selectbox("Output format", ["Readable", "JSON"])

    if question:
        with st.spinner("Generating answer..."):
            response = route_question(question, st.session_state.vectordb, output_format)

        if output_format == "JSON":
            st.subheader("📊 Structured JSON Output")
            st.json(response)
        else:
            # عرض الإجابة داخل التصميم الجميل (الـ Card)
            st.subheader("🤖 إجابة المساعد الذكي")
            
            # هنا نستخدم ['answer'] بأمان لأننا وحدناها في الـ Agent
            ans = response.get('answer', 'No answer found.')
            
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; color: #1a1a1a;">
                {ans}
            </div>
            """, unsafe_allow_html=True)

            # المصادر والتحقق
            with st.expander("📌 المصادر المعتمدة وتفاصيل الموثوقية"):
                st.write(f"**نسبة الثقة:** {response.get('confidence', 0)*100:.0f}%")
                st.info(response.get("source_documents", "لا توجد مصادر محددة."))

            # زر التحميل
            st.download_button(
                label="📄 تحميل الإجابة (TXT)",
                data=ans,
                file_name="ai_answer.txt",
                mime="text/plain"
            )
