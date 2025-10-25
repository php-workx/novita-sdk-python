"""GPU endpoints management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Endpoints(BaseResource):
    """Synchronous GPU endpoints management resource."""

    def get_limit_ranges(self) -> dict[str, Any]:
        """Get endpoint limit ranges.

        Returns:
            Endpoint limit range information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/endpoint/limit")
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new endpoint.

        Args:
            **kwargs: Endpoint creation parameters

        Returns:
            Created endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/endpoint/create", json=kwargs)
        return response.json()

    def list(self) -> dict[str, Any]:
        """List all endpoints.

        Returns:
            List of endpoints

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/endpoints")
        return response.json()

    def get(self, endpoint_id: str) -> dict[str, Any]:
        """Get details of a specific endpoint.

        Args:
            endpoint_id: The ID of the endpoint

        Returns:
            Detailed information about the endpoint

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/endpoint", params={"endpoint_id": endpoint_id})
        return response.json()


class AsyncEndpoints(AsyncBaseResource):
    """Asynchronous GPU endpoints management resource."""

    async def get_limit_ranges(self) -> dict[str, Any]:
        """Get endpoint limit ranges.

        Returns:
            Endpoint limit range information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/endpoint/limit")
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new endpoint.

        Args:
            **kwargs: Endpoint creation parameters

        Returns:
            Created endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/endpoint/create", json=kwargs)
        return response.json()

    async def list(self) -> dict[str, Any]:
        """List all endpoints.

        Returns:
            List of endpoints

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/endpoints")
        return response.json()

    async def get(self, endpoint_id: str) -> dict[str, Any]:
        """Get details of a specific endpoint.

        Args:
            endpoint_id: The ID of the endpoint

        Returns:
            Detailed information about the endpoint

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(
            f"{BASE_PATH}/endpoint", params={"endpoint_id": endpoint_id}
        )
        return response.json()
