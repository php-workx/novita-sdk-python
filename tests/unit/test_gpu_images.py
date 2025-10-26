"""Tests for image prewarming API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_image_prewarm_tasks(httpx_mock: HTTPXMock) -> None:
    """Test listing image prewarm tasks."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"tasks": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.images.list()

    assert "tasks" in response
    assert isinstance(response["tasks"], list)
    client.close()


def test_create_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test creating an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"task_id": "task-123", "status": "pending"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.images.create(image_url="docker.io/myimage:latest")

    assert response["task_id"] == "task-123"
    client.close()


def test_update_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test updating an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/edit",
        json={"task_id": "task-123", "status": "active"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.images.update("task-123", enabled=True)

    assert response["task_id"] == "task-123"
    client.close()


def test_delete_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test deleting an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.images.delete("task-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_get_image_prewarm_quota(httpx_mock: HTTPXMock) -> None:
    """Test getting image prewarm quota."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/quota",
        json={"quota": 10, "used": 3},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.images.get_quota()

    assert response["quota"] == 10
    assert response["used"] == 3
    client.close()


@pytest.mark.asyncio
async def test_async_list_image_prewarm_tasks(httpx_mock: HTTPXMock) -> None:
    """Test listing image prewarm tasks using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"tasks": [{"task_id": "task-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.images.list()

        assert len(response["tasks"]) == 1
