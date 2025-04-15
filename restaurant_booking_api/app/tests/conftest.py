
import pytest
import pytest_asyncio
import httpx
from typing import AsyncGenerator, Dict, Any

BASE_URL = "http://app:8000"


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as client:

        yield client


@pytest_asyncio.fixture(scope="function")
async def create_test_table(async_client: httpx.AsyncClient) -> Dict[str, Any]:

    table_data = {
        "name": f"Test Table Fixture {datetime.datetime.utcnow().isoformat()}",
        "seats": 4,
        "location": "Fixture Area"
    }
    created_table = None
    try:
        response = await async_client.post("/tables/", json=table_data)
        response.raise_for_status()
        created_table = response.json()

        yield created_table

    finally:

        if created_table and "id" in created_table:
            try:

                await async_client.delete(f"/tables/{created_table['id']}")
            except Exception as e:

                print(f"\nWarning: Could not cleanup test table {created_table.get('id')}. Error: {e}")
        elif created_table is None:
             print(f"\nWarning: Test table was not created successfully, skipping cleanup.")



@pytest_asyncio.fixture(scope="function")
async def create_test_reservation(async_client: httpx.AsyncClient, create_test_table: Dict[str, Any]) -> Dict[str, Any]:

    table_id = create_test_table["id"]
    reservation_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat()
    reservation_data = {
        "customer_name": "Fixture Customer",
        "table_id": table_id,
        "reservation_time": reservation_time,
        "duration_minutes": 60
    }
    created_reservation = None
    try:
        response = await async_client.post("/reservations/", json=reservation_data)
        response.raise_for_status()
        created_reservation = response.json()
        yield created_reservation
    finally:
        if created_reservation and "id" in created_reservation:
            try:
                await async_client.delete(f"/reservations/{created_reservation['id']}")
            except Exception as e:
                print(f"\nWarning: Could not cleanup test reservation {created_reservation.get('id')}. Error: {e}")
        elif created_reservation is None:
            print(f"\nWarning: Test reservation was not created successfully, skipping cleanup.")


import datetime
