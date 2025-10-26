"""GPU templates management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Templates(BaseResource):
    """Synchronous GPU templates management resource."""

    def list(self) -> dict[str, Any]:
        """List all templates.

        Returns:
            List of templates

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/templates")
        return response.json()

    def get(self, template_id: str) -> dict[str, Any]:
        """Get details of a specific template.

        Args:
            template_id: The ID of the template

        Returns:
            Detailed information about the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/template", params={"template_id": template_id})
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new template.

        Args:
            **kwargs: Template creation parameters (e.g., name, instance_id)

        Returns:
            Created template information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/template/create", json=kwargs)
        return response.json()

    def delete(self, template_id: str) -> None:
        """Delete a template.

        Args:
            template_id: The ID of the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/template/delete", json={"template_id": template_id})


class AsyncTemplates(AsyncBaseResource):
    """Asynchronous GPU templates management resource."""

    async def list(self) -> dict[str, Any]:
        """List all templates.

        Returns:
            List of templates

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/templates")
        return response.json()

    async def get(self, template_id: str) -> dict[str, Any]:
        """Get details of a specific template.

        Args:
            template_id: The ID of the template

        Returns:
            Detailed information about the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(
            f"{BASE_PATH}/template", params={"template_id": template_id}
        )
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new template.

        Args:
            **kwargs: Template creation parameters (e.g., name, instance_id)

        Returns:
            Created template information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/template/create", json=kwargs)
        return response.json()

    async def delete(self, template_id: str) -> None:
        """Delete a template.

        Args:
            template_id: The ID of the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/template/delete", json={"template_id": template_id})
