def smart_answer(query: str):
    q = query.lower().strip()

    # 1️⃣ Simple factual keywords
    simple_keywords = [
        "gdp", "population", "capital", "president", "pm",
        "who is", "what is", "when", "where", "india", "china"
    ]

    # 2️⃣ Entity-style query (1–3 words, no verbs)
    is_entity_query = len(q.split()) <= 3

    is_simple = any(k in q for k in simple_keywords) or is_entity_query

    # Try PDF first (fast)
    if st.session_state.pdf_qa:
        try:
            pdf_ans = st.session_state.pdf_qa.run(query)
            if pdf_ans and len(pdf_ans.strip()) > 50:
                return f"### 📄 From PDF\n{pdf_ans}"
        except Exception:
            pass

    # Simple → FAST web (no agent)
    if is_simple:
        from app.tools.web_fast import fast_web_answer
        return f"### 🌐 From Web\n{fast_web_answer(query)}"

    # Complex → Agent
    return f"### 🌐 From Web\n{run_agent(query)}"