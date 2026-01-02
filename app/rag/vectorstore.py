from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},   # ✅ force CPU
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore