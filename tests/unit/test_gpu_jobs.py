"""Tests for jobs API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_jobs(httpx_mock: HTTPXMock) -> None:
    """Test listing jobs."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/jobs",
        json={"jobs": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.jobs.list()

    assert "jobs" in response
    assert isinstance(response["jobs"], list)
    client.close()


def test_break_job(httpx_mock: HTTPXMock) -> None:
    """Test breaking/canceling a job."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/job/break",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.jobs.break_job("job-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


@pytest.mark.asyncio
async def test_async_list_jobs(httpx_mock: HTTPXMock) -> None:
    """Test listing jobs using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/jobs",
        json={"jobs": [{"job_id": "job-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.jobs.list()

        assert len(response["jobs"]) == 1
