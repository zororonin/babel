"""Sprint 1 baseline audit model for database migration verification."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class BaselineAudit(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Minimal audit model strictly used to validate migrations and transactions."""

    __tablename__ = "sprint1_audit"

    component: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Name of the initialized component",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Validation status indicator",
    )
    details: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Optional diagnostics or metadata",
    )
