# API Specification: Health & Readiness Probes

This document specifies the initial endpoints implemented in Sprint 1 for container health checking, process liveness, and infrastructure readiness.

---

## 1. Endpoints Overview

| Endpoint | Method | Purpose | Success Code | Failure Code |
| :--- | :--- | :--- | :--- | :--- |
| `/health` | `GET` | General application metadata and health status | `200 OK` | `500 Internal Error` |
| `/health/live` | `GET` | Container / process liveness probe | `200 OK` | N/A (Process down) |
| `/health/ready`| `GET` | Infrastructure dependency readiness (PostgreSQL) | `200 OK` | `503 Service Unavailable` |

*Note: All endpoints are additionally exposed under the `/api/v1` versioned prefix (`/api/v1/health`, `/api/v1/health/live`, `/api/v1/health/ready`).*

---

## 2. Endpoint Details

### 2.1 GET `/health`
Returns high-level application health metadata.

#### Success Response (`200 OK`):
```json
{
  "status": "ok",
  "app_name": "Project Babel",
  "version": "0.1.0",
  "environment": "development"
}
```

---

### 2.2 GET `/health/live`
Confirms the application process is running and accepting HTTP requests.

#### Success Response (`200 OK`):
```json
{
  "status": "alive"
}
```

---

### 2.3 GET `/health/ready`
Verifies that downstream infrastructure dependencies (PostgreSQL database) are reachable. Executes an asynchronous `SELECT 1` ping.

#### Success Response (`200 OK`):
```json
{
  "status": "ready",
  "database": "connected"
}
```

#### Failure Response (`503 Service Unavailable`):
```json
{
  "error": {
    "code": "DATABASE_UNAVAILABLE",
    "message": "Database connectivity check failed. Service is not ready.",
    "details": {}
  }
}
```
*Security note: No credentials, database hostnames, or internal error traces are exposed in readiness failure responses.*
