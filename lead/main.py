from dotenv import load_dotenv
from crew import LeadGeneration

load_dotenv()

if __name__ == "__main__":

    print("⚙️ Starting Lead Generation Crew...")
    
    customer_name_or_business = input("Enter the customer name or business to search for: ")
    target_industry = input("Enter the target industry for lead generation: ")

    inputs = {
        'customer_name_or_business': customer_name_or_business,
        'target_industry': target_industry
    }

    try:
        # Correctly instantiate LeadGeneration and call crew().kickoff()
        results = LeadGeneration().crew().kickoff(inputs=inputs)
        print("\n-------------------------------")
        print("|| Lead Generation Results ||")
        print("-------------------------------\n")
        print(results)
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        raise

    
