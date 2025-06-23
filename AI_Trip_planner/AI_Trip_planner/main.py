import os
from crewai import Crew

from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv
load_dotenv()


class TripCrew:
    def __init__(self, origin, cities, dates, interests):
        self.origin = origin
        self.cities = cities
        self.dates = dates 
        self.interests = interests 

    def run(self):
    
        agents = TravelAgents()
        tasks = TravelTasks()

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        plan_itenary = tasks.plan_itenary(
            expert_travel_agent,
            city=self.cities,
            dates=self.dates,
            interests=self.interests,
        )

        identify_city = tasks.identify_city(
            city_selection_expert,
            origin=self.origin,
            dates=self.dates,
            interests=self.interests,
            cities=self.cities,
        )

        gathering_city_info = tasks.gather_city_info(
            local_tour_guide,
            city=self.cities,
            dates=self.dates,
            interests=self.interests,
        )

        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_itenary, identify_city, gathering_city_info],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Trip planner CrewAI Demo ##")
    print("-------------------------------")
    location = input(
        dedent("""
            From where you will be travelling from?
        """))
    cities = input(
        dedent("""
            Which cities are you intrested in visiting? 
        """))
    dates = input(
        dedent("""
            What are the date range of your travel?
        """))
    interests = input(
        dedent("""
            What are your interests? (e.g. culture, food, adventure, etc.)
        """))   
    
    tripCrew = TripCrew(origin=location, cities=cities, dates=dates, interests=interests)
    result = tripCrew.run()
    print("CrewAI Result:")
    print("-------------------------------")
    print(result)

