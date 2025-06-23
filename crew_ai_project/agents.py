import os
import requests
from crewai import Agent

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama2-70b-4096')  # Change to your preferred Groq model
GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/v1/chat/completions')

class GroqLLM:
    def __init__(self, api_key, model, api_url):
        self.api_key = api_key
        self.model = model
        self.api_url = api_url

    def __call__(self, prompt, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': kwargs.get('max_tokens', 512),
            'temperature': kwargs.get('temperature', 0.1),
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

llm = GroqLLM(GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL)

researcher = Agent(
    role='Research Analyst',
    goal='Find in-depth information on current tech trends',
    backstory='Expert in analyzing large datasets and online sources',
    verbose=True,
    llm=llm
)

writer = Agent(
    role='Technical Writer',
    goal='Write a clear article based on the research',
    backstory='Has a background in journalism and AI communication',
    verbose=True,
    llm=llm
)
