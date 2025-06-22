from api.orders.repository import OrderRepository
from api.orders.models import Order
from api.orders.dto import CreateOrderDTO, OrderDTO


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def get_all(self) -> list[OrderDTO]:
        orders = await self.repository.get_all()
        return [OrderDTO.model_validate(order) for order in orders]

    async def get_by_id(self, order_id: int) -> OrderDTO:
        order = await self.repository.get_by_id(order_id)
        return OrderDTO.model_validate(order)

    async def create(self, order: CreateOrderDTO) -> OrderDTO:
        obj = Order(**order.model_dump())
        created = await self.repository.create(obj)
        serialized_order = OrderDTO.model_validate(created)

        await self.repository.rabbitmq.publish(serialized_order.model_dump_json())

        return serialized_order
