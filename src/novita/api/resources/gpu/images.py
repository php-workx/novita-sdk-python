"""GPU images management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Images(BaseResource):
    """Synchronous GPU images management resource."""

    def list(self) -> dict[str, Any]:
        """List all image prewarm tasks.

        Returns:
            List of image prewarm tasks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/image/prewarm")
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new image prewarm task.

        Args:
            **kwargs: Image prewarm task parameters (e.g., image_url)

        Returns:
            Created image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/image/prewarm", json=kwargs)
        return response.json()

    def update(self, task_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an image prewarm task.

        Args:
            task_id: The ID of the prewarm task
            **kwargs: Fields to update (e.g., enabled)

        Returns:
            Updated image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"task_id": task_id, **kwargs}
        response = self._client.post(f"{BASE_PATH}/image/prewarm/edit", json=data)
        return response.json()

    def delete(self, task_id: str) -> None:
        """Delete an image prewarm task.

        Args:
            task_id: The ID of the prewarm task

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/image/prewarm/delete", json={"task_id": task_id})

    def get_quota(self) -> dict[str, Any]:
        """Get image prewarm quota information.

        Returns:
            Quota information for image prewarming

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/image/prewarm/quota")
        return response.json()


class AsyncImages(AsyncBaseResource):
    """Asynchronous GPU images management resource."""

    async def list(self) -> dict[str, Any]:
        """List all image prewarm tasks.

        Returns:
            List of image prewarm tasks

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/image/prewarm")
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new image prewarm task.

        Args:
            **kwargs: Image prewarm task parameters (e.g., image_url)

        Returns:
            Created image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/image/prewarm", json=kwargs)
        return response.json()

    async def update(self, task_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an image prewarm task.

        Args:
            task_id: The ID of the prewarm task
            **kwargs: Fields to update (e.g., enabled)

        Returns:
            Updated image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"task_id": task_id, **kwargs}
        response = await self._client.post(f"{BASE_PATH}/image/prewarm/edit", json=data)
        return response.json()

    async def delete(self, task_id: str) -> None:
        """Delete an image prewarm task.

        Args:
            task_id: The ID of the prewarm task

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/image/prewarm/delete", json={"task_id": task_id})

    async def get_quota(self) -> dict[str, Any]:
        """Get image prewarm quota information.

        Returns:
            Quota information for image prewarming

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/image/prewarm/quota")
        return response.json()
