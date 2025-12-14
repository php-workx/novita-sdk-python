"""Tests for image prewarming API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import (
    CreateImagePrewarmRequest,
    CreateImagePrewarmResponse,
    ImagePrewarmTask,
    UpdateImagePrewarmRequest,
)


def _task_payload(**overrides: object) -> dict[str, object]:
    base = {
        "id": "task-1",
        "imageName": "demo",
        "imageUrl": "docker.io/test:latest",
        "clusterId": "cluster-1",
        "clusterName": "Cluster",
        "products": [{"productId": "prod-1", "productName": "GPU"}],
        "createTime": "1234567890",
        "state": "Pending",
    }
    base.update(overrides)
    model = ImagePrewarmTask.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def test_list_image_prewarm_tasks(httpx_mock: HTTPXMock) -> None:
    """Test listing image prewarm tasks."""
    mock_tasks = [
        _task_payload(id="task-1", imageName="demo-1", clusterId="cluster-1"),
        _task_payload(id="task-2", imageName="demo-2", clusterId="cluster-2"),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"data": mock_tasks, "total": len(mock_tasks)},
    )

    client = NovitaClient(api_key="test-key")
    tasks = client.gpu.image_prewarm.list()

    assert isinstance(tasks, list)
    assert len(tasks) == 2
    assert isinstance(tasks[0], ImagePrewarmTask)
    assert tasks[0].id == "task-1"
    assert tasks[0].image_name == "demo-1"
    assert tasks[1].id == "task-2"
    client.close()


def test_create_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test creating an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"id": "task-123"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.image_prewarm.create(
        CreateImagePrewarmRequest(
            image_url="docker.io/myimage:latest",
            cluster_id="cluster-1",
        )
    )

    assert isinstance(response, CreateImagePrewarmResponse)
    assert response.id == "task-123"
    client.close()


def test_update_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test updating an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/edit",
        json=_task_payload(id="task-123", imageName="demo-2"),
    )

    client = NovitaClient(api_key="test-key")
    task = client.gpu.image_prewarm.update(
        "task-123",
        UpdateImagePrewarmRequest(
            id="task-123",
            note="Updated note",
        ),
    )

    assert isinstance(task, ImagePrewarmTask)
    assert task.id == "task-123"
    assert task.image_name == "demo-2"
    client.close()


def test_delete_image_prewarm(httpx_mock: HTTPXMock) -> None:
    """Test deleting an image prewarm task."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.image_prewarm.delete("task-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


def test_get_image_prewarm_quota(httpx_mock: HTTPXMock) -> None:
    """Test getting image prewarm quota."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm/quota",
        json={"total": 3, "limit": 10, "perImageSize": 50},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.image_prewarm.get_quota()

    assert response["limit"] == 10
    assert response["total"] == 3
    client.close()


@pytest.mark.asyncio
async def test_async_list_image_prewarm_tasks(httpx_mock: HTTPXMock) -> None:
    """Test listing image prewarm tasks using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/image/prewarm",
        json={"data": [_task_payload()], "total": 1},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        tasks = await client.gpu.image_prewarm.list()

        assert isinstance(tasks, list)
        assert len(tasks) == 1
        assert tasks[0].id == "task-1"
        assert isinstance(tasks[0], ImagePrewarmTask)
