from dotenv import load_dotenv

#!/usr/bin/env python
from crew import LeadGeneration

load_dotenv() # Load environment variables from .env file


if __name__ == "__main__":

    print("⚙️ Starting crew kickoff...") 
    try:
        # Correctly instantiate LeadGeneration and call crew().kickoff()
        results = LeadGeneration().crew().kickoff(inputs={'target_industry': 'B2B SaaS'})
        print(results)
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")

    
