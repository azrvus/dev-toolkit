from __future__ import annotations

import os
from typing import Any

__all__ = ["get_env_or_raise", "validate_env"]


def get_env_or_raise(key: str, default: Any = None) -> str:
    """Get an environment variable or raise a ValueError if missing."""
    val = os.getenv(key, default)
    if val is None or val == "":
        raise ValueError(f"Required environment variable '{key}' is missing or empty.")
    return str(val)


def validate_env(required_keys: list[str]) -> dict[str, str]:
    """Validate that multiple required environment variables are set."""
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
    return {key: os.environ[key] for key in required_keys}
