from __future__ import annotations

import logging
import os

import httpx

from providers.base import LLMProvider, ProviderConfig

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """Provider for locally-hosted Ollama models.

    This is a future upgrade path. Requires Ollama running on a VPS.
    """

    def __init__(self, model: str = "llama3.2:1b", base_url: str = ""):
        api_key = os.getenv("OLLAMA_API_KEY", "")
        ollama_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        config = ProviderConfig(
            api_key=api_key,
            model=model,
            base_url=ollama_url,
            max_tokens=2048,
            temperature=0.7,
        )
        super().__init__(config)

    def _build_client(self):
        return httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=60.0,  # Ollama can be slow on CPU
        )

    async def generate(
        self,
        system_prompt: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> str:
        # Ollama OpenAI-compatible endpoint
        body = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages,
            ],
            "options": {
                "num_predict": self.config.max_tokens,
                "temperature": self.config.temperature,
            },
            "stream": False,
        }

        response = await self._client.post("/v1/chat/completions", json=body)
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"] or ""

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self.config.model

    async def close(self):
        await self._client.aclose()
