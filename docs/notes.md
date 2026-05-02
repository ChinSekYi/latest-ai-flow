# Learning Log

# what I implemented vs what Cursor assisted with
- Built a CrewAI content-generation flow end-to-end (planning -> writing -> editing -> save output) and deployed it to CrewAI AMP.
- Defined project architecture and debugging strategy myself (provider routing, env var ownership, deployment checks, API wrapper approach).
- Used Cursor to speed up boilerplate (file scaffolding, API wiring, repetitive config updates, quick refactors).
- Kept core logic decisions manual: LLM provider handling, error diagnosis, secret validation strategy, and production-safe token flow.
- Added a custom Cursor rule in `.cursor/rules/learning-protocol.mdc` so Cursor assists on boilerplate while I own engineering logic.
- Implemented a FastAPI wrapper so external users call my API, while deployment credentials stay server-side.

# key engineering insights



# tradeoffs and why you chose current approach




---
# Learning plan
1) Build a mental model first (30 min)
Read in this order:

README.md (big picture)
src/latest_ai_flow/main.py (flow orchestration)
src/latest_ai_flow/crews/content_crew/content_crew.py (agent + LLM wiring)
src/latest_ai_flow/crews/content_crew/config/agents.yaml
src/latest_ai_flow/crews/content_crew/config/tasks.yaml
Goal: answer in your own words:

What triggers each step?
Which agent does what?
Where is LLM config resolved?
2) Trace one full run (30–45 min)
Run locally and watch logs:

uv run crewai run
As it runs, note:

flow methods called (plan_content → generate_content → save_content)
task order
which agent handles each task
where output is persisted (output/post.md)
3) Do 3 tiny experiments (best learning)
Change one thing at a time, rerun, observe:

Edit planner goal in agents.yaml (see style change)
Tighten word count in tasks.yaml (see behavior shift)
Switch model in env (see quality/speed change)
4) Learn agent concepts through your own code
Use your project as examples:

Agent = role + goal + backstory (agents.yaml)
Task = concrete job (tasks.yaml)
Crew = executes tasks sequentially (content_crew.py)
Flow = orchestrates when crew runs (main.py)

5) Keep a learning log (5 min/session)
In docs/notes.md, add 3 bullets after each session:

What I changed
What happened
What I learned