# Troubleshooting

## Incident: OpenRouter 401 "Missing Authentication header"

- **Symptom**
  - Deployment runs failed with `401` and message: `Missing Authentication header`.
  - Flow failed at `generate_content` / crew kickoff.

- **Root cause**
  - Runtime `OPENROUTER_API_KEY` was malformed in deployment env (`ssk-...` instead of `sk-or-...`), even though local `.env` looked correct.

- **Fix**
  - Added runtime diagnostics to show key source, masked value, and length.
  - Corrected deployment secret values and redeployed.
  - Added temporary sanitizer for `ssk-or-...` -> `sk-or-...` to unblock runs.

- **How to prevent next time**
  - Rotate and re-paste secrets carefully (no extra chars/whitespace).
  - Keep both `OPENROUTER_API_KEY` and `OPENAI_API_KEY` aligned for compatibility paths.
  - Validate with one fresh kickoff after every secret update.