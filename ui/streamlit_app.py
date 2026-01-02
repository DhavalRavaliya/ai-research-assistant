import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
import streamlit as st
import tempfile
from app.agent_runner import run_agent
from app.rag.loader import load_pdf
from app.rag.vectorstore import create_vectorstore
from app.rag.qa import create_pdf_qa
def hybrid_answer(query: str):
    answers = []

    # PDF answer (if available)
    if st.session_state.pdf_qa:
        try:
            pdf_ans = st.session_state.pdf_qa.run(query)
            answers.append(f"### 📄 From PDF\n{pdf_ans}")
        except Exception:
            pass

    # Web answer (always allowed)
    try:
        web_ans = run_agent(query)
        answers.append(f"### 🌐 From Web\n{web_ans}")
    except Exception:
        pass

    return "\n\n".join(answers)
st.set_page_config(page_title="AI Research Assistant", layout="centered")

st.title("🧠 AI Research Assistant")
st.caption("Web research + PDF question answering")

# Sidebar
st.sidebar.header("📄 Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if "pdf_qa" not in st.session_state:
    st.session_state.pdf_qa = None

if uploaded_file:
    with st.spinner("Processing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        docs = load_pdf(pdf_path)
        vectorstore = create_vectorstore(docs)
        st.session_state.pdf_qa = create_pdf_qa(vectorstore)

    st.sidebar.success("PDF ready for questions!")

# Input
query = st.text_input(
    "Ask a question",
    placeholder="Ask from PDF or ask a web research question..."
)
mode = st.radio(
    "Answer mode",
    ["Auto", "PDF only", "Web only", "Hybrid"],
    horizontal=True
)
def smart_answer(query: str):
    # Keywords for simple factual questions
    simple_keywords = [
        "gdp", "population", "capital", "president",
        "pm", "who is", "what is", "india", "china"
    ]

    is_simple = any(k in query.lower() for k in simple_keywords)

    # 1️⃣ Try PDF first (fast)
    if st.session_state.pdf_qa:
        try:
            pdf_ans = st.session_state.pdf_qa.run(query)
            if pdf_ans and len(pdf_ans.strip()) > 50:
                return f"### 📄 From PDF\n{pdf_ans}"
        except Exception:
            pass

    # 2️⃣ Simple web question → FAST path
    if is_simple:
        from app.tools.web_fast import fast_web_answer
        return f"### 🌐 From Web\n{fast_web_answer(query)}"

    # 3️⃣ Complex → Agent
    return f"### 🌐 From Web\n{run_agent(query)}"
if st.button("Ask"):
    with st.spinner("Thinking..."):
        result = smart_answer(query)
        st.markdown(result)