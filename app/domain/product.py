from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    id: int
    name: str
    is_displayed: bool
    created_dtm: datetime
    updated_dtm: datetime
    items: list["ProductItem"]


@dataclass
class ProductItem:
    id: int
    product_id: int
    name: str
    cost: int
    price: int
    is_active: bool
    item_quantity: int
    sold_quantity: int
    sale_start_dtm: datetime | None
    sale_close_dtm: datetime | None
    created_dtm: datetime
    updated_dtm: datetime
