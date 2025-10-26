"""Tests for GPU endpoints API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_endpoints(httpx_mock: HTTPXMock) -> None:
    """Test listing all endpoints."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoints",
        json={"endpoints": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.endpoints.list()

    assert "endpoints" in response
    assert isinstance(response["endpoints"], list)

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    client.close()


def test_get_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific endpoint."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint?endpoint_id=ep-123",
        json={"endpoint_id": "ep-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.endpoints.get("ep-123")

    assert response["endpoint_id"] == "ep-123"
    client.close()


def test_create_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test creating a new endpoint."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/create",
        json={"endpoint_id": "ep-new", "status": "creating"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.endpoints.create(name="test-endpoint", instance_id="inst-123")

    assert response["endpoint_id"] == "ep-new"

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_update_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test updating an endpoint."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/update",
        json={"endpoint_id": "ep-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.endpoints.update("ep-123", name="updated-endpoint")

    assert response["endpoint_id"] == "ep-123"
    client.close()


def test_delete_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test deleting an endpoint."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.endpoints.delete("ep-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_get_endpoint_limit_ranges(httpx_mock: HTTPXMock) -> None:
    """Test getting endpoint limit ranges."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/limit",
        json={"max_endpoints": 10},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.endpoints.get_limit_ranges()

    assert response["max_endpoints"] == 10
    client.close()


@pytest.mark.asyncio
async def test_async_list_endpoints(httpx_mock: HTTPXMock) -> None:
    """Test listing endpoints using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoints",
        json={"endpoints": [{"endpoint_id": "ep-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.endpoints.list()

        assert len(response["endpoints"]) == 1
        assert response["endpoints"][0]["endpoint_id"] == "ep-1"
