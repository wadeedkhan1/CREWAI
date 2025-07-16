from crew import SalesPersonalizedEmailCrew


if __name__ == "__main__":

    try:
        inputs = {
        "name": "Alice Smith",
        "title": "CTO",
        "company": "TechCorp",
        "industry": "Software",
        "linkedin_url": "https://linkedin.com/in/alicesmith",
        "our_product": "SuperApp",
        }
        results = SalesPersonalizedEmailCrew().crew().kickoff(inputs=inputs)
        print(results)

    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        raise

    
