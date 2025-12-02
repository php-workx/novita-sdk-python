"""Tests for network storage API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import NetworkStorageModel


def _storage_payload(**overrides: object) -> dict[str, object]:
    base = {
        "storageId": "stor-1",
        "storageName": "Storage 1",
        "storageSize": 100,
        "clusterId": "cluster-1",
        "clusterName": "Cluster",
    }
    base.update(overrides)
    model = NetworkStorageModel.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def test_list_storages(httpx_mock: HTTPXMock) -> None:
    """Test listing network storages."""
    mock_storages = [
        _storage_payload(storageId="stor-1", storageName="Storage 1"),
        _storage_payload(storageId="stor-2", storageName="Storage 2"),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorages/list",
        json={"data": mock_storages, "total": len(mock_storages)},
    )

    client = NovitaClient(api_key="test-key")
    storages = client.gpu.storages.list()

    assert isinstance(storages, list)
    assert len(storages) == 2
    assert isinstance(storages[0], NetworkStorageModel)
    assert storages[0].storage_id == "stor-1"
    assert storages[0].storage_name == "Storage 1"
    assert storages[1].storage_id == "stor-2"
    client.close()


def test_create_storage(httpx_mock: HTTPXMock) -> None:
    """Test creating a network storage."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorage/create",
        json=_storage_payload(storageId="stor-123", storageName="Storage created"),
    )

    client = NovitaClient(api_key="test-key")
    storage = client.gpu.storages.create(name="test-storage", size=100)

    assert isinstance(storage, NetworkStorageModel)
    assert storage.storage_id == "stor-123"
    assert storage.storage_name == "Storage created"
    client.close()


def test_update_storage(httpx_mock: HTTPXMock) -> None:
    """Test updating a network storage."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networkstorage/update",
        json=_storage_payload(storageId="stor-123", storageName="Updated storage"),
    )

    client = NovitaClient(api_key="test-key")
    storage = client.gpu.storages.update("stor-123", name="updated-storage")

    assert storage.storage_id == "stor-123"
    assert storage.storage_name == "Updated storage"
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
        json={"data": [_storage_payload()], "total": 1},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        storages = await client.gpu.storages.list()

        assert isinstance(storages, list)
        assert len(storages) == 1
        assert storages[0].storage_id == "stor-1"
        assert isinstance(storages[0], NetworkStorageModel)
