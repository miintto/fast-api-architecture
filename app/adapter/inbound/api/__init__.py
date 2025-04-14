from fastapi.routing import APIRouter

from .auth import router as auth_router
from .order import router as order_router
from .product import router as product_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(order_router)
router.include_router(product_router)
