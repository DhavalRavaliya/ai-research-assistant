from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_groq import ChatGroq

search = DuckDuckGoSearchAPIWrapper()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def fast_web_answer(query: str) -> str:
    results = search.run(query)

    prompt = f"""
    Answer the question briefly and clearly using the info below.

    Info:
    {results}

    Question: {query}
    """

    return llm.invoke(prompt).content