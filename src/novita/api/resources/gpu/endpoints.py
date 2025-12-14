"""GPU endpoints management resource."""

from __future__ import annotations

from typing import Any, cast

from novita.generated.models import (
    CreateEndpointRequest,
    EndpointDetail,
    ListEndpointsResponse,
    UpdateEndpointRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


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
        return cast(dict[str, Any], response.json())

    def create(self, request: CreateEndpointRequest) -> EndpointDetail:
        """Create a new endpoint.

        Args:
            request: Endpoint creation parameters

        Returns:
            Created endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/endpoint/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return EndpointDetail.model_validate(response.json())

    def list(self) -> list[EndpointDetail]:
        """List all endpoints.

        Returns:
            List of endpoint objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/endpoints")
        parsed = ListEndpointsResponse.model_validate(response.json())
        return parsed.endpoints

    def get(self, endpoint_id: str) -> EndpointDetail:
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
        return EndpointDetail.model_validate(response.json())

    def update(self, endpoint_id: str, request: UpdateEndpointRequest) -> EndpointDetail:
        """Update an endpoint.

        Args:
            endpoint_id: The ID of the endpoint
            request: Endpoint update parameters

        Returns:
            Updated endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {
            "endpoint_id": endpoint_id,
            **request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        }
        response = self._client.post(f"{BASE_PATH}/endpoint/update", json=data)
        return EndpointDetail.model_validate(response.json())

    def delete(self, endpoint_id: str) -> None:
        """Delete an endpoint.

        Args:
            endpoint_id: The ID of the endpoint

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/endpoint/delete", json={"endpoint_id": endpoint_id})


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
        return cast(dict[str, Any], response.json())

    async def create(self, request: CreateEndpointRequest) -> EndpointDetail:
        """Create a new endpoint.

        Args:
            request: Endpoint creation parameters

        Returns:
            Created endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/endpoint/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return EndpointDetail.model_validate(response.json())

    async def list(self) -> list[EndpointDetail]:
        """List all endpoints.

        Returns:
            List of endpoint objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/endpoints")
        parsed = ListEndpointsResponse.model_validate(response.json())
        return parsed.endpoints

    async def get(self, endpoint_id: str) -> EndpointDetail:
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
        return EndpointDetail.model_validate(response.json())

    async def update(self, endpoint_id: str, request: UpdateEndpointRequest) -> EndpointDetail:
        """Update an endpoint.

        Args:
            endpoint_id: The ID of the endpoint
            request: Endpoint update parameters

        Returns:
            Updated endpoint information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {
            "endpoint_id": endpoint_id,
            **request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        }
        response = await self._client.post(f"{BASE_PATH}/endpoint/update", json=data)
        return EndpointDetail.model_validate(response.json())

    async def delete(self, endpoint_id: str) -> None:
        """Delete an endpoint.

        Args:
            endpoint_id: The ID of the endpoint

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If endpoint doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/endpoint/delete", json={"endpoint_id": endpoint_id})
