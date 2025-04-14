from abc import ABC, abstractmethod


class AuthUseCase(ABC):
    @abstractmethod
    async def register(
        self, email: str, password: str, password_check: str
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def login(self, email: str, password: str):
        raise NotImplementedError
