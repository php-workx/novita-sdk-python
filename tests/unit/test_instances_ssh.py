"""Tests for SSH endpoint extraction from instances."""

import pytest
from pytest_httpx import HTTPXMock

from novita import AsyncNovitaClient, NotFoundError, NovitaClient
from novita.generated.models import SSHEndpoint


def test_get_ssh_endpoint_from_connect_component(httpx_mock: HTTPXMock) -> None:
    """Test extracting SSH endpoint from connect_component_ssh field."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-123",
        json={
            "id": "inst-123",
            "name": "test-instance",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "connectComponentSSH": {
                "user": "ubuntu",
                "command": "ssh ubuntu@example.com -p 22345",
            },
        },
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.instances.get_ssh_endpoint("inst-123")

    assert isinstance(endpoint, SSHEndpoint)
    assert endpoint.user == "ubuntu"
    assert endpoint.host == "example.com"
    assert endpoint.port == 22345
    assert endpoint.command == "ssh ubuntu@example.com -p 22345"
    client.close()


def test_get_ssh_endpoint_from_connect_component_minimal(httpx_mock: HTTPXMock) -> None:
    """Test extracting SSH endpoint with minimal connect_component_ssh data."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-456",
        json={
            "id": "inst-456",
            "name": "test-instance-2",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "connectComponentSSH": {
                "user": "root",
                "command": "ssh root@10.0.0.5",
            },
        },
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.instances.get_ssh_endpoint("inst-456")

    assert endpoint.user == "root"
    assert endpoint.host == "10.0.0.5"
    assert endpoint.port == 22  # Default port
    assert endpoint.command == "ssh root@10.0.0.5"
    client.close()


def test_get_ssh_endpoint_from_port_mappings(httpx_mock: HTTPXMock) -> None:
    """Test extracting SSH endpoint from port_mappings fallback."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-789",
        json={
            "id": "inst-789",
            "name": "test-instance-3",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "portMappings": [
                {"port": 80, "endpoint": "tcp://node1.example.com:8080", "type": "http"},
                {"port": 22, "endpoint": "tcp://node1.example.com:22222", "type": "tcp"},
            ],
        },
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.instances.get_ssh_endpoint("inst-789")

    assert endpoint.user == "root"  # Default user
    assert endpoint.host == "node1.example.com"
    assert endpoint.port == 22222
    assert endpoint.command == "ssh root@node1.example.com -p 22222"
    client.close()


def test_get_ssh_endpoint_from_port_mappings_without_scheme(httpx_mock: HTTPXMock) -> None:
    """Test extracting SSH endpoint from port_mappings with plain host:port format."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-999",
        json={
            "id": "inst-999",
            "name": "test-instance-4",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "portMappings": [
                {"port": 22, "endpoint": "192.168.1.100:23456", "type": "tcp"},
            ],
        },
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.instances.get_ssh_endpoint("inst-999")

    assert endpoint.user == "root"
    assert endpoint.host == "192.168.1.100"
    assert endpoint.port == 23456
    client.close()


def test_get_ssh_endpoint_not_found(httpx_mock: HTTPXMock) -> None:
    """Test that NotFoundError is raised when no SSH endpoint is available."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-nossh",
        json={
            "id": "inst-nossh",
            "name": "no-ssh-instance",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            # No connectComponentSSH and no port 22 in portMappings
            "portMappings": [
                {"port": 80, "endpoint": "http://example.com:8080", "type": "http"},
            ],
        },
    )

    client = NovitaClient(api_key="test-key")

    with pytest.raises(NotFoundError) as exc_info:
        client.gpu.instances.get_ssh_endpoint("inst-nossh")

    assert "No SSH endpoint found" in str(exc_info.value)
    client.close()


def test_get_ssh_endpoint_command_with_port_flag(httpx_mock: HTTPXMock) -> None:
    """Test parsing SSH command with -p flag before user@host."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-alt",
        json={
            "id": "inst-alt",
            "name": "test-instance-alt",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "connectComponentSSH": {
                "user": "admin",
                "command": "ssh -p 2222 admin@server.example.com",
            },
        },
    )

    client = NovitaClient(api_key="test-key")
    endpoint = client.gpu.instances.get_ssh_endpoint("inst-alt")

    assert endpoint.user == "admin"
    assert endpoint.host == "server.example.com"
    assert endpoint.port == 2222
    client.close()


@pytest.mark.asyncio
async def test_async_get_ssh_endpoint(httpx_mock: HTTPXMock) -> None:
    """Test getting SSH endpoint using async client."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-async",
        json={
            "id": "inst-async",
            "name": "async-test",
            "clusterId": "cluster-1",
            "status": "running",
            "imageUrl": "ubuntu:22.04",
            "cpuNum": "4",
            "memory": "16",
            "gpuNum": "1",
            "productId": "gpu-a10",
            "productName": "A10",
            "rootfsSize": 100,
            "connectComponentSSH": {
                "user": "ubuntu",
                "command": "ssh ubuntu@async-host.com -p 2200",
            },
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        endpoint = await client.gpu.instances.get_ssh_endpoint("inst-async")

        assert endpoint.user == "ubuntu"
        assert endpoint.host == "async-host.com"
        assert endpoint.port == 2200


def test_parse_ssh_command_variants() -> None:
    """Test SSH command parsing with various formats."""
    from novita.api.resources.gpu.instances import _parse_ssh_command

    # Standard format
    result = _parse_ssh_command("ssh root@example.com -p 2222")
    assert result["user"] == "root"
    assert result["host"] == "example.com"
    assert result["port"] == 2222

    # Port flag first
    result = _parse_ssh_command("ssh -p 22000 ubuntu@10.0.0.1")
    assert result["user"] == "ubuntu"
    assert result["host"] == "10.0.0.1"
    assert result["port"] == 22000

    # No port specified
    result = _parse_ssh_command("ssh admin@server.local")
    assert result["user"] == "admin"
    assert result["host"] == "server.local"
    assert "port" not in result

    # Port with equals sign
    result = _parse_ssh_command("ssh user@host.com -p=3000")
    assert result["user"] == "user"
    assert result["host"] == "host.com"
    assert result["port"] == 3000


def test_normalize_endpoint_variants() -> None:
    """Test endpoint normalization with various formats."""
    from novita.api.resources.gpu.instances import _normalize_endpoint

    # TCP scheme
    host, port = _normalize_endpoint("tcp://example.com:2222")
    assert host == "example.com"
    assert port == 2222

    # HTTP scheme
    host, port = _normalize_endpoint("http://api.example.com:8080")
    assert host == "api.example.com"
    assert port == 8080

    # Plain host:port
    host, port = _normalize_endpoint("192.168.1.100:22345")
    assert host == "192.168.1.100"
    assert port == 22345

    # IPv6 format
    host, port = _normalize_endpoint("tcp://[2001:db8::1]:2222")
    assert host == "2001:db8::1"
    assert port == 2222

    # No port
    host, port = _normalize_endpoint("example.com")
    assert host == "example.com"
    assert port is None
