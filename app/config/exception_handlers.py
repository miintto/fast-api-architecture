import logging

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from app.common.response import JSONResponse

logger = logging.getLogger(__name__)


async def request_validation_exception_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(f"RequestValidationError - {exc}")
    return JSONResponse(content=exc.errors(), status_code=400)


async def server_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(f"Exception - {exc}")
    return JSONResponse(content=exc.args, status_code=500)
