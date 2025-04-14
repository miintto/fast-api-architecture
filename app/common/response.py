from typing import Any, Mapping
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse as _JSONResponse


class JSONResponse(_JSONResponse):
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(
            content=jsonable_encoder(content),
            status_code=status_code,
            headers=headers,
        )
