from __future__ import annotations

import json
import logging
import os

import httpx

from providers.base import LLMProvider, ProviderConfig, ProviderQuotaExceeded

logger = logging.getLogger(__name__)


class NIMProvider(LLMProvider):
    """Provider for NVIDIA NIM (hosted API at integrate.api.nvidia.com).

    NVIDIA NIM provides OpenAI-compatible chat completions endpoints
    for a wide range of LLMs. Uses NVIDIA_API_KEY env variable.
    """

    NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self, model: str = "meta/llama-3.1-70b-instruct"):
        api_key = os.getenv("NVIDIA_API_KEY", "")
        config = ProviderConfig(
            api_key=api_key,
            model=model,
            base_url=self.NIM_BASE_URL,
            max_tokens=2048,
            temperature=0.7,
        )
        super().__init__(config)

    def _build_client(self):
        return httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def generate(
        self,
        system_prompt: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> str:
        body = {
            "model": self.config.model,
            "messages": [{"role": "system", "content": system_prompt}, *messages],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }
        if tools:
            body["tools"] = tools

        response = await self._client.post("/chat/completions", json=body)

        # Log response body for debugging non-200 responses
        if response.status_code != 200:
            try:
                error_body = response.json()
                logger.warning(
                    "NIM API error | status=%d | body=%s",
                    response.status_code,
                    json.dumps(error_body),
                )
            except Exception:
                logger.warning(
                    "NIM API error | status=%d | body=%s",
                    response.status_code,
                    response.text[:500],
                )

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
        return data["choices"][0]["message"]["content"] or ""

    @property
    def name(self) -> str:
        return "nim"

    @property
    def model_name(self) -> str:
        return self.config.model

    async def close(self):
        await self._client.aclose()
