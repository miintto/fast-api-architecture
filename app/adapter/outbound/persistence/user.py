from sqlalchemy import select

from app.adapter.outbound.persistence.entity.user import UserEntity
from app.application.port.output import UserRepositoryPort
from app.domain.user import User
from .base import BaseRepository


class UserPersistenceAdapter(BaseRepository, UserRepositoryPort):
    async def save(self, user: User) -> User:
        entity = await self._save(user, UserEntity)
        return entity.to_domain()

    async def find_by_id_or_none(self, id_: int) -> User | None:
        if not (user := await self._find_by_id_or_none(id_, UserEntity)):
            return None
        return user.to_domain()

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserEntity).where(UserEntity.email == email)
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        return user.to_domain()
