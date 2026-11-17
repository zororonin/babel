"""Health and readiness probe endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import SettingsDep, get_db_session
from app.core.exceptions import DatabaseConnectionException
from app.infrastructure.database.session import check_database_connection
from app.shared.schemas.health import (
    HealthResponse,
    LivenessResponse,
    ReadinessResponse,
)

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic application health check",
    description=(
        "Returns high-level application health metadata including version "
        "and runtime environment."
    ),
)
async def health_check(settings: SettingsDep) -> HealthResponse:
    """Return high-level application status."""
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )


@router.get(
    "/health/live",
    response_model=LivenessResponse,
    status_code=status.HTTP_200_OK,
    summary="Process liveness probe",
    description=(
        "Verifies that the FastAPI application process is alive and "
        "accepting connections."
    ),
)
async def liveness_check() -> LivenessResponse:
    """Return process liveness confirmation."""
    return LivenessResponse(status="alive")


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database or required infrastructure is unavailable.",
        }
    },
    summary="Infrastructure readiness probe",
    description=(
        "Verifies that essential dependencies (PostgreSQL database) are "
        "reachable and ready to process traffic."
    ),
)
async def readiness_check(
    db: AsyncSession = Depends(get_db_session),
) -> ReadinessResponse:
    """Verify backend and database connectivity."""
    is_healthy = await check_database_connection(db)
    if not is_healthy:
        raise DatabaseConnectionException(
            message="Database connectivity check failed. Service is not ready."
        )

    return ReadinessResponse(status="ready", database="connected")
