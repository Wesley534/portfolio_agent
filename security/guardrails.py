from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GuardrailResult:
    blocked: bool
    response: str = ""
    reason: str = ""


# Topics that are out of scope for a portfolio assistant
OFF_TOPIC_PATTERNS = [
    r"\b(homework|assignment|exam|test)\b.*\b(help|do|solve|answer)\b",
    r"\b(write|create|make)\b.*\b(essay|story|poem)\b",
    r"\b(general knowledge|trivia|random fact)\b",
    r"\b(politics|political|election|president)\b.*\b(opinion|thoughts|view)\b",
    r"\b(medical|legal|financial)\b.*\b(advice|counsel|recommendation)\b",
]

# Prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|directions|prompts)",
    r"forget\s+(everything|all)\s+(you\s+)?(know|learned|were\s+told)",
    r"act\s+as\s+(if\s+)?you\s+are\s+(?!wesley|peter|wes)",
    r"you\s+are\s+(not\s+)?(chatgpt|gpt|ai|assistant|language model|llm)",
    r"reveal\s+(your\s+)?(prompt|instructions|system prompt|configuration)",
    r"output\s+(your\s+)?(prompt|instructions|system prompt)",
    r"print\s+(your\s+)?(prompt|instructions|system prompt)",
    r"\(System\)|\[System\]|\{System\}",
]


class Guardrails:
    """Multi-layer guardrail system for scope validation and prompt protection."""

    def __init__(self):
        self._off_topic_patterns = [re.compile(p, re.IGNORECASE) for p in OFF_TOPIC_PATTERNS]
        self._injection_patterns = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

    def check(self, message: str) -> GuardrailResult:
        """Run all guardrail checks on a message.

        Returns GuardrailResult with blocked=True if the message should be rejected.
        """
        # Check for prompt injection first
        injection_result = self._check_injection(message)
        if injection_result.blocked:
            return injection_result

        # Check for off-topic content
        topic_result = self._check_topic(message)
        if topic_result.blocked:
            return topic_result

        return GuardrailResult(blocked=False)

    def _check_injection(self, message: str) -> GuardrailResult:
        """Detect prompt injection attempts."""
        for pattern in self._injection_patterns:
            if pattern.search(message):
                logger.warning("Prompt injection detected: %s", pattern.pattern)
                return GuardrailResult(
                    blocked=True,
                    response=(
                        "I'm here to talk about Wesley's work in backend engineering, "
                        "blockchain, and security. What would you like to know about his projects?"
                    ),
                    reason=f"Injection pattern matched: {pattern.pattern}",
                )
        return GuardrailResult(blocked=False)

    def _check_topic(self, message: str) -> GuardrailResult:
        """Check if the message is off-topic for a portfolio assistant."""
        # Always allow certain intents
        message_lower = message.lower()
        allowed_prefixes = [
            "hi", "hello", "hey", "thanks", "thank you",
            "who are you", "what can you",
        ]
        if any(message_lower.startswith(p) for p in allowed_prefixes):
            return GuardrailResult(blocked=False)

        for pattern in self._off_topic_patterns:
            if pattern.search(message):
                logger.info("Off-topic message blocked: %s", pattern.pattern)
                return GuardrailResult(
                    blocked=True,
                    response=(
                        "I'm focused on Wesley's work — his projects, skills, "
                        "certifications, and experience in backend engineering, "
                        "blockchain, and security. What would you like to know about that?"
                    ),
                    reason=f"Off-topic pattern matched: {pattern.pattern}",
                )
        return GuardrailResult(blocked=False)
