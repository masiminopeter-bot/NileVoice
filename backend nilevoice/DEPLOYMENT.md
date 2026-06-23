# NileVoice AI Production Deployment Guide

This guide describes how to deploy NileVoice AI in production using Docker Compose and Nginx.

## Prerequisites

- Docker Engine
- Docker Compose
- A valid TLS certificate pair (`fullchain.pem`, `privkey.pem`)
- Secure secrets for database and JWT
- Network access to the production host

## Deployment files

- `Dockerfile`
- `docker-compose.prod.yml`
- `docker/nginx/conf.d/nilevoice.conf`
- `.env.production.example`

## Production build and run

1. Copy the production env example:

```bash
cp .env.production.example .env.production
```

2. Update `.env.production` with secure credentials:

- `DB_PASSWORD`
- `DB_ROOT_PASSWORD`
- `JWT_SECRET_KEY`

3. Place TLS certificates under `docker/nginx/ssl/`:

- `docker/nginx/ssl/fullchain.pem`
- `docker/nginx/ssl/privkey.pem`

4. Start containers:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

5. Verify status:

```bash
docker compose -f docker-compose.prod.yml ps
```

## Application URL

- `http://<host>/` will redirect to HTTPS
- `https://<host>/api/v1/docs` is available only if the app environment allows documentation in production

## Database migrations

Run Alembic migrations once after deployment using the `web` service:

```bash
docker compose -f docker-compose.prod.yml exec web alembic upgrade head
```

If you prefer to run migrations locally with the repo:

```bash
alembic upgrade head
```

## Security recommendations

- Use strong random values for `JWT_SECRET_KEY`
- Do not expose MySQL to the public internet
- Keep `DB_ROOT_PASSWORD` and `DB_PASSWORD` secret
- Use HTTPS and `HSTS`
- Restrict access to management endpoints
- Enable access logging at the reverse proxy layer

## Runtime configuration

The application loads settings from environment variables via `app/core/config.py`.

Production-specific behavior:

- `APP_ENV=production` disables OpenAPI docs and schema endpoints
- Nginx terminates SSL and forwards requests to the backend

## Monitoring and logging

- Collect container logs from `docker compose -f docker-compose.prod.yml logs -f`
- Consider external log aggregation
- Configure health checks and service alerts

## Cleanup

Stop services:

```bash
docker compose -f docker-compose.prod.yml down
```

Remove volumes if you want a clean rebuild:

```bash
docker compose -f docker-compose.prod.yml down -v
```
