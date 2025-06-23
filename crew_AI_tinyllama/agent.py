from crewai import Agent
from tools.search_tools import search_internet

def create_simple_agent(llm):
    return Agent(
        role="Assistant",
        goal="Answer a single, simple user query",
        backstory="An assistant using a lightweight local model to help users.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_researcher_agent(llm):
    return Agent(
        role="Research Analyst",
        goal="Uncover critical information on advanced topics.",
        backstory="You are a meticulous research analyst, adept at sifting through vast amounts of data to extract precise and relevant information. You are essential for complex investigations.",
        verbose=True,
        allow_delegation=False,
        tools=[search_internet],
        llm=llm
    )

def create_writer_agent(llm):
    return Agent(
        role="Content Creator",
        goal="Compose compelling and insightful articles based on research.",
        backstory="You are a skilled content creator, transforming raw data and complex ideas into engaging and easy-to-understand narratives. Your writing is precise, clear, and always on point.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_reviewer_agent(llm):
    return Agent(
        role="Article Reviewer",
        goal="Review and refine articles for clarity, structure, and adherence to requirements.",
        backstory="You are a meticulous editor and reviewer, ensuring that all content is polished, coherent, and meets high editorial standards. You catch errors and improve readability.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )