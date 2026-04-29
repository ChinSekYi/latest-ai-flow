import os
from crewai import Agent, Crew, LLM, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ContentCrew:
    """Content Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def _openrouter_llm(self) -> LLM:
        key_candidates = [
            ("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY")),
            ("OPEN_ROUTER_API_KEY", os.getenv("OPEN_ROUTER_API_KEY")),
            ("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")),
        ]
        key_source = "none"
        api_key = None
        for name, value in key_candidates:
            if value:
                key_source = name
                api_key = value
                break
        if api_key:
            api_key = api_key.strip().strip('"').strip("'")
            # Deployment UIs sometimes persist a pasted typo with an extra
            # leading "s" (e.g. "ssk-or-..."). Normalize this safely.
            if api_key.startswith("ssk-or-"):
                print(
                    "Warning: OPENROUTER_API_KEY had unexpected 'ssk-' prefix. "
                    "Normalizing to 'sk-'."
                )
                api_key = api_key[1:]
        if not api_key:
            raise ValueError(
                "Missing API key. Set OPENROUTER_API_KEY (or OPENAI_API_KEY) in environment. "
                "No candidate env var had a value."
            )
        if not api_key.startswith("sk-or-"):
            masked = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) >= 8 else "***"
            raise ValueError(
                "OpenRouter API key looks invalid for this deployment. "
                "Expected key prefix 'sk-or-'. "
                f"Using source={key_source}, value={masked}, length={len(api_key)}."
            )

        # Force env names to the same non-empty key so OpenAI-compatible
        # paths always send Authorization headers.
        os.environ["OPENROUTER_API_KEY"] = api_key
        os.environ["OPENAI_API_KEY"] = api_key

        model = (
            os.getenv("OPENROUTER_MODEL")
            or os.getenv("MODEL")
            or os.getenv("OPENAI_MODEL_NAME")
            or "openrouter/meta-llama/llama-3-8b-instruct"
        )
        base_url = (
            os.getenv("OPENROUTER_BASE_URL")
            or os.getenv("OPENROUTER_API_BASE")
            or os.getenv("OPENAI_API_BASE")
            or "https://openrouter.ai/api/v1"
        )
        base_url = base_url.strip().strip('"').strip("'")
        os.environ["OPENROUTER_API_BASE"] = base_url

        if "openrouter.ai" in base_url and not model.startswith("openrouter/"):
            model = f"openrouter/{model}"

        return LLM(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )

    # If you would like to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def planner(self) -> Agent:
        llm = self._openrouter_llm()
        return Agent(
            config=self.agents_config["planner"],  # type: ignore[index]
            llm=llm,
        )

    @agent
    def writer(self) -> Agent:
        llm = self._openrouter_llm()
        return Agent(
            config=self.agents_config["writer"],  # type: ignore[index]
            llm=llm,
        )

    @agent
    def editor(self) -> Agent:
        llm = self._openrouter_llm()
        return Agent(
            config=self.agents_config["editor"],  # type: ignore[index]
            llm=llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
