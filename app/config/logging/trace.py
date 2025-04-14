from contextvars import ContextVar
from uuid import uuid4


class ContextVarContextManager:
    fastapi_trace = ContextVar("fastapi_trace")

    def set_trace(self):
        self.fastapi_trace.set(uuid4().hex[:16])

    def get_trace(self) -> str:
        return self.fastapi_trace.get()


contextvar_ctx = ContextVarContextManager()
