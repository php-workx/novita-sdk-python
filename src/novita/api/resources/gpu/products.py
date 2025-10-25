"""GPU products and pricing resource."""

from typing import TYPE_CHECKING

from novita.models import ListGPUProductsResponse

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    import httpx


class Products(BaseResource):
    """Synchronous GPU products and pricing resource."""

    def list(self) -> ListGPUProductsResponse:
        """Get pricing information for GPU instance types.

        Returns:
            Response containing pricing for each instance type

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/products")
        return ListGPUProductsResponse.model_validate(response.json())

    def list_cpu(self) -> ListGPUProductsResponse:
        """Get pricing information for CPU instance types.

        Returns:
            Response containing pricing for each instance type

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/cpu/products")
        return ListGPUProductsResponse.model_validate(response.json())


class AsyncProducts(AsyncBaseResource):
    """Asynchronous GPU products and pricing resource."""

    async def list(self) -> ListGPUProductsResponse:
        """Get pricing information for GPU instance types.

        Returns:
            Response containing pricing for each instance type

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/products")
        return ListGPUProductsResponse.model_validate(response.json())

    async def list_cpu(self) -> ListGPUProductsResponse:
        """Get pricing information for CPU instance types.

        Returns:
            Response containing pricing for each instance type

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/cpu/products")
        return ListGPUProductsResponse.model_validate(response.json())
