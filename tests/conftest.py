from unittest.mock import AsyncMock

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from api.database import Base, db
from core.rabbitmq_client import RabbitMQClient, get_rabbitmq_dependency


@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    """
    Set the backend for async tests.
    """
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def rabbitmq_client_mock():
    """
    Create a RabbitMQ client for testing.
    """

    mock_client = AsyncMock(spec=RabbitMQClient)
    async with mock_client as rabbitmq_client:
        yield rabbitmq_client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_engine():
    """
    Create an in-memory SQLite database for testing.
    """

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine, rabbitmq_client_mock):
    """
    Create a new database session for each test.
    """
    async with test_engine.connect() as connection:
        async with connection.begin() as transaction:

            TestSessionLocal = sessionmaker(
                bind=connection,
                autoflush=False,
                autocommit=False,
                class_=AsyncSession,
                expire_on_commit=False
            )
            async def override_get_db():
                async with TestSessionLocal() as session:
                    yield session

            app.dependency_overrides[get_rabbitmq_dependency] = lambda: rabbitmq_client_mock
            app.dependency_overrides[db.get_db] = override_get_db

            yield override_get_db

            await transaction.rollback()
    
    app.dependency_overrides.clear()



@pytest_asyncio.fixture(scope="function")
async def client(db_session, rabbitmq_client_mock):
    """
    Test FastAPI application with test database.
    """
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test/api/v1") as ac:
        yield ac

    
