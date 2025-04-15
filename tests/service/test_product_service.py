from unittest.mock import AsyncMock

from fastapi.exceptions import HTTPException
import pytest

from app.application.service.product import ProductService
from app.domain.product import Product
from .factory import ProductFactory


@pytest.mark.asyncio
async def test_상품_리스트_조회():
    mock_repo = AsyncMock()
    mock_repo.find_displayed_products.return_value = [
        ProductFactory.generate(),
        ProductFactory.generate(),
        ProductFactory.generate(),
    ]

    service = ProductService(mock_repo)
    products = await service.get_product_list()

    assert len(products) == 3
    mock_repo.find_displayed_products.assert_called_once()


@pytest.mark.asyncio
async def test_상품_조회():
    mock_repo = AsyncMock()
    mock_repo.find_by_id_with_item.return_value = ProductFactory.generate()

    service = ProductService(mock_repo)
    product = await service.get_product(product_id=1)

    assert isinstance(product, Product)
    mock_repo.find_by_id_with_item.assert_called_once()


@pytest.mark.asyncio
async def test_존재하지_않는_상품_조회():
    mock_repo = AsyncMock()
    mock_repo.find_by_id_with_item.return_value = None

    service = ProductService(mock_repo)
    with pytest.raises(HTTPException) as exc:
        await service.get_product(product_id=1)
    assert exc.value.status_code == 404
