from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from latest_ai_flow.crews.content_crew.utils import openrouter_llm


@CrewBase
class ContentCrew:
    """Content Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def _build_agent(self, config_key: str) -> Agent:
        return Agent(
            config=self.agents_config[config_key],  # type: ignore[index]
            verbose=True,  # Enable logging for debugging
            llm=openrouter_llm(),
        )

    @agent
    def planner(self) -> Agent:
        return self._build_agent("planner")

    @agent
    def writer(self) -> Agent:
        return self._build_agent("writer")

    @agent
    def editor(self) -> Agent:
        return self._build_agent("editor")

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"],  # type: ignore[index]
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],  # type: ignore[index]
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config["editing_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Content Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
