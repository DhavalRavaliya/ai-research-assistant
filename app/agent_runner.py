from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, AgentType

from app.tools.web import web_search

# LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# Agent (tool-using assistant)
agent = initialize_agent(
    tools=[web_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

def run_agent(query: str) -> str:
    return agent.run(query)