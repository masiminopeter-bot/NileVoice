from fastapi import FastAPI

from app.api.v1 import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging


def create_application() -> FastAPI:
    configure_logging()
    settings = get_settings()

    docs_url = "/api/v1/docs" if settings.app_env != "production" else None
    redoc_url = "/api/v1/redoc" if settings.app_env != "production" else None
    openapi_url = "/api/v1/openapi.json" if settings.app_env != "production" else None

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        openapi_url=openapi_url,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_application()
