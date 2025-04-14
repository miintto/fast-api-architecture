import os
from app.config.settings import BASE_DIR


LOG_DIR = os.path.join(BASE_DIR, "logs/")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[{asctime}] - {levelname} - {name} - {message}",
            "style": "{",
        },
        "ecs": {
            "()": "ecs_logging.StdlibFormatter",
            "exclude_fields": ["log.original"],
        },
    },
    "filters": {
        "trace": {
            "()": "app.config.logging.filters.TraceFilter",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/debug.log",
            "formatter": "ecs",
            "filters": ["trace"],
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
