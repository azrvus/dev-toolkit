"""Asynchronous HTTP request utilities."""

import asyncio
import json
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen


async def fetch_json(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 10.0,
) -> Dict[str, Any]:
    """Fetch JSON payload asynchronously from a URL."""
    req = Request(url, headers=headers or {})

    def _sync_fetch() -> Dict[str, Any]:
        with urlopen(req, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    return await asyncio.to_thread(_sync_fetch)
