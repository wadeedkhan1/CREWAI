from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itenary(self, agent, city, dates, interests):
        return Task(
            description=dedent(
                f"""
                **Task**: Plan a detailed travel itinerary.
                **Description**: Expand the city guide into a comprehensive 7-day travel itinerary with detailed
                per day plans, including flights, hotels, activities, and safety tips. You MUST suggest actual 
                places to visit, actual hotels to stay at, and actual flights to take and actual restaurants to eat at. 
                This itinerary should cover all aspects of the trip, from arrival to departure, integrating the city guide information 
                with practical travel advice.

                **Parameters**:
                - **City**: {city}  
                - **Dates**: {dates}
                - **Interests**: {interests}    

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output="A full 7-day itinerary including daily schedule, recommended flights, hotels, restaurants, and safety tips.",
            agent=agent,
        )

    def identify_city(self, agent, origin, dates, interests, cities):
        return Task(
            description=dedent(
                f"""
                **Task**: Identify the best city for the travel itinerary.
                **Description**: Analyze the provided cities based on the user's origin, travel dates, and interests.
                Select the most suitable city that aligns with the user's preferences and budget constraints. This task
                involves comparing different cities, considering factors such as cost, attractions, and user interests.
                Your final answer must be a detailed report on the selected city, including flight costs, weather forecast,
                and attractions.

                **Parameters**:
                - **Origin**: {origin}
                - **Dates**: {dates}
                - **Interests**: {interests}
                - **Cities**: {cities}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output="A report recommending the best city to visit with supporting data: flights, weather, and attractions.",
            agent=agent,
        )
    
    def gather_city_info(self, agent, city, dates, interests):
        return Task(
            description=dedent(
                f"""
                **Task**: Gather detailed information about the selected city.
                **Description**: Compile an in-depth guide for the selected city, including key attractions, local culture,
                special events, daily activity suggestions, and local customs.   

                **Parameters**:
                - **City**: {city}
                - **Dates**: {dates}
                - **Interests**: {interests}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output="A cultural and practical guide to the city: attractions, events, customs, and suggested daily activities.",
            agent=agent,
        )