from langchain_ollama import OllamaLLM
from crewai import Agent

llm = OllamaLLM(model="tinyllama")

SimpleAgent = Agent(
    role="Assistant",
    goal="Answer a single, simple user query",
    backstory="An assistant using a lightweight local model to help users.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)