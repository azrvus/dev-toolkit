from __future__ import annotations

import random
import string
import uuid

__all__ = ["generate_uuid", "random_string"]


def random_string(
    length: int = 10, chars: str = string.ascii_letters + string.digits
) -> str:
    """Generate a random string of specified length from given characters."""
    return "".join(random.choices(chars, k=length))


def generate_uuid() -> str:
    """Generate a random UUID4 hex string."""
    return uuid.uuid4().hex
