from fastapi.exceptions import HTTPException
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from starlette.requests import Request

from .security.credential import HTTPAuthorizationCredentials
from .security.jwt import JWTProvider


class Authentication(SecurityBase):
    scheme = "JWT"

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.upper() != self.scheme:
            raise HTTPException(status_code=401)
        return self.decode_token(scheme, token)

    @staticmethod
    def decode_token(scheme: str, token: str) -> HTTPAuthorizationCredentials:
        try:
            return HTTPAuthorizationCredentials(
                scheme=scheme,
                token=token,
                payload=JWTProvider().decode(token),
            )
        except ValidationError:
            raise HTTPException(status_code=401)
