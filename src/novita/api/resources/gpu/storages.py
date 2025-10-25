"""GPU storages management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Storages(BaseResource):
    """Synchronous GPU storages management resource."""

    def list(self) -> dict[str, Any]:
        """List storages.

        Returns:
            List of storages

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Storages API endpoints not yet specified")


class AsyncStorages(AsyncBaseResource):
    """Asynchronous GPU storages management resource."""

    async def list(self) -> dict[str, Any]:
        """List storages.

        Returns:
            List of storages

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Storages API endpoints not yet specified")