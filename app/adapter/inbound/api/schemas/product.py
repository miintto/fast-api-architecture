from pydantic import BaseModel

from app.domain.product import Product, ProductItem


class ProductItemResponse(BaseModel):
    id: int
    name: str
    cost: int
    price: int
    discount: int
    item_quantity: int
    sold_quantity: int

    @staticmethod
    def _calc_discount(item: ProductItem):
        try:
            return 100 - int(item.price * 100 / item.cost)
        except ZeroDivisionError:
            return 0

    @classmethod
    def from_domain(cls, item: ProductItem) -> "ProductItemResponse":
        return cls(
            id=item.id,
            name=item.name,
            cost=item.cost,
            price=item.price,
            discount=cls._calc_discount(item),
            item_quantity=item.item_quantity,
            sold_quantity=item.sold_quantity,
        )


class ProductResponse(BaseModel):
    id: int
    name: str
    items: list[ProductItemResponse]

    @classmethod
    def from_domain(cls, product: Product) -> "ProductResponse":
        return cls(
            id=product.id,
            name=product.name,
            items=[ProductItemResponse.from_domain(item) for item in product.items],
        )

