"""Tests for async HTTP utilities."""

import asyncio

from dev_toolkit.http import fetch_json


def test_fetch_json_mock(monkeypatch):
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

    data = asyncio.run(fetch_json("https://api.example.com/data"))
    assert data == {"status": "ok"}
