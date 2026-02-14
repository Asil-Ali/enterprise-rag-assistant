from ml.reranker import rerank

def retrieve_context(question, vectordb):
    docs = vectordb.similarity_search(question, k=5)
    ranked = rerank(question, docs)
    return "\n".join([d.page_content for d in ranked])
