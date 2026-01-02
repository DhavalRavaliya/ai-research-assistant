from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date and factual information.
    Use this for research, news, politics, history, etc.
    """
    return search.run(query)