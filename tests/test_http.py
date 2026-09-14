"""Tests for async HTTP utilities."""

import pytest

from dev_toolkit.http import fetch_json


@pytest.mark.asyncio
async def test_fetch_json_mock(monkeypatch):
    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return b'{"status": "ok"}'

    monkeypatch.setattr(
        "dev_toolkit.http.urlopen", lambda req, timeout=10.0: MockResponse()
    )

    data = await fetch_json("https://api.example.com/data")
    assert data == {"status": "ok"}
