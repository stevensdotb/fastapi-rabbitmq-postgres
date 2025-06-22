from fastapi import APIRouter

from .orders.controller import router as orders_router

router = APIRouter()
router.include_router(orders_router)
