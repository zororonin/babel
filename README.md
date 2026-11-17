# Project Babel

[![Backend CI](https://github.com/zororonin/babel/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/zororonin/babel/actions/workflows/backend-ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791.svg)](https://www.postgresql.org/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy-2.0%20(async)-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Project Babel is a multilingual social networking platform engineered to eliminate language barriers through integrated, user-controlled communication.

This repository contains the backend foundation established in **Sprint 1**, following a **Modular Monolith** architecture with asynchronous database access, strict layer separation, containerized infrastructure, automated testing, and CI/CD quality gates.

---

## Architecture Overview

```mermaid
flowchart TD
    subgraph Client [Clients & Orchestrators]
        WebClient[Web / Mobile Clients]
        HealthCheck[Docker / K8s Health Probes]
    end

    subgraph AppMonolith [Project Babel Backend (FastAPI)]
        APILayer["API Layer (/api/v1 & /health)"]
        AppModules["Application Modules & Services"]
        DomainCore["Domain Layer (Entities & Rules)"]
        Infra["Infrastructure Layer (SQLAlchemy 2.0 Async)"]
    end

    subgraph Persistence [PostgreSQL 18]
        AppDB[("babel_db (User: babel_app)")]
        Volume[("Persistent Named Volume: postgres_data (/var/lib/postgresql)")]
    end

    WebClient --> APILayer
    HealthCheck --> APILayer
    APILayer --> AppModules
    AppModules --> DomainCore
    AppModules --> Infra
    Infra --> AppDB
    AppDB --> Volume
```

---

## Technology Stack

- **Backend Framework**: Python 3.12, FastAPI, Uvicorn, Pydantic v2, Pydantic Settings.
- **Database**: PostgreSQL 18, SQLAlchemy 2.0 (async), Psycopg 3, Alembic.
- **Code Quality**: Ruff (linter and formatter), Mypy (strict static type checking).
- **Testing**: Pytest, HTTPX, Pytest-asyncio, Coverage reporting.
- **Infrastructure**: Docker Desktop, Docker Compose, non-root container security.
- **CI/CD**: GitHub Actions.

---

## Quickstart (Reproducible Development Setup)

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Docker Compose.
- [Git](https://git-scm.com/).
- [PostgreSQL 18 client tools (`psql`)](https://www.postgresql.org/download/) (optional, for direct CLI queries).

### 2. Clone and Configure
```bash
git clone https://github.com/zororonin/babel.git
cd babel

# Copy the environment configuration template
cp .env.example .env
```

### 3. Start Application with Docker Compose
```bash
# Build images and start all services in detached mode
docker-compose up --build -d

# Verify running services and health status
docker-compose ps
```

### 4. Verify Application Endpoints
```bash
# General application health
curl http://localhost:8000/health

# Process liveness probe
curl http://localhost:8000/health/live

# Database readiness probe
curl http://localhost:8000/health/ready
```

### 5. Connect to PostgreSQL via psql
The PostgreSQL 18 container publishes its port to host port `5433` (or configured `POSTGRES_PORT` in `.env`) to prevent conflicts with any native Windows PostgreSQL services running on port `5432`:

```bash
# Connect as application user babel_app (prompts for password securely)
psql -h localhost -p 5433 -U babel_app -d babel_db
```

### 5. Access Interactive Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Local Python Development & Testing

To run the application locally on the host machine without containerizing the backend:

```bash
# 1. Start the PostgreSQL container
docker-compose up -d postgres

# 2. Set up virtual environment (Python 3.12 recommended)
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\Activate.ps1

# 3. Install dependencies in editable mode
pip install --upgrade pip
pip install -e "./backend[dev]"

# 4. Run database migrations
cd backend
alembic upgrade head

# 5. Start development server with reload
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## Quality Assurance & Verification

```bash
# Linting
ruff check backend/

# Formatting verification
ruff format --check backend/

# Static type checking
mypy backend/app

# Run full test suite with coverage
pytest backend/tests/ -v --cov=app --cov-report=term-missing
```

---

## Project Structure

```text
project-babel/
├── backend/
│   ├── app/
│   │   ├── main.py                          # Application factory, lifespan & middleware
│   │   ├── api/v1/                          # Versioned API routes & /health endpoints
│   │   ├── core/                            # Settings, logging, and custom exceptions
│   │   ├── domain/                          # Business entities and value objects
│   │   ├── modules/                         # Feature business logic modules
│   │   ├── infrastructure/database/         # SQLAlchemy 2.0 session, base, and models
│   │   └── shared/                          # Shared schemas and DTOs
│   ├── migrations/                          # Async Alembic migrations
│   ├── tests/                               # Unit, Integration, and API test suites
│   ├── alembic.ini                          # Alembic configuration
│   ├── pyproject.toml                       # Python package configuration & dependencies
│   └── Dockerfile                           # Non-root Python 3.12 runtime container
├── infrastructure/docker/postgres/          # Database init scripts & application user setup
├── docs/                                    # Technical architecture, database, & testing docs
├── .github/workflows/                       # GitHub Actions CI workflow (backend-ci.yml)
├── .env.example                             # Environment configuration template
├── .gitignore                               # Git ignore rules
├── docker-compose.yml                       # Multi-container development orchestration
├── CONTRIBUTING.md                          # Contribution guidelines & branching strategy
└── README.md                                # Project documentation & setup instructions
```

---

## Git Branching & Contribution Workflow

Project Babel follows a modified **GitFlow** branching model:
- **`main`**: Production-ready, verified release milestones (protected).
- **`develop`**: Central integration branch for active sprint development (protected).
- **`feature/*`**: Feature deliverables and user stories (e.g., `feature/sprint-2-identity-auth`).
- **`release/*`** & **`hotfix/*`**: Release hardening and critical production hotfixes.

All commits adhere to **Conventional Commits 1.0.0**, and all PRs require green CI checks (linting, typing, 80%+ test coverage).

For complete branching diagrams, commit rules, and cheat sheets, see:
- [Git Branching Strategy & Workflow Guide](docs/workflows/git-workflow.md)

---

## Documentation Inventory

Comprehensive documentation is available in the [`docs/`](docs/) directory:
- [Git Workflow Guide](docs/workflows/git-workflow.md)
- [Backend Architecture](docs/architecture/backend-architecture.md)
- [Docker Architecture](docs/architecture/docker-architecture.md)
- [Database Foundation](docs/database/database-foundation.md)
- [Testing Strategy](docs/testing/testing-strategy.md)
- [Development Workflow](docs/workflows/development-workflow.md)
- [API Specification](docs/api/openapi-spec.md)
- [Container Guidelines](docs/deployment/container-guidelines.md)
- [ADR 0001: Modular Monolith](docs/decisions/adr-0001-modular-monolith.md)
- [Sprint 1 Scope & Exclusions](docs/requirements/sprint-1-scope.md)

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
