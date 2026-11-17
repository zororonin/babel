# Contributing to Project Babel

Thank you for contributing to Project Babel. This document outlines the standards, conventions, and engineering workflows required for code contributions.

---

## 1. Architectural Philosophy

Project Babel employs a **Modular Monolith** architecture. When submitting contributions:
- Maintain strict separation of concerns across the API, Application/Business Logic, Domain, and Infrastructure layers.
- Do not place raw database queries inside API route handlers.
- Use dependency injection for data access and external services.
- Keep business logic independent of transport protocols (HTTP, WebSockets).
- Never hardcode credentials, URLs, or secrets.
- Use explicit transaction boundaries with asynchronous SQLAlchemy 2.0 sessions.

---

## 2. Branching Strategy

We follow a GitFlow-inspired branching model:

- `main`: Protected production branch. Direct commits are strictly prohibited.
- `develop`: Integration branch for active sprint development.
- `feature/<issue-or-feature-name>`: Dedicated branch for new features or modules.
- `bugfix/<issue-name>`: Dedicated branch for non-critical defect fixes.
- `hotfix/<issue-name>`: Critical patches branched directly from `main`.

### Rules:
1. Never push directly to `main` or `develop`.
2. Always create a feature or bugfix branch from `develop`.
3. Submit a Pull Request targeting `develop`.

---

## 3. Commit Message Conventions

Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### Allowed Types:
- `feat`: A new feature or endpoint.
- `fix`: A bug fix.
- `docs`: Documentation changes only.
- `style`: Changes that do not affect the meaning of the code (formatting, white-space).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `ci`: Changes to CI configuration files and scripts.
- `chore`: Routine maintenance, dependency updates, build tooling.

---

## 4. Code Quality Standards

Before committing or opening a Pull Request, verify that all quality gates pass locally:

### 4.1 Formatting & Linting (Ruff)
```bash
ruff check backend/
ruff format --check backend/
```

### 4.2 Static Type Checking (Mypy)
```bash
mypy backend/app
```

### 4.3 Automated Testing & Coverage (Pytest)
```bash
pytest backend/tests -v --cov=backend/app --cov-report=term-missing
```

---

## 5. Pull Request Process

1. Ensure the branch is rebased on latest `develop`.
2. Verify all CI checks pass without errors or warnings.
3. Complete the PR template in full, including:
   - Summary of changes.
   - Associated issue ticket.
   - Verification steps and testing evidence.
4. Request review from at least one core backend engineer.
