from __future__ import annotations

import re
from typing import Any

__all__ = ["mask_email", "mask_secret_string", "sanitize_dict"]

_EMAIL_REGEX = re.compile(r"(^[\w.%+-]+)@([\w.-]+\.[a-zA-Z]{2,})")
_TOKEN_KEYS = {"password", "secret", "token", "api_key", "auth", "credential"}


def mask_email(email: str, mask_char: str = "*", visible_chars: int = 2) -> str:
    """Mask an email address, keeping a few characters visible before the domain."""
    match = _EMAIL_REGEX.match(email)
    if not match:
        return email

    username, domain = match.groups()
    if len(username) <= visible_chars:
        masked_user = mask_char * len(username)
    else:
        masked_user = username[:visible_chars] + mask_char * (
            len(username) - visible_chars
        )
    return f"{masked_user}@{domain}"


def mask_secret_string(secret: str, mask_char: str = "*", visible_end: int = 4) -> str:
    """Mask a token or password, keeping the last few characters visible."""
    if len(secret) <= visible_end:
        return mask_char * len(secret)
    return mask_char * (len(secret) - visible_end) + secret[-visible_end:]


def sanitize_dict(data: dict[str, Any], mask_char: str = "*") -> dict[str, Any]:
    """Recursively traverse a dictionary and mask sensitive keys and values."""
    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(token in key_lower for token in _TOKEN_KEYS):
            if isinstance(value, str):
                sanitized[key] = mask_secret_string(value, mask_char=mask_char)
            else:
                sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, mask_char=mask_char)
        elif isinstance(value, str) and _EMAIL_REGEX.match(value):
            sanitized[key] = mask_email(value, mask_char=mask_char)
        else:
            sanitized[key] = value
    return sanitized
