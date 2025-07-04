from crewai import Task
from datetime import date

class TripTasks:
    def research_city_info(self, agent, cities, travel_dates, interests):
        return Task(
            description=(
                f"Research comprehensive information about the following cities: {cities}. "
                f"Focus on attractions, local customs, best times to visit (considering {travel_dates}), and activities related to {interests}. "
                "Compile all findings into a detailed summary for each city." 
            ),
            expected_output=(
                "A detailed summary for each city, including: "
                "- Top attractions and their estimated costs (e.g., entrance fees)" 
                "- Local customs and etiquette" 
                "- Recommended activities based on interests" 
                "- Best time to visit and weather considerations" 
                "- Average daily cost for food, accommodation, and local transport"
            ),
            agent=agent,
        )

    def plan_trip_itinerary(self, agent, origin, cities, travel_dates, interests, city_info_context):
        return Task(
            description=(
                f"Create a detailed 7-day trip itinerary for a trip starting from {origin} to {cities} "
                f"during {travel_dates}, focusing on user interests: {interests}. "
                "Include day-by-day activities, estimated costs for each activity (transport, food, attractions), "
                "and practical travel tips. Leverage the provided city information context." 
                "Your final output MUST be a complete 7-day itinerary in markdown format, with a clear breakdown of costs per day and total estimated cost." 
            ),
            expected_output=(
                "A well-structured 7-day trip plan in markdown format, including: "
                "- Day-by-day breakdown of activities and locations" 
                "- Estimated costs for transportation, accommodation, food, and attractions per day" 
                "- Total estimated cost for the entire trip" 
                "- Practical travel tips (e.g., visa requirements, packing list, local phrases)" 
                "- References to sources for cost estimations (e.g., website names or assumptions)."
            ),
            agent=agent,
            context=[city_info_context],
        ) 