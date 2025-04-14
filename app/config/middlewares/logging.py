import logging
import re

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.config.logging.trace import contextvar_ctx

logger = logging.getLogger("app.request")


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        contextvar_ctx.set_trace()
        path = self._get_full_path(scope)
        logger.info(path)

        async def receive_before_logging():
            nonlocal scope
            message = await receive()
            headers = Headers(scope=scope)
            if re.search(r"^application/json", headers.get("Content-Type")):
                logger.info(f"Request - {message["body"].decode()}")
            return message

        async def send_before_logging(message: Message):
            await send(message)
            if message["type"] == "http.response.start":
                logger.info(f"{path} - {message["status"]}")
            elif message["type"] == "http.response.body":
                logger.info(f"Response - {message["body"].decode()}")

        await self.app(scope, receive_before_logging, send_before_logging)

    def _get_full_path(self, scope: Scope) -> str:
        return f"{scope["method"]} {scope["path"]}{
            f"?{scope["query_string"].decode()}"
            if scope.get("query_string")
            else ""
        }"
