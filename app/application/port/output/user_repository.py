from abc import ABC, abstractmethod

from app.domain.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id_or_none(self, id_: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError
