"""Tests for the Novita client."""

import os

import pytest

from novita import AsyncNovitaClient, AuthenticationError, NovitaClient


def test_client_requires_api_key() -> None:
    """Test that client raises error without API key."""
    # Clear environment variable if it exists
    old_key = os.environ.pop("NOVITA_API_KEY", None)

    try:
        with pytest.raises(AuthenticationError, match="No API key provided"):
            NovitaClient()
    finally:
        # Restore environment variable if it existed
        if old_key:
            os.environ["NOVITA_API_KEY"] = old_key


def test_client_accepts_api_key_parameter() -> None:
    """Test that client can be initialized with API key parameter."""
    client = NovitaClient(api_key="test-key-123")
    assert client._api_key == "test-key-123"
    assert "Bearer test-key-123" in client._http_client.headers["Authorization"]
    client.close()


def test_client_reads_env_variable() -> None:
    """Test that client reads API key from environment."""
    os.environ["NOVITA_API_KEY"] = "env-key-456"

    try:
        client = NovitaClient()
        assert client._api_key == "env-key-456"
        client.close()
    finally:
        os.environ.pop("NOVITA_API_KEY", None)


def test_client_has_gpu_resource() -> None:
    """Test that client has GPU resource available."""
    client = NovitaClient(api_key="test-key")
    assert hasattr(client, "gpu")
    assert client.gpu is not None
    client.close()


def test_client_context_manager() -> None:
    """Test that client works as context manager."""
    with NovitaClient(api_key="test-key") as client:
        assert client._api_key == "test-key"
    # Client should be closed after exiting context


def test_async_client_requires_api_key() -> None:
    """Test that async client raises error without API key."""
    old_key = os.environ.pop("NOVITA_API_KEY", None)

    try:
        with pytest.raises(AuthenticationError, match="No API key provided"):
            AsyncNovitaClient()
    finally:
        if old_key:
            os.environ["NOVITA_API_KEY"] = old_key


def test_async_client_accepts_api_key() -> None:
    """Test that async client can be initialized with API key."""
    client = AsyncNovitaClient(api_key="test-key-async")
    assert client._api_key == "test-key-async"
    assert "Bearer test-key-async" in client._http_client.headers["Authorization"]


@pytest.mark.asyncio
async def test_async_client_context_manager() -> None:
    """Test that async client works as async context manager."""
    async with AsyncNovitaClient(api_key="test-key") as client:
        assert client._api_key == "test-key"
    # Client should be closed after exiting context
