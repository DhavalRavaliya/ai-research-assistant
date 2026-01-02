from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.tools.web import web_search

load_dotenv()

SYSTEM_PROMPT = """
You are a research agent.

Rules:
- Always use web_search for factual or historical research.
- Collect information from multiple sources.
- Summarize clearly and concisely.
- Stop once the task is complete.
- Do NOT loop unnecessarily.
"""

def main():
    model = ChatGroq(
       model="llama-3.1-8b-instant",
        temperature=0.2
    )

    tools = [web_search]
    agent = create_react_agent(model, tools)

    print("🧠 Research Agent (type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]

        for chunk in agent.stream(
            {"messages": messages},
            config={"recursion_limit": 20},
            stream_mode="values"
        ):
            if "messages" in chunk:
                print(chunk["messages"][-1].content, end="", flush=True)

        print()

if __name__ == "__main__":
    main()