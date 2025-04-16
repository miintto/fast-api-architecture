from fastapi.routing import APIRouter

from .auth_router import router as auth_router
from .order_router import router as order_router
from .product_router import router as product_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(order_router)
router.include_router(product_router)
