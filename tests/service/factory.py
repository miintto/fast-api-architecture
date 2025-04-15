from datetime import datetime

from bcrypt import gensalt, hashpw

from app.domain.order import Order, OrderItem, OrderStatus
from app.domain.product import Product, ProductItem
from app.domain.user import User, UserPermission
from app.common.security.credential import (
    CredentialPayload,
    HTTPAuthorizationCredentials,
)


class UserFactory:
    @staticmethod
    def generate(password: str = None) -> User:
        return User(
            id=1,
            email="test@test.com",
            password=(
                hashpw(password.encode(), salt=gensalt()).decode()
                if password else None
            ),
            permission=UserPermission.NORMAL,
            is_active=True,
            last_login=None,
            created_dtm=datetime.now()
        )


class ProductFactory:
    @staticmethod
    def generate() -> Product:
        return Product(
            id=1,
            name="상품",
            is_displayed=True,
            created_dtm=datetime.now(),
            updated_dtm=datetime.now(),
            items=[
                ProductItem(
                    id=12,
                    product_id=1,
                    name="상품 옵션",
                    cost=20000,
                    price=15000,
                    is_active=True,
                    item_quantity=1,
                    sold_quantity=1,
                    sale_start_dtm=None,
                    sale_close_dtm=None,
                    created_dtm=datetime.now(),
                    updated_dtm=datetime.now(),
                )
            ]
        )


class OrderFactory:
    @staticmethod
    def generate(count: int = 2) -> Order:
        return Order(
            id=123,
            order_number="order_number",
            product_id=1,
            status=OrderStatus.CONFIRMED,
            user_id=1,
            canceled_dtm=None,
            confirmed_dtm=None,
            created_dtm=datetime.now(),
            items=[
                OrderItem(
                    id=1234,
                    order_id=123,
                    item_id=12,
                    price=15000,
                    created_dtm=datetime.now(),
                )
                for _ in range(count)
            ]
        )


def generate_credential() -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        token="token",
        payload=CredentialPayload(
            pk=1,
            email="test@test.com",
            permission=UserPermission.NORMAL,
            exp=-1,
            iat=-1
        )
    )
