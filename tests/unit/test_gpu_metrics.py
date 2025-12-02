"""Tests for metrics API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_get_instance_metrics(httpx_mock: HTTPXMock) -> None:
    """Test getting instance metrics."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/instance/metrics?instance_id=inst-123",
        json={
            "cpu_usage": 45.5,
            "memory_usage": 60.2,
            "gpu_usage": 85.0,
        },
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.metrics.get("inst-123")

    expected = {
        "cpu_usage": 45.5,
        "memory_usage": 60.2,
        "gpu_usage": 85.0,
    }

    assert response == expected
    client.close()


@pytest.mark.asyncio
async def test_async_get_instance_metrics(httpx_mock: HTTPXMock) -> None:
    """Test getting instance metrics using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/instance/metrics?instance_id=inst-123",
        json={
            "cpu_usage": 50.0,
            "memory_usage": 70.0,
            "gpu_usage": 90.0,
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.metrics.get("inst-123")

        expected = {
            "cpu_usage": 50.0,
            "memory_usage": 70.0,
            "gpu_usage": 90.0,
        }
        assert response == expected
