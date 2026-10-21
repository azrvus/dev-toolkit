from dev_toolkit.url_utils import (
    add_query_params,
    parse_query_params,
    remove_query_params,
)


def test_parse_query_params():
    url = "https://example.com/path?foo=bar&baz=123"
    params = parse_query_params(url)
    assert params == {"foo": "bar", "baz": "123"}


def test_add_query_params():
    url = "https://example.com/path?foo=bar"
    updated = add_query_params(url, {"baz": "456", "foo": "updated"})
    assert "foo=updated" in updated
    assert "baz=456" in updated


def test_remove_query_params():
    url = "https://example.com/path?foo=bar&baz=123"
    cleaned = remove_query_params(url, ["baz"])
    assert cleaned == "https://example.com/path?foo=bar"
