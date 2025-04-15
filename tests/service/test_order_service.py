from fastapi.exceptions import HTTPException
import pytest

from app.adapter.inbound.api.schemas.order import OrderInfo, OrderItemInfo
from app.application.service.order import OrderService
from .factory import OrderFactory, ProductFactory, generate_credential


def get_order_info() -> OrderInfo:
    return OrderInfo(
        order_number="order_number",
        product_id=1,
        items=[OrderItemInfo(item_id=12, quantity=2)]
    )


@pytest.mark.asyncio
async def test_존재하지_않은_상품_주문_요청(order_repo, product_repo, user_repo):
    product_repo.find_by_id_or_none.return_value = None

    service = OrderService(order_repo, product_repo, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.create_order(get_order_info(), generate_credential())
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_주문자_조회_실패(order_repo, product_repo, user_repo):
    product_repo.find_by_id_or_none.return_value = ProductFactory.generate()
    user_repo.find_by_id_or_none.return_value = None

    service = OrderService(order_repo, product_repo, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.create_order(get_order_info(), generate_credential())
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_중복된_주문번호_존재하는_경우(order_repo, product_repo, user_repo):
    product_repo.find_by_id_or_none.return_value = ProductFactory.generate()
    user_repo.find_by_id_or_none.return_value = None
    order_repo.find_by_order_number.return_value = OrderFactory.generate()

    service = OrderService(order_repo, product_repo, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.create_order(get_order_info(), generate_credential())
    assert exc.value.status_code == 400
