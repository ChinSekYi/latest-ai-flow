# Command Log

Use this file to track terminal commands run for this project.

- setup crewai
    - url -LsSf https://astral.sh/uv/install.sh | sh  #(for Mac)
    - uv tool install crewai
    - uv tool list
- setup llm provider
    - uv add "crewai[google-genai]
- set up crewai project
    - crewai create flow sales-assistant


# install and run
crewai install
crewai run
uv run crewai run

# deploy
pip install crewai[tools]
crewai login
crewai deploy create