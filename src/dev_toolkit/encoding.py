from __future__ import annotations

import base64

__all__ = ["base64_decode", "base64_encode"]


def base64_encode(data: str | bytes) -> str:
    """Encode a string or bytes into a Base64 string."""
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data
    return base64.b64encode(data_bytes).decode("utf-8")


def base64_decode(encoded_str: str) -> str:
    """Decode a Base64 string back to a UTF-8 string."""
    return base64.b64decode(encoded_str.encode("utf-8")).decode("utf-8")
