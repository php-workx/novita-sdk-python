"""Tests for GPU instance management API."""

from __future__ import annotations

import json

import pytest
from pytest_httpx import HTTPXMock

from novita import (
    AsyncNovitaClient,
    CreateInstanceRequest,
    EditInstanceRequest,
    InstanceInfo,
    NovitaClient,
    SaveImageRequest,
    UpgradeInstanceRequest,
)


def _instance_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": "inst-1",
        "name": "demo-instance",
        "clusterId": "cluster-1",
        "clusterName": "Cluster One",
        "status": "running",
        "imageUrl": "repo/image:latest",
        "imageAuthId": "auth-1",
        "command": "bash start.sh",
        "cpuNum": "8",
        "memory": "64",
        "gpuNum": "1",
        "portMappings": [{"port": 8080, "type": "tcp"}],
        "productId": "prod-1",
        "productName": "Standard GPU",
        "rootfsSize": 100,
        "volumeMounts": [
            {
                "type": "network",
                "size": "500",
                "id": "vol-1",
                "mountPath": "/data",
            }
        ],
        "billingMode": "onDemand",
        "endTime": "-1",
    }
    payload.update(overrides)
    return payload


def _last_request_json(httpx_mock: HTTPXMock) -> dict[str, object]:
    request = httpx_mock.get_request()
    body = request.content.decode() if request.content else "{}"
    return json.loads(body or "{}")


def test_create_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        json={"id": "inst-123"},
    )

    client = NovitaClient(api_key="test-key")
    request = CreateInstanceRequest(
        name="test",
        product_id="prod-1",
        gpu_num=1,
        rootfs_size=50,
        image_url="repo/demo:latest",
        kind="gpu",
    )

    response = client.gpu.instances.create(request)

    assert response.id == "inst-123"
    payload = _last_request_json(httpx_mock)
    assert payload["productId"] == "prod-1"
    client.close()


def test_list_instances(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances",
        json={"instances": [_instance_payload()], "total": 1},
    )

    client = NovitaClient(api_key="test-key")
    instances = client.gpu.instances.list()

    assert len(instances) == 1
    assert instances[0].cluster_id == "cluster-1"
    assert instances[0].status.value == "running"
    client.close()


def test_list_instances_with_filters(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url=(
            "https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances"
            "?pageSize=10&pageNum=2&name=demo&status=running"
        ),
        json={"instances": [_instance_payload(id="inst-filter")], "total": 1},
    )

    client = NovitaClient(api_key="test-key")
    instances = client.gpu.instances.list(page_size=10, page_num=2, name="demo", status="running")

    request = httpx_mock.get_request()
    assert request.url.params["pageSize"] == "10"
    assert request.url.params["name"] == "demo"
    assert len(instances) == 1
    assert instances[0].id == "inst-filter"
    client.close()


def test_get_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance?instanceId=inst-123",
        json=_instance_payload(id="inst-123"),
    )

    client = NovitaClient(api_key="test-key")
    instance = client.gpu.instances.get("inst-123")

    assert isinstance(instance, InstanceInfo)
    assert instance.id == "inst-123"
    assert instance.cluster_name == "Cluster One"
    client.close()


def test_edit_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/edit",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    request = EditInstanceRequest(
        instance_id="inst-123",
        ports=[{"port": 8080, "type": "tcp"}],
        expand_root_disk=100,
    )
    client.gpu.instances.edit(request)

    payload = _last_request_json(httpx_mock)
    assert payload["instanceId"] == "inst-123"
    assert payload["expandRootDisk"] == 100
    client.close()


def test_start_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/start",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.instances.start("inst-123")

    payload = _last_request_json(httpx_mock)
    assert payload == {"instanceId": "inst-123"}
    client.close()


def test_upgrade_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/upgrade",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    request = UpgradeInstanceRequest(
        instance_id="inst-123",
        image_url="repo/new:tag",
        envs=[{"key": "ENV", "value": "1"}],
        command="bash run.sh",
        save=True,
        network_volume={"volumeMounts": [{"type": "network", "id": "vol-1", "mountPath": "/data"}]},
    )
    client.gpu.instances.upgrade(request)

    payload = _last_request_json(httpx_mock)
    assert payload["instanceId"] == "inst-123"
    assert payload["networkVolume"]["volumeMounts"][0]["mountPath"] == "/data"
    client.close()


def test_migrate_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/migrate",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.instances.migrate("inst-123")

    assert _last_request_json(httpx_mock)["instanceId"] == "inst-123"
    client.close()


def test_renew_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/renewInstance",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.instances.renew("inst-123", month=3)

    payload = _last_request_json(httpx_mock)
    assert payload == {"instanceId": "inst-123", "month": 3}
    client.close()


def test_convert_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/transToMonthlyInstance",
        json={},
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.instances.convert_to_monthly("inst-123", month=1)

    payload = _last_request_json(httpx_mock)
    assert payload == {"instanceId": "inst-123", "month": 1}
    client.close()


def test_save_image(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/job/save/image",
        json={"jobId": "job-1"},
    )

    client = NovitaClient(api_key="test-key")
    job_id = client.gpu.instances.save_image(
        SaveImageRequest(instance_id="inst-123", image="repo/image:tag")
    )

    assert job_id == "job-1"
    client.close()


@pytest.mark.asyncio
async def test_async_create_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        json={"id": "inst-async"},
    )

    request = CreateInstanceRequest(
        product_id="prod-1",
        gpu_num=1,
        rootfs_size=50,
        image_url="repo/demo:latest",
        kind="gpu",
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.instances.create(request)
        assert response.id == "inst-async"


@pytest.mark.asyncio
async def test_async_list_instances(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instances?status=running",
        json={"instances": [_instance_payload()], "total": 1},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        instances = await client.gpu.instances.list(status="running")
        assert instances[0].status.value == "running"


@pytest.mark.asyncio
async def test_async_edit_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/edit",
        json={},
    )

    request = EditInstanceRequest(instance_id="inst-async", ports=[{"port": 8080, "type": "tcp"}])

    async with AsyncNovitaClient(api_key="test-key") as client:
        await client.gpu.instances.edit(request)
    assert _last_request_json(httpx_mock)["instanceId"] == "inst-async"
