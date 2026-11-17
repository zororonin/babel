"""Unit tests for structured logging and log record formatting."""

import json
import logging

from app.core.logging import JSONFormatter, get_logger, setup_logging


def test_json_formatter_serializes_fields() -> None:
    """Verify JSONFormatter outputs valid JSON with expected metadata fields."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Sample log message: %s",
        args=("babel",),
        exc_info=None,
    )

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert data["level"] == "INFO"
    assert data["logger"] == "test_logger"
    assert data["message"] == "Sample log message: babel"
    assert "timestamp" in data
    assert "line_no" in data


def test_setup_logging_configures_root_logger() -> None:
    """Verify setup_logging sets root log level and attaches stream handler."""
    setup_logging(log_level="DEBUG", log_format="json")
    root = logging.getLogger()
    assert root.level == logging.DEBUG
    assert len(root.handlers) >= 1

    setup_logging(log_level="WARNING", log_format="text")
    assert root.level == logging.WARNING


def test_get_logger_returns_named_logger() -> None:
    """Verify get_logger returns an instance of logging.Logger."""
    logger = get_logger("custom_service")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "custom_service"
