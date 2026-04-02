"""
Anthropic Claude API wrapper for the recruitment system.
"""

import json
import os
import re

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-20250514"


class ClaudeClient:
    """Thin wrapper around the Anthropic client with JSON-parsing helpers."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not found. "
                "Copy .env.example to .env and add your key."
            )
        self.client = anthropic.Anthropic(api_key=api_key)

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def chat(self, system: str, user: str, max_tokens: int = 2048) -> str:
        """Single-turn chat. Returns the text content of the response."""
        message = self.client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return message.content[0].text

    def chat_json(self, system: str, user: str, max_tokens: int = 2048) -> dict | list:
        """
        Like chat(), but strips markdown fences and parses JSON.
        The system prompt should instruct the model to return only JSON.
        """
        raw = self.chat(system=system, user=user, max_tokens=max_tokens)
        # Strip ```json ... ``` or ``` ... ``` fences if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip())
        return json.loads(cleaned)
