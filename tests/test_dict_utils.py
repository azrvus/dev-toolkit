"""Tests for dictionary and sequence utilities."""

import pytest

from dev_toolkit.dict_utils import (
    chunk_list,
    deep_merge,
    filter_keys,
    flatten_dict,
    get_in,
    omit,
    pick,
)


def test_get_in():
    data = {"a": {"b": {"c": 42}}}
    assert get_in(data, ["a", "b", "c"]) == 42
    assert get_in(data, ["a", "x"], default="missing") == "missing"


def test_flatten_dict():
    data = {"a": {"b": 1}, "c": 2}
    assert flatten_dict(data) == {"a.b": 1, "c": 2}


def test_deep_merge():
    d1 = {"a": 1, "b": {"c": 2}}
    d2 = {"b": {"d": 3}, "e": 4}
    assert deep_merge(d1, d2) == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}


def test_pick_and_omit():
    data = {"a": 1, "b": 2, "c": 3}
    assert pick(data, ["a", "c"]) == {"a": 1, "c": 3}
    assert omit(data, ["b"]) == {"a": 1, "c": 3}


def test_filter_keys():
    data = {"a": 1, "b": None, "c": {"d": 2, "e": None}}
    filtered = filter_keys(data, lambda k, v: v is not None)
    assert filtered == {"a": 1, "c": {"d": 2}}


def test_chunk_list():
    items = [1, 2, 3, 4, 5]
    chunks = list(chunk_list(items, chunk_size=2))
    assert chunks == [[1, 2], [3, 4], [5]]

    with pytest.raises(ValueError):
        list(chunk_list(items, chunk_size=0))
