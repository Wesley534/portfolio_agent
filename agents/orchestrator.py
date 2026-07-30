from __future__ import annotations

import logging
import os
from typing import Any

from agents.context import build_system_prompt
from providers.groq import GroqProvider
from providers.gemini import GeminiProvider
from providers.nim import NIMProvider
from providers.ollama import OllamaProvider
from providers.base import LLMProvider, ProviderQuotaExceeded
from rag.chroma import VectorStore
from tools.portfolio import PortfolioTool
from tools.resume import ResumeTool
from tools.certificates import CertificatesTool
from tools.case_studies import CaseStudiesTool
from tools.contact import ContactTool
from tools.email import EmailTool
from tools.whatsapp import WhatsAppTool
from tools.github import GitHubTool
from tools.blog import BlogTool
from tools.web_search import WebSearchTool

logger = logging.getLogger(__name__)


class PortfolioAgent:
    """Orchestrates the AI agent: intent detection, tool execution, response generation.

    Supports automatic provider failover — if one LLM provider runs out of credits
    (429/402/403 quota errors), it automatically falls back to the next configured provider.

    Priority order: Groq → Gemini → NVIDIA NIM → Ollama
    """

    _instance: PortfolioAgent | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._providers: list[LLMProvider] = []
        self._active_provider: LLMProvider | None = None
        self._failed_providers: set[str] = set()
        self._vector_store: VectorStore | None = None
        self._tools: dict[str, Any] = {}
        self._register_tools()
        self._init_providers()
        self._initialized = True

    def _register_tools(self):
        """Register all available tools."""
        self._tools = {
            "portfolio": PortfolioTool(),
            "resume": ResumeTool(),
            "certificates": CertificatesTool(),
            "case_studies": CaseStudiesTool(),
            "contact": ContactTool(),
            "email": EmailTool(),
            "whatsapp": WhatsAppTool(),
            "github": GitHubTool(),
            "blog": BlogTool(),
            "web_search": WebSearchTool(),
        }

    def _init_providers(self):
        """Initialize all configured providers in priority order.

        Priority: Groq → Gemini → NVIDIA NIM → Ollama
        Only initializes providers that have their API keys configured.
        """
        self._providers = []
        self._failed_providers = set()

        if os.getenv("GROQ_API_KEY"):
            provider = GroqProvider()
            self._providers.append(provider)
            logger.info("Registered provider: %s (%s)", provider.name, provider.model_name)

        if os.getenv("GEMINI_API_KEY"):
            provider = GeminiProvider()
            self._providers.append(provider)
            logger.info("Registered provider: %s (%s)", provider.name, provider.model_name)

        if os.getenv("NVIDIA_API_KEY"):
            provider = NIMProvider()
            self._providers.append(provider)
            logger.info("Registered provider: %s (%s)", provider.name, provider.model_name)

        if os.getenv("OLLAMA_BASE_URL"):
            provider = OllamaProvider()
            self._providers.append(provider)
            logger.info("Registered provider: %s (%s)", provider.name, provider.model_name)

        if self._providers:
            self._active_provider = self._providers[0]
            logger.info(
                "Active provider: %s (with %d fallback(s) configured)",
                self._active_provider.name,
                len(self._providers) - 1,
            )
        else:
            logger.warning("No LLM providers configured!")
            self._active_provider = None

    def _get_next_provider(self) -> LLMProvider | None:
        """Get the next available provider that hasn't failed yet.

        Skips providers in the failed set. If no providers remain, returns None.
        """
        for provider in self._providers:
            if provider.name not in self._failed_providers:
                self._active_provider = provider
                logger.info("Failing over to provider: %s", provider.name)
                return provider
        return None

    @property
    def provider(self) -> LLMProvider | None:
        """Return the current active provider."""
        return self._active_provider

    @property
    def active_provider(self) -> str:
        """Return the active provider name."""
        return self._active_provider.name if self._active_provider else "none"

    @property
    def available_providers(self) -> list[str]:
        """Return names of all registered providers."""
        return [p.name for p in self._providers]

    @property
    def vector_store(self) -> VectorStore:
        """Lazy-load the vector store."""
        if self._vector_store is None:
            persist_dir = os.getenv("CHROMA_PERSIST_DIR", "index")
            self._vector_store = VectorStore(persist_dir=persist_dir)
            if self._vector_store.is_loaded():
                logger.info(
                    "Vector store loaded with %d documents",
                    self._vector_store.get_document_count(),
                )
        return self._vector_store

    def _detect_intent(self, message: str) -> str | None:
        """Simple keyword-based intent detection to route to the right tool."""
        msg_lower = message.lower()

        if any(word in msg_lower for word in ["contact", "email", "reach", "message", "get in touch"]):
            return "contact"
        if any(word in msg_lower for word in ["resume", "cv", "experience", "background", "work history"]):
            return "resume"
        if any(word in msg_lower for word in ["certif", "credential", "badge", "course", "training"]):
            return "certificates"
        if any(word in msg_lower for word in ["case study", "case-study", "deployment"]):
            return "case_studies"
        if any(word in msg_lower for word in ["github", "repository", "repo", "open source", "source code"]):
            return "github"
        if any(word in msg_lower for word in ["blog", "article", "post", "write", "tutorial"]):
            return "blog"
        if any(word in msg_lower for word in ["search", "find", "look up", "google", "web"]):
            return "web_search"
        if any(word in msg_lower for word in ["project", "build", "develop", "create", "software", "app", "application"]):
            return "portfolio"

        return None

    async def _generate_with_failover(
        self,
        system_prompt: str,
        messages: list[dict],
    ) -> tuple[str, str]:
        """Try to generate a response, failing over between providers on quota errors.

        Logs each provider's specific failure reason separately so it's clear
        exactly why each provider was skipped.

        Returns:
            Tuple of (response_text, provider_name).
        """
        last_error = None
        failure_log = []

        while True:
            provider = self._get_next_provider()
            if not provider:
                # All providers exhausted — log the full failure chain
                for entry in failure_log:
                    logger.warning(
                        "Provider failure chain | %s | reason=%s",
                        entry["provider"],
                        entry["reason"],
                    )
                if last_error:
                    raise last_error
                raise RuntimeError("No LLM providers available")

            try:
                response = await provider.generate(
                    system_prompt=system_prompt,
                    messages=messages,
                )
                # Success — return response and provider name
                return response, provider.name

            except ProviderQuotaExceeded as e:
                # Provider ran out of credits — mark as failed and try next
                self._failed_providers.add(provider.name)
                # Extract a concise reason from the error message
                reason = self._extract_quota_reason(str(e))
                failure_log.append({
                    "provider": provider.name,
                    "reason": reason,
                    "status_code": e.status_code,
                })
                logger.warning(
                    "Provider '%s' failed | type=quota | status=%d | reason=%s | "
                    "remaining_providers=%s",
                    provider.name,
                    e.status_code,
                    reason,
                    [p.name for p in self._providers if p.name not in self._failed_providers],
                )
                last_error = e
                # Continue loop to try next provider

            except Exception as e:
                # Non-quota error — mark as failed too (something's wrong)
                self._failed_providers.add(provider.name)
                reason = f"{type(e).__name__}: {e!s}"
                failure_log.append({
                    "provider": provider.name,
                    "reason": reason,
                    "status_code": getattr(e, "status_code", None),
                })
                logger.error(
                    "Provider '%s' failed | type=error | reason=%s | "
                    "remaining_providers=%s",
                    provider.name,
                    reason,
                    [p.name for p in self._providers if p.name not in self._failed_providers],
                )
                last_error = e
                # Continue loop to try next provider

    @staticmethod
    def _extract_quota_reason(error_message: str) -> str:
        """Extract a concise quota reason from a verbose provider error."""
        # Try to extract the status message portion
        if "RESOURCE_EXHAUSTED" in error_message:
            return "rate_limit_exceeded"
        if "quota" in error_message.lower():
            # Truncate to first 120 chars for readability
            return error_message[:120]
        return error_message[:100]

    async def run(self, messages: list[dict], session_id: str = "") -> dict[str, Any]:
        """Process a conversation turn and return the response."""
        user_message = messages[-1]["content"] if messages else ""

        # Step 1: Check provider availability
        if not self._providers:
            return {
                "response": (
                    "I'm not fully configured yet — I need an API key to run. "
                    "In the meantime, feel free to browse my projects or reach out directly!"
                ),
                "tool_used": None,
            }

        # Step 2: Detect intent
        intent = self._detect_intent(user_message)

        # Step 3: Execute tool and get results
        tool_result = None
        tool_used = None

        if intent and intent in self._tools:
            tool = self._tools[intent]
            try:
                tool_result = await tool.execute(user_message)
                tool_used = tool.name
                logger.info("Tool used: %s", tool_used)
            except Exception as e:
                logger.error("Tool execution failed: %s | error=%s: %s", tool_used, type(e).__name__, e)
                tool_result = None
        else:
            try:
                results = self.vector_store.search(user_message, n_results=5, min_score=0.3)
                if results:
                    tool_result = results
                    tool_used = "portfolio_search"
            except Exception as e:
                # RAG failure is non-fatal — LLM still runs without context
                logger.warning(
                    "RAG vector search failed (non-fatal) | error=%s: %s | "
                    "LLM will respond without portfolio context",
                    type(e).__name__, e,
                )
                tool_result = None

        # Step 4: Build system prompt with context
        system_prompt = build_system_prompt(retrieved_context=tool_result)

        # Step 5: Generate response with automatic provider failover
        try:
            response, used_provider = await self._generate_with_failover(
                system_prompt=system_prompt,
                messages=messages,
            )
            logger.info("Response generated by provider: %s", used_provider)
        except Exception as e:
            logger.exception("All LLM providers failed")
            response = (
                "Sorry, all my AI providers are currently unavailable. "
                "Please try again later or reach out directly via the Contact page!"
            )

        return {
            "response": response,
            "tool_used": tool_used,
        }

    def get_tool_descriptions(self) -> list[dict]:
        """Return descriptions of all registered tools."""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._tools.values()
        ]

    def get_tool(self, name: str) -> Any | None:
        """Get a registered tool by name."""
        return self._tools.get(name)

    def get_index_info(self) -> dict:
        """Return information about the loaded vector index."""
        return {
            "loaded": self.vector_store.is_loaded(),
            "document_count": self.vector_store.get_document_count(),
        }

    async def cleanup(self):
        """Clean up resources (httpx clients, etc.)."""
        for provider in self._providers:
            if hasattr(provider, "close"):
                try:
                    await provider.close()
                except Exception:
                    pass
        logger.info("Cleaned up %d provider(s)", len(self._providers))
