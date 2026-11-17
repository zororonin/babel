# Container Deployment Guidelines: Project Babel

This document summarizes security standards, container configuration guidelines, and operational recommendations for containerized deployments.

---

## 1. Container Security Guidelines

1. **Non-Root Execution**:
   - The backend container runs as dedicated user `appuser` (UID 1001, GID 1001).
   - Container processes never run as `root`.
2. **Minimal Base Image**:
   - Built on `python:3.12-slim` to eliminate unnecessary build utilities and attack surface.
3. **Dedicated Database Roles**:
   - The PostgreSQL instance isolates the superuser (`postgres`) from application transactions.
   - The application connects strictly via `babel_app` with restricted schema privileges.
4. **Secrets Management**:
   - No `.env` files or credentials are baked into Docker images (`.dockerignore` enforces this).
   - All secrets must be supplied via runtime environment variables.
5. **Network Exposure**:
   - In development, host port bindings are bound to `127.0.0.1` (loopback only).
   - Internal inter-service traffic routes exclusively across the custom `babel-network` bridge.
