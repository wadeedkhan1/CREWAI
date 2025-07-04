from crewai.tools import tool
import os
import requests

@tool("Search the Internet")
def search_internet(query: str) -> str:
    """Search the internet using Serper and return the top 5 results."""
    try:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER_API_KEY not set in environment."
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 5
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Error: Serper API returned status code {response.status_code}"
        data = response.json()
        results = []
        for r in data.get("organic", []):
            results.append(f"{r.get('title')}: {r.get('link')}\n{r.get('snippet')}\n")
        if not results:
            return "Error: No results returned (maybe rate-limited)."
        return '\n'.join(results)
    except Exception as e:
        return f"Error: {e}" 