from fastapi import Depends, HTTPException

from app.adapter.outbound.persistence.entity.product import Product
from app.adapter.outbound.persistence.product import ProductPersistenceAdapter
from app.application.port.input import ProductUseCase


class ProductService(ProductUseCase):
    def __init__(
        self,
        repo: ProductPersistenceAdapter = Depends(ProductPersistenceAdapter),
    ):
        self._repo = repo

    async def get_product_list(self) -> list[Product]:
        return await self._repo.find_displayed_products()

    async def get_product(self, product_id: int) -> Product:
        if not (product := await self._repo.find_by_id_with_item(product_id)):
            raise HTTPException(status_code=404)
        return product
