"""GPU networks management resource."""

from __future__ import annotations

from typing import Any

from novita.exceptions import NotFoundError
from novita.generated.models import (
    CreateNetworkRequest,
    ListNetworksResponse,
    Network,
    NetworkModel,
    UpdateNetworkRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


def _parse_single_network(payload: Any) -> Network:
    """Parse a single network from API response.

    Args:
        payload: API response payload containing network data

    Returns:
        Network object

    Raises:
        NotFoundError: If the API returns an empty list (network not found)
    """
    raw = payload.get("network", payload) if isinstance(payload, dict) else payload
    # Handle case where API returns a list with single item
    if isinstance(raw, list):
        if len(raw) == 0:
            raise NotFoundError("Network not found")
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
        return parsed.networks

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
        response = self._client.get(f"{BASE_PATH}/network", params={"networkId": network_id})
        return _parse_single_network(response.json())

    def create(self, request: CreateNetworkRequest) -> Network:
        """Create a new VPC network.

        Args:
            request: Network creation parameters

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/network/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return _parse_single_network(response.json())

    def update(self, request: UpdateNetworkRequest) -> Network:
        """Update a VPC network.

        Args:
            request: Network update parameters (includes network_id)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/network/update",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
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
        self._client.post(f"{BASE_PATH}/network/delete", json={"networkId": network_id})


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
        return parsed.networks

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
        response = await self._client.get(f"{BASE_PATH}/network", params={"networkId": network_id})
        return _parse_single_network(response.json())

    async def create(self, request: CreateNetworkRequest) -> Network:
        """Create a new VPC network.

        Args:
            request: Network creation parameters

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/network/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return _parse_single_network(response.json())

    async def update(self, request: UpdateNetworkRequest) -> Network:
        """Update a VPC network.

        Args:
            request: Network update parameters (includes network_id)

        Returns:
            Network information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If network doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/network/update",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
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
        await self._client.post(f"{BASE_PATH}/network/delete", json={"networkId": network_id})
