from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from app.adapter.outbound.persistence.entity.order import (
    OrderEntity,
    OrderItemEntity,
)
from app.application.port.output import OrderRepositoryPort
from app.domain.order import Order, OrderItem
from .base import BaseRepository


class OrderPersistenceAdapter(BaseRepository, OrderRepositoryPort):
    async def save(self, order: Order) -> Order:
        entity = await self._save(order, OrderEntity)
        return entity.to_domain()

    async def create_items(self, items: list[dict]) -> list[OrderItem]:
        result = await self._session.execute(
            insert(OrderItemEntity).values(items).returning(OrderItemEntity)
        )
        await self._session.commit()
        return [item.OrderItemEntity.to_domain() for item in result]

    async def find_by_order_number(self, order_number: str) -> Order | None:
        result = await self._session.execute(
            select(OrderEntity).where(OrderEntity.order_number == order_number)
        )
        if not (order := result.scalar_one_or_none()):
            return None
        return order.to_domain()

    async def find_by_id_with_item(self, id_: int) -> Order | None:
        result = await self._session.execute(
            select(OrderEntity)
            .options(selectinload(OrderEntity.items))
            .where(OrderEntity.id == id_)
        )
        if not (order := result.scalar_one_or_none()):
            return None
        return order.to_domain(item=True)
