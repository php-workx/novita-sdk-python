"""Core client implementation for the Novita SDK."""

import os
from typing import Any

import httpx

from novita.api.gpu import AsyncGpuClient, GpuClient
from novita.exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
)

DEFAULT_BASE_URL = "https://api.novita.ai"
DEFAULT_TIMEOUT = 60.0


def _handle_error_response(response: httpx.Response) -> None:
    """Handle error responses from the API (synchronous version).

    Args:
        response: The HTTP response

    Raises:
        AuthenticationError: For 401 status codes
        BadRequestError: For 400 status codes
        NotFoundError: For 404 status codes
        RateLimitError: For 429 status codes
        APIError: For other error status codes
    """
    # Read the response to avoid streaming issues
    response.read()

    if response.status_code == 401:
        raise AuthenticationError("Authentication failed. Check your API key.")
    elif response.status_code == 400:
        try:
            error_data = response.json()
            raise BadRequestError(
                f"Bad request: {error_data.get('message', 'Invalid parameters')}",
                details=error_data,
            )
        except ValueError:
            raise BadRequestError("Bad request. Check your request parameters.") from None
    elif response.status_code == 404:
        raise NotFoundError(f"Resource not found: {response.url}")
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded. Please retry later.")
    elif response.status_code >= 500:
        raise APIError(
            f"Server error ({response.status_code})",
            status_code=response.status_code,
            response_body=response.text,
        )
    else:
        raise APIError(
            f"API error ({response.status_code})",
            status_code=response.status_code,
            response_body=response.text,
        )


async def _handle_error_response_async(response: httpx.Response) -> None:
    """Handle error responses from the API (asynchronous version).

    Args:
        response: The HTTP response

    Raises:
        AuthenticationError: For 401 status codes
        BadRequestError: For 400 status codes
        NotFoundError: For 404 status codes
        RateLimitError: For 429 status codes
        APIError: For other error status codes
    """
    # Read the response to avoid streaming issues (async version)
    await response.aread()

    if response.status_code == 401:
        raise AuthenticationError("Authentication failed. Check your API key.")
    elif response.status_code == 400:
        try:
            error_data = response.json()
            raise BadRequestError(
                f"Bad request: {error_data.get('message', 'Invalid parameters')}",
                details=error_data,
            )
        except ValueError:
            raise BadRequestError("Bad request. Check your request parameters.") from None
    elif response.status_code == 404:
        raise NotFoundError(f"Resource not found: {response.url}")
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded. Please retry later.")
    elif response.status_code >= 500:
        raise APIError(
            f"Server error ({response.status_code})",
            status_code=response.status_code,
            response_body=response.text,
        )
    else:
        raise APIError(
            f"API error ({response.status_code})",
            status_code=response.status_code,
            response_body=response.text,
        )


class NovitaClient:
    """Synchronous client for the Novita AI API."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the Novita client.

        Args:
            api_key: API key for authentication. If not provided, will look for NOVITA_API_KEY env var
            base_url: Base URL for the API. Defaults to https://api.novita.ai
            timeout: Request timeout in seconds

        Raises:
            AuthenticationError: If no API key is provided or found in environment
        """
        # Get API key from parameter or environment
        self._api_key = api_key or os.getenv("NOVITA_API_KEY")
        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key parameter or set NOVITA_API_KEY environment variable."
            )

        self._base_url = base_url or DEFAULT_BASE_URL
        self._timeout = timeout

        # Create httpx client with authentication
        self._http_client = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=timeout,
            event_hooks={"response": [self._handle_response]},
        )

        # Initialize API resources
        self.gpu = GpuClient(self._http_client)

    def _handle_response(self, response: httpx.Response) -> None:
        """Handle HTTP responses and raise appropriate exceptions.

        Args:
            response: The HTTP response
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            _handle_error_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out after {self._timeout}s") from e

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()

    def __enter__(self) -> "NovitaClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()


class AsyncNovitaClient:
    """Asynchronous client for the Novita AI API."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the async Novita client.

        Args:
            api_key: API key for authentication. If not provided, will look for NOVITA_API_KEY env var
            base_url: Base URL for the API. Defaults to https://api.novita.ai
            timeout: Request timeout in seconds

        Raises:
            AuthenticationError: If no API key is provided or found in environment
        """
        # Get API key from parameter or environment
        self._api_key = api_key or os.getenv("NOVITA_API_KEY")
        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key parameter or set NOVITA_API_KEY environment variable."
            )

        self._base_url = base_url or DEFAULT_BASE_URL
        self._timeout = timeout

        # Create httpx async client with authentication
        self._http_client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=timeout,
            event_hooks={"response": [self._handle_response]},
        )

        # Initialize API resources
        self.gpu = AsyncGpuClient(self._http_client)

    async def _handle_response(self, response: httpx.Response) -> None:
        """Handle HTTP responses and raise appropriate exceptions.

        Args:
            response: The HTTP response
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            await _handle_error_response_async(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out after {self._timeout}s") from e

    async def aclose(self) -> None:
        """Close the HTTP client."""
        await self._http_client.aclose()

    async def __aenter__(self) -> "AsyncNovitaClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.aclose()
