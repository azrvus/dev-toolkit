"""Asynchronous HTTP request utilities."""

import asyncio
import json
from typing import Any
from urllib.request import Request, urlopen


async def fetch_json(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Fetch JSON payload asynchronously from a URL."""
    req = Request(url, headers=headers or {})

    def _sync_fetch() -> dict[str, Any]:
        with urlopen(req, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    return await asyncio.to_thread(_sync_fetch)
