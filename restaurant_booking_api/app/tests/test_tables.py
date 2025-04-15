import pytest
import httpx
from typing import Dict, Any


pytestmark = pytest.mark.asyncio

async def test_read_root(async_client: httpx.AsyncClient):

    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Restaurant Booking API!"}



async def test_create_table(async_client: httpx.AsyncClient):

    table_data = {
        "name": "Window Table 1",
        "seats": 2,
        "location": "Near window"
    }
    response = await async_client.post("/tables/", json=table_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == table_data["name"]
    assert data["seats"] == table_data["seats"]
    assert data["location"] == table_data["location"]
    assert "id" in data


    table_id = data["id"]
    await async_client.delete(f"/tables/{table_id}")

async def test_get_tables(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    response = await async_client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    assert any(table["id"] == create_test_table["id"] for table in data)

async def test_get_specific_table(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    table_id = create_test_table["id"]
    response = await async_client.get(f"/tables/{table_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == table_id
    assert data["name"] == create_test_table["name"]

async def test_get_nonexistent_table(async_client: httpx.AsyncClient):

    response = await async_client.get("/tables/999999")
    assert response.status_code == 404

async def test_delete_table(async_client: httpx.AsyncClient):

    table_data = {
        "name": "Table to Delete",
        "seats": 1
    }
    response_post = await async_client.post("/tables/", json=table_data)
    assert response_post.status_code == 201
    table_id = response_post.json()["id"]


    response_delete = await async_client.delete(f"/tables/{table_id}")
    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == table_id


    response_get = await async_client.get(f"/tables/{table_id}")
    assert response_get.status_code == 404

async def test_delete_nonexistent_table(async_client: httpx.AsyncClient):

    response = await async_client.delete("/tables/999999")
    assert response.status_code == 404
