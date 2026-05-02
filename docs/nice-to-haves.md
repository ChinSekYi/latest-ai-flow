# Nice-to-Haves

## P1 - High Impact
- **Input validation**  
  - Vibe version: accept any topic string.  
  - Engineer version: use a strict Pydantic request model (e.g. `topic`, `word_count`, `target_audience`).

- **Output guardrails**  
  - Vibe version: trust model output as-is.  
  - Engineer version: add a fact-check/review step (agent + tool) before final output.

## P2 - Medium Impact
- **Observability and tracing**  
  - Vibe version: rely on terminal logs.  
  - Engineer version: integrate AgentOps or LangSmith for token, latency, and step-level traces.

## P3 - Nice polish
- **User-facing UX**  
  - Add a simple frontend form for topic submission and result viewing.
- **Config profiles**  
  - Add `dev` vs `prod` config presets for model, verbosity, and timeout settings.