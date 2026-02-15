from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

def build_vectorstore(documents):
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    return FAISS.from_documents(documents, embeddings)
