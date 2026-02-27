"""Anthropic client with prompt caching support."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from cert_pepper.config import get_settings

# Lazy import to avoid startup cost when AI is not needed
_client: Any = None


def get_client() -> Any:
    """Return the Anthropic client (singleton)."""
    global _client
    if _client is None:
        import anthropic
        settings = get_settings()
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def make_prompt_hash(system: str, user: str) -> str:
    """Create a stable hash for deduplication."""
    combined = json.dumps({"system": system, "user": user}, sort_keys=True)
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def generate_explanation(
    system_prompt: str,
    user_message: str,
    model: str | None = None,
    use_cache: bool = True,
) -> tuple[str, int, bool]:
    """
    Generate an explanation using the Anthropic API.

    Returns:
        (content, tokens_used, cache_hit)
    """
    import anthropic

    settings = get_settings()
    if model is None:
        model = settings.sonnet_model

    client = get_client()

    if use_cache:
        # Use prompt caching on the system prompt (must be ≥1024 tokens for cache)
        messages_kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": 512,
            "system": [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            "messages": [{"role": "user", "content": user_message}],
        }
    else:
        messages_kwargs = {
            "model": model,
            "max_tokens": 512,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }

    response = client.messages.create(**messages_kwargs)

    content = response.content[0].text
    tokens = response.usage.input_tokens + response.usage.output_tokens
    cache_hit = hasattr(response.usage, "cache_read_input_tokens") and bool(
        response.usage.cache_read_input_tokens
    )

    return content, tokens, cache_hit


def generate_hint(question_stem: str, options: dict[str, str], model: str | None = None) -> str:
    """Generate a one-sentence hint for a question."""
    from cert_pepper.ai.prompts import get_hint_system

    settings = get_settings()
    if model is None:
        model = settings.haiku_model

    user = (
        f"Question: {question_stem}\n"
        + "\n".join(f"{k}) {v}" for k, v in options.items())
        + "\n\nGive me a hint without revealing the answer."
    )

    content, _, _ = generate_explanation(
        system_prompt=get_hint_system(),
        user_message=user,
        model=model,
        use_cache=False,  # hints are short-lived, no cache benefit
    )
    return content
