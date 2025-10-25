"""GPU clusters management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Clusters(BaseResource):
    """Synchronous GPU clusters management resource."""

    def list(self) -> list[dict[str, Any]]:
        """List all available GPU clusters.

        Returns:
            List of available clusters

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/clusters")
        return response.json()


class AsyncClusters(AsyncBaseResource):
    """Asynchronous GPU clusters management resource."""

    async def list(self) -> list[dict[str, Any]]:
        """List all available GPU clusters.

        Returns:
            List of available clusters

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/clusters")
        return response.json()