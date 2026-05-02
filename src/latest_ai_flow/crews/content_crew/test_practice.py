from pathlib import Path
from typing import List

from crewai import Agent
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

if __name__ == "__main__":
    company_name = "5th Dimension AI"
    target_country = "Singapore"
    result = researcher.kickoff(
        f"Generate a list of sales leads for {company_name} in {target_country}.\n"
        "You must also:\n"
        "- Rank the leads by their likelihood to convert\n"
        "- Give reasoning for the ranking\n"
        "- List the person to contact for each lead",
        response_format=SalesLeads
    )
    out_path = Path("output") / "sales_leads_output.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.raw, encoding="utf-8")
    print(f"Wrote {out_path.resolve()}")
