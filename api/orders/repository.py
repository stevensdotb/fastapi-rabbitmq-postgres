from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status as http_status

from api.orders.models import Order
from api.database import db
from core.rabbitmq_client import get_rabbitmq_dependency, RabbitMQClient


class OrderRepository:
    def __init__(self, db: AsyncSession, rabbitmq: RabbitMQClient):
        self.db = db
        self.rabbitmq = rabbitmq

    async def get_all(self) -> list[Order]:
        query = await self.db.execute(select(Order))
        return query.scalars().all()

    async def get_by_id(self, order_id: int) -> Order:
        order = await self.db.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def create(self, order: Order) -> Order:
        try:
            self.db.add(order)
            await self.db.commit()
            await self.db.refresh(order)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        return order


def get_order_repository(
    db: AsyncSession = Depends(db.get_db),
    rabbitmq: RabbitMQClient = Depends(get_rabbitmq_dependency)
) -> OrderRepository:
    """Dependency to get the order repository"""
    return OrderRepository(db, rabbitmq)
    