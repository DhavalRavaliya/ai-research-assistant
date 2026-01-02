from fastapi import FastAPI
from app.agent import AdvancedAgent
from app.tools.math import add, subtract, multiply, divide
from app.tools.web import web_search

app = FastAPI()

agent = AdvancedAgent(
    tools=[add, subtract, multiply, divide, web_search]
)

@app.post("/chat")
def chat(prompt: str):
    return {"response": agent.run(prompt)}