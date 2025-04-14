from logging.config import DictConfigurator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.adapter.inbound.api import router
from app.config.connection import db
from app.config.logging.config import LOGGING
from app.config.middlewares.logging import LoggingMiddleware
from .exception_handlers import (
    request_validation_exception_error_handler,
    server_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url="/documents",
        exception_handlers={
            RequestValidationError: request_validation_exception_error_handler,
            Exception: server_exception_handler,
        },
    )
    app.include_router(router)

    # Logging
    DictConfigurator(LOGGING).configure()

    # Databases
    app.add_event_handler("startup", db.check_connection)
    app.add_event_handler("shutdown", db.dispose_connection)

    # Middlewares
    app.add_middleware(LoggingMiddleware)
    return app
