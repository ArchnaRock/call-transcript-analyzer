# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI application for analyzing call transcripts. Built with Python 3.12.3.

## Environment Setup

```bash
# Python version
python3.12 --version  # must be 3.12.3

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

## Common Commands

```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run a single test file
pytest tests/test_transcripts.py

# Run a single test
pytest tests/test_transcripts.py::test_function_name -v

# Lint
ruff check .

# Format
ruff format .

# Type check
mypy app/
```

## Folder Structure

```
call-transcript-analyzer/
├── app/
│   ├── main.py           # FastAPI app instantiation, router registration, lifespan
│   ├── config.py         # Settings via pydantic-settings (loaded from .env)
│   ├── dependencies.py   # Shared FastAPI dependencies (DB sessions, auth, etc.)
│   ├── routers/          # One file per domain (e.g., transcripts.py, calls.py)
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic, decoupled from HTTP layer
│   └── utils/            # Stateless helper functions
├── tests/
│   ├── conftest.py       # Shared fixtures (test client, DB, mocks)
│   ├── unit/             # Pure function and service tests (no HTTP)
│   └── integration/      # Route-level tests using TestClient
├── requirements.txt
├── requirements-dev.txt
├── .env                  # Local secrets — never committed
├── .env.example          # Committed template with placeholder values
└── pyproject.toml        # Tool config (ruff, mypy, pytest)
```

## Coding Conventions

- **Routers** live in `app/routers/`. Each router uses `APIRouter` with a prefix and tags. Routers only handle HTTP concerns (parsing, status codes, response models); business logic belongs in services.
- **Schemas** use Pydantic v2. Separate `Create`, `Update`, and `Read` schemas per resource. `Read` schemas include `model_config = ConfigDict(from_attributes=True)` for ORM compatibility.
- **Services** are plain Python classes or functions in `app/services/`. They accept domain objects, not `Request` objects.
- **Config** is a single `Settings` class in `app/config.py` using `pydantic-settings`. Access it via a cached `get_settings()` dependency.
- **Type hints** are required on all function signatures. Run `mypy app/` to verify.
- Use `async def` for all route handlers and any I/O-bound service functions.

## Error Handling

- Raise `HTTPException` only in routers, not in services.
- Services raise domain exceptions (e.g., `TranscriptNotFoundError`). Routers catch these and map them to `HTTPException`.
- Register global exception handlers in `app/main.py` for unhandled domain exceptions and unexpected errors.
- All error responses follow the shape `{"detail": "..."}` (FastAPI default).
- Log unexpected exceptions with `logger.exception(...)` before re-raising or returning a 500.

## Testing Plan

- **Unit tests** (`tests/unit/`): Test service functions and utilities in isolation. Mock external calls (LLM APIs, DB) using `pytest-mock`.
- **Integration tests** (`tests/integration/`): Use FastAPI's `TestClient`. Override dependencies via `app.dependency_overrides` to inject a test database or mock services.
- **Fixtures**: Define a `test_client` fixture in `conftest.py`. Use a separate SQLite or in-memory DB for tests; never run tests against the production DB.
- **Coverage**: Run `pytest --cov=app --cov-report=term-missing` to check coverage.
- Test file naming: `test_<module>.py`. Test function naming: `test_<behavior>_<condition>`.
