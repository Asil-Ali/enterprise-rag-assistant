from langchain_community.document_loaders import PyPDFLoader, TextLoader
import tempfile

def load_documents(files):
    documents = []

    for file in files:
        suffix = file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(file.read())
            path = tmp.name

        if suffix.lower() == "pdf":
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        else:
            loader = TextLoader(path)
            documents.extend(loader.load())
    return documents
