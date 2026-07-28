from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider."""

    api_key: str
    model: str = ""
    base_url: str = ""
    max_tokens: int = 1024
    temperature: float = 0.7


class ProviderQuotaExceeded(Exception):
    """Raised when a provider has run out of credits or hit rate limits.

    The orchestrator catches this and falls back to the next available provider.
    """

    def __init__(self, provider_name: str, status_code: int, message: str = ""):
        self.provider_name = provider_name
        self.status_code = status_code
        super().__init__(f"{provider_name} quota exceeded ({status_code}): {message}")


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self._client = self._build_client()

    @abstractmethod
    def _build_client(self):
        """Build the provider-specific client."""
        ...

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> str:
        """Generate a response from the LLM.

        Args:
            system_prompt: The system prompt with context and personality.
            messages: Conversation history as list of {role, content} dicts.
            tools: Optional list of tool definitions the model can use.

        Returns:
            The generated response text.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Current model name."""
        ...
