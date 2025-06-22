from fastapi import APIRouter, status as http_status, Depends

from api.orders.dto import OrderDTO, CreateOrderDTO
from api.orders.repository import OrderRepository, get_order_repository
from api.orders.services import OrderService


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderDTO, status_code=http_status.HTTP_201_CREATED)
async def create_order(order: CreateOrderDTO, repository: OrderRepository = Depends(get_order_repository)):
    """Create a new order"""
    return await OrderService(repository).create(order)


@router.get("/{order_id}", response_model=OrderDTO)
async def get_order(order_id: int, repository: OrderRepository = Depends(get_order_repository)):
    """Get an order by id"""
    return await OrderService(repository).get_by_id(order_id)


@router.get("", response_model=list[OrderDTO])
async def get_orders(repository: OrderRepository = Depends(get_order_repository)):
    """Get all orders"""
    return await OrderService(repository).get_all()
    
