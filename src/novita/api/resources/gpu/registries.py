"""GPU registries management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Registries(BaseResource):
    """Synchronous GPU registries management resource."""

    def list(self) -> dict[str, Any]:
        """List registries.

        Returns:
            List of registries

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Registries API endpoints not yet specified")


class AsyncRegistries(AsyncBaseResource):
    """Asynchronous GPU registries management resource."""

    async def list(self) -> dict[str, Any]:
        """List registries.

        Returns:
            List of registries

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Registries API endpoints not yet specified")