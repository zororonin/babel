"""Unit tests for centralized application settings and configuration."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


def test_default_settings() -> None:
    """Verify default configuration values."""
    settings = Settings(_env_file=None)
    assert settings.APP_NAME == "Project Babel"
    assert settings.APP_ENV == "development"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.APP_DEBUG is False
    assert settings.SERVER_PORT == 8000
    assert settings.LOG_LEVEL == "INFO"
    assert settings.is_development is True
    assert settings.is_testing is False
    assert settings.is_production is False


def test_settings_environment_modes() -> None:
    """Verify environment property flags for testing and production."""
    test_settings = Settings(APP_ENV="testing")
    assert test_settings.is_testing is True
    assert test_settings.is_development is False
    assert test_settings.is_production is False

    prod_settings = Settings(APP_ENV="production")
    assert prod_settings.is_production is True
    assert prod_settings.is_development is False
    assert prod_settings.is_testing is False


def test_invalid_environment_raises_validation_error() -> None:
    """Verify that an unsupported environment name fails validation."""
    with pytest.raises(ValidationError):
        Settings(APP_ENV="invalid_env")  # type: ignore[arg-type]


def test_invalid_database_url_scheme_raises_error() -> None:
    """Verify that non-async database URL schemes are rejected."""
    with pytest.raises(ValidationError):
        Settings(DATABASE_URL="postgresql://user:password@localhost/db")


def test_masked_database_url() -> None:
    """Verify that passwords are scrubbed in the masked database URL property."""
    settings = Settings(
        DATABASE_URL="postgresql+psycopg://myuser:secretpassword123@dbhost:5432/mydb"
    )
    masked = settings.masked_database_url
    assert "secretpassword123" not in masked
    assert "myuser:*****@dbhost:5432" in masked
    assert masked.endswith("/mydb")


def test_get_settings_cached_singleton() -> None:
    """Verify get_settings returns the same cached instance."""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
