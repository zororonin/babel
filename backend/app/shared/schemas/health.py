"""Pydantic schemas for health and readiness endpoints."""

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """General application health status response schema."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="ok", description="Application health status")
    app_name: str = Field(description="Configured application name")
    version: str = Field(description="Current application version")
    environment: str = Field(description="Active runtime environment")


class LivenessResponse(BaseModel):
    """Process liveness probe response schema."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="alive", description="Process liveness state")


class ReadinessResponse(BaseModel):
    """Infrastructure readiness probe response schema."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="ready", description="Overall readiness state")
    database: str = Field(default="connected", description="Database subsystem status")
