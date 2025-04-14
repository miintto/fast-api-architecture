from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, relationship

from app.domain.order import Order, OrderItem, OrderStatus
from .base import Base


class OrderEntity(Base[Order]):
    __tablename__ = "tb_order"

    id = Column(BigInteger, primary_key=True)
    order_number = Column(
        String(100), comment="주문 번호", nullable=False, unique=True
    )
    product_id = Column(
        BigInteger, ForeignKey("tb_product.id", ondelete="CASCADE")
    )
    status = Column(
        Enum(OrderStatus, native_enum=False, length=10),
        comment="주문 상태",
        nullable=False,
        default=OrderStatus.PENDING
    )
    user_id = Column(
        BigInteger, ForeignKey("tb_user.id", ondelete="CASCADE")
    )
    canceled_dtm = Column(
        DateTime(timezone=True), comment="주문 취소 일시", nullable=True
    )
    confirmed_dtm = Column(
        DateTime(timezone=True), comment="주문 확정 일시", nullable=True
    )
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    items: Mapped[list["OrderItemEntity"]] = relationship(back_populates="order")

    def to_domain(self, item: bool = False) -> Order:
        return Order(
            id=self.id,
            order_number=self.order_number,
            product_id=self.product_id,
            status=self.status,
            user_id=self.user_id,
            canceled_dtm=self.canceled_dtm,
            confirmed_dtm=self.confirmed_dtm,
            created_dtm=self.created_dtm,
            items=[item.to_domain() for item in self.items] if item else [],
        )


class OrderItemEntity(Base[OrderItem]):
    __tablename__ = "tb_order_item"

    id = Column(BigInteger, primary_key=True)
    order_id = Column(
        BigInteger, ForeignKey("tb_order.id", ondelete="CASCADE")
    )
    item_id = Column(
        BigInteger, ForeignKey("tb_product_item.id", ondelete="CASCADE")
    )
    price = Column(BigInteger, comment="판매가", nullable=False)
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    order: Mapped["OrderEntity"] = relationship(back_populates="items")
