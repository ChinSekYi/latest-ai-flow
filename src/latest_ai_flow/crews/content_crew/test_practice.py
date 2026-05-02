from pathlib import Path
from typing import List

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

from latest_ai_flow.crews.content_crew.utils import openrouter_llm


class SalesLeads(BaseModel):
    leads: List[str]
    ranking: List[str]
    reasoning: List[str]
    person_to_contact: List[str]


researcher = Agent(
    role="Sales leads generator",
    goal="Generate sales leads for {company_name} in {target_country} from credible sources",
    backstory="Expert sales leads generator with a knack for finding the latest, most relevant information.",
    verbose=True,  # Enable logging for debugging
    llm=openrouter_llm(),
)

task = Task(
    description="Generate a list of sales leads for {company_name} in {target_country}.\n"
    "You must also:\n"
    "- Rank the leads by their likelihood to convert\n"
    "- Give reasoning for the ranking\n"
    "- List the person to contact for each lead",
    agent=researcher,
    expected_output=SalesLeads,
    # guardrails=[ #can be a function or a string(for LLM-based guardrails)
    # Guardrail(
    # description="Must be a valid list of sales leads",
    # condition=lambda x: len(x.leads) > 0,
    # fix=lambda x: x.leads = [x.leads[0]],
    # )
    # ]
)

crew = Crew(
    agents=[researcher],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
)


def save_content(content: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.resolve()}")


if __name__ == "__main__":
    company_name = "5th Dimension AI"
    target_country = "Singapore"

    # consider using kickoff_async for async support
    result = researcher.kickoff(
        inputs={"company_name": company_name, "target_country": target_country}
    )
    save_content(result.raw, Path("output") / "sales_leads_output.md")

    print(result.pydantic)
    print(newline)
    print(task.output.summary)
