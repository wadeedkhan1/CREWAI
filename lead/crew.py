from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.search_tools import search_internet
from crewai.llm import LLM
from crewai_tools import SerperDevTool


@CrewBase
class LeadGeneration:
    """LeadGeneration crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def lead_generation_agent(self) -> Agent:
        ollama_llm = LLM(
            model="ollama/tinyllama",
            base_url="http://localhost:11434"
        )
        # Initialize SerperDevTool with desired parameters
        serper_tool = SerperDevTool(
            n_results=10,
            save_file=False,
            search_type="search",
            country="us",
            location="New York",
            locale="en-US"
        )
        return Agent(
            config=self.agents_config['lead_generation_agent'], # type: ignore[index]
            tools=[serper_tool], # Use the initialized SerperDevTool
            verbose=True,
            llm=ollama_llm
        )

    @task
    def search_for_public_info_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_for_public_info_task'], # type: ignore[index]
            description="""Find publicly available information (LinkedIn, company website, social profiles) about the given person or company."""
        )

    @task
    def extract_key_details_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_key_details_task'], # type: ignore[index]
            description="""From the results, extract job title, company name, industry, location, and website."""
        )

    @task
    def evaluate_lead_potential_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_lead_potential_task'], # type: ignore[index]
            description="""Based on the extracted info, analyze whether this customer fits our ideal profile. Assign a lead score: High, Medium, or Low."""
        )

    @task
    def summarize_findings_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_findings_task'], # type: ignore[index]
            description="""Prepare a short report including the data found and the lead score.""",
            output_file='lead_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LeadGeneration crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            
        )


