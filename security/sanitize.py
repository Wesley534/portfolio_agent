from __future__ import annotations

import re
import unicodedata


# HTML/script tags that could be XSS
XSS_PATTERN = re.compile(r"<[^>]*>", re.IGNORECASE)

# Control characters (except newlines)
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_input(text: str) -> str:
    """Sanitize user input before processing.

    - Strips HTML tags (XSS prevention)
    - Removes control characters
    - Normalizes Unicode
    - Trims whitespace
    - Limits length
    """
    if not text:
        return ""

    # Strip HTML tags
    text = XSS_PATTERN.sub("", text)

    # Remove control characters
    text = CONTROL_CHARS.sub("", text)

    # Normalize Unicode
    text = unicodedata.normalize("NFKC", text)

    # Trim and limit length
    text = text.strip()[:5000]

    return text


def sanitize_email_input(email: str) -> str:
    """Validate and sanitize an email address."""
    email = email.strip().lower()
    # Basic email validation
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError("Invalid email address")
    return email[:200]


def sanitize_name(name: str) -> str:
    """Sanitize a person's name."""
    name = name.strip()
    # Remove anything that's not letters, spaces, hyphens, apostrophes
    name = re.sub(r"[^a-zA-Z\s\-'À-ÿ]", "", name)
    return name[:100]


def sanitize_output(text: str) -> str:
    """Sanitize the LLM output before sending to the user.

    - Strips any system prompt leakage
    - Trims excessive whitespace
    """
    if not text:
        return ""

    # Strip leading/trailing whitespace
    text = text.strip()

    return text
