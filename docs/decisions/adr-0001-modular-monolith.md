# ADR 0001: Modular Monolith Architecture & Technology Selection

## Status
Accepted

## Context
Project Babel is designed as a multilingual social platform enabling real-time cross-language communication. In Sprint 1, the backend foundation is established. A primary architectural decision was required regarding deployment topology (Microservices vs. Distributed Services vs. Modular Monolith) and core runtime frameworks.

## Decision
We have chosen a **Modular Monolith** architecture for Project Babel, implemented using:
- **FastAPI** with **Uvicorn** and **Pydantic v2 / Pydantic Settings**.
- **PostgreSQL 16** with **SQLAlchemy 2.0 (async)** and **Psycopg 3**.
- **Alembic** for explicit, tracked database migrations.
- **Ruff** and **Mypy** for linting, formatting, and static typing.
- **Docker Compose** for local containerized development.

### Key Architectural Tenets:
1. **Single Deployment Artifact**: A single container deployment avoids premature operational overhead (Kubernetes ingress complexity, distributed tracing, network latency between microservices).
2. **Strict Layer Separation**: Clear boundary separation between API routes, Application logic, Domain models, and Infrastructure persistence.
3. **No Direct Queries in Routes**: Route handlers only call application services via Dependency Injection.
4. **Asynchronous I/O**: Full async stack (FastAPI -> AsyncSession -> Psycopg 3 async engine) ensures high concurrency for future real-time messaging workloads without blocking the event loop.

## Consequences
### Positive:
- Simplified local development setup and rapid iteration cycles.
- Lower operational costs and zero inter-service network latency during early sprints.
- Clear module isolation allows future extraction of high-load services (e.g. real-time WebSockets or translation worker queues) into independent microservices if and when justified by metrics.

### Negative:
- Developers must maintain domain boundary discipline to avoid tight coupling between modules within the monolith.
