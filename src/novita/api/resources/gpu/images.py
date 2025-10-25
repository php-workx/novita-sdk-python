"""GPU images management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Images(BaseResource):
    """Synchronous GPU images management resource."""

    def list(self) -> dict[str, Any]:
        """List all available images.

        Returns:
            List of available images

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/images")
        return response.json()


class AsyncImages(AsyncBaseResource):
    """Asynchronous GPU images management resource."""

    async def list(self) -> dict[str, Any]:
        """List all available images.

        Returns:
            List of available images

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/images")
        return response.json()