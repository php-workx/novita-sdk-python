"""GPU jobs management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Jobs(BaseResource):
    """Synchronous GPU jobs management resource."""

    def list(self) -> dict[str, Any]:
        """List all jobs.

        Returns:
            List of jobs

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        # Placeholder implementation - endpoint not specified in requirements
        raise NotImplementedError("Jobs API endpoints not yet specified")


class AsyncJobs(AsyncBaseResource):
    """Asynchronous GPU jobs management resource."""

    async def list(self) -> dict[str, Any]:
        """List all jobs.

        Returns:
            List of jobs

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        # Placeholder implementation - endpoint not specified in requirements
        raise NotImplementedError("Jobs API endpoints not yet specified")