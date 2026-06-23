# NileVoice AI Backend

Production-ready FastAPI backend scaffold for NileVoice AI.

## Features

- FastAPI application structure
- SQLAlchemy ORM with MySQL support
- Alembic migrations
- JWT authentication scaffolding
- Repository pattern and service layer
- API versioning
- Environment configuration
- Structured logging
- Docker and Docker Compose support

## Project layout

- `app/`
  - `api/` - versioned routers and API entrypoints
  - `core/` - configuration, logging, and security
  - `db/` - database initialization and session management
  - `models/` - SQLAlchemy models
  - `repositories/` - repository layer abstractions
  - `schemas/` - Pydantic request/response schemas
  - `services/` - business service layer
- `alembic/` - migration environment
- `tests/` - recommended tests location

## Getting started

1. Copy `.env.example` to `.env`.
2. Update database and JWT settings.
3. Build and run with Docker:

```bash
docker compose up --build
```

4. Visit `http://localhost:8000/docs` for Swagger UI.

## Environment variables

Required:

- `APP_NAME`
- `APP_VERSION`
- `APP_ENV`
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`

For production deployments, copy `.env.production.example` to `.env.production`, set strong secrets, and never commit the file to version control.

## Production deployment

Use `docker-compose.prod.yml` for production containers and Nginx reverse proxying. The production deployment includes:

- `web` service running Uvicorn in production mode
- `nginx` reverse proxy with HTTP/HTTPS settings
- `mysql` database service

See `DEPLOYMENT.md` for a complete production deployment guide.

## Alembic

Run migrations from inside the container or local environment:

```bash
alembic upgrade head
```

## Notes

This scaffold contains the core startup and architecture. Business logic, models, and endpoint implementations can be added incrementally.
