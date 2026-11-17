"""API v1 master router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_v1_router = APIRouter(prefix="/v1")

# Include feature and system routers
api_v1_router.include_router(health.router)
