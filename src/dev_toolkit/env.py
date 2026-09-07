"""Environment variable helpers and validation utilities."""

import os


def check_required_env(required_vars: list[str]) -> list[str]:
    """Return a list of required environment variable names that are missing."""
    return [var for var in required_vars if var not in os.environ]


def mask_secret(secret: str, visible_chars: int = 4) -> str:
    """Mask a sensitive string, leaving only the last few characters visible."""
    if len(secret) <= visible_chars:
        return "*" * len(secret)
    return "*" * (len(secret) - visible_chars) + secret[-visible_chars:]


def get_env_summary() -> dict[str, bool]:
    """Check standard developer environment flags."""
    return {
        "DEBUG": os.getenv("DEBUG", "0").lower() in ("1", "true", "yes"),
        "CI": os.getenv("CI", "0").lower() in ("1", "true", "yes"),
    }
