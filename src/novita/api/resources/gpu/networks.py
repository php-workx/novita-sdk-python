"""GPU networks management resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from novita.generated.models import ListNetworksResponse, Network, NetworkModel

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


def _parse_single_network(payload: Any) -> Network:
    """Parse a single network from API response."""
    raw = payload.get("network", payload) if isinstance(payload, dict) else payload
    # Handle case where API returns a list with single item
    if isinstance(raw, list):
        if len(raw) == 0:
            raise ValueError("Expected a network object but received empty list")
        raw = raw[0]
    return Network.model_validate(raw)


class Networks(BaseResource):
    """Synchronous GPU networks management resource."""

    def list(self) -> list[NetworkModel]:
        """List all VPC networks.

        Returns:
            List of network objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/networks")
        parsed = ListNetworksResponse.model_validate(response.json())
        return parsed.network

    def get(self, network_id: str) -> Network:
        """Get details of a specific network.

        Args:
            network_id: The ID of the network

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/network", params={"network_id": network_id})
        return _parse_single_network(response.json())

    def create(self, **kwargs: Any) -> Network:
        """Create a new VPC network.

        Args:
            **kwargs: Network creation parameters (e.g., name)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/network/create", json=kwargs)
        return _parse_single_network(response.json())

    def update(self, network_id: str, **kwargs: Any) -> Network:
        """Update a VPC network.

        Args:
            network_id: The ID of the network
            **kwargs: Fields to update (e.g., name)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"network_id": network_id, **kwargs}
        response = self._client.post(f"{BASE_PATH}/network/update", json=data)
        return _parse_single_network(response.json())

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

    async def list(self) -> list[NetworkModel]:
        """List all VPC networks.

        Returns:
            List of network objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/networks")
        parsed = ListNetworksResponse.model_validate(response.json())
        return parsed.network

    async def get(self, network_id: str) -> Network:
        """Get details of a specific network.

        Args:
            network_id: The ID of the network

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/network", params={"network_id": network_id})
        return _parse_single_network(response.json())

    async def create(self, **kwargs: Any) -> Network:
        """Create a new VPC network.

        Args:
            **kwargs: Network creation parameters (e.g., name)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/network/create", json=kwargs)
        return _parse_single_network(response.json())

    async def update(self, network_id: str, **kwargs: Any) -> Network:
        """Update a VPC network.

        Args:
            network_id: The ID of the network
            **kwargs: Fields to update (e.g., name)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"network_id": network_id, **kwargs}
        response = await self._client.post(f"{BASE_PATH}/network/update", json=data)
        return _parse_single_network(response.json())

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
