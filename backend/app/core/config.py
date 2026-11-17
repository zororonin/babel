"""Application configuration module using Pydantic Settings."""

from functools import lru_cache
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application Metadata
    APP_NAME: str = Field(default="Project Babel", description="Application name")
    APP_ENV: Literal["development", "testing", "staging", "production"] = Field(
        default="development",
        description="Deployment environment name",
    )
    APP_VERSION: str = Field(default="0.1.0", description="Semantic version string")
    APP_DEBUG: bool = Field(default=False, description="Debug mode flag")

    # Server Networking
    SERVER_HOST: str = Field(default="0.0.0.0", description="Host to bind HTTP server")
    SERVER_PORT: int = Field(default=8000, description="Port to bind HTTP server")

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    LOG_FORMAT: Literal["json", "text"] = Field(
        default="json",
        description="Structured JSON or plain text console logging format",
    )

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+psycopg://babel_app:babel_dev_password@localhost:5432/babel_db",
        description="Asynchronous PostgreSQL connection URL",
    )
    DB_POOL_SIZE: int = Field(
        default=10, ge=1, le=50, description="Connection pool size"
    )
    DB_MAX_OVERFLOW: int = Field(
        default=20, ge=0, le=100, description="Max overflow connections"
    )
    DB_POOL_TIMEOUT: int = Field(
        default=30, ge=1, description="Connection acquisition timeout in seconds"
    )
    DB_POOL_RECYCLE: int = Field(
        default=1800, ge=60, description="Recycle connections after seconds"
    )

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url_scheme(cls, v: str) -> str:
        """Ensure DATABASE_URL uses an asynchronous driver."""
        if not v.startswith(("postgresql+psycopg://", "sqlite+aiosqlite://")):
            raise ValueError(
                "DATABASE_URL must specify an async driver, e.g., 'postgresql+psycopg://...'"
            )
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.APP_ENV == "testing"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.APP_ENV == "production"

    @property
    def masked_database_url(self) -> str:
        """Return DATABASE_URL with user password masked for safe logging."""
        try:
            parsed = urlparse(self.DATABASE_URL)
            if parsed.password:
                netloc = f"{parsed.username}:*****@{parsed.hostname}"
                if parsed.port:
                    netloc += f":{parsed.port}"
                return parsed._replace(netloc=netloc).geturl()
            return self.DATABASE_URL
        except Exception:
            return "postgresql+psycopg://<credentials_masked>"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton instance of application settings."""
    return Settings()
