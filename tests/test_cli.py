"""Tests for CLI utilities."""

import pytest

from dev_toolkit.cli import main, parse_args


def test_parse_args_default():
    args = parse_args([])
    assert args.verbose is False


def test_parse_args_verbose():
    args = parse_args(["--verbose"])
    assert args.verbose is True

    args_short = parse_args(["-v"])
    assert args_short.verbose is True


def test_main_default_output(capsys):
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Dev Toolkit CLI operational." in captured.out
    assert "Verbose mode enabled." not in captured.out


def test_main_verbose_output(capsys):
    exit_code = main(["--verbose"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Verbose mode enabled." in captured.out


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "dev-toolkit 0.1.0" in captured.out
