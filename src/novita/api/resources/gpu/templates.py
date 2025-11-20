"""GPU templates management resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from novita.generated.models import (
    CreateTemplateResponse,
    GetTemplateResponse,
    ListTemplatesResponse,
    Template,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Templates(BaseResource):
    """Synchronous GPU templates management resource."""

    def list(self) -> list[Template]:
        """List all templates.

        Returns:
            List of template objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/templates")
        parsed = ListTemplatesResponse.model_validate(response.json())
        return parsed.template

    def get(self, template_id: str) -> Template:
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
        response = self._client.get(f"{BASE_PATH}/template", params={"templateId": template_id})
        parsed = GetTemplateResponse.model_validate(response.json())
        return parsed.template

    def create(self, **kwargs: Any) -> CreateTemplateResponse:
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
        return CreateTemplateResponse.model_validate(response.json())

    def delete(self, template_id: str) -> None:
        """Delete a template.

        Args:
            template_id: The ID of the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/template/delete", json={"templateId": template_id})


class AsyncTemplates(AsyncBaseResource):
    """Asynchronous GPU templates management resource."""

    async def list(self) -> list[Template]:
        """List all templates.

        Returns:
            List of template objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/templates")
        parsed = ListTemplatesResponse.model_validate(response.json())
        return parsed.template

    async def get(self, template_id: str) -> Template:
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
            f"{BASE_PATH}/template", params={"templateId": template_id}
        )
        parsed = GetTemplateResponse.model_validate(response.json())
        return parsed.template

    async def create(self, **kwargs: Any) -> CreateTemplateResponse:
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
        return CreateTemplateResponse.model_validate(response.json())

    async def delete(self, template_id: str) -> None:
        """Delete a template.

        Args:
            template_id: The ID of the template

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If template doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/template/delete", json={"templateId": template_id})
