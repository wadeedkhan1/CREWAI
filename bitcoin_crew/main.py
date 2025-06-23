import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from tools.search_tools import BitcoinSearchTool

# Load environment variables from .env file
load_dotenv()

# Initialize LLM using crewai.LLM for Groq
# Ensure GROQ_API_KEY is set in your .env file
llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.1,
    api_key=os.environ.get("GROQ_API_KEY")
)

# Define the Agents
news_researcher = Agent(
    role="Bitcoin News Researcher",
    goal="Find the latest and most relevant news articles about Bitcoin and the crypto market.",
    backstory="You are an expert financial news researcher specializing in cryptocurrencies, particularly Bitcoin. You excel at finding breaking news and key developments from reputable sources.",
    llm=llm,
    tools=[BitcoinSearchTool()],
    verbose=True
)

bitcoin_analyst = Agent(
    role="Bitcoin Trend Analyst",
    goal="Analyze the gathered Bitcoin news and identify significant trends, potential impacts, and summarize key insights.",
    backstory="You are a seasoned cryptocurrency analyst with a deep understanding of market dynamics. You can synthesize information, identify patterns, and provide concise, actionable insights into Bitcoin's trajectory.",
    llm=llm,
    verbose=True
)

# Define the Tasks
research_bitcoin_news = Task(
    description="Generate a concise and effective search query for the most recent and impactful news regarding Bitcoin from the last 24-48 hours. Your final answer must be ONLY the search query string, without any additional text or formatting.",
    expected_output="A detailed list of relevant Bitcoin news articles with brief summaries and sources.",
    agent=news_researcher
)

analyze_bitcoin_trends = Task(
    description="Based on the news articles provided by the News Researcher, identify and explain the top 3-5 current trends or significant developments influencing Bitcoin. Summarize their potential impact on the cryptocurrency market.",
    expected_output="A well-structured report outlining the key Bitcoin trends, their explanations, and potential market impacts.",
    agent=bitcoin_analyst,
    context=[research_bitcoin_news]
)

# Form the Crew
bitcoin_crew = Crew(
    agents=[news_researcher, bitcoin_analyst],
    tasks=[research_bitcoin_news, analyze_bitcoin_trends],
    verbose=True,
    process="sequential" # Tasks run in defined order
)

# Kick off the Crew
if __name__ == "__main__":
    print("\n### Bitcoin News & Trend Analysis Starting... ###\n")
    result = bitcoin_crew.kickoff()
    print("\n✅ Bitcoin News & Trend Analysis Completed!\n")
    print(result) 