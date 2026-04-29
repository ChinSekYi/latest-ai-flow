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

# 1) Kickoff
curl -sS -X POST \
  -H "Authorization: Bearer 080eb21cd814" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Asian literature"}' \
  "https://latest-ai-flow-273bc72f-2749-43bc-9797-7c8f-9409cbfa.crewai.com/kickoff" | jq .

  # 2) Status (replace KICKOFF_ID with value from kickoff response)
curl -sS \
  -H "Authorization: Bearer 080eb21cd814" \
  "https://latest-ai-flow-273bc72f-2749-43bc-9797-7c8f-9409cbfa.crewai.com/status/KICKOFF_ID" | jq .

curl -sS \
  -H "Authorization: Bearer 080eb21cd814" \
  "https://latest-ai-flow-273bc72f-2749-43bc-9797-7c8f-9409cbfa.crewai.com/status/5d2b29ad-8178-45d7-b0f3-b15b689ae316" | jq .