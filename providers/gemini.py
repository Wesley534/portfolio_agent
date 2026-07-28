from __future__ import annotations

import logging
import os

import httpx

from providers.base import LLMProvider, ProviderConfig, ProviderQuotaExceeded

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Provider for Google's Gemini API."""

    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, model: str = "gemini-1.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY", "")
        config = ProviderConfig(
            api_key=api_key,
            model=model,
            base_url=self.GEMINI_BASE_URL,
            max_tokens=2048,
            temperature=0.7,
        )
        super().__init__(config)

    def _build_client(self):
        return httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=30.0,
        )

    async def generate(
        self,
        system_prompt: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> str:
        # Gemini uses a slightly different API format
        # Convert messages to Gemini format
        gemini_contents = []

        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}],
            })

        # Build request body
        body = {
            "contents": gemini_contents,
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "maxOutputTokens": self.config.max_tokens,
                "temperature": self.config.temperature,
            },
        }

        url = f"/models/{self.config.model}:generateContent?key={self.config.api_key}"
        response = await self._client.post(url, json=body)

        # Check for quota / rate-limit errors
        if response.status_code in (429, 402):
            raise ProviderQuotaExceeded(
                provider_name=self.name,
                status_code=response.status_code,
                message=response.text,
            )
        if response.status_code == 403 and "quota" in response.text.lower():
            raise ProviderQuotaExceeded(
                provider_name=self.name,
                status_code=response.status_code,
                message=response.text,
            )

        response.raise_for_status()

        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return ""

        parts = candidates[0]["content"].get("parts", [])
        return "".join(part.get("text", "") for part in parts)

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self.config.model

    async def close(self):
        await self._client.aclose()
