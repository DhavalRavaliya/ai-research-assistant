from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool

class AdvancedAgent:
    def __init__(self, tools: list[BaseTool]):
        self.model = ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=0.2
        ).bind_tools(tools)

        self.tools = {tool.name: tool for tool in tools}

    def run(self, user_input: str) -> str:
        response = self.model.invoke([HumanMessage(content=user_input)])

        if response.tool_calls:
            results = []
            for call in response.tool_calls:
                tool = self.tools[call["name"]]
                result = tool.invoke(call["args"])
                results.append(result)
            return "\n".join(results)

        return response.content