"""GPU jobs management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


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
        response = self._client.get(f"{BASE_PATH}/jobs")
        return response.json()

    def break_job(self, job_id: str) -> None:
        """Break/cancel a job.

        Args:
            job_id: The ID of the job to break

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If job doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/job/break", json={"job_id": job_id})


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
        response = await self._client.get(f"{BASE_PATH}/jobs")
        return response.json()

    async def break_job(self, job_id: str) -> None:
        """Break/cancel a job.

        Args:
            job_id: The ID of the job to break

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If job doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/job/break", json={"job_id": job_id})
