"""SSH keys management resource."""

from __future__ import annotations

from novita.generated.models import (
    CreateSSHKeyRequest,
    ListSSHKeysResponse,
    SSHKey,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


class SSHKeys(BaseResource):
    """Synchronous SSH keys management resource."""

    def list(self) -> list[SSHKey]:
        """List all SSH keys for the account.

        Returns:
            List of SSH key objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/ssh-keys")
        parsed = ListSSHKeysResponse.model_validate(response.json())
        return parsed.data

    def create(self, name: str, public_key: str) -> SSHKey:
        """Create a new SSH key.

        Args:
            name: Name for the SSH key
            public_key: SSH public key content (e.g., from ~/.ssh/id_rsa.pub)

        Returns:
            Created SSH key object

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If the request is invalid
            APIError: If the API returns an error
        """
        request = CreateSSHKeyRequest(name=name, public_key=public_key)
        response = self._client.post(
            f"{BASE_PATH}/ssh-key/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return SSHKey.model_validate(response.json())

    def delete(self, key_id: str) -> None:
        """Delete an SSH key.

        Args:
            key_id: SSH key ID to delete

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If the key doesn't exist
            APIError: If the API returns an error
        """
        self._client.post(
            f"{BASE_PATH}/ssh-key/delete",
            json={"id": key_id},
        )


class AsyncSSHKeys(AsyncBaseResource):
    """Asynchronous SSH keys management resource."""

    async def list(self) -> list[SSHKey]:
        """List all SSH keys for the account.

        Returns:
            List of SSH key objects

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/ssh-keys")
        parsed = ListSSHKeysResponse.model_validate(response.json())
        return parsed.data

    async def create(self, name: str, public_key: str) -> SSHKey:
        """Create a new SSH key.

        Args:
            name: Name for the SSH key
            public_key: SSH public key content (e.g., from ~/.ssh/id_rsa.pub)

        Returns:
            Created SSH key object

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If the request is invalid
            APIError: If the API returns an error
        """
        request = CreateSSHKeyRequest(name=name, public_key=public_key)
        response = await self._client.post(
            f"{BASE_PATH}/ssh-key/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return SSHKey.model_validate(response.json())

    async def delete(self, key_id: str) -> None:
        """Delete an SSH key.

        Args:
            key_id: SSH key ID to delete

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If the key doesn't exist
            APIError: If the API returns an error
        """
        await self._client.post(
            f"{BASE_PATH}/ssh-key/delete",
            json={"id": key_id},
        )
