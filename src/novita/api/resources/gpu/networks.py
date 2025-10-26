"""GPU networks management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Networks(BaseResource):
    """Synchronous GPU networks management resource."""

    def list(self) -> dict[str, Any]:
        """List all VPC networks.

        Returns:
            List of networks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/networks")
        return response.json()

    def get(self, network_id: str) -> dict[str, Any]:
        """Get details of a specific network.

        Args:
            network_id: The ID of the network

        Returns:
            Detailed information about the network

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/network", params={"network_id": network_id})
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new VPC network.

        Args:
            **kwargs: Network creation parameters (e.g., name)

        Returns:
            Created network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/network/create", json=kwargs)
        return response.json()

    def update(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a VPC network.

        Args:
            network_id: The ID of the network
            **kwargs: Fields to update (e.g., name)

        Returns:
            Updated network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"network_id": network_id, **kwargs}
        response = self._client.post(f"{BASE_PATH}/network/update", json=data)
        return response.json()

    def delete(self, network_id: str) -> None:
        """Delete a VPC network.

        Args:
            network_id: The ID of the network

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/network/delete", json={"network_id": network_id})


class AsyncNetworks(AsyncBaseResource):
    """Asynchronous GPU networks management resource."""

    async def list(self) -> dict[str, Any]:
        """List all VPC networks.

        Returns:
            List of networks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/networks")
        return response.json()

    async def get(self, network_id: str) -> dict[str, Any]:
        """Get details of a specific network.

        Args:
            network_id: The ID of the network

        Returns:
            Detailed information about the network

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/network", params={"network_id": network_id})
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new VPC network.

        Args:
            **kwargs: Network creation parameters (e.g., name)

        Returns:
            Created network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/network/create", json=kwargs)
        return response.json()

    async def update(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a VPC network.

        Args:
            network_id: The ID of the network
            **kwargs: Fields to update (e.g., name)

        Returns:
            Updated network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"network_id": network_id, **kwargs}
        response = await self._client.post(f"{BASE_PATH}/network/update", json=data)
        return response.json()

    async def delete(self, network_id: str) -> None:
        """Delete a VPC network.

        Args:
            network_id: The ID of the network

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/network/delete", json={"network_id": network_id})
