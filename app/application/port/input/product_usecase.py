from abc import ABC, abstractmethod

from app.domain.product import Product


class ProductUseCase(ABC):
    @abstractmethod
    async def get_product_list(self) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def get_product(self, product_id: int) -> Product:
        raise NotImplementedError
