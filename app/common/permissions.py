from fastapi import Depends, HTTPException

from .authentication import Authentication
from .security.credential import HTTPAuthorizationCredentials

auth_scheme = Authentication()


class BasePermission:
    """클라이언트의 접근 권한을 확인합니다."""

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    ) -> HTTPAuthorizationCredentials:
        return await self.authorization(credentials)

    async def authorization(self, *args, **kwargs):
        raise NotImplementedError("`authorization()` must be overridden")


class IsAuthenticated(BasePermission):
    async def authorization(
        self, credentials: HTTPAuthorizationCredentials
    ) -> HTTPAuthorizationCredentials:
        if not credentials.payload.permission.is_authenticated():
            raise HTTPException(status_code=403)
        return credentials
