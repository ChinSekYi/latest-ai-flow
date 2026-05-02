# AI Blog Writer

Simple multi-agent blog/article writer built with [CrewAI](https://crewai.com).

This project takes a topic, generates an outline, writes a full draft, edits it, and saves the final post.

## Installation

Ensure you have Python 3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Run a local [Ollama](https://ollama.com/) server and use one of the models already installed locally**

- Start Ollama locally: `ollama serve`
- Check your installed models with `ollama list`
- Modify `src/latest_ai_flow/crews/content_crew/config/agents.yaml` if you want a different local model name
- You do not need a cloud API key for Ollama-based runs

- Modify `src/latest_ai_flow/config/agents.yaml` to define your agents
- Modify `src/latest_ai_flow/config/tasks.yaml` to define your tasks
- Modify `src/latest_ai_flow/crew.py` to add your own logic, tools and specific args
- Modify `src/latest_ai_flow/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command runs the `ContentFlow`.

It generates an article and saves the output to `output/post.md`.

## FastAPI Wrapper (for external users)

Use this service to safely expose your deployed CrewAI flow without leaking the deployment bearer token in a frontend.

Set environment variables:

```bash
export CREWAI_DEPLOYMENT_URL="https://latest-ai-flow-273bc72f-2749-43bc-9797-7c8f-9409cbfa.crewai.com"
export CREWAI_DEPLOYMENT_TOKEN="<your-deployment-token>"
```

Run API server:

```bash
uv run run_api
```

Available endpoints:

- `GET /health`
- `POST /kickoff` with body `{"topic":"Kelp in the UK"}`
- `GET /status/{kickoff_id}`
- `POST /generate` (kicks off + polls until `COMPLETED`/`FAILED`)

Note: the deployment status path is `/status/...` (not `/stauts/...`).

## How It Works

The `ContentCrew` has 3 agents:
- `planner` creates an outline
- `writer` creates the full draft
- `editor` polishes the final output

Tasks are defined in `src/latest_ai_flow/crews/content_crew/config/tasks.yaml` and agent roles are in `src/latest_ai_flow/crews/content_crew/config/agents.yaml`.