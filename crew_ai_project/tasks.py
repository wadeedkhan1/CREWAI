from crewai import Task
from agents import researcher, writer

research_task = Task(
    description='Research the top 3 emerging AI trends in 2025',
    expected_output='A concise report on top 3 AI trends with sources',
    agent=researcher
)

write_article_task = Task(
    description='Write a blog article using the research provided',
    expected_output='A 600-word engaging blog post on AI trends',
    agent=writer,
    context=[research_task]
)
