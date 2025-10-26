"""GPU storages management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Storages(BaseResource):
    """Synchronous GPU storages management resource."""

    def list(self) -> dict[str, Any]:
        """List all network storages.

        Returns:
            List of network storages

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/networkstorages/list")
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
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
        return response.json()

    def update(self, storage_id: str, **kwargs: Any) -> dict[str, Any]:
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
        return response.json()

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

    async def list(self) -> dict[str, Any]:
        """List all network storages.

        Returns:
            List of network storages

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/networkstorages/list")
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
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
        return response.json()

    async def update(self, storage_id: str, **kwargs: Any) -> dict[str, Any]:
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
        return response.json()

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
