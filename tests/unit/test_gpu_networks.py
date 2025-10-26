"""Tests for VPC networks API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_networks(httpx_mock: HTTPXMock) -> None:
    """Test listing VPC networks."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networks",
        json={"networks": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.networks.list()

    assert "networks" in response
    assert isinstance(response["networks"], list)
    client.close()


def test_get_network(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific network."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network?network_id=net-123",
        json={"network_id": "net-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.networks.get("net-123")

    assert response["network_id"] == "net-123"
    client.close()


def test_create_network(httpx_mock: HTTPXMock) -> None:
    """Test creating a VPC network."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network/create",
        json={"network_id": "net-new", "status": "creating"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.networks.create(name="test-network")

    assert response["network_id"] == "net-new"
    client.close()


def test_update_network(httpx_mock: HTTPXMock) -> None:
    """Test updating a VPC network."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network/update",
        json={"network_id": "net-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.networks.update("net-123", name="updated-network")

    assert response["network_id"] == "net-123"
    client.close()


def test_delete_network(httpx_mock: HTTPXMock) -> None:
    """Test deleting a VPC network."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.networks.delete("net-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


@pytest.mark.asyncio
async def test_async_list_networks(httpx_mock: HTTPXMock) -> None:
    """Test listing networks using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networks",
        json={"networks": [{"network_id": "net-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.networks.list()

        assert len(response["networks"]) == 1
