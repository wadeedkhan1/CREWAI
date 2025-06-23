from crewai import Task
from agent import SimpleAgent

simple_tasks = [
    Task(
        description="Answer the question: What is a healthy breakfast option?",
        expected_output="A brief and simple answer, suitable for a general audience.",
        agent=SimpleAgent
    )
]