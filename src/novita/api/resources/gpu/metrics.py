"""GPU metrics management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Metrics(BaseResource):
    """Synchronous GPU metrics management resource."""

    def list(self) -> dict[str, Any]:
        """List metrics data.

        Returns:
            Metrics data

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Metrics API endpoints not yet specified")


class AsyncMetrics(AsyncBaseResource):
    """Asynchronous GPU metrics management resource."""

    async def list(self) -> dict[str, Any]:
        """List metrics data.

        Returns:
            Metrics data

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Metrics API endpoints not yet specified")
