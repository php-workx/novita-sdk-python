"""GPU clusters management resource."""

from collections.abc import Iterable
from typing import Any

from novita.generated.models import Cluster

from .base import BASE_PATH, AsyncBaseResource, BaseResource


def _parse_clusters(payload: Any) -> list[Cluster]:
    """Normalize API payloads into a list of Cluster models."""
    items: Iterable[Any]
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            items = data
        elif data is None:
            items = []
        else:
            items = [data]
    elif isinstance(payload, list):
        items = payload
    else:
        items = [payload]
    return [Cluster.model_validate(item) for item in items]


class Clusters(BaseResource):
    """Synchronous GPU clusters management resource."""

    def list(self) -> list[Cluster]:
        """List all available GPU clusters.

        Returns:
            List of available clusters

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/clusters")
        return _parse_clusters(response.json())


class AsyncClusters(AsyncBaseResource):
    """Asynchronous GPU clusters management resource."""

    async def list(self) -> list[Cluster]:
        """List all available GPU clusters.

        Returns:
            List of available clusters

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/clusters")
        return _parse_clusters(response.json())
