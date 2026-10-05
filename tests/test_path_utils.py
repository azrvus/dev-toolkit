"""Tests for path and filesystem pattern utilities."""

from pathlib import Path

import pytest

from dev_toolkit.path_utils import (
    find_files,
    get_dir_size,
    get_tree,
    replace_extension,
)


def test_replace_extension():
    assert replace_extension("script.py", "txt") == Path("script.txt")
    assert replace_extension("archive.tar.gz", ".zip") == Path("archive.tar.zip")
    assert replace_extension("file_no_ext", "json") == Path("file_no_ext.json")


def test_get_dir_size(tmp_path):
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    f1 = tmp_path / "file1.txt"
    f2 = sub_dir / "file2.txt"

    f1.write_bytes(b"12345")  # 5 bytes
    f2.write_bytes(b"1234567890")  # 10 bytes

    assert get_dir_size(tmp_path) == 15

    with pytest.raises(ValueError):
        get_dir_size(tmp_path / "non_existent")


def test_find_files(tmp_path):
    (tmp_path / "app.py").touch()
    (tmp_path / "data.json").touch()

    ignored = tmp_path / ".git"
    ignored.mkdir()
    (ignored / "config.py").touch()

    py_files = list(find_files(tmp_path, patterns=["*.py"]))
    py_paths = [p.name for p in py_files]

    assert "app.py" in py_paths
    assert "config.py" not in py_paths


def test_get_tree(tmp_path):
    (tmp_path / "folder_a").mkdir()
    (tmp_path / "folder_a" / "file1.py").touch()
    (tmp_path / "file2.txt").touch()

    tree_str = get_tree(tmp_path, max_depth=2)
    assert tmp_path.name in tree_str
    assert "folder_a/" in tree_str
    assert "file1.py" in tree_str
    assert "file2.txt" in tree_str
