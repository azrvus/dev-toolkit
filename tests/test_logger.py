"""Tests for JSON logger utility."""

import json
import logging

from dev_toolkit.logger import get_json_logger


def test_json_logger_output(capsys):
    logger = get_json_logger("test_logger", level=logging.INFO)
    logger.info("Test structured log message")

    captured = capsys.readouterr()
    log_entry = json.loads(captured.out.strip())

    assert log_entry["level"] == "INFO"
    assert log_entry["message"] == "Test structured log message"
    assert "timestamp" in log_entry
    assert log_entry["module"] == "test_logger"
