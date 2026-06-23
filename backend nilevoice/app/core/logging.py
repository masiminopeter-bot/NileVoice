import logging
from logging.config import dictConfig

from .config import get_settings


def configure_logging() -> None:
    settings = get_settings()

    log_level = "DEBUG" if settings.app_env == "development" else "INFO"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }

    dictConfig(config)
