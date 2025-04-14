from datetime import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field
from app.domain.order import Order, OrderItem

NonBlank = Len(min_length=1)


class OrderItemInfo(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)


class OrderInfo(BaseModel):
    order_number: str
    product_id: int
    items: Annotated[list[OrderItemInfo], NonBlank]


class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    price: int

    @classmethod
    def from_domain(cls, item: OrderItem) -> "OrderItemResponse":
        return cls(id=item.id, item_id=item.item_id, price=item.price)


class OrderResponse(BaseModel):
    id: int
    order_number: str
    product_id: int
    status: str
    user_id: int
    canceled_dtm: datetime | None
    confirmed_dtm: datetime | None
    created_dtm: datetime
    items: list[OrderItemResponse]

    @classmethod
    def from_domain(cls, order: Order) -> "OrderResponse":
        return cls(
            id=order.id,
            order_number=order.order_number,
            product_id=order.product_id,
            status=order.status.name,
            user_id=order.user_id,
            canceled_dtm=order.canceled_dtm,
            confirmed_dtm=order.confirmed_dtm,
            created_dtm=order.created_dtm,
            items=[OrderItemResponse.from_domain(item) for item in order.items],
        )
