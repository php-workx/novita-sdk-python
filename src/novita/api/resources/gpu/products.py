"""GPU products and pricing resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from novita.generated.models import (
    CPUProduct,
    GPUProduct,
    ListCPUProductsResponse,
    ListGPUProductsResponse,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Products(BaseResource):
    """Synchronous GPU products and pricing resource."""

    def list(self) -> list[GPUProduct]:
        """Get pricing information for GPU instance types.

        Returns:
            List of GPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/products")
        parsed = ListGPUProductsResponse.model_validate(response.json())
        return parsed.data

    def list_cpu(self) -> list[CPUProduct]:
        """Get pricing information for CPU instance types.

        Returns:
            List of CPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/cpu/products")
        parsed = ListCPUProductsResponse.model_validate(response.json())
        return parsed.data


class AsyncProducts(AsyncBaseResource):
    """Asynchronous GPU products and pricing resource."""

    async def list(self) -> list[GPUProduct]:
        """Get pricing information for GPU instance types.

        Returns:
            List of GPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/products")
        parsed = ListGPUProductsResponse.model_validate(response.json())
        return parsed.data

    async def list_cpu(self) -> list[CPUProduct]:
        """Get pricing information for CPU instance types.

        Returns:
            List of CPU product objects with pricing information

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/cpu/products")
        parsed = ListCPUProductsResponse.model_validate(response.json())
        return parsed.data
