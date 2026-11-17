"""Integration tests for database session lifecycle and connectivity checks."""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.audit import BaselineAudit
from app.infrastructure.database.session import check_database_connection, get_db


@pytest.mark.asyncio
async def test_check_database_connection_success() -> None:
    """Verify check_database_connection returns True when query succeeds."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    mock_session.execute.return_value = mock_result

    result = await check_database_connection(mock_session)
    assert result is True


@pytest.mark.asyncio
async def test_check_database_connection_failure() -> None:
    """Verify check_database_connection returns False when query raises an exception."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.side_effect = ConnectionRefusedError("Connection refused")

    result = await check_database_connection(mock_session)
    assert result is False


@pytest.mark.asyncio
async def test_get_db_session_lifecycle_rollback_on_error() -> None:
    """Verify get_db generator rolls back transaction upon encountering an error."""
    mock_session = AsyncMock(spec=AsyncSession)

    class MockContextManager:
        async def __aenter__(self) -> AsyncSession:
            return mock_session

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: object,
        ) -> None:
            pass

    mock_factory = MagicMock(return_value=MockContextManager())

    with patch(
        "app.infrastructure.database.session.get_session_factory",
        return_value=mock_factory,
    ):
        gen = get_db()
        await gen.asend(None)
        with pytest.raises(RuntimeError):
            await gen.athrow(RuntimeError("Simulated transaction fault"))

    mock_session.rollback.assert_awaited_once()
    mock_session.close.assert_awaited_once()


def test_baseline_audit_model_attributes() -> None:
    """Verify BaselineAudit ORM model field definitions and defaults."""
    audit_id = uuid.uuid4()
    audit = BaselineAudit(
        id=audit_id,
        component="FastAPI Backend",
        status="INITIALIZED",
        details="Sprint 1 foundation verification",
    )

    assert audit.id == audit_id
    assert audit.component == "FastAPI Backend"
    assert audit.status == "INITIALIZED"
    assert audit.details == "Sprint 1 foundation verification"
    assert audit.__tablename__ == "sprint1_audit"
