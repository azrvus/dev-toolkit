"""Tests for dictionary manipulation utilities."""

from dev_toolkit.dict_utils import deep_merge, flatten_dict, get_in


def test_deep_merge():
    base = {"a": 1, "b": {"x": 10, "y": 20}}
    override = {"b": {"y": 99, "z": 30}, "c": 3}
    merged = deep_merge(base, override)

    assert merged == {"a": 1, "b": {"x": 10, "y": 99, "z": 30}, "c": 3}
    # Ensure original dictionaries were not mutated
    assert base["b"]["y"] == 20


def test_flatten_dict():
    nested = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
    flattened = flatten_dict(nested)

    assert flattened == {"a": 1, "b.c": 2, "b.d.e": 3}


def test_get_in():
    data = {"db": {"connection": {"host": "localhost", "port": 5432}}}

    assert get_in(data, "db.connection.host") == "localhost"
    assert get_in(data, "db.connection.port") == 5432
    assert get_in(data, "db.connection.user", default="postgres") == "postgres"
    assert get_in(data, "invalid.path", default=None) is None
