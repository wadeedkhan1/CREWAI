from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.llm import LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Output model
class PersonalizedEmail(BaseModel):
    subject_line: str
    email_body: str
    follow_up_notes: str


@CrewBase
class SalesPersonalizedEmailCrew:
    """SalesPersonalizedEmail crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def prospect_researcher(self) -> Agent:
        llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
        serper_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["prospect_researcher"], 
            tools=[serper_tool, ScrapeWebsiteTool()],
            llm=llm,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def content_personalizer(self) -> Agent:
        llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
        return Agent(
            config=self.agents_config["content_personalizer"],
            tools=[],
            llm=llm,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def email_copywriter(self) -> Agent:
        llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
        return Agent(
            config=self.agents_config["email_copywriter"],
            tools=[],
            llm=llm,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_prospect_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_prospect_task"],
            agent=self.prospect_researcher(),
        )

    @task
    def personalize_content_task(self) -> Task:
        return Task(
            config=self.tasks_config["personalize_content_task"],
            agent=self.content_personalizer(),
        )

    @task
    def write_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_email_task"],
            agent=self.email_copywriter(),
            output_json=PersonalizedEmail,
            output_file="personalized_email.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SalesPersonalizedEmail crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
