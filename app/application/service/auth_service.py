from datetime import datetime, timezone

from bcrypt import checkpw, gensalt, hashpw
from fastapi import Depends, HTTPException

from app.adapter.outbound.persistence.user_adapter import UserPersistenceAdapter
from app.application.port.input import AuthUseCase
from app.application.port.output import UserRepositoryPort
from app.common.security.jwt import JWTProvider
from app.domain.user import User, UserPermission


class AuthService(AuthUseCase):
    def __init__(
        self,
        jwt: JWTProvider = Depends(JWTProvider),
        user_repo: UserRepositoryPort = Depends(UserPersistenceAdapter),
    ):
        self._jwt = jwt
        self._user_repo = user_repo

    async def register(
        self, email: str, password: str, password_check: str
    ) -> str:
        if await self._user_repo.find_by_email(email=email):
            raise HTTPException(status_code=400)
        elif password != password_check:
            raise HTTPException(status_code=400)

        user = await self._user_repo.save(
            User(
                id=None,
                email=email,
                password=hashpw(password.encode(), salt=gensalt()).decode(),
                permission=UserPermission.NORMAL,
                is_active=True,
                last_login=None,
                created_dtm=datetime.now(),
            )
        )
        return self._jwt.encode(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.find_by_email(email=email)
        if not user:
            raise HTTPException(status_code=400)
        elif not checkpw(password.encode(), user.password.encode()):
            raise HTTPException(status_code=400)

        user.last_login = datetime.now(timezone.utc)
        await self._user_repo.save(user)
        return self._jwt.encode(user)
