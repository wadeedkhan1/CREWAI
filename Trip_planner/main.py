import os
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

from agents import TripAgents
from tasks import TripTasks

# Load environment variables from .env file
load_dotenv()

# Initialize LLM for Ollama TinyLlama
# Ensure 'tinyllama' model is pulled in Ollama (ollama pull tinyllama)
llm = LLM(
    model="ollama/tinyllama",
    base_url="http://localhost:11434"
)

# Initialize Agents and Tasks
trip_agents = TripAgents()
trip_tasks = TripTasks()

# Create Agents
city_researcher = trip_agents.city_researcher()
trip_planner = trip_agents.trip_planner()

# Get user input for the trip
origin_city = input("From where are you traveling?\n").strip()
destination_cities = input("Which cities do you want to visit (comma-separated)?\n").strip()
travel_dates = input("What are your travel dates (e.g., 'June 1st to June 7th, 2025')?\n").strip()
interests = input("What are your interests for this trip (e.g., 'historical sites, food, museums')?\n").strip()

# Create Tasks
research_task = trip_tasks.research_city_info(city_researcher, destination_cities, travel_dates, interests)
plan_task = trip_tasks.plan_trip_itinerary(trip_planner, origin_city, destination_cities, travel_dates, interests, research_task)

# Instantiate the Crew
trip_crew = Crew(
    agents=[city_researcher, trip_planner],
    tasks=[research_task, plan_task],
    verbose=True,
    process=Process.sequential,
    llm=llm
)

if __name__ == "__main__":
    print("\n### Initiating your 7-Day Trip Planner Crew... ###\n")
    result = trip_crew.kickoff()
    print("\n✅ Trip Planning Completed! Here is your detailed itinerary:\n")
    print(result) 