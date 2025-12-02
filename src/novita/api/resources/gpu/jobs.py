"""GPU jobs management resource."""

from __future__ import annotations

from novita.generated.models import JobModel, ListJobsResponse

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class Jobs(BaseResource):
    """Synchronous GPU jobs management resource."""

    def list(self) -> list[JobModel]:
        """List all jobs.

        Returns:
            List of job objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/jobs")
        parsed = ListJobsResponse.model_validate(response.json())
        return parsed.jobs

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

    async def list(self) -> list[JobModel]:
        """List all jobs.

        Returns:
            List of job objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/jobs")
        parsed = ListJobsResponse.model_validate(response.json())
        return parsed.jobs

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
