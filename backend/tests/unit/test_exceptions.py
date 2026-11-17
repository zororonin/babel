"""Unit tests for domain exceptions and exception handling."""

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient

from app.core.exceptions import (
    BabelException,
    ConfigurationException,
    DatabaseConnectionException,
    EntityNotFoundException,
    register_exception_handlers,
)


def test_babel_exception_defaults() -> None:
    """Verify default attributes of BabelException."""
    exc = BabelException(message="Sample error")
    assert exc.message == "Sample error"
    assert exc.code == "INTERNAL_ERROR"
    assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.details == {}


def test_specialized_exceptions() -> None:
    """Verify status codes and error codes of specialized exceptions."""
    config_exc = ConfigurationException("Missing secret")
    assert config_exc.code == "CONFIGURATION_ERROR"
    assert config_exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    db_exc = DatabaseConnectionException()
    assert db_exc.code == "DATABASE_UNAVAILABLE"
    assert db_exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    entity_exc = EntityNotFoundException(entity_name="User", identifier=42)
    assert entity_exc.code == "ENTITY_NOT_FOUND"
    assert entity_exc.status_code == status.HTTP_404_NOT_FOUND
    assert entity_exc.details == {"entity": "User", "identifier": "42"}


@pytest.mark.asyncio
async def test_custom_exception_handler_response() -> None:
    """Verify that raised BabelExceptions are translated to formatted JSON responses."""
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/trigger-error")
    async def trigger_error() -> None:
        raise DatabaseConnectionException("Connection timeout")

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/trigger-error")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "DATABASE_UNAVAILABLE"
    assert data["error"]["message"] == "Connection timeout"
