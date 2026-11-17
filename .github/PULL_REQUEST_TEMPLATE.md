## Summary of Changes

Provide a clear and concise description of what was changed and why.

## Related Issue / Ticket

Fixes / Closes #(issue number)

## Architecture Compliance

- [ ] Clear separation of concerns maintained across layers (API, Application, Domain, Infrastructure).
- [ ] No raw database queries or direct session manipulation in route handlers.
- [ ] Dependency injection utilized for external services and repositories.
- [ ] Pydantic v2 schemas used for input and output validation.
- [ ] No secrets or sensitive data hardcoded or logged.

## Testing & Quality Verification

- [ ] Unit tests added / updated.
- [ ] Integration tests added / updated (if database or external adapters affected).
- [ ] API tests added / updated (if endpoints added or modified).
- [ ] `ruff check .` passes without errors.
- [ ] `ruff format --check .` passes without changes.
- [ ] `mypy app` passes with zero type errors.
- [ ] `pytest` passes with required test coverage.

## Screenshots / Evidence (if applicable)

Provide command output or terminal screenshots validating the changes.
