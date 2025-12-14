"""Tests for VPC networks API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import (
    CreateNetworkRequest,
    Network,
    NetworkModel,
    UpdateNetworkRequest,
)


def _network_payload(**overrides: object) -> dict[str, object]:
    base = {
        "Id": "net-1",
        "user": "user-1",
        "name": "Network 1",
        "state": {"state": "ready"},
        "segment": "10.0.0.0/24",
        "clusterId": "cluster-1",
        "Addresses": [{"Id": "addr-1", "Ip": "10.0.0.5"}],
        "createTime": "1234567890",
    }
    base.update(overrides)
    model = NetworkModel.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def _network_detail_payload(**overrides: object) -> dict[str, object]:
    base = {
        "id": "net-123",
        "ip": "10.0.0.5",
    }
    base.update(overrides)
    model = Network.model_validate(base)
    return model.model_dump(mode="json")


def test_list_networks(httpx_mock: HTTPXMock) -> None:
    """Test listing VPC networks."""
    mock_networks = [
        _network_payload(Id="net-1", name="Network 1", state={"state": "ready"}),
        _network_payload(Id="net-2", name="Network 2", state={"state": "creating"}),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/networks",
        json={"networks": mock_networks, "total": str(len(mock_networks))},
    )

    client = NovitaClient(api_key="test-key")
    networks = client.gpu.networks.list()

    assert isinstance(networks, list)
    assert len(networks) == 2
    assert isinstance(networks[0], NetworkModel)
    assert networks[0].id == "net-1"
    assert networks[0].state.state.value == "ready"
    assert networks[1].id == "net-2"
    client.close()


def test_get_network(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific network."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network?network_id=net-123",
        json={"network": [_network_detail_payload()]},
    )

    client = NovitaClient(api_key="test-key")
    network = client.gpu.networks.get("net-123")

    assert isinstance(network, Network)
    assert network.id == "net-123"
    assert network.ip == "10.0.0.5"
    client.close()


def test_create_network(httpx_mock: HTTPXMock) -> None:
    """Test creating a VPC network."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network/create",
        json={"network": [_network_detail_payload(id="net-new")]},
    )

    client = NovitaClient(api_key="test-key")
    network = client.gpu.networks.create(
        CreateNetworkRequest(
            cluster_id="cluster-1",
            name="test-network",
        )
    )

    assert isinstance(network, Network)
    assert network.id == "net-new"
    client.close()


def test_update_network(httpx_mock: HTTPXMock) -> None:
    """Test updating a VPC network."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/network/update",
        json={"network": [_network_detail_payload(id="net-123", ip="10.0.0.10")]},
    )

    client = NovitaClient(api_key="test-key")
    network = client.gpu.networks.update(
        UpdateNetworkRequest(
            network_id="net-123",
            name="updated-network",
        )
    )

    assert isinstance(network, Network)
    assert network.id == "net-123"
    assert network.ip == "10.0.0.10"
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
        json={"networks": [_network_payload()], "total": "1"},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        networks = await client.gpu.networks.list()

        assert isinstance(networks, list)
        assert len(networks) == 1
        assert networks[0].id == "net-1"
        assert isinstance(networks[0], NetworkModel)
