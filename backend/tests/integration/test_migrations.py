"""Integration tests for Alembic migration definitions and metadata registration."""

import importlib.util
from pathlib import Path

import app.infrastructure.database.models  # noqa: F401
from app.infrastructure.database.base import Base


def test_models_registered_in_base_metadata() -> None:
    """Verify that ORM models are registered in SQLAlchemy metadata for Alembic."""
    assert "sprint1_audit" in Base.metadata.tables
    table = Base.metadata.tables["sprint1_audit"]
    assert "id" in table.columns
    assert "component" in table.columns
    assert "status" in table.columns
    assert "created_at" in table.columns
    assert "updated_at" in table.columns


def test_baseline_migration_revision_structure() -> None:
    """Verify that initial migration script defines upgrade and downgrade."""
    migration_path = (
        Path(__file__).parent.parent.parent
        / "migrations"
        / "versions"
        / "0001_initial_baseline.py"
    )
    assert migration_path.exists(), f"Migration file missing at {migration_path}"

    spec = importlib.util.spec_from_file_location("baseline_migration", migration_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "upgrade"), "Migration script missing upgrade() function"
    assert hasattr(module, "downgrade"), "Migration script missing downgrade() function"
    assert module.revision == "0001_initial_baseline"
    assert module.down_revision is None
