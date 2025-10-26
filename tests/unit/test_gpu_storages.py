"""Tests for network storage API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_storages(httpx_mock: HTTPXMock) -> None:
    """Test listing network storages."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorages/list",
        json={"storages": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.storages.list()

    assert "storages" in response
    assert isinstance(response["storages"], list)
    client.close()


def test_create_storage(httpx_mock: HTTPXMock) -> None:
    """Test creating a network storage."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorage/create",
        json={"storage_id": "stor-123", "status": "creating"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.storages.create(name="test-storage", size=100)

    assert response["storage_id"] == "stor-123"
    client.close()


def test_update_storage(httpx_mock: HTTPXMock) -> None:
    """Test updating a network storage."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorage/update",
        json={"storage_id": "stor-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.storages.update("stor-123", name="updated-storage")

    assert response["storage_id"] == "stor-123"
    client.close()


def test_delete_storage(httpx_mock: HTTPXMock) -> None:
    """Test deleting a network storage."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorage/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.storages.delete("stor-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


@pytest.mark.asyncio
async def test_async_list_storages(httpx_mock: HTTPXMock) -> None:
    """Test listing storages using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorages/list",
        json={"storages": [{"storage_id": "stor-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.storages.list()

        assert len(response["storages"]) == 1
