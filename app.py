import streamlit as st
from agents.router_agent import route_question
from rag.loader import load_documents
from rag.vectorstore import build_vectorstore

st.set_page_config(page_title="Enterprise AI Assistant")

st.title("Enterprise AI Assistant")

uploaded_files = st.file_uploader(
    "Upload company documents",
    accept_multiple_files=True
)

if uploaded_files:
    docs = load_documents(uploaded_files)
    vectordb = build_vectorstore(docs)
    st.success("Documents processed and indexed")

    question = st.text_input("Ask a question")
    output_format = st.selectbox("Output format", ["Readable", "JSON"])

    if question:
        response = route_question(question, vectordb, output_format)
        if output_format == "JSON":
            st.json(response)
        else:
            st.write(response["answer"])
