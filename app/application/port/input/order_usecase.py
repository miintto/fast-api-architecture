from abc import ABC, abstractmethod

from app.adapter.inbound.api.schemas.order import OrderInfo
from app.common.security.credential import HTTPAuthorizationCredentials
from app.domain.order import Order


class OrderUseCase(ABC):
    @abstractmethod
    async def create_order(
        self, data: OrderInfo, credential: HTTPAuthorizationCredentials
    ) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def search_order(self, order_id: int) -> Order | None:
        raise NotImplementedError
