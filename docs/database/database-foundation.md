# Database Foundation: Project Babel

This document details the database architecture, driver configuration, connection pooling, session lifecycle, and Alembic migration procedures.

---

## 1. Technology & Driver Stack

- **Engine**: PostgreSQL 18.
- **ORM**: SQLAlchemy 2.0 (typed declarative mappings).
- **Driver**: Psycopg 3 (`psycopg[binary]`) in asynchronous mode.
- **Connection URI (Internal Docker)**: `postgresql+psycopg://babel_app:<password>@postgres:5432/babel_db`
- **Connection URI (Host External)**: `postgresql+psycopg://babel_app:<password>@127.0.0.1:5433/babel_db`
- **Migrations**: Alembic 1.13+ configured for asynchronous migrations.

---

## 2. Direct psql CLI Connectivity

To connect to the database from the Windows host using PostgreSQL 18 `psql`:

```bash
# Connect on port 5433 (or configured POSTGRES_PORT) as dedicated application user
psql -h localhost -p 5433 -U babel_app -d babel_db
```

### Role & Privilege Verification
```sql
SELECT version();
SELECT current_database(), current_user;
SELECT rolname, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname = current_user;
```
*Expected: `rolsuper = false`, confirming non-superuser application execution.*

---

## 2. SQLAlchemy 2.0 Declarative Mappings

All database models inherit from `app.infrastructure.database.base.Base`, which provides common conventions:

```python
from app.infrastructure.database.base import Base, UUIDPrimaryKeyMixin, TimestampMixin

class SampleEntity(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sample_entities"

    # id: Mapped[uuid.UUID] provided by UUIDPrimaryKeyMixin (primary key)
    # created_at: Mapped[datetime] provided by TimestampMixin
    # updated_at: Mapped[datetime] provided by TimestampMixin
```

### Table Naming Convention
If `__tablename__` is omitted, the base class automatically derives the table name from the lowercase class name.

---

## 3. Connection Pool Configuration

Connection pools are managed by SQLAlchemy's `create_async_engine` with parameters configured through environment variables:

| Setting | Default | Purpose |
| :--- | :--- | :--- |
| `DB_POOL_SIZE` | `10` | The number of permanent connections held in the connection pool. |
| `DB_MAX_OVERFLOW` | `20` | Max temporary burst connections created above `DB_POOL_SIZE`. |
| `DB_POOL_TIMEOUT` | `30` | Seconds to wait before raising a TimeoutError when the pool is exhausted. |
| `DB_POOL_RECYCLE` | `1800` | Periodically recycles connections (every 30 mins) to prevent stale socket closures. |
| `pool_pre_ping` | `True` | Emits a test ping query before checkout to discard dead connections gracefully. |

---

## 4. Session Management & Transaction Boundaries

Database sessions are managed as FastAPI dependencies using `app.infrastructure.database.session.get_db`:

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Guarantees:
- **No Direct Session Creation in Routes**: Route handlers receive an injected `AsyncSession`.
- **Automatic Rollback**: Any unhandled exception triggers an immediate transaction rollback before propagating.
- **Leak Prevention**: Connections are guaranteed to close and return to the pool in the `finally:` block.

---

## 5. Alembic Database Migrations

Migrations are stored in `backend/migrations/versions/`.

### Migration Commands:
```bash
# Apply all pending migrations to the latest revision
alembic upgrade head

# Rollback the single most recent migration
alembic downgrade -1

# View migration history and current head
alembic history --verbose
alembic current

# Generate a new auto-detected migration based on model changes
alembic revision --autogenerate -m "describe_migration_purpose"
```

> [!IMPORTANT]
> Never call `Base.metadata.create_all()` in normal production application startup. Always manage schema lifecycle through tracked Alembic revisions.
