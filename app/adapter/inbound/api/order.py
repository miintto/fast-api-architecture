from fastapi import APIRouter, Depends

from app.adapter.inbound.api.schemas.order import OrderInfo
from app.application.port.input import OrderUseCase
from app.application.service.order import OrderService
from app.common.permissions import IsAuthenticated
from app.common.response import JSONResponse
from app.common.security.credential import HTTPAuthorizationCredentials
from .schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("", summary="주문 요청")
async def request_order(
    body: OrderInfo,
    service: OrderUseCase = Depends(OrderService),
    credentials: HTTPAuthorizationCredentials = Depends(IsAuthenticated()),
) -> JSONResponse:
    order = await service.create_order(body, credentials)
    return JSONResponse(content=OrderResponse.from_domain(order))


@router.get("/{order_id}", summary="주문 조회")
async def search_order(
    order_id: int,
    service: OrderUseCase = Depends(OrderService),
    credentials: HTTPAuthorizationCredentials = Depends(IsAuthenticated()),
) -> JSONResponse:
    order = await service.search_order(order_id)
    return JSONResponse(content=OrderResponse.from_domain(order))
