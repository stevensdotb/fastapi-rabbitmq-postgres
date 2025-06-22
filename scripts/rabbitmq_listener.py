import asyncio

from core.rabbitmq_client import RabbitMQClient, logger

"""
Script to listen to the RabbitMQ queue and process messages.
"""

async def main():
    try:
        async with RabbitMQClient() as rabbitmq_client:   
            await rabbitmq_client.consume()
    except asyncio.CancelledError:
        logger.info("RabbitMQ Listener Stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass