"""Tests for repository authentication API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_repository_auths(httpx_mock: HTTPXMock) -> None:
    """Test listing repository authentications."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auths",
        json={"auths": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.registries.list()

    assert "auths" in response
    assert isinstance(response["auths"], list)
    client.close()


def test_create_repository_auth(httpx_mock: HTTPXMock) -> None:
    """Test creating a repository authentication."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/save",
        json={"auth_id": "auth-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.registries.create(registry="docker.io", username="user", password="pass")

    assert response["auth_id"] == "auth-123"
    client.close()


def test_delete_repository_auth(httpx_mock: HTTPXMock) -> None:
    """Test deleting a repository authentication."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.registries.delete("auth-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


@pytest.mark.asyncio
async def test_async_list_repository_auths(httpx_mock: HTTPXMock) -> None:
    """Test listing repository auths using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auths",
        json={"auths": [{"auth_id": "auth-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.registries.list()

        assert len(response["auths"]) == 1
