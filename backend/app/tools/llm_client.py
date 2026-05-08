"""Generic LLM client — supports both OpenAI and Anthropic API formats.

Auto-detects format based on URL (contains "anthropic" → Anthropic format).
Configure via .env:
    LLM_BASE_URL=https://token-plan-cn.xiaomimimo.com/anthropic
    LLM_API_KEY=your-key
    LLM_MODEL=mimo-v2.5-pro
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Synchronous LLM client supporting OpenAI and Anthropic API formats."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        timeout: int | None = None,
    ) -> None:
        self.base_url = (base_url or settings.llm_base_url).rstrip("/")
        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model
        self.max_tokens = max_tokens or settings.llm_max_tokens
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self.timeout = timeout or settings.llm_timeout_seconds

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    @property
    def _is_anthropic(self) -> bool:
        """Detect Anthropic format from URL."""
        return "anthropic" in self.base_url.lower()

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """Send a chat request and return the assistant message text."""
        if not self.is_configured:
            raise RuntimeError("LLM API key not configured. Set LLM_API_KEY in .env")

        if self._is_anthropic:
            return self._chat_anthropic(messages, temperature=temperature, max_tokens=max_tokens)
        return self._chat_openai(messages, temperature=temperature, max_tokens=max_tokens, response_format=response_format)

    def _chat_openai(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """OpenAI-compatible /chat/completions endpoint."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }
        if response_format:
            payload["response_format"] = response_format

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            resp = httpx.post(url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("LLM API HTTP error: %s — %s", e.response.status_code, e.response.text[:500])
            raise RuntimeError(f"LLM API error {e.response.status_code}: {e.response.text[:200]}") from e
        except Exception as e:
            logger.error("LLM API request failed: %s", e)
            raise RuntimeError(f"LLM API request failed: {e}") from e

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error("Unexpected LLM response: %s", data)
            raise RuntimeError(f"Unexpected LLM response: {data}") from e

    def _chat_anthropic(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Anthropic Messages API endpoint."""
        # Extract system message if present
        system_text = ""
        user_messages: list[dict[str, str]] = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                user_messages.append(msg)

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": user_messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }
        if system_text:
            payload["system"] = system_text

        url = f"{self.base_url}/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        try:
            resp = httpx.post(url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("LLM API HTTP error: %s — %s", e.response.status_code, e.response.text[:500])
            raise RuntimeError(f"LLM API error {e.response.status_code}: {e.response.text[:200]}") from e
        except Exception as e:
            logger.error("LLM API request failed: %s", e)
            raise RuntimeError(f"LLM API request failed: {e}") from e

        try:
            # Anthropic response: {"content": [{"type": "text", "text": "..."}]}
            return data["content"][0]["text"]
        except (KeyError, IndexError) as e:
            logger.error("Unexpected LLM response: %s", data)
            raise RuntimeError(f"Unexpected LLM response: {data}") from e

    def chat_json(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        """Send a chat request and parse the response as JSON."""
        # Anthropic doesn't support response_format, so we always request text
        # and parse JSON from the response
        text = self.chat(messages, temperature=temperature, max_tokens=max_tokens)

        # Try parsing as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            if "```json" in text:
                start = text.index("```json") + 7
                end = text.index("```", start)
                return json.loads(text[start:end].strip())
            if "```" in text:
                start = text.index("```") + 3
                end = text.index("```", start)
                return json.loads(text[start:end].strip())
            raise


# Module-level singleton
llm = LLMClient()
