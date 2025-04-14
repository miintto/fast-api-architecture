from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = "PENDING"  # 주문 대기
    COMPLETED = "COMPLETED"  # 주문 완료
    CONFIRMED = "CONFIRMED"  # 주문 확정
    CANCELLED = "CANCELLED"  # 주문 취소


@dataclass
class Order:
    id: int | None
    order_number: str
    product_id: int
    status: OrderStatus
    user_id: int
    canceled_dtm: datetime | None
    confirmed_dtm: datetime | None
    created_dtm: datetime
    items: list["OrderItem"]


@dataclass
class OrderItem:
    id: int | None
    order_id: int
    item_id: int
    price: int
    created_dtm: datetime
