"""Tests for GPU instance API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import (
    AuthenticationError,
    BadRequestError,
    CreateInstanceRequest,
    InstanceType,
    NotFoundError,
    NovitaClient,
    RateLimitError,
    UpdateInstanceRequest,
)


def test_create_instance(httpx_mock: HTTPXMock) -> None:
    """Test creating a GPU instance."""
    # Mock the API response
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        json={"instance_id": "inst-123", "status": "PENDING"},
    )

    client = NovitaClient(api_key="test-key")
    request = CreateInstanceRequest(name="test-instance", instance_type=InstanceType.A100_80GB)

    response = client.gpu.instances.create(request)

    assert response.instance_id == "inst-123"
    assert response.status == "PENDING"

    # Verify request was made correctly
    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    assert "Bearer test-key" in request_made.headers["authorization"]
    client.close()


def test_list_instances(httpx_mock: HTTPXMock) -> None:
    """Test listing GPU instances."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances",
        json={
            "instances": [
                {
                    "instance_id": "inst-1",
                    "name": "test-1",
                    "instance_type": "A100_80GB",
                    "status": "RUNNING",
                    "disk_size": 50,
                    "created_at": 1234567890,
                }
            ],
            "total": 1,
        },
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.list()

    assert response.total == 1
    assert len(response.instances) == 1
    assert response.instances[0].instance_id == "inst-1"
    assert response.instances[0].name == "test-1"

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    assert "Bearer test-key" in request_made.headers["authorization"]
    client.close()


def test_get_instance(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific instance."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instance_id=inst-123",
        json={
            "instance_id": "inst-123",
            "name": "test-instance",
            "instance_type": "A100_80GB",
            "status": "RUNNING",
            "disk_size": 100,
            "created_at": 1234567890,
            "ssh_host": "10.0.0.1",
            "ssh_port": 22,
        },
    )

    client = NovitaClient(api_key="test-key")
    instance = client.gpu.instances.get("inst-123")

    assert instance.instance_id == "inst-123"
    assert instance.ssh_host == "10.0.0.1"
    assert instance.ssh_port == 22
    client.close()


def test_update_instance(httpx_mock: HTTPXMock) -> None:
    """Test updating an instance."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/edit",
        json={
            "instance_id": "inst-123",
            "name": "updated-name",
            "instance_type": "A100_80GB",
            "status": "RUNNING",
            "disk_size": 200,
            "created_at": 1234567890,
        },
    )

    client = NovitaClient(api_key="test-key")
    request = UpdateInstanceRequest(name="updated-name", disk_size=200)
    instance = client.gpu.instances.edit("inst-123", request)

    assert instance.name == "updated-name"
    assert instance.disk_size == 200
    client.close()


def test_start_instance(httpx_mock: HTTPXMock) -> None:
    """Test starting an instance."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/start",
        json={"instance_id": "inst-123", "success": True, "message": "Instance starting"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.start("inst-123")

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


def test_stop_instance(httpx_mock: HTTPXMock) -> None:
    """Test stopping an instance."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/stop",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.stop("inst-123")

    assert response.success is True
    client.close()


def test_delete_instance(httpx_mock: HTTPXMock) -> None:
    """Test deleting an instance."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/delete",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.delete("inst-123")

    assert response.success is True
    client.close()


def test_get_pricing(httpx_mock: HTTPXMock) -> None:
    """Test getting pricing information."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/pricing",
        json={
            "pricing": [
                {"instance_type": "A100_80GB", "price_per_hour": 3.5, "available": True},
                {"instance_type": "A10", "price_per_hour": 1.2, "available": True},
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.products.list()

    assert len(response.pricing) == 2
    assert response.pricing[0].instance_type == "A100_80GB"
    assert response.pricing[0].price_per_hour == 3.5
    client.close()


def test_authentication_error(httpx_mock: HTTPXMock) -> None:
    """Test that 401 raises AuthenticationError."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances",
        status_code=401,
        json={"error": "Unauthorized"},
    )

    client = NovitaClient(api_key="invalid-key")

    with pytest.raises(AuthenticationError):
        client.gpu.instances.list()

    client.close()


def test_not_found_error(httpx_mock: HTTPXMock) -> None:
    """Test that 404 raises NotFoundError."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instance_id=nonexistent",
        status_code=404,
        json={"error": "Not found"},
    )

    client = NovitaClient(api_key="test-key")

    with pytest.raises(NotFoundError):
        client.gpu.instances.get("nonexistent")

    client.close()


def test_bad_request_error(httpx_mock: HTTPXMock) -> None:
    """Test that 400 raises BadRequestError."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        status_code=400,
        json={"message": "Instance name already exists"},
    )

    client = NovitaClient(api_key="test-key")
    request = CreateInstanceRequest(name="test", instance_type="A100_80GB", disk_size=50)

    with pytest.raises(BadRequestError, match="Instance name already exists"):
        client.gpu.instances.create(request)

    client.close()


def test_rate_limit_error(httpx_mock: HTTPXMock) -> None:
    """Test that 429 raises RateLimitError."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances",
        status_code=429,
        json={"error": "Rate limit exceeded"},
    )

    client = NovitaClient(api_key="test-key")

    with pytest.raises(RateLimitError):
        client.gpu.instances.list()

    client.close()
