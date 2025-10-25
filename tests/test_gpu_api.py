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
        url="https://api.novita.ai/gpu-instance/openapi/v1/products",
        json={
            "data": [
                {
                    "id": "gpu-a100-80gb",
                    "name": "A100 80GB",
                    "cpuPerGpu": 8,
                    "memoryPerGpu": 120,
                    "diskPerGpu": 100,
                    "availableDeploy": True,
                    "minRootFS": 20,
                    "maxRootFS": 1000,
                    "minLocalStorage": 0,
                    "maxLocalStorage": 500,
                    "regions": [],
                    "price": 350,
                    "monthlyPrice": [],
                    "billingMethods": ["onDemand"],
                    "spotPrice": "200",
                },
                {
                    "id": "gpu-a10",
                    "name": "A10",
                    "cpuPerGpu": 4,
                    "memoryPerGpu": 60,
                    "diskPerGpu": 50,
                    "availableDeploy": True,
                    "minRootFS": 20,
                    "maxRootFS": 500,
                    "minLocalStorage": 0,
                    "maxLocalStorage": 200,
                    "regions": [],
                    "price": 120,
                    "monthlyPrice": [],
                    "billingMethods": ["onDemand", "spot"],
                    "spotPrice": "80",
                },
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.products.list()

    assert len(response.data) == 2
    assert response.data[0].id == "gpu-a100-80gb"
    assert response.data[0].name == "A100 80GB"
    assert response.data[0].price == 350
    assert response.data[1].id == "gpu-a10"
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


def test_restart_instance(httpx_mock: HTTPXMock) -> None:
    """Test restarting an instance."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/restart",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.restart("inst-123")

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


def test_upgrade_instance(httpx_mock: HTTPXMock) -> None:
    """Test upgrading an instance to a different type."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/upgrade",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.upgrade("inst-123", "A100_80GB_PCIE")

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


def test_migrate_instance(httpx_mock: HTTPXMock) -> None:
    """Test migrating an instance to a different region."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/migrate",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.migrate("inst-123", "us-west-2")

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


def test_renew_instance(httpx_mock: HTTPXMock) -> None:
    """Test renewing an instance for additional hours."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/renewInstance",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.renew("inst-123", 24)

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


def test_convert_to_monthly_instance(httpx_mock: HTTPXMock) -> None:
    """Test converting an instance to monthly billing."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/transToMonthlyInstance",
        json={"instance_id": "inst-123", "success": True},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.convert_to_monthly("inst-123")

    assert response.instance_id == "inst-123"
    assert response.success is True
    client.close()


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
async def test_async_create_instance(httpx_mock: HTTPXMock) -> None:
    """Test creating a GPU instance using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        json={"instance_id": "inst-async-123", "status": "PENDING"},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        request = CreateInstanceRequest(name="async-test", instance_type=InstanceType.A100_80GB)
        response = await client.gpu.instances.create(request)

        assert response.instance_id == "inst-async-123"
        assert response.status == "PENDING"


@pytest.mark.asyncio
async def test_async_list_instances(httpx_mock: HTTPXMock) -> None:
    """Test listing GPU instances using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances",
        json={
            "instances": [
                {
                    "instance_id": "inst-async-1",
                    "name": "async-test-1",
                    "instance_type": "A100_80GB",
                    "status": "RUNNING",
                    "disk_size": 50,
                    "created_at": 1234567890,
                }
            ],
            "total": 1,
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.instances.list()

        assert response.total == 1
        assert len(response.instances) == 1
        assert response.instances[0].instance_id == "inst-async-1"
