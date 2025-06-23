import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from textwrap import dedent
from langchain_ollama import OllamaLLM
from tools.search_tools import search_internet
from tools.calculator_tools import calculate


class TravelAgents:
    def __init__(self):
        self.llm = OllamaLLM(model="tinyllama:latest")
        response = self.llm.invoke("Hello, who are you?")
        print(response)

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(f"""Expert in travel planning and logistics with over 10 years of experience"""),
            goal=dedent(f"""Create 7 day travel itinerary with details per day,
                         including flights, hotels, activities and safety. If unable to access the internet, fallback to generic answers."""),
            tools=[search_internet, calculate],
            verbose=True,
            llm=self.llm,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory=dedent(f"""Expert in analyzing cities based on user preferences and budget 
                             constraints with a strong background in urban studies and travel trends."""),
            goal=dedent(f"""Select the best city for the travel itinerary based on user preferences and budget. If unable to access the internet, fallback to generic answers."""),
            tools=[search_internet],
            verbose=True,
            llm=self.llm
        )
    
    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""Expert in local culture and attractions with extensive 
                             knowledge of the city's history and hidden gems."""),
            goal=dedent(f"""Provide detailed local insights and recommendations for the selected city,
                         including cultural attractions, dining options, and hidden gems.
                        If unable to access the internet, fallback to generic answers."""),
            tools=[search_internet],
            verbose=True,
            llm=self.llm,
        )