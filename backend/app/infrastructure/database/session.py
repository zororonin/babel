"""Asynchronous SQLAlchemy 2.0 session and engine management."""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Return the initialized async engine singleton, creating it if needed."""
    global _engine
    if _engine is None:
        settings = get_settings()
        engine_kwargs: dict[str, Any] = {
            "echo": settings.APP_DEBUG,
            "future": True,
        }
        # SQLite in unit tests does not support pool_size / max_overflow
        if not settings.DATABASE_URL.startswith("sqlite"):
            engine_kwargs.update(
                {
                    "pool_size": settings.DB_POOL_SIZE,
                    "max_overflow": settings.DB_MAX_OVERFLOW,
                    "pool_timeout": settings.DB_POOL_TIMEOUT,
                    "pool_recycle": settings.DB_POOL_RECYCLE,
                    "pool_pre_ping": True,
                }
            )
        _engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
        logger.info(
            "Initialized async database engine: %s",
            settings.masked_database_url,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the session factory singleton, binding to the current engine."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        _session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
    return _session_factory


async def close_db_engine() -> None:
    """Dispose of the global async database engine and active connection pool."""
    global _engine, _session_factory
    if _engine is not None:
        logger.info("Disposing async database engine connection pool...")
        await _engine.dispose()
        _engine = None
        _session_factory = None
        logger.info("Database engine disposed.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection generator yielding an AsyncSession with cleanup."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection(session: AsyncSession) -> bool:
    """Execute a simple query to verify active database connectivity."""
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception as exc:
        logger.error("Database connectivity check failed: %s", str(exc))
        return False
