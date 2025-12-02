"""GPU metrics management resource."""

from typing import Any, cast

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class Metrics(BaseResource):
    """Synchronous GPU metrics management resource."""

    def get(self, instance_id: str) -> dict[str, Any]:
        """Get metrics for a specific instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Instance metrics data

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(
            f"{BASE_PATH}/instance/metrics", params={"instance_id": instance_id}
        )
        return cast(dict[str, Any], response.json())


class AsyncMetrics(AsyncBaseResource):
    """Asynchronous GPU metrics management resource."""

    async def get(self, instance_id: str) -> dict[str, Any]:
        """Get metrics for a specific instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Instance metrics data

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(
            f"{BASE_PATH}/instance/metrics", params={"instance_id": instance_id}
        )
        return cast(dict[str, Any], response.json())
