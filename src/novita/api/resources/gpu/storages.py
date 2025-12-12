"""GPU storages management resource."""

from __future__ import annotations

from typing import Any

from novita.generated.models import ListNetworkStoragesResponse, NetworkStorageModel

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

    def create(self, **kwargs: Any) -> NetworkStorageModel:
        """Create a new network storage.

        Args:
            **kwargs: Network storage parameters (e.g., name, size)

        Returns:
            Created network storage information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/networkstorage/create", json=kwargs)
        return NetworkStorageModel.model_validate(response.json())

    def update(self, storage_id: str, **kwargs: Any) -> NetworkStorageModel:
        """Update a network storage.

        Args:
            storage_id: The ID of the storage
            **kwargs: Fields to update (e.g., name)

        Returns:
            Updated network storage information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"storage_id": storage_id, **kwargs}
        response = self._client.post(f"{BASE_PATH}/networkstorage/update", json=data)
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
        self._client.post(f"{BASE_PATH}/networkstorage/delete", json={"storage_id": storage_id})


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

    async def create(self, **kwargs: Any) -> NetworkStorageModel:
        """Create a new network storage.

        Args:
            **kwargs: Network storage parameters (e.g., name, size)

        Returns:
            Created network storage information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/networkstorage/create", json=kwargs)
        return NetworkStorageModel.model_validate(response.json())

    async def update(self, storage_id: str, **kwargs: Any) -> NetworkStorageModel:
        """Update a network storage.

        Args:
            storage_id: The ID of the storage
            **kwargs: Fields to update (e.g., name)

        Returns:
            Updated network storage information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If storage doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"storage_id": storage_id, **kwargs}
        response = await self._client.post(f"{BASE_PATH}/networkstorage/update", json=data)
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
            f"{BASE_PATH}/networkstorage/delete", json={"storage_id": storage_id}
        )
