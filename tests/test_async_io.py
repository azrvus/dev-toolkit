"""Tests for asynchronous I/O utilities."""

import asyncio

from dev_toolkit.async_io import read_json_async, write_json_async


def test_async_write_and_read_json(tmp_path):
    file_path = tmp_path / "async_data.json"
    data = {"key": "async_value", "status": True}

    async def run_test():
        await write_json_async(file_path, data)
        result = await read_json_async(file_path)
        return result

    result = asyncio.run(run_test())
    assert result == data
    assert file_path.exists()
