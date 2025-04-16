from fastapi import Depends, HTTPException

from app.adapter.outbound.persistence.product_adapter import ProductPersistenceAdapter
from app.application.port.input import ProductUseCase
from app.application.port.output import ProductRepositoryPort
from app.domain.product import Product


class ProductService(ProductUseCase):
    def __init__(
        self,
        product_repo: ProductRepositoryPort = Depends(ProductPersistenceAdapter),
    ):
        self._product_repo = product_repo

    async def get_product_list(self) -> list[Product]:
        return await self._product_repo.find_displayed_products()

    async def get_product(self, product_id: int) -> Product:
        if not (product := await self._product_repo.find_by_id_with_item(product_id)):
            raise HTTPException(status_code=404)
        return product
