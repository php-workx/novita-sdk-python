"""GPU networks management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Networks(BaseResource):
    """Synchronous GPU networks management resource."""

    def list(self) -> dict[str, Any]:
        """List networks.

        Returns:
            List of networks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Networks API endpoints not yet specified")


class AsyncNetworks(AsyncBaseResource):
    """Asynchronous GPU networks management resource."""

    async def list(self) -> dict[str, Any]:
        """List networks.

        Returns:
            List of networks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Networks API endpoints not yet specified")
