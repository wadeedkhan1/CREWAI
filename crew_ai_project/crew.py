from crewai import Crew
from agents import researcher, writer
from tasks import research_task, write_article_task

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_article_task],
    verbose=True
)
