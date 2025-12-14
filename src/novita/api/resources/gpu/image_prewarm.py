"""GPU image prewarm management resource."""

from __future__ import annotations

from typing import Any, cast

from novita.generated.models import (
    CreateImagePrewarmRequest,
    CreateImagePrewarmResponse,
    ImagePrewarmTask,
    ListImagePrewarmTasksResponse,
    UpdateImagePrewarmRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class ImagePrewarm(BaseResource):
    """Synchronous GPU image prewarm management resource."""

    def list(self) -> list[ImagePrewarmTask]:
        """List all image prewarm tasks.

        Returns:
            List of image prewarm task objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/image/prewarm")
        parsed = ListImagePrewarmTasksResponse.model_validate(response.json())
        return parsed.data

    def create(self, request: CreateImagePrewarmRequest) -> CreateImagePrewarmResponse:
        """Create a new image prewarm task.

        Args:
            request: Image prewarm task parameters

        Returns:
            Created image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/image/prewarm",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return CreateImagePrewarmResponse.model_validate(response.json())

    def update(self, task_id: str, request: UpdateImagePrewarmRequest) -> ImagePrewarmTask:
        """Update an image prewarm task.

        Args:
            task_id: The ID of the prewarm task
            request: Image prewarm task update parameters

        Returns:
            Updated image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {
            "task_id": task_id,
            **request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        }
        response = self._client.post(f"{BASE_PATH}/image/prewarm/edit", json=data)
        return ImagePrewarmTask.model_validate(response.json())

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
        return cast(dict[str, Any], response.json())


class AsyncImagePrewarm(AsyncBaseResource):
    """Asynchronous GPU image prewarm management resource."""

    async def list(self) -> list[ImagePrewarmTask]:
        """List all image prewarm tasks.

        Returns:
            List of image prewarm task objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/image/prewarm")
        parsed = ListImagePrewarmTasksResponse.model_validate(response.json())
        return parsed.data

    async def create(self, request: CreateImagePrewarmRequest) -> CreateImagePrewarmResponse:
        """Create a new image prewarm task.

        Args:
            request: Image prewarm task parameters

        Returns:
            Created image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/image/prewarm",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return CreateImagePrewarmResponse.model_validate(response.json())

    async def update(self, task_id: str, request: UpdateImagePrewarmRequest) -> ImagePrewarmTask:
        """Update an image prewarm task.

        Args:
            task_id: The ID of the prewarm task
            request: Image prewarm task update parameters

        Returns:
            Updated image prewarm task information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If task doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {
            "task_id": task_id,
            **request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        }
        response = await self._client.post(f"{BASE_PATH}/image/prewarm/edit", json=data)
        return ImagePrewarmTask.model_validate(response.json())

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
        return cast(dict[str, Any], response.json())
