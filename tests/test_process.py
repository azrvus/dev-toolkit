"""Tests for process execution utilities."""

import sys

import pytest

from dev_toolkit.process import ProcessResult, run_command


def test_run_command_success():
    cmd = [sys.executable, "-c", "print('hello from python')"]
    result = run_command(cmd)

    assert isinstance(result, ProcessResult)
    assert result.success is True
    assert result.returncode == 0
    assert result.stdout.strip() == "hello from python"
    assert result.stderr == ""


def test_run_command_str_input():
    cmd = f"{sys.executable} -c \"print('string cmd')\""
    result = run_command(cmd)

    assert result.success is True
    assert result.stdout.strip() == "string cmd"


def test_run_command_failure_no_check():
    cmd = [sys.executable, "-c", "import sys; sys.exit(2)"]
    result = run_command(cmd)

    assert result.success is False
    assert result.returncode == 2


def test_run_command_failure_with_check():
    cmd = [sys.executable, "-c", "import sys; sys.exit(1)"]
    with pytest.raises(RuntimeError) as exc_info:
        run_command(cmd, check=True)

    assert "failed with exit code 1" in str(exc_info.value)


def test_run_command_timeout():
    cmd = [sys.executable, "-c", "import time; time.sleep(0.5)"]
    with pytest.raises(TimeoutError) as exc_info:
        run_command(cmd, timeout=0.05)

    assert "timed out after 0.05 seconds" in str(exc_info.value)


def test_run_command_empty():
    with pytest.raises(ValueError):
        run_command([])
