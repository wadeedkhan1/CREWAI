import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load environment variables from .env file
load_dotenv()

print(f"DEBUG: GROQ_API_KEY loaded: {os.environ.get('GROQ_API_KEY')}")

# Initialize LLM using crewai.LLM for Groq with explicit API key
llm = LLM(
    model="groq/llama3-8b-8192", # Changed model back to llama3-8b-8192
    temperature=0.1,
    api_key=os.environ.get("GROQ_API_KEY") # Explicitly passing API key
)

research_agent = Agent(
    role="AI Trend Researcher",
    goal="Discover emerging trends in artificial intelligence",
    backstory="You're an expert in AI market analysis and tech trend forecasting.",
    llm=llm,
    verbose=True # Reverted verbose to True
)

research_task = Task(
    description="Provide a short paragraph explaining artificial intelligence as your final answer. Do not include any introductory phrases like 'Thought:' or 'Final Answer:'. Just the paragraph.",
    expected_output="A short paragraph explaining artificial intelligence.",
    agent=research_agent
)

crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True # Reverted verbose to True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("✅ Final Output:\n", result)
