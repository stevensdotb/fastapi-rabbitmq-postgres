import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings:
    """Class to manage all the environment variables from the .env file"""

    @property
    def DEBUG(self):
        return os.getenv("DEBUG", "0").lower() in ("1", "true")

    @property
    def postgres_url(self):
        postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
        postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
        postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
        postgres_password: str = os.getenv("POSTGRES_PASSWORD")
        postgres_db: str = os.getenv("POSTGRES_DB")
        return f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    @property
    def rabbitmq_url(self):
        rabbitmq_host: str = os.getenv("RABBITMQ_HOST")
        rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT"))
        rabbitmq_user: str = os.getenv("RABBITMQ_USER")
        rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD")
        return f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}"

    @property
    def rabbitmq_queue(self):
        return os.getenv("RABBITMQ_QUEUE")

settings = Settings()