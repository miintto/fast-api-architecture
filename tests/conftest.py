import asyncio
import os

from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy import insert

from app.adapter.outbound.persistence.entity.base import Base
from app.adapter.outbound.persistence.entity.product import (
    ProductEntity,
    ProductItemEntity,
)

os.environ.setdefault("APP_ENV", "test")

try:
    from app.main import app
    from app.config.connection import db
except ImportError:
    raise


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield conn
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(setup_db) -> AsyncClient:
    async with AsyncClient(
        base_url="http://test.miintto.com",
        transport=ASGITransport(app),
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function")
async def create_products():
    async with db._session() as session:
        res = await session.execute(
            insert(ProductEntity)
            .values(({"name": "상품1"}, {"name": "상품2"}, {"name": "상품3"}))
            .returning(ProductEntity.id)
        )
        await session.flush()
        product_ids = [int(product[0]) for product in res.fetchall()]
        await session.execute(
            insert(ProductItemEntity)
            .values(
                (
                    {
                        "product_id": product_ids[0],
                        "name": "아이템1",
                        "cost": 10000,
                        "price": 8900,
                        "item_quantity": 100,
                    },
                    {
                        "product_id": product_ids[0],
                        "name": "아이템2",
                        "cost": 20000,
                        "price": 14900,
                        "item_quantity": 100,
                    },
                    {
                        "product_id": product_ids[0],
                        "name": "아이템3",
                        "cost": 28000,
                        "price": 15900,
                        "item_quantity": 100,
                    },
                    {
                        "product_id": product_ids[0],
                        "name": "아이템4",
                        "cost": 35000,
                        "price": 18900,
                        "item_quantity": 100,
                    },
                )
            )
        )
        await session.commit()
        yield product_ids
