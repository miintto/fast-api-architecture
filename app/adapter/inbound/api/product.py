from fastapi import APIRouter, Depends

from app.application.port.input import ProductUseCase
from app.application.service.product import ProductService
from app.common.response import JSONResponse
from .schemas.product import ProductResponse

router = APIRouter(prefix="/products", tags=["Product"])


@router.get("", summary="상품 리스트")
async def product_list(
    service: ProductUseCase = Depends(ProductService),
) -> JSONResponse:
    products = await service.get_product_list()
    return JSONResponse(
        content=[ProductResponse.from_domain(product) for product in products]
    )


@router.get("/{product_id}", summary="상품 상세")
async def product_detail(
    product_id: int,
    service: ProductUseCase = Depends(ProductService),
) -> JSONResponse:
    product = await service.get_product(product_id)
    return JSONResponse(content=ProductResponse.from_domain(product))
