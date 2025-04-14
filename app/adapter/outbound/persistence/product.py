from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import datetime
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.adapter.outbound.persistence.entity.product import (
    ProductEntity,
    ProductItemEntity,
)
from app.application.port.output import ProductRepositoryPort
from app.domain.product import Product, ProductItem
from .base import BaseRepository


class ProductPersistenceAdapter(BaseRepository, ProductRepositoryPort):
    async def find_by_id_or_none(self, id_: int) -> Product | None:
        return await self._find_by_id_or_none(id_, ProductEntity)

    async def find_by_id_with_item(self, id_: int) -> Product | None:
        result = await self._session.execute(
            select(ProductEntity)
            .options(selectinload(ProductEntity.items))
            .where(ProductEntity.id == id_)
        )
        if not (product := result.scalar_one_or_none()):
            return None
        return product.to_domain(item=True)

    async def find_items_by_ids(self, ids: Iterable[int]) -> list[ProductItem]:
        result = await self._session.execute(
            select(ProductItemEntity).where(ProductItemEntity.id.in_(ids))
        )
        return [item.to_domain() for item in result.scalars()]

    async def find_displayed_products(self) -> list[Product]:
        result = await self._session.execute(
            select(
                ProductEntity,
                (
                    select(func.min(ProductItemEntity.price))
                    .where(
                        ProductItemEntity.sale_start_dtm.is_(None)
                        | (ProductItemEntity.sale_start_dtm < datetime.now()),
                        ProductItemEntity.sale_close_dtm.is_(None)
                        | (ProductItemEntity.sale_close_dtm > datetime.now()),
                        ProductItemEntity.product_id == ProductEntity.id,
                        ProductItemEntity.is_active.is_(True),
                        ProductItemEntity.sold_quantity < ProductItemEntity.item_quantity,
                    )
                    .scalar_subquery()
                    .label("min_price")
                ),
            )
            .where(ProductEntity.is_displayed.is_(True))
        )
        return [row.ProductEntity.to_domain() for row in result.fetchall()]

    @asynccontextmanager
    async def find_by_id_for_update(self, id_: int) -> Product:
        result = await self._session.execute(
            select(ProductEntity)
            .where(ProductEntity.id == id_)
            .with_for_update()
        )
        yield result.scalar_one_or_none()
        await self._session.commit()

    async def update_item(self, item: ProductItem) -> ProductItem:
        entity = await self._session.get(ProductItemEntity, item.id)
        for field, value in asdict(item).items():
            setattr(entity, field, value)
        return entity.to_domain()
