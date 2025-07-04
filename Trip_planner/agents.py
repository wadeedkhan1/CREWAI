from crewai import Agent
from tools.search_tools import search_internet
from tools.calculator_tools import calculate

class TripAgents:
    def city_researcher(self):
        return Agent(
            role="City Research Expert",
            goal="Gather comprehensive information about specified cities, including attractions, local customs, and key points of interest.",
            backstory=(
                "You are a highly experienced research analyst specializing in urban tourism. "
                "Your expertise lies in quickly identifying and compiling essential data about cities worldwide, ensuring no detail is overlooked." 
                "You provide factual, concise, and useful information for trip planning." 
            ),
            verbose=True,
            allow_delegation=False,
            tools=[search_internet],
        )

    def trip_planner(self):
        return Agent(
            role="7-Day Trip Planner",
            goal="Create a detailed, day-by-day 7-day travel itinerary including activities, estimated costs, and travel tips, tailored to user interests.",
            backstory=(
                "You are a meticulous travel agent with an unparalleled ability to craft perfect itineraries. "
                "You consider all aspects: logistics, budget, interests, and local insights to deliver a seamless and memorable travel plan." 
                "You are an expert in optimizing travel routes and finding cost-effective solutions." 
            ),
            verbose=True,
            allow_delegation=True,
            tools=[search_internet, calculate],
        ) 