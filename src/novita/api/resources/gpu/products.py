"""GPU products and pricing resource."""

from __future__ import annotations

import builtins

from novita.generated.models import (
    CPUProduct,
    GPUProduct,
    ListCPUProductsResponse,
    ListGPUProductsResponse,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class Products(BaseResource):
    """Synchronous GPU products and pricing resource."""

    def list(
        self,
        *,
        cluster_id: str | None = None,
        gpu_num: int | None = None,
        product_name: str | None = None,
        billing_method: str | None = None,
    ) -> builtins.list[GPUProduct]:
        """Get pricing information for GPU instance types.

        Args:
            cluster_id: Filter by cluster
            gpu_num: Filter by GPU count
            product_name: Fuzzy matching on product names
            billing_method: Filter by billing method

        Returns:
            List of GPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        params: dict[str, str | int] = {}
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if gpu_num is not None:
            params["gpuNum"] = gpu_num
        if product_name is not None:
            params["productName"] = product_name
        if billing_method is not None:
            params["billingMethod"] = billing_method

        response = self._client.get(f"{BASE_PATH}/products", params=params or None)
        parsed = ListGPUProductsResponse.model_validate(response.json())
        return parsed.data

    def list_cpu(
        self,
        *,
        cluster_id: str | None = None,
        product_name: str | None = None,
    ) -> builtins.list[CPUProduct]:
        """Get pricing information for CPU instance types.

        Args:
            cluster_id: Filter by cluster identifier
            product_name: Fuzzy match filtering by product name

        Returns:
            List of CPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        params: dict[str, str] = {}
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if product_name is not None:
            params["productName"] = product_name

        response = self._client.get(f"{BASE_PATH}/cpu/products", params=params or None)
        parsed = ListCPUProductsResponse.model_validate(response.json())
        return parsed.data


class AsyncProducts(AsyncBaseResource):
    """Asynchronous GPU products and pricing resource."""

    async def list(
        self,
        *,
        cluster_id: str | None = None,
        gpu_num: int | None = None,
        product_name: str | None = None,
        billing_method: str | None = None,
    ) -> builtins.list[GPUProduct]:
        """Get pricing information for GPU instance types.

        Args:
            cluster_id: Filter by cluster
            gpu_num: Filter by GPU count
            product_name: Fuzzy matching on product names
            billing_method: Filter by billing method

        Returns:
            List of GPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        params: dict[str, str | int] = {}
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if gpu_num is not None:
            params["gpuNum"] = gpu_num
        if product_name is not None:
            params["productName"] = product_name
        if billing_method is not None:
            params["billingMethod"] = billing_method

        response = await self._client.get(f"{BASE_PATH}/products", params=params or None)
        parsed = ListGPUProductsResponse.model_validate(response.json())
        return parsed.data

    async def list_cpu(
        self,
        *,
        cluster_id: str | None = None,
        product_name: str | None = None,
    ) -> builtins.list[CPUProduct]:
        """Get pricing information for CPU instance types.

        Args:
            cluster_id: Filter by cluster identifier
            product_name: Fuzzy match filtering by product name

        Returns:
            List of CPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        params: dict[str, str] = {}
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if product_name is not None:
            params["productName"] = product_name

        response = await self._client.get(f"{BASE_PATH}/cpu/products", params=params or None)
        parsed = ListCPUProductsResponse.model_validate(response.json())
        return parsed.data
