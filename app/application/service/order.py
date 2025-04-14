from fastapi import Depends, HTTPException

from app.adapter.outbound.persistence.order import OrderPersistenceAdapter
from app.adapter.outbound.persistence.product import ProductPersistenceAdapter
from app.adapter.outbound.persistence.user import UserPersistenceAdapter
from app.adapter.inbound.api.schemas.order import OrderInfo
from app.application.port.input import OrderUseCase
from app.application.port.output import (
    OrderRepositoryPort,
    ProductRepositoryPort,
    UserRepositoryPort,
)
from app.common.security.credential import HTTPAuthorizationCredentials
from app.domain.order import Order, OrderItem, OrderStatus
from app.domain.user import User


class OrderService(OrderUseCase):
    def __init__(
        self,
        order_repo: OrderRepositoryPort = Depends(OrderPersistenceAdapter),
        product_repo: ProductRepositoryPort = Depends(ProductPersistenceAdapter),
        user_repo: UserRepositoryPort = Depends(UserPersistenceAdapter),
    ):
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._user_repo = user_repo

    async def _create_order(self, data: OrderInfo, user: User) -> Order:
        return await self._order_repo.save(
            Order(
                id=None,
                order_number=data.order_number,
                product_id=data.product_id,
                status=OrderStatus.PENDING,
                user_id=user.id,
                canceled_dtm=None,
                confirmed_dtm=None,
                created_dtm=None,
                items=[]
            )
        )

    async def _reduce_item_quantity(self, product_id: int, item_map: dict[int, dict]):
        async with self._product_repo.find_by_id_for_update(product_id):
            for item in await self._product_repo.find_items_by_ids(item_map.keys()):
                if item.item_quantity <= item.sold_quantity:
                    raise HTTPException(status_code=400, detail="Out of stock")
                item_map[item.id]["price"] = item.price
                item.sold_quantity += item_map[item.id]["quantity"]
                await self._product_repo.update_item(item)

    async def _create_items(
        self, order: Order, item_map: dict[int, dict]
    ) -> list[OrderItem]:
        return await self._order_repo.create_items(
            [
                {"order_id": order.id, "item_id": item_id, "price": data["price"]}
                for item_id, data in item_map.items()
                for _ in range(data["quantity"])
            ]
        )

    async def create_order(
        self, data: OrderInfo, credential: HTTPAuthorizationCredentials
    ) -> Order:
        if not await self._product_repo.find_by_id_or_none(data.product_id):
            raise HTTPException(status_code=400)
        elif not (user := await self._user_repo.find_by_id_or_none(credential.payload.pk)):
            raise HTTPException(status_code=400)
        elif await self._order_repo.find_by_order_number(data.order_number):
            raise HTTPException(status_code=400)

        order = await self._create_order(data, user)
        item_map = {it.item_id: {"quantity": it.quantity} for it in data.items}
        await self._reduce_item_quantity(order.product_id, item_map)
        order.items = await self._create_items(order, item_map)
        order.status = OrderStatus.COMPLETED
        await self._order_repo.save(order)
        return order

    async def search_order(self, order_id: int) -> Order | None:
        if not (order := await self._order_repo.find_by_id_with_item(order_id)):
            raise HTTPException(status_code=404)
        return order
