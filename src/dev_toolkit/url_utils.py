from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

__all__ = ["add_query_params", "parse_query_params", "remove_query_params"]


def parse_query_params(url: str) -> dict[str, str]:
    """Extract query parameters from a URL string into a dictionary."""
    parsed = urlparse(url)
    return dict(parse_qsl(parsed.query))


def add_query_params(url: str, params: dict[str, str]) -> str:
    """Add or update query parameters on a given URL."""
    parsed = urlparse(url)
    query_params = dict(parse_qsl(parsed.query))
    query_params.update(params)

    new_query = urlencode(query_params)
    new_parts = parsed._replace(query=new_query)
    return urlunparse(new_parts)


def remove_query_params(url: str, keys_to_remove: list[str]) -> str:
    """Remove specific query parameters from a URL string."""
    parsed = urlparse(url)
    query_params = dict(parse_qsl(parsed.query))

    for key in keys_to_remove:
        query_params.pop(key, None)

    new_query = urlencode(query_params)
    new_parts = parsed._replace(query=new_query)
    return urlunparse(new_parts)
