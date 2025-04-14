from abc import ABC, abstractmethod

from app.domain.order import Order, OrderItem


class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def create_items(self, items: list[dict]) -> list[OrderItem]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_order_number(self, order_number: str) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id_with_item(self, id_: int) -> Order | None:
        raise NotImplementedError
