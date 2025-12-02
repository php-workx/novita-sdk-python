"""GPU registries management resource."""

from __future__ import annotations

from pydantic import SecretStr

from novita.generated.models import (
    CreateRepositoryAuthRequest,
    DeleteRepositoryAuthRequest,
    ListRepositoryAuthsResponse,
    RepositoryAuth,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class Registries(BaseResource):
    """Synchronous GPU registries management resource."""

    def list(self) -> list[RepositoryAuth]:
        """List all repository authentications.

        Returns:
            List of repository authentication objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/repository/auths")
        parsed = ListRepositoryAuthsResponse.model_validate(response.json())
        return parsed.data

    def create(
        self,
        name: str,
        username: str,
        password: str | SecretStr,
    ) -> None:
        """Create a new repository authentication.

        Args:
            name: Registry name/URL (e.g., 'docker.io', 'ghcr.io')
            username: Registry username
            password: Registry password (will be handled securely and not logged)

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        # Convert plain string to SecretStr if needed
        secret_password = password if isinstance(password, SecretStr) else SecretStr(password)

        request = CreateRepositoryAuthRequest(
            name=name,
            username=username,
            password=secret_password,
        )
        self._client.post(
            f"{BASE_PATH}/repository/auth/save",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    def delete(self, auth_id: str) -> None:
        """Delete a repository authentication.

        Args:
            auth_id: The ID of the repository authentication

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If auth doesn't exist
            APIError: If the API returns an error
        """
        request = DeleteRepositoryAuthRequest(id=auth_id)
        self._client.post(
            f"{BASE_PATH}/repository/auth/delete",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )


class AsyncRegistries(AsyncBaseResource):
    """Asynchronous GPU registries management resource."""

    async def list(self) -> list[RepositoryAuth]:
        """List all repository authentications.

        Returns:
            List of repository authentication objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/repository/auths")
        parsed = ListRepositoryAuthsResponse.model_validate(response.json())
        return parsed.data

    async def create(
        self,
        name: str,
        username: str,
        password: str | SecretStr,
    ) -> None:
        """Create a new repository authentication.

        Args:
            name: Registry name/URL (e.g., 'docker.io', 'ghcr.io')
            username: Registry username
            password: Registry password (will be handled securely and not logged)

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        # Convert plain string to SecretStr if needed
        secret_password = password if isinstance(password, SecretStr) else SecretStr(password)

        request = CreateRepositoryAuthRequest(
            name=name,
            username=username,
            password=secret_password,
        )
        await self._client.post(
            f"{BASE_PATH}/repository/auth/save",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    async def delete(self, auth_id: str) -> None:
        """Delete a repository authentication.

        Args:
            auth_id: The ID of the repository authentication

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If auth doesn't exist
            APIError: If the API returns an error
        """
        request = DeleteRepositoryAuthRequest(id=auth_id)
        await self._client.post(
            f"{BASE_PATH}/repository/auth/delete",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
