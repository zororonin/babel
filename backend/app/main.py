"""FastAPI application entry point, lifecycle management, and routing."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.infrastructure.database.session import close_db_engine, get_engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle events."""
    settings = get_settings()
    setup_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)
    logger.info(
        "Starting %s v%s in %s environment...",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.APP_ENV,
    )

    # Initialize database engine on startup
    try:
        get_engine()
        logger.info("Database engine initialized successfully.")
    except Exception as exc:
        logger.warning(
            "Database engine initialization deferred or encountered warning: %s",
            str(exc),
        )

    yield

    # Clean up resources on shutdown
    logger.info("Shutting down %s...", settings.APP_NAME)
    await close_db_engine()
    logger.info("Application shutdown complete.")


def create_app() -> FastAPI:
    """Application factory initializing FastAPI with middleware and routes."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Project Babel backend foundation API.",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.is_development else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register centralized exception handlers
    register_exception_handlers(app)

    # Mount health probe endpoints at root level for orchestrators / load balancers
    app.include_router(health_router)

    # Mount versioned API routes
    app.include_router(api_v1_router, prefix="/api")

    return app


app = create_app()
