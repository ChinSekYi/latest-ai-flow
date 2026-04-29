import os
from crewai import Agent, Crew, LLM, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ContentCrew:
    """Content Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

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

    def _build_agent(self, config_key: str) -> Agent:
        return Agent(
            config=self.agents_config[config_key],  # type: ignore[index]
            llm=self._openrouter_llm(),
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
