import pytest
import httpx
import datetime
from typing import Dict, Any

pytestmark = pytest.mark.asyncio


NOW = datetime.datetime.now()
DEFAULT_RESERVATION_TIME = (NOW + datetime.timedelta(hours=1)).isoformat()
DEFAULT_DURATION = 60

async def test_create_reservation(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    table_id = create_test_table["id"]
    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": table_id,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": DEFAULT_DURATION
    }
    response = await async_client.post("/reservations/", json=reservation_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == reservation_data["customer_name"]
    assert data["table_id"] == table_id
    assert data["duration_minutes"] == DEFAULT_DURATION

    assert data["reservation_time"].startswith(DEFAULT_RESERVATION_TIME.split('.')[0])
    assert "id" in data
    assert data["table"]["id"] == table_id

    reservation_id = data["id"]
    await async_client.delete(f"/reservations/{reservation_id}")

async def test_create_reservation_table_not_found(async_client: httpx.AsyncClient):

    reservation_data = {
        "customer_name": "Ghost Customer",
        "table_id": 999999,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": DEFAULT_DURATION
    }
    response = await async_client.post("/reservations/", json=reservation_data)
    assert response.status_code == 404

async def test_create_reservation_conflict(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    table_id = create_test_table["id"]


    reservation_data_1 = {
        "customer_name": "First Customer",
        "table_id": table_id,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": DEFAULT_DURATION
    }
    response1 = await async_client.post("/reservations/", json=reservation_data_1)
    assert response1.status_code == 201
    reservation_id_1 = response1.json()["id"]


    reservation_data_2 = {
        "customer_name": "Second Customer",
        "table_id": table_id,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": 30
    }
    response2 = await async_client.post("/reservations/", json=reservation_data_2)
    assert response2.status_code == 409


    overlapping_time = (datetime.datetime.fromisoformat(DEFAULT_RESERVATION_TIME) + datetime.timedelta(minutes=DEFAULT_DURATION // 2)).isoformat()
    reservation_data_3 = {
        "customer_name": "Third Customer",
        "table_id": table_id,
        "reservation_time": overlapping_time,
        "duration_minutes": 60
    }
    response3 = await async_client.post("/reservations/", json=reservation_data_3)
    assert response3.status_code == 409


    await async_client.delete(f"/reservations/{reservation_id_1}")

async def test_get_reservations(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    table_id = create_test_table["id"]

    reservation_data = {
        "customer_name": "List Test Customer",
        "table_id": table_id,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": 15
    }
    response_post = await async_client.post("/reservations/", json=reservation_data)
    assert response_post.status_code == 201
    created_reservation_id = response_post.json()["id"]

    response_get = await async_client.get("/reservations/")
    assert response_get.status_code == 200
    data = response_get.json()
    assert isinstance(data, list)
    assert any(res["id"] == created_reservation_id for res in data)


    await async_client.delete(f"/reservations/{created_reservation_id}")


async def test_delete_reservation(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]):

    table_id = create_test_table["id"]

    reservation_data = {
        "customer_name": "To Delete",
        "table_id": table_id,
        "reservation_time": DEFAULT_RESERVATION_TIME,
        "duration_minutes": 30
    }
    response_post = await async_client.post("/reservations/", json=reservation_data)
    assert response_post.status_code == 201
    reservation_id = response_post.json()["id"]

    response_delete = await async_client.delete(f"/reservations/{reservation_id}")
    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == reservation_id

    response_get = await async_client.get(f"/reservations/{reservation_id}")
    assert response_get.status_code == 404

