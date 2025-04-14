from abc import ABC, abstractmethod
from typing import Iterable


from app.domain.product import Product, ProductItem


class ProductRepositoryPort(ABC):
    @abstractmethod
    async def find_by_id_or_none(self, id_: int) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id_with_item(self, id_: int) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def find_items_by_ids(self, ids: Iterable[int]) -> list[ProductItem]:
        raise NotImplementedError

    @abstractmethod
    async def find_displayed_products(self) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id_for_update(self, id_: int) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def update_item(self, item: ProductItem) -> ProductItem:
        raise NotImplementedError
