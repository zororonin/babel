# Sprint 1 Scope & Boundary Specification: Project Babel

This document records the exact scope, boundaries, and explicit exclusions for Sprint 1 (Backend Foundation).

---

## 1. Sprint 1 Inclusions

- Modular Monolith directory skeleton and layer separation.
- Centralized configuration via Pydantic Settings with safe URL masking.
- Structured logging (JSON format) and centralized custom exception handling.
- Docker Compose configuration for PostgreSQL 16 and FastAPI backend.
- Dedicated non-superuser database role (`babel_app`) with restricted privileges.
- Non-root container execution (`appuser`, UID 1001).
- SQLAlchemy 2.0 asynchronous connection pool and session generator (`get_db`).
- Alembic asynchronous migration environment and baseline audit migration.
- Health probe endpoints: `/health`, `/health/live`, `/health/ready`.
- Test suite spanning Unit, Integration, and API testing layers with Pytest and HTTPX.
- GitHub Actions CI pipeline covering linting, formatting, type checking, tests, and Docker build.
- Comprehensive technical documentation and developer guides.

---

## 2. Explicit Sprint 1 Exclusions

The following features were intentionally excluded from Sprint 1 to prevent premature complexity:

- User registration, login, and JWT/session authentication.
- Authorization and role-based access control (RBAC).
- User profile schemas and user relationship graphs.
- Real-time WebSockets and conversation/message persistence.
- Translation APIs, translation provider integrations, and language detection.
- Translation caching layers.
- Redis and Celery background task processing.
- End-to-end encryption (E2EE) algorithms or claims.
- Frontend web or mobile applications.
- Media upload and asset storage.
