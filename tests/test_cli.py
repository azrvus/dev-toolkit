"""Tests for CLI interface."""

import pytest

from dev_toolkit.cli import main


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["dev-toolkit", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Developer utility toolkit" in captured.out


def test_cli_sysinfo_subcommand(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["dev-toolkit", "sysinfo"])
    main()
    captured = capsys.readouterr()
    assert "System Information" in captured.out
