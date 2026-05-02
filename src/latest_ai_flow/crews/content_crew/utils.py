import os

from crewai import LLM


def openrouter_llm() -> LLM:
    """Build a CrewAI LLM configured for OpenRouter from environment variables."""
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
