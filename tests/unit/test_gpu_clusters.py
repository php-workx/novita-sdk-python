"""Tests for GPU clusters API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import Cluster


def _cluster_payload(**overrides: object) -> dict[str, object]:
    base = {
        "id": "us-west-1",
        "name": "US West 1",
        "availableGpuType": ["A100_80GB", "A10"],
        "supportNetworkStorage": True,
        "supportInstanceNetwork": True,
    }
    base.update(overrides)
    model = Cluster.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def test_list_clusters(httpx_mock: HTTPXMock) -> None:
    """Test listing all clusters/regions."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/clusters",
        json={
            "data": [
                _cluster_payload(),
                _cluster_payload(
                    id="eu-central-1",
                    name="EU Central 1",
                    availableGpuType=["A100_40GB", "RTX_4090"],
                    supportNetworkStorage=False,
                ),
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    clusters = client.gpu.clusters.list()

    assert isinstance(clusters, list)
    assert len(clusters) == 2
    assert all(isinstance(cluster, Cluster) for cluster in clusters)
    assert clusters[0].id == "us-west-1"
    assert clusters[0].available_gpu_type == ["A100_80GB", "A10"]
    assert clusters[1].id == "eu-central-1"
    assert clusters[1].support_network_storage is False

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
        json={"data": [_cluster_payload()]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        clusters = await client.gpu.clusters.list()

        assert isinstance(clusters, list)
        assert len(clusters) == 1
        assert isinstance(clusters[0], Cluster)
        assert clusters[0].id == "us-west-1"
