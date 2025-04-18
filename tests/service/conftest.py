from unittest.mock import AsyncMock

import pytest_asyncio

from app.adapter.outbound.persistence.order_adapter import OrderPersistenceAdapter
from app.adapter.outbound.persistence.product_adapter import ProductPersistenceAdapter
from app.adapter.outbound.persistence.user_adapter import UserPersistenceAdapter


@pytest_asyncio.fixture(scope="function")
async def order_repo():
    yield AsyncMock(OrderPersistenceAdapter)


@pytest_asyncio.fixture(scope="function")
async def product_repo():
    yield AsyncMock(ProductPersistenceAdapter)


@pytest_asyncio.fixture(scope="function")
async def user_repo():
    yield AsyncMock(UserPersistenceAdapter)
