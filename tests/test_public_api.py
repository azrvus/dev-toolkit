"""Regression checks for package exports."""

import dev_toolkit


def test_all_public_exports_resolve():
    for name in dev_toolkit.__all__:
        assert hasattr(dev_toolkit, name), f"Missing public export: {name}"

