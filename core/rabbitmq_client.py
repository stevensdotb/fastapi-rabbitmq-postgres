import aio_pika

from logger import get_logger
from core.settings import settings

logger = get_logger(name="rabbitmq")

class RabbitMQClient:
    def __init__(self):
        self.queue_name = settings.rabbitmq_queue
        self.connection = None
        self.channel = None
        self.queue = None

    async def __aenter__(self):
        self.connection = await aio_pika.connect_robust(
            settings.rabbitmq_url,
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=5)

        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()

    async def publish(self, message):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self.queue_name,
        )
        logger.info(f"Published :: {message}")

    async def consume(self):
        logger.info("Listening for incoming messages...")
        
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logger.info(f"Processing :: {message.body.decode()}")


async def get_rabbitmq_dependency():
    """Dependency to get the rabbitmq client"""
    async with RabbitMQClient() as rabbitmq_client:
        yield rabbitmq_client
