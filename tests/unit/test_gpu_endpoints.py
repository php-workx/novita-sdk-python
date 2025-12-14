"""Tests for GPU endpoints API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import (
    CreateEndpointRequest,
    Endpoint,
    EndpointDetail,
    Healthy1,
    Image1,
    ImageItem,
    Policy1,
    PolicyItem,
    Port2,
    Ports,
    Product1,
    Type4,
    Type6,
    UpdateEndpointRequest,
    WorkerConfig1,
    WorkerConfigItem,
)


def _endpoint_payload(**overrides: object) -> dict[str, object]:
    model = EndpointDetail.model_validate(overrides)
    return model.model_dump(by_alias=True, mode="json")


def test_list_endpoints(httpx_mock: HTTPXMock) -> None:
    """Test listing all endpoints."""
    mock_endpoints = [
        _endpoint_payload(
            id="ep-1",
            name="Primary endpoint",
            state={"state": "running"},
            address={"host": "1.2.3.4", "ports": []},
        ),
        _endpoint_payload(
            id="ep-2",
            name="Backup endpoint",
            state={"state": "stopped"},
            address={"host": "5.6.7.8", "ports": []},
        ),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoints",
        json={"endpoints": mock_endpoints, "total": len(mock_endpoints)},
    )

    client = NovitaClient(api_key="test-key")
    endpoints = client.gpu.endpoints.list()

    assert isinstance(endpoints, list)
    assert len(endpoints) == 2

    primary, secondary = endpoints
    assert isinstance(primary, EndpointDetail)
    assert primary.id == "ep-1"
    assert primary.name == "Primary endpoint"
    assert primary.state.state == "running"

    assert isinstance(secondary, EndpointDetail)
    assert secondary.id == "ep-2"
    assert secondary.state.state == "stopped"

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    client.close()


def test_get_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific endpoint."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint?endpoint_id=ep-123",
        json=_endpoint_payload(id="ep-123", name="Endpoint 123", state={"state": "active"}),
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.endpoints.get("ep-123")

    assert isinstance(endpoint, EndpointDetail)
    assert endpoint.id == "ep-123"
    assert endpoint.name == "Endpoint 123"
    assert endpoint.state.state == "active"
    client.close()


def test_create_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test creating a new endpoint."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/create",
        json=_endpoint_payload(id="ep-new", name="New Endpoint", state={"state": "creating"}),
    )

    client = NovitaClient(api_key="test-key")
    # Create a minimal Endpoint object for testing
    endpoint_config = Endpoint(
        name="test-endpoint",
        app_name="test-app",
        worker_config=WorkerConfig1(
            min_num=1,
            max_num=2,
            free_timeout=60,
            max_concurrent=1,
            gpu_num=1,
        ),
        ports=Ports(port="80"),
        policy=Policy1(type=Type4.concurrency, value=25),
        image=Image1(image="docker.io/library/nginx:latest"),
        products=[Product1(id="prod-1")],
        rootfs_size=100,
        volume_mounts=[],
        cluster_id="cluster-1",
        healthy=Healthy1(path="/health"),
    )
    endpoint = client.gpu.endpoints.create(CreateEndpointRequest(endpoint=endpoint_config))

    assert isinstance(endpoint, EndpointDetail)
    assert endpoint.id == "ep-new"
    assert endpoint.name == "New Endpoint"
    assert endpoint.state.state == "creating"

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_update_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test updating an endpoint."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/endpoint/update",
        json=_endpoint_payload(id="ep-123", state={"state": "active"}),
    )

    client = NovitaClient(api_key="test-key")
    update_request = UpdateEndpointRequest(
        worker_config=[
            WorkerConfigItem(
                min_num=1,
                max_num=2,
                free_timeout=60,
                max_concurrent=1,
                gpu_num=1,
            )
        ],
        ports=[Port2(port="80")],
        policy=[PolicyItem(type=Type6.concurrency, value=25)],
        image=[ImageItem(image="docker.io/library/nginx:latest")],
        name="updated-endpoint",
    )
    endpoint = client.gpu.endpoints.update("ep-123", update_request)

    assert isinstance(endpoint, EndpointDetail)
    assert endpoint.id == "ep-123"
    assert endpoint.state.state == "active"
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
        json={
            "endpoints": [
                _endpoint_payload(id="ep-1", name="Endpoint 1", state={"state": "running"})
            ],
            "total": 1,
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        endpoints = await client.gpu.endpoints.list()

        assert isinstance(endpoints, list)
        assert len(endpoints) == 1
        assert endpoints[0].id == "ep-1"
        assert isinstance(endpoints[0], EndpointDetail)
