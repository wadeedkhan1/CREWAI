from agent import SimpleAgent
from tasks import simple_tasks
from crewai import Crew


crew = Crew(
    agents=[SimpleAgent],
    tasks=simple_tasks,
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n--- Output ---\n")
    print(result)