from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from core.settings import settings


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session

db = Database(settings.postgres_url)
Base = declarative_base()
