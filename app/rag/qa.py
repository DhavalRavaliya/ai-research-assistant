from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

_qa_chain = None

def create_pdf_qa(vectorstore):
    global _qa_chain

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    _qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

def get_pdf_answer(query: str) -> str:
    if _qa_chain is None:
        return "❌ PDF not loaded yet."
    return _qa_chain.run(query)