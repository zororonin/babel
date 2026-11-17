"""Initial baseline migration creating sprint1_audit table.

Revision ID: 0001_initial_baseline
Revises:
Create Date: 2026-11-17 18:00:00.000000+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_initial_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply baseline schema migration."""
    op.create_table(
        "sprint1_audit",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("component", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("details", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sprint1_audit_component"),
        "sprint1_audit",
        ["component"],
        unique=False,
    )


def downgrade() -> None:
    """Revert baseline schema migration."""
    op.drop_index(op.f("ix_sprint1_audit_component"), table_name="sprint1_audit")
    op.drop_table("sprint1_audit")
