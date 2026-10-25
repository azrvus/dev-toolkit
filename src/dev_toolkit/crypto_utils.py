from __future__ import annotations

import hashlib
import secrets

__all__ = ["generate_token", "md5_hash", "sha256_hash"]


def generate_token(length: int = 32) -> str:
    """Generate a secure URL-safe random token."""
    return secrets.token_hex(length)


def sha256_hash(text: str) -> str:
    """Compute the SHA-256 cryptographic hash of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def md5_hash(text: str) -> str:
    """Compute the MD5 hash of a string."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()
