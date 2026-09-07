"""Tests for file I/O utilities."""

import pytest

from dev_toolkit.io import ensure_dir, read_json, write_json


def test_ensure_dir(tmp_path):
    nested_dir = tmp_path / "a" / "b" / "c"
    created = ensure_dir(nested_dir)
    assert created.exists()
    assert created.is_dir()


def test_write_and_read_json(tmp_path):
    target_file = tmp_path / "data" / "payload.json"
    data = {"status": "success", "code": 200, "items": ["a", "b"]}

    write_json(target_file, data)
    assert target_file.exists()

    loaded = read_json(target_file)
    assert loaded == data


def test_write_json_no_overwrite(tmp_path):
    target_file = tmp_path / "existing.json"
    write_json(target_file, {"initial": "value"})

    with pytest.raises(FileExistsError):
        write_json(target_file, {"new": "value"}, overwrite=False)
