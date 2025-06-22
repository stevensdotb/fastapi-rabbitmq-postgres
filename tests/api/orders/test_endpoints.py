from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_orders(client: AsyncClient):
    """Test GET /orders endpoint."""
    response = await client.get("/orders")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, rabbitmq_client_mock: AsyncMock):
    """Test POST /orders endpoint."""
    order_data = {
        "customer_name": "John Doe",
        "product_name": "Product 1",
        "quantity": 2,
    }

    response = await client.post("/orders", json=order_data)
    assert response.status_code == 201
    
    created_order = response.json()
    assert "id" in created_order
    assert created_order["customer_name"] == "John Doe"
    assert created_order["product_name"] == "Product 1"
    assert created_order["quantity"] == 2
    assert created_order["status"] == "pending"


@pytest.mark.asyncio
async def test_get_order_by_id(client: AsyncClient):
    """Test GET /orders/{id} endpoint."""
    # Create an order first
    response = await client.post(
        "/orders",
        json={
            "customer_name": "John Doe",
            "product_name": "Product 1",
            "quantity": 2,
        }
    )
    assert response.status_code == 201
    order_id = response.json()["id"]

    # Get the order by ID
    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    
    order = response.json()
    assert order["id"] == order_id
    assert order["customer_name"] == "John Doe"
    assert order["product_name"] == "Product 1"
    assert order["quantity"] == 2
    assert order["status"] == "pending"


@pytest.mark.asyncio
async def test_get_order_by_id_not_found(client: AsyncClient):
    """Test GET /orders/{id} with non-existent ID."""
    response = await client.get("/orders/999")
    assert response.status_code == 404

