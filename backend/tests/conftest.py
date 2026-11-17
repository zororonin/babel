"""Pytest fixtures for Project Babel test suite."""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.core.config import Settings, get_settings
from app.main import app


@pytest.fixture
def test_settings() -> Settings:
    """Provide isolated settings for the test environment."""
    return Settings(
        APP_NAME="Project Babel Test",
        APP_ENV="testing",
        APP_VERSION="0.1.0-test",
        APP_DEBUG=True,
        DATABASE_URL="postgresql+psycopg://babel_app:babel_dev_password@localhost:5432/babel_test_db",
        LOG_LEVEL="DEBUG",
        LOG_FORMAT="text",
    )


@pytest_asyncio.fixture
async def async_client(test_settings: Settings) -> AsyncGenerator[AsyncClient, None]:
    """Provide an HTTPX AsyncClient bound to the FastAPI application."""
    app.dependency_overrides[get_settings] = lambda: test_settings

    # Provide a mock database session by default so API tests don't require external DB
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    mock_session.execute.return_value = mock_result

    app.dependency_overrides[get_db_session] = lambda: mock_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
