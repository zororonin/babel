"""API endpoint tests for health, liveness, and readiness probes."""

from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.main import app


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Verify GET /health returns 200 OK with expected application metadata."""
    response = await async_client.get("/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "Project Babel Test"
    assert data["version"] == "0.1.0-test"
    assert data["environment"] == "testing"


@pytest.mark.asyncio
async def test_liveness_check_endpoint(async_client: AsyncClient) -> None:
    """Verify GET /health/live returns 200 OK with alive status."""
    response = await async_client.get("/health/live")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {"status": "alive"}


@pytest.mark.asyncio
async def test_readiness_check_endpoint_success(async_client: AsyncClient) -> None:
    """Verify GET /health/ready returns 200 OK when database is reachable."""
    response = await async_client.get("/health/ready")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {"status": "ready", "database": "connected"}


@pytest.mark.asyncio
async def test_readiness_check_endpoint_failure(async_client: AsyncClient) -> None:
    """Verify GET /health/ready returns 503 Service Unavailable when database fails."""
    # Override database session with a failing connection
    mock_failing_session = AsyncMock(spec=AsyncSession)
    mock_failing_session.execute.side_effect = ConnectionRefusedError(
        "PostgreSQL host unreachable"
    )

    app.dependency_overrides[get_db_session] = lambda: mock_failing_session

    response = await async_client.get("/health/ready")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "DATABASE_UNAVAILABLE"
    # Ensure sensitive credentials and raw connection parameters are not exposed
    assert "password" not in response.text.lower()
    assert "postgres://" not in response.text


@pytest.mark.asyncio
async def test_versioned_health_routes(async_client: AsyncClient) -> None:
    """Verify that health endpoints are also reachable under /api/v1 prefix."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK

    live_response = await async_client.get("/api/v1/health/live")
    assert live_response.status_code == status.HTTP_200_OK

    ready_response = await async_client.get("/api/v1/health/ready")
    assert ready_response.status_code == status.HTTP_200_OK
