"""Tests for GPU clusters API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_clusters(httpx_mock: HTTPXMock) -> None:
    """Test listing all clusters/regions."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/clusters",
        json={
            "data": [
                {
                    "id": "us-west-1",
                    "name": "US West 1",
                    "availableGpuType": ["A100_80GB", "A10"],
                    "supportNetworkStorage": True,
                    "supportInstanceNetwork": True,
                },
                {
                    "id": "eu-central-1",
                    "name": "EU Central 1",
                    "availableGpuType": ["A100_40GB", "RTX_4090"],
                    "supportNetworkStorage": False,
                    "supportInstanceNetwork": True,
                },
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.clusters.list()

    # OpenAPI spec returns {"data": [...]} but implementation returns response.json() directly
    # This test will fail until implementation is fixed to return the full response
    assert "data" in response
    assert len(response["data"]) == 2
    assert response["data"][0]["id"] == "us-west-1"
    assert response["data"][0]["name"] == "US West 1"
    assert response["data"][1]["id"] == "eu-central-1"

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    assert "Bearer test-key" in request_made.headers["authorization"]
    client.close()


@pytest.mark.asyncio
async def test_async_list_clusters(httpx_mock: HTTPXMock) -> None:
    """Test listing clusters using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/clusters",
        json={
            "data": [
                {
                    "id": "us-west-1",
                    "name": "US West 1",
                    "availableGpuType": ["A100_80GB"],
                    "supportNetworkStorage": True,
                    "supportInstanceNetwork": True,
                }
            ]
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.clusters.list()

        # OpenAPI spec returns {"data": [...]} but implementation returns response.json() directly
        assert "data" in response
        assert len(response["data"]) == 1
        assert response["data"][0]["id"] == "us-west-1"
