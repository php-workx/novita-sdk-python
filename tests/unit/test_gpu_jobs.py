"""Tests for jobs API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import JobModel


def _job_payload(**overrides: object) -> dict[str, object]:
    base = {
        "Id": "job-1",
        "user": "user-1",
        "type": "saveImage",
        "state": {"state": "running"},
        "createdAt": "1234567890",
        "instanceId": "inst-1",
    }
    base.update(overrides)
    model = JobModel.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def test_list_jobs(httpx_mock: HTTPXMock) -> None:
    """Test listing jobs."""
    mock_jobs = [
        _job_payload(Id="job-1", type="saveImage"),
        _job_payload(Id="job-2", type="instanceMigrate"),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/jobs",
        json={"jobs": mock_jobs, "total": len(mock_jobs)},
    )

    client = NovitaClient(api_key="test-key")
    jobs = client.gpu.jobs.list()

    assert isinstance(jobs, list)
    assert len(jobs) == 2
    assert isinstance(jobs[0], JobModel)
    assert jobs[0].id == "job-1"
    assert jobs[0].type.value == "saveImage"
    assert jobs[1].id == "job-2"
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
        json={"jobs": [_job_payload()], "total": 1},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        jobs = await client.gpu.jobs.list()

        assert isinstance(jobs, list)
        assert len(jobs) == 1
        assert jobs[0].id == "job-1"
        assert isinstance(jobs[0], JobModel)
