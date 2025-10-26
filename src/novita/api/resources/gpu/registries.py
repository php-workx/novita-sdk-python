"""GPU registries management resource."""

from typing import TYPE_CHECKING, Any

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Registries(BaseResource):
    """Synchronous GPU registries management resource."""

    def list(self) -> dict[str, Any]:
        """List all repository authentications.

        Returns:
            List of repository authentications

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/repository/auths")
        return response.json()

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new repository authentication.

        Args:
            **kwargs: Repository auth parameters (e.g., registry, username, password)

        Returns:
            Created repository authentication information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(f"{BASE_PATH}/repository/auth/save", json=kwargs)
        return response.json()

    def delete(self, auth_id: str) -> None:
        """Delete a repository authentication.

        Args:
            auth_id: The ID of the repository authentication

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If auth doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(f"{BASE_PATH}/repository/auth/delete", json={"auth_id": auth_id})


class AsyncRegistries(AsyncBaseResource):
    """Asynchronous GPU registries management resource."""

    async def list(self) -> dict[str, Any]:
        """List all repository authentications.

        Returns:
            List of repository authentications

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/repository/auths")
        return response.json()

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new repository authentication.

        Args:
            **kwargs: Repository auth parameters (e.g., registry, username, password)

        Returns:
            Created repository authentication information

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(f"{BASE_PATH}/repository/auth/save", json=kwargs)
        return response.json()

    async def delete(self, auth_id: str) -> None:
        """Delete a repository authentication.

        Args:
            auth_id: The ID of the repository authentication

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If auth doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(f"{BASE_PATH}/repository/auth/delete", json={"auth_id": auth_id})
