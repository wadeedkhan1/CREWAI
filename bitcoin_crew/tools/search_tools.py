import os
import requests
import json
from crewai.tools import BaseTool

class BitcoinSearchTool(BaseTool):
    name: str = "Bitcoin_Search_Tool"
    description: str = "A tool to search the internet for the latest Bitcoin news and trends. It can accept a comprehensive query string or a dictionary containing the query."

    def _run(self, **kwargs) -> str:
        # Attempt to extract the query from various possible input formats from the LLM
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
            if isinstance(query, dict) and 'description' in query:
                query = query['description']
        elif 'description' in kwargs:
            query = kwargs['description']
        elif kwargs and isinstance(list(kwargs.values())[0], str):
            # If there's only one argument and it's a string, assume it's the query
            query = list(kwargs.values())[0]
        
        if not query or not isinstance(query, str):
            raise ValueError(f"Query not provided or could not be extracted as a string from the search tool input. Received: {kwargs}")

        api_key = os.environ.get("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY environment variable not set.")

        url = "https://serper.dev/search"
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = json.dumps({"q": query})

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json() 