"""Structured JSON logging utilities."""

import json
import logging
import sys
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def get_json_logger(
    name: str = "dev_toolkit", level: int = logging.INFO
) -> logging.Logger:
    """Configure and return a logger with JSON formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger
