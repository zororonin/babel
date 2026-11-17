# Development Workflow & Local Setup: Project Babel

This guide provides practical commands and workflows for developers working on Project Babel.

---

## 1. Prerequisites

- **Docker Desktop** (with Docker Compose enabled)
- **Python 3.12+**
- **Git**

---

## 2. Quickstart with Docker Compose

The fastest way to spin up the local development stack:

```bash
# 1. Copy the environment configuration template
cp .env.example .env

# 2. Build backend container and launch services in the background
docker-compose up --build -d

# 3. View service status and health
docker-compose ps

# 4. Tail application logs
docker-compose logs -f backend

# 5. Stop running containers
docker-compose down
```

Once running, access:
- **Application Health**: `http://localhost:8000/health`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 3. Local Python Development (Without Docker for Backend)

If you prefer to run FastAPI directly on the host machine while keeping PostgreSQL containerized:

```bash
# 1. Start only the PostgreSQL database container
docker-compose up -d postgres

# 2. Connect via psql to verify database connectivity
psql -h localhost -p 5433 -U babel_app -d babel_db

# 3. Create and activate a Python virtual environment (Python 3.12 recommended)
python -m venv .venv

# On Linux / macOS / WSL:
source .venv/bin/activate
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# 4. Install backend dependencies in editable mode with development tools
pip install --upgrade pip
pip install -e "./backend[dev]"

# 5. Apply database migrations
cd backend
alembic upgrade head

# 6. Run Uvicorn development server with live reload
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 4. Code Quality & Testing Commands

Run these checks frequently during local development:

```bash
# Linting
ruff check backend/
ruff check backend/ --fix   # Auto-apply safe fixes

# Formatting
ruff format backend/
ruff format --check backend/

# Static type checking
mypy backend/app

# Run all automated tests
pytest backend/tests/ -v

# Run tests with terminal coverage report
pytest backend/tests/ -v --cov=app --cov-report=term-missing
```

---

## 5. Database Migration Commands

```bash
cd backend

# Apply pending migrations
alembic upgrade head

# Roll back the previous migration
alembic downgrade -1

# Generate a new migration after modifying models
alembic revision --autogenerate -m "add_new_feature_table"
```

---

## 6. Git Branching & Pull Request Workflow

1. Update your local `develop` branch:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Create your dedicated feature branch:
   ```bash
   git checkout -b feature/issue-123-your-feature-name
   ```
3. Commit using conventional commit format:
   ```bash
   git commit -m "feat(api): add new validation endpoint"
   ```
4. Push and open a Pull Request targeting `develop`.
