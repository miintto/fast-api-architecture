from logging import Filter, LogRecord

from .trace import contextvar_ctx


class TraceFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        record.trace = contextvar_ctx.get_trace()
        return True
