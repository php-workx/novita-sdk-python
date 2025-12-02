"""Base classes for GPU API resources."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx

# Base path for all GPU instance API endpoints
BASE_PATH = "/gpu-instance/openapi/v1"


class BaseResource:
    """Base class for synchronous GPU API resources."""

    def __init__(self, client: "httpx.Client") -> None:
        """Initialize the resource.

        Args:
            client: The httpx client instance
        """
        self._client = client


class AsyncBaseResource:
    """Base class for asynchronous GPU API resources."""

    def __init__(self, client: "httpx.AsyncClient") -> None:
        """Initialize the async resource.

        Args:
            client: The httpx async client instance
        """
        self._client = client
