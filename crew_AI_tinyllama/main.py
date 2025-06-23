import os
from dotenv import load_dotenv
from agent import create_researcher_agent, create_writer_agent, create_reviewer_agent
from tasks import create_research_task, create_write_article_task, create_review_article_task
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# Initialize LLM for Ollama TinyLlama
llm = LLM(
    model="ollama/tinyllama", # Assuming 'tinyllama' is the model pulled in Ollama
    base_url="http://localhost:11434"
)

# Create agents
researcher_agent = create_researcher_agent(llm)
writer_agent = create_writer_agent(llm)
reviewer_agent = create_reviewer_agent(llm)

# Create tasks
research_task = create_research_task(researcher_agent)
write_article_task = create_write_article_task(writer_agent, context_tasks=[research_task])
review_article_task = create_review_article_task(reviewer_agent, context_tasks=[write_article_task])

crew = Crew(
    agents=[researcher_agent, writer_agent, reviewer_agent],
    tasks=[research_task, write_article_task, review_article_task],
    verbose=True,
    process=Process.sequential
)

if __name__ == "__main__":
    print("\n### AI Article Writing and Review Crew Starting... ###\n")
    result = crew.kickoff()
    print("\n✅ AI Article Writing and Review Crew Completed!\n")
    print(result)