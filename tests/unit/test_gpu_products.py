"""Tests for GPU and CPU product listing API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient, RateLimitError
from novita.generated.models import CPUProduct, GPUProduct


def test_list_gpu_products(httpx_mock: HTTPXMock) -> None:
    """Test getting GPU product pricing information."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/products",
        json={
            "data": [
                {
                    "id": "gpu-a100-80gb",
                    "name": "A100 80GB",
                    "cpuPerGpu": 8,
                    "memoryPerGpu": 120,
                    "diskPerGpu": 100,
                    "availableDeploy": True,
                    "minRootFS": 20,
                    "maxRootFS": 1000,
                    "minLocalStorage": 0,
                    "maxLocalStorage": 500,
                    "regions": [],
                    "price": 350,
                    "monthlyPrice": [],
                    "billingMethods": ["onDemand"],
                    "spotPrice": "200",
                },
                {
                    "id": "gpu-a10",
                    "name": "A10",
                    "cpuPerGpu": 4,
                    "memoryPerGpu": 60,
                    "diskPerGpu": 50,
                    "availableDeploy": True,
                    "minRootFS": 20,
                    "maxRootFS": 500,
                    "minLocalStorage": 0,
                    "maxLocalStorage": 200,
                    "regions": [],
                    "price": 120,
                    "monthlyPrice": [],
                    "billingMethods": ["onDemand", "spot"],
                    "spotPrice": "80",
                },
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    products = client.gpu.products.list()

    assert isinstance(products, list)
    assert all(isinstance(product, GPUProduct) for product in products)
    assert len(products) == 2
    assert products[0].id == "gpu-a100-80gb"
    assert products[0].name == "A100 80GB"
    assert products[0].price == 350
    assert products[1].id == "gpu-a10"

    request_made = httpx_mock.get_request()
    assert request_made.method == "GET"
    assert "Bearer test-key" in request_made.headers["authorization"]
    client.close()


def test_list_cpu_products(httpx_mock: HTTPXMock) -> None:
    """Test getting CPU product pricing information."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/cpu/products",
        json={
            "data": [
                {
                    "id": "cpu-4-8",
                    "name": "CPU 4 cores 8GB",
                    "cpuNum": 4,
                    "memorySize": 8,
                    "rootfsSize": 50,
                    "localVolumeSize": 50,
                    "availableDeploy": True,
                    "price": 20,
                },
            ]
        },
    )

    client = NovitaClient(api_key="test-key")
    products = client.gpu.products.list_cpu()

    assert isinstance(products, list)
    assert all(isinstance(product, CPUProduct) for product in products)
    assert len(products) == 1
    assert products[0].id == "cpu-4-8"
    assert products[0].name == "CPU 4 cores 8GB"
    assert products[0].price == 20
    client.close()


def test_list_gpu_products_rate_limit(httpx_mock: HTTPXMock) -> None:
    """Test that 429 raises RateLimitError."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/products",
        status_code=429,
        json={"error": "Rate limit exceeded"},
    )

    client = NovitaClient(api_key="test-key")

    with pytest.raises(RateLimitError):
        client.gpu.products.list()

    client.close()


@pytest.mark.asyncio
async def test_async_list_gpu_products(httpx_mock: HTTPXMock) -> None:
    """Test listing GPU products using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/products",
        json={
            "data": [
                {
                    "id": "gpu-a100-80gb",
                    "name": "A100 80GB",
                    "cpuPerGpu": 8,
                    "memoryPerGpu": 120,
                    "diskPerGpu": 100,
                    "availableDeploy": True,
                    "minRootFS": 20,
                    "maxRootFS": 1000,
                    "minLocalStorage": 0,
                    "maxLocalStorage": 500,
                    "regions": [],
                    "price": 350,
                    "monthlyPrice": [],
                    "billingMethods": ["onDemand"],
                    "spotPrice": "200",
                },
            ]
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        products = await client.gpu.products.list()

        assert isinstance(products, list)
        assert all(isinstance(product, GPUProduct) for product in products)
        assert len(products) == 1
        assert products[0].id == "gpu-a100-80gb"
