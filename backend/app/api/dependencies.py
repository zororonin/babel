"""API dependency injection providers."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import get_db

# Type annotations for dependency injection
SettingsDep = Annotated[Settings, Depends(get_settings)]
DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency provider for database sessions."""
    async for session in get_db():
        yield session
