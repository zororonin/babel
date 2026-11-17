# ==============================================================================
# Project Babel — Backend Container Dockerfile
# Base: Python 3.12 Slim (Official Debian-based)
# Security: Non-root execution, minimal attack surface
# ==============================================================================

FROM python:3.12-slim AS runtime

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime system dependencies (curl for container healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user and group
RUN groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid appgroup --create-home appuser

# Set working directory
WORKDIR /app

# Copy dependency specifications first to leverage Docker layer caching
COPY pyproject.toml README.md /app/

# Upgrade pip and install production dependencies system-wide as root
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Copy application source code, Alembic configurations, and migrations with appuser ownership
COPY --chown=appuser:appgroup app /app/app
COPY --chown=appuser:appgroup migrations /app/migrations
COPY --chown=appuser:appgroup alembic.ini /app/alembic.ini

# Ensure app directory permissions
RUN chown -R appuser:appgroup /app

# Expose HTTP service port
EXPOSE 8000

# Switch to non-root user for runtime
USER appuser

# Container healthcheck probing liveness endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

# Launch Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
