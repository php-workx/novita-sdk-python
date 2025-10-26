"""Tests for repository authentication API."""

import pytest
from pydantic import SecretStr
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import RepositoryAuth


def test_list_repository_auths(httpx_mock: HTTPXMock) -> None:
    """Test listing repository authentications."""
    mock_data = [
        {"id": "auth-1", "name": "docker.io", "username": "user1", "password": "password1"},
        {"id": "auth-2", "name": "ghcr.io", "username": "user2", "password": "password2"},
        {"id": "auth-3", "name": "quay.io", "username": "user3", "password": "password3"},
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auths",
        json={"data": mock_data},
    )

    client = NovitaClient(api_key="test-key")
    auths = client.gpu.registries.list()

    assert isinstance(auths, list)
    assert len(auths) == 3
    
    for i, expected_item in enumerate(mock_data):
        auth = auths[i]
        assert isinstance(auth, RepositoryAuth)
        assert auth.id == expected_item["id"]
        assert auth.name == expected_item["name"]
        assert auth.username == expected_item["username"]
        # Password is returned as SecretStr, so we need to get the secret value
        assert isinstance(auth.password, SecretStr)
        assert auth.password.get_secret_value() == expected_item["password"]
    
    client.close()


def test_create_repository_auth(httpx_mock: HTTPXMock) -> None:
    """Test creating a repository authentication."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/save",
        status_code=204,
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.registries.create(name="docker.io", username="user", password="pass")

    assert response is None
    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_delete_repository_auth(httpx_mock: HTTPXMock) -> None:
    """Test deleting a repository authentication."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/delete",
        status_code=204,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.registries.delete("auth-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_password_not_exposed_in_repr() -> None:
    """Test that passwords are not exposed in string representation."""
    from novita.generated.models import CreateRepositoryAuthRequest

    request = CreateRepositoryAuthRequest(
        name="docker.io",
        username="testuser",
        password=SecretStr("super-secret-password"),
    )

    # Verify password is not exposed in repr
    repr_str = repr(request)
    assert "super-secret-password" not in repr_str
    assert "**********" in repr_str or "SecretStr" in repr_str

    # Verify password is not exposed in str
    str_repr = str(request)
    assert "super-secret-password" not in str_repr

    # Verify password can still be accessed when needed
    assert request.password.get_secret_value() == "super-secret-password"


def test_create_accepts_plain_string_password(httpx_mock: HTTPXMock) -> None:
    """Test that create() accepts plain string passwords for convenience."""
    # Register two responses for the two create calls
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/save",
        status_code=204,
    )
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auth/save",
        status_code=204,
    )

    client = NovitaClient(api_key="test-key")
    # Should work with plain string
    client.gpu.registries.create(name="docker.io", username="user", password="plain-password")
    
    # Should also work with SecretStr
    client.gpu.registries.create(
        name="ghcr.io", username="user", password=SecretStr("secret-password")
    )

    client.close()


@pytest.mark.asyncio
async def test_async_list_repository_auths(httpx_mock: HTTPXMock) -> None:
    """Test listing repository auths using async client."""
    from novita import AsyncNovitaClient

    mock_data = [{"id": "auth-1", "name": "docker.io", "username": "user1", "password": "password1"}]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/repository/auths",
        json={"data": mock_data},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        auths = await client.gpu.registries.list()

        assert isinstance(auths, list)
        assert len(auths) == 1
        assert auths[0].id == mock_data[0]["id"]
        assert auths[0].name == mock_data[0]["name"]
        assert isinstance(auths[0].password, SecretStr)
