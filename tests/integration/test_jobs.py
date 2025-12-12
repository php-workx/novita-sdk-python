"""Integration tests for job endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestJobs:
    """Test job-related endpoints."""

    def test_list_jobs(self, client: NovitaClient) -> None:
        """Test listing all jobs."""
        jobs = client.gpu.jobs.list()

        assert jobs is not None
        assert isinstance(jobs, list)

    def test_job_structure(self, client: NovitaClient) -> None:
        """Test that jobs have all expected fields."""
        jobs = client.gpu.jobs.list()

        if len(jobs) > 0:
            job = jobs[0]

            # Required fields
            assert hasattr(job, "id")
            assert hasattr(job, "type")
            assert hasattr(job, "status")

            # Verify data types
            assert isinstance(job.id, str)
            assert isinstance(job.type, str)
            assert isinstance(job.status, str)

    def test_jobs_have_valid_ids(self, client: NovitaClient) -> None:
        """Test that all jobs have non-empty IDs."""
        jobs = client.gpu.jobs.list()

        for job in jobs:
            assert job.id
            assert len(job.id) > 0
