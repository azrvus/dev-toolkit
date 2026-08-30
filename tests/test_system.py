"""Tests for system inspection utilities."""

from dev_toolkit.system import get_system_info


def test_get_system_info_keys():
    info = get_system_info()
    expected_keys = {
        "os",
        "os_release",
        "architecture",
        "python_version",
        "python_implementation",
    }
    assert set(info.keys()) == expected_keys


def test_get_system_info_values_not_empty():
    info = get_system_info()
    for value in info.values():
        assert isinstance(value, str)
        assert len(value) > 0