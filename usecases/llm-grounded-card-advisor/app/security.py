"""Input gates that run before customer data is accessed."""

from __future__ import annotations

import re


class UnsafeQueryError(ValueError):
    """Raised for prompt injection or sensitive personal data."""


_INJECTION_PATTERNS = (
    re.compile(r"\b(ignore|forget|override)\b.{0,30}\b(instructions?|prompt|policy|rules?)\b", re.I),
    re.compile(r"\b(system prompt|developer message|jailbreak)\b", re.I),
    re.compile(r"\b(reveal|print|dump|exfiltrate)\b.{0,30}\b(secret|token|key|credential)\b", re.I),
)
_PII_PATTERNS = (
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("payment-card number", re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)")),
    ("social-security number", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", re.I)),
)


def validate_query(query: str, *, max_length: int = 500) -> str:
    """Return normalized text or reject it before any retrieval occurs."""
    if any(ord(character) < 32 and character not in "\t\r\n" for character in query):
        raise UnsafeQueryError("query contains control characters")
    normalized = " ".join(query.split())
    if not normalized:
        raise UnsafeQueryError("query must not be empty")
    if len(normalized) > max_length:
        raise UnsafeQueryError(f"query exceeds {max_length} characters")
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(normalized):
            raise UnsafeQueryError("possible prompt-injection attempt")
    for label, pattern in _PII_PATTERNS:
        if pattern.search(normalized):
            raise UnsafeQueryError(f"query contains {label}; remove personal data")
    return normalized
