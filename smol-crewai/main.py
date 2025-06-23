from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",
    model_name="llama3-8b-8192",
    temperature=0.1
)

research_agent = Agent(
    role="AI Trend Researcher",
    goal="Discover emerging trends in artificial intelligence",
    backstory="You're an expert in AI market analysis and tech trend forecasting.",
    llm=llm,
    verbose=True
)

research_task = Task(
    description="Find and explain the top 3 AI trends likely to dominate in 2025.",
    expected_output="A list of the top 3 AI trends for 2025, each with a short explanation.",
    agent=research_agent
)

crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("✅ Final Output:\n", result)
