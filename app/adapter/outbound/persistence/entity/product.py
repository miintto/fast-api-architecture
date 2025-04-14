from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship

from app.domain.product import Product, ProductItem
from .base import Base


class ProductEntity(Base[Product]):
    __tablename__ = "tb_product"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), comment="상품명", nullable=False)
    is_displayed = Column(
        Boolean, comment="노출 여부", nullable=False, default=True
    )
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    items: Mapped[list["ProductItemEntity"]] = relationship(back_populates="product")

    def to_domain(self, item: bool = False) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            is_displayed=self.is_displayed,
            created_dtm=self.created_dtm,
            updated_dtm=self.updated_dtm,
            items=[item.to_domain() for item in self.items] if item else [],
        )


class ProductItemEntity(Base[ProductItem]):
    __tablename__ = "tb_product_item"

    id = Column(BigInteger, primary_key=True)
    product_id = Column(
        BigInteger, ForeignKey("tb_product.id", ondelete="CASCADE")
    )
    name = Column(String(100), comment="품목명", nullable=False)
    cost = Column(BigInteger, comment="원가", nullable=False)
    price = Column(BigInteger, comment="판매가", nullable=False)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    item_quantity = Column(Integer, comment="재고", nullable=False)
    sold_quantity = Column(Integer, comment="판매 수량", nullable=False, default=0)
    sale_start_dtm = Column(
        DateTime(timezone=True), comment="판매 시작일", nullable=True
    )
    sale_close_dtm = Column(
        DateTime(timezone=True), comment="판매 종료일", nullable=True
    )
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    product: Mapped["ProductEntity"] = relationship(back_populates="items")
