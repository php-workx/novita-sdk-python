"""Tests for the Novita client."""

import os
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from novita import (
    APIError,
    AsyncNovitaClient,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    NovitaClient,
    RateLimitError,
)


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


def test_sync_error_handling_401() -> None:
    """Test that sync client properly handles 401 errors."""
    client = NovitaClient(api_key="test-key")

    # Create a mock response with 401 status
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 401
    mock_response.read = Mock()  # Synchronous read
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("401", request=Mock(), response=mock_response)
    )

    with pytest.raises(AuthenticationError, match="Authentication failed"):
        client._handle_response(mock_response)

    # Verify read() was called (sync version)
    mock_response.read.assert_called_once()
    client.close()


def test_sync_error_handling_400() -> None:
    """Test that sync client properly handles 400 errors."""
    client = NovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.read = Mock()
    mock_response.json = Mock(return_value={"message": "Invalid input"})
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("400", request=Mock(), response=mock_response)
    )

    with pytest.raises(BadRequestError, match="Invalid input"):
        client._handle_response(mock_response)

    mock_response.read.assert_called_once()
    client.close()


def test_sync_error_handling_404() -> None:
    """Test that sync client properly handles 404 errors."""
    client = NovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.read = Mock()
    mock_response.url = "https://api.novita.ai/test"
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("404", request=Mock(), response=mock_response)
    )

    with pytest.raises(NotFoundError, match="Resource not found"):
        client._handle_response(mock_response)

    mock_response.read.assert_called_once()
    client.close()


def test_sync_error_handling_429() -> None:
    """Test that sync client properly handles 429 errors."""
    client = NovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 429
    mock_response.read = Mock()
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("429", request=Mock(), response=mock_response)
    )

    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        client._handle_response(mock_response)

    mock_response.read.assert_called_once()
    client.close()


def test_sync_error_handling_500() -> None:
    """Test that sync client properly handles 500 errors."""
    client = NovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.read = Mock()
    mock_response.text = "Internal server error"
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("500", request=Mock(), response=mock_response)
    )

    with pytest.raises(APIError, match="Server error"):
        client._handle_response(mock_response)

    mock_response.read.assert_called_once()
    client.close()


@pytest.mark.asyncio
async def test_async_error_handling_401() -> None:
    """Test that async client properly handles 401 errors with async read."""
    client = AsyncNovitaClient(api_key="test-key")

    # Create a mock response with 401 status
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 401
    mock_response.aread = AsyncMock()  # Async read
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("401", request=Mock(), response=mock_response)
    )

    with pytest.raises(AuthenticationError, match="Authentication failed"):
        await client._handle_response(mock_response)

    # Verify aread() was called (async version)
    mock_response.aread.assert_awaited_once()
    await client.aclose()


@pytest.mark.asyncio
async def test_async_error_handling_400() -> None:
    """Test that async client properly handles 400 errors with async read."""
    client = AsyncNovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.aread = AsyncMock()
    mock_response.json = Mock(return_value={"message": "Invalid parameters"})
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("400", request=Mock(), response=mock_response)
    )

    with pytest.raises(BadRequestError, match="Invalid parameters"):
        await client._handle_response(mock_response)

    mock_response.aread.assert_awaited_once()
    await client.aclose()


@pytest.mark.asyncio
async def test_async_error_handling_404() -> None:
    """Test that async client properly handles 404 errors with async read."""
    client = AsyncNovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.aread = AsyncMock()
    mock_response.url = "https://api.novita.ai/test"
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("404", request=Mock(), response=mock_response)
    )

    with pytest.raises(NotFoundError, match="Resource not found"):
        await client._handle_response(mock_response)

    mock_response.aread.assert_awaited_once()
    await client.aclose()


@pytest.mark.asyncio
async def test_async_error_handling_429() -> None:
    """Test that async client properly handles 429 errors with async read."""
    client = AsyncNovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 429
    mock_response.aread = AsyncMock()
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("429", request=Mock(), response=mock_response)
    )

    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        await client._handle_response(mock_response)

    mock_response.aread.assert_awaited_once()
    await client.aclose()


@pytest.mark.asyncio
async def test_async_error_handling_500() -> None:
    """Test that async client properly handles 500 errors with async read."""
    client = AsyncNovitaClient(api_key="test-key")

    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.aread = AsyncMock()
    mock_response.text = "Internal server error"
    mock_response.raise_for_status = Mock(
        side_effect=httpx.HTTPStatusError("500", request=Mock(), response=mock_response)
    )

    with pytest.raises(APIError, match="Server error"):
        await client._handle_response(mock_response)

    mock_response.aread.assert_awaited_once()
    await client.aclose()
