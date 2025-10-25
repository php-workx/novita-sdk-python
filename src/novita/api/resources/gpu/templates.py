"""GPU templates management resource."""

from typing import TYPE_CHECKING, Any

from .base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Templates(BaseResource):
    """Synchronous GPU templates management resource."""

    def list(self) -> dict[str, Any]:
        """List templates.

        Returns:
            List of templates

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Templates API endpoints not yet specified")


class AsyncTemplates(AsyncBaseResource):
    """Asynchronous GPU templates management resource."""

    async def list(self) -> dict[str, Any]:
        """List templates.

        Returns:
            List of templates

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        raise NotImplementedError("Templates API endpoints not yet specified")
