"""Asynchronous file I/O utilities."""

import asyncio
from pathlib import Path
from typing import Any

from dev_toolkit.io import read_json, write_json


async def read_json_async(path: str | Path) -> dict[str, Any]:
    """Read and parse a JSON file asynchronously."""
    return await asyncio.to_thread(read_json, path)


async def write_json_async(
    path: str | Path, data: dict[str, Any], indent: int = 2
) -> None:
    """Write data to a JSON file asynchronously."""
    await asyncio.to_thread(write_json, path, data, indent)
