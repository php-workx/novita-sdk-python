"""GPU storages management resource."""

from __future__ import annotations

from novita.generated.models import (
    CreateNetworkStorageRequest,
    ListNetworkStoragesResponse,
    NetworkStorageModel,
    UpdateNetworkStorageRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class Storages(BaseResource):
    """Synchronous GPU storages management resource."""

    def list(self) -> list[NetworkStorageModel]:
        """List all network storages.

        Returns:
            List of network storage objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/networkstorages/list")
        parsed = ListNetworkStoragesResponse.model_validate(response.json())
        return parsed.data or []

    def create(self, request: CreateNetworkStorageRequest) -> NetworkStorageModel:
        """Create a new network storage.

        Args:
            request: Network storage creation parameters

        Returns:
            Created network storage information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/networkstorage/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return NetworkStorageModel.model_validate(response.json())

    def update(self, request: UpdateNetworkStorageRequest) -> NetworkStorageModel:
        """Update a network storage.

        Args:
            request: Network storage update parameters (includes storage_id)

        Returns:
            Updated network storage information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/networkstorage/update",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return NetworkStorageModel.model_validate(response.json())

    def delete(self, storage_id: str) -> None:
        """Delete a network storage.

        Args:
            storage_id: The ID of the storage

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/networkstorage/delete", json={"storageId": storage_id})


class AsyncStorages(AsyncBaseResource):
    """Asynchronous GPU storages management resource."""

    async def list(self) -> list[NetworkStorageModel]:
        """List all network storages.

        Returns:
            List of network storage objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/networkstorages/list")
        parsed = ListNetworkStoragesResponse.model_validate(response.json())
        return parsed.data or []

    async def create(self, request: CreateNetworkStorageRequest) -> NetworkStorageModel:
        """Create a new network storage.

        Args:
            request: Network storage creation parameters

        Returns:
            Created network storage information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/networkstorage/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return NetworkStorageModel.model_validate(response.json())

    async def update(self, request: UpdateNetworkStorageRequest) -> NetworkStorageModel:
        """Update a network storage.

        Args:
            request: Network storage update parameters (includes storage_id)

        Returns:
            Updated network storage information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/networkstorage/update",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return NetworkStorageModel.model_validate(response.json())

    async def delete(self, storage_id: str) -> None:
        """Delete a network storage.

        Args:
            storage_id: The ID of the storage

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(
            f"{BASE_PATH}/networkstorage/delete", json={"storageId": storage_id}
        )
