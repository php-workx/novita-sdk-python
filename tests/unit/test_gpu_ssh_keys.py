"""Tests for SSH keys management API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import AsyncNovitaClient, NovitaClient
from novita.generated.models import SSHKey


def test_list_ssh_keys(httpx_mock: HTTPXMock) -> None:
    """Test listing SSH keys."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-keys",
        json={
            "data": [
                {
                    "id": "key-123",
                    "name": "my-laptop",
                    "publicKey": "ssh-rsa AAAAB3NzaC1yc2EA...",
                    "createdAt": "2024-01-15T10:30:00Z",
                },
                {
                    "id": "key-456",
                    "name": "ci-server",
                    "publicKey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5...",
                    "createdAt": "2024-01-20T15:45:00Z",
                },
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    keys = client.gpu.ssh_keys.list()

    assert isinstance(keys, list)
    assert all(isinstance(key, SSHKey) for key in keys)
    assert len(keys) == 2
    assert keys[0].id == "key-123"
    assert keys[0].name == "my-laptop"
    assert keys[0].public_key == "ssh-rsa AAAAB3NzaC1yc2EA..."
    assert keys[1].id == "key-456"
    assert keys[1].name == "ci-server"

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    assert "Bearer test-key" in request_made.headers["authorization"]
    client.close()


def test_list_ssh_keys_empty(httpx_mock: HTTPXMock) -> None:
    """Test listing SSH keys when no keys exist."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-keys",
        json={"data": []},
    )

    client = NovitaClient(api_key="test-key")
    keys = client.gpu.ssh_keys.list()

    assert isinstance(keys, list)
    assert len(keys) == 0
    client.close()


def test_create_ssh_key(httpx_mock: HTTPXMock) -> None:
    """Test creating a new SSH key."""
    test_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... user@host"

    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-key/create",
        json={
            "id": "key-789",
            "name": "new-key",
            "publicKey": test_public_key,
            "createdAt": "2024-01-25T12:00:00Z",
        },
    )

    client = NovitaClient(api_key="test-key")
    key = client.gpu.ssh_keys.create(name="new-key", public_key=test_public_key)

    assert isinstance(key, SSHKey)
    assert key.id == "key-789"
    assert key.name == "new-key"
    assert key.public_key == test_public_key
    assert key.created_at == "2024-01-25T12:00:00Z"

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    assert "Bearer test-key" in request_made.headers["authorization"]

    # Verify request body
    import json

    request_body = json.loads(request_made.content)
    assert request_body["name"] == "new-key"
    assert request_body["publicKey"] == test_public_key
    client.close()


def test_delete_ssh_key(httpx_mock: HTTPXMock) -> None:
    """Test deleting an SSH key."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-key/delete",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    # Should not raise an exception
    client.gpu.ssh_keys.delete("key-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"

    # Verify request body
    import json

    request_body = json.loads(request_made.content)
    assert request_body["id"] == "key-123"
    client.close()


@pytest.mark.asyncio
async def test_async_list_ssh_keys(httpx_mock: HTTPXMock) -> None:
    """Test listing SSH keys using async client."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-keys",
        json={
            "data": [
                {
                    "id": "key-123",
                    "name": "my-laptop",
                    "publicKey": "ssh-rsa AAAAB3NzaC1yc2EA...",
                    "createdAt": "2024-01-15T10:30:00Z",
                }
            ]
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        keys = await client.gpu.ssh_keys.list()

        assert isinstance(keys, list)
        assert len(keys) == 1
        assert keys[0].id == "key-123"
        assert keys[0].name == "my-laptop"


@pytest.mark.asyncio
async def test_async_create_ssh_key(httpx_mock: HTTPXMock) -> None:
    """Test creating SSH key using async client."""
    test_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... user@host"

    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-key/create",
        json={
            "id": "key-999",
            "name": "async-key",
            "publicKey": test_public_key,
            "createdAt": "2024-01-26T08:00:00Z",
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        key = await client.gpu.ssh_keys.create(name="async-key", public_key=test_public_key)

        assert key.id == "key-999"
        assert key.name == "async-key"
        assert key.public_key == test_public_key


@pytest.mark.asyncio
async def test_async_delete_ssh_key(httpx_mock: HTTPXMock) -> None:
    """Test deleting SSH key using async client."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/ssh-key/delete",
        json={},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        # Should not raise an exception
        await client.gpu.ssh_keys.delete("key-456")
