"""GPU instances management resource."""

from __future__ import annotations

import re
from typing import Any, cast
from urllib.parse import urlparse

from novita.exceptions import NotFoundError
from novita.generated.models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    EditInstanceRequest,
    InstanceInfo,
    ListInstancesResponse,
    SaveImageRequest,
    SSHEndpoint,
    UpgradeInstanceRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


def _parse_ssh_command(command: str) -> dict[str, Any]:
    """Parse SSH command to extract user, host, and port.

    Args:
        command: SSH command string (e.g., "ssh user@host -p 2222")

    Returns:
        Dict with user, host, and port keys

    Examples:
        >>> _parse_ssh_command("ssh root@example.com -p 2222")
        {'user': 'root', 'host': 'example.com', 'port': 2222}
        >>> _parse_ssh_command("ssh -p 22000 ubuntu@10.0.0.1")
        {'user': 'ubuntu', 'host': '10.0.0.1', 'port': 22000}
    """
    result: dict[str, Any] = {}

    # Extract user@host pattern
    # Username can contain alphanumeric, hyphens, underscores, and dots
    user_host_match = re.search(r"([\w\.\-]+)@([\w\.\-]+)", command)
    if user_host_match:
        result["user"] = user_host_match.group(1)
        result["host"] = user_host_match.group(2)

    # Extract port (both -p PORT and -p=PORT formats)
    port_match = re.search(r"-p[=\s]+(\d+)", command)
    if port_match:
        result["port"] = int(port_match.group(1))

    return result


def _normalize_endpoint(endpoint: str) -> tuple[str, int | None]:
    """Normalize endpoint URL to extract host and port.

    Args:
        endpoint: Endpoint URL (e.g., "tcp://host:port", "host:port", "http://host:port")

    Returns:
        Tuple of (host, port)

    Examples:
        >>> _normalize_endpoint("tcp://example.com:2222")
        ('example.com', 2222)
        >>> _normalize_endpoint("example.com:2222")
        ('example.com', 2222)
    """
    # Handle URLs with schemes
    if "://" in endpoint:
        parsed = urlparse(endpoint)
        return parsed.hostname or "", parsed.port

    # Handle host:port format
    if ":" in endpoint:
        parts = endpoint.rsplit(":", 1)
        try:
            return parts[0], int(parts[1])
        except (ValueError, IndexError):
            return endpoint, None

    return endpoint, None


def _extract_ssh_endpoint(instance: InstanceInfo) -> SSHEndpoint:
    """Extract SSH endpoint from instance metadata.

    This function contains the shared logic for parsing SSH connection details
    from an instance, used by both sync and async methods.

    Args:
        instance: Instance information object

    Returns:
        SSHEndpoint with user, host, port, and optional command

    Raises:
        NotFoundError: If no SSH endpoint is available
    """
    # Try connect_component_ssh first (preferred)
    if instance.connect_component_ssh:
        ssh = instance.connect_component_ssh
        result: dict[str, Any] = {}

        # Extract from command if available
        if ssh.command:
            parsed = _parse_ssh_command(ssh.command)
            result.update(parsed)
            result["command"] = ssh.command

        # Override with direct fields if available
        if ssh.user:
            result["user"] = ssh.user

        # Only proceed when we have a user and a real host
        if result.get("user") and result.get("host"):
            # Default port if not found
            if "port" not in result:
                result["port"] = 22

            return SSHEndpoint(
                user=result["user"],
                host=result["host"],
                port=result["port"],
                command=result.get("command"),
            )

    # Fallback: check port_mappings for port 22
    if instance.port_mappings:
        for mapping in instance.port_mappings:
            if mapping.port == 22 and mapping.type in ("tcp", "ssh") and mapping.endpoint:
                host, port = _normalize_endpoint(mapping.endpoint)
                if host and port:
                    # Assume root user if not specified
                    return SSHEndpoint(
                        user="root",
                        host=host,
                        port=port,
                        command=f"ssh root@{host} -p {port}",
                    )

    # No SSH endpoint found
    msg = f"No SSH endpoint found for instance {instance.id}"
    raise NotFoundError(msg)


def _build_list_filters(
    page_size: int | None,
    page_num: int | None,
    name: str | None,
    product_name: str | None,
    status: str | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if page_size is not None:
        params["pageSize"] = page_size
    if page_num is not None:
        params["pageNum"] = page_num
    if name is not None:
        params["name"] = name
    if product_name is not None:
        params["productName"] = product_name
    if status is not None:
        params["status"] = status
    return params


class Instances(BaseResource):
    """Synchronous GPU instances management resource."""

    def create(self, request: CreateInstanceRequest) -> CreateInstanceResponse:
        """Create a new GPU instance."""

        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return CreateInstanceResponse.model_validate(response.json())

    def list(
        self,
        *,
        page_size: int | None = None,
        page_num: int | None = None,
        name: str | None = None,
        product_name: str | None = None,
        status: str | None = None,
    ) -> list[InstanceInfo]:
        """List GPU instances with optional filters."""

        params = _build_list_filters(page_size, page_num, name, product_name, status)
        response = self._client.get(
            f"{BASE_PATH}/gpu/instances",
            params=params or None,
        )
        parsed = ListInstancesResponse.model_validate(response.json())
        return parsed.instances

    def get(self, instance_id: str) -> InstanceInfo:
        """Fetch details for a specific instance."""

        response = self._client.get(
            f"{BASE_PATH}/gpu/instance",
            params={"instanceId": instance_id},
        )
        return InstanceInfo.model_validate(response.json())

    def edit(self, request: EditInstanceRequest) -> None:
        """Edit instance ports or root disk."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/edit",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    def start(self, instance_id: str) -> None:
        """Start an instance."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/start",
            json={"instanceId": instance_id},
        )

    def stop(self, instance_id: str) -> None:
        """Stop an instance."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/stop",
            json={"instanceId": instance_id},
        )

    def delete(self, instance_id: str) -> None:
        """Delete an instance."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/delete",
            json={"instanceId": instance_id},
        )

    def restart(self, instance_id: str) -> None:
        """Restart an instance."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/restart",
            json={"instanceId": instance_id},
        )

    def upgrade(self, request: UpgradeInstanceRequest) -> None:
        """Upgrade an instance with a new configuration."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/upgrade",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    def migrate(self, instance_id: str) -> None:
        """Migrate an instance to a different region."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/migrate",
            json={"instanceId": instance_id},
        )

    def renew(self, instance_id: str, month: int) -> None:
        """Renew a subscription instance."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/renewInstance",
            json={"instanceId": instance_id, "month": month},
        )

    def convert_to_monthly(self, instance_id: str, month: int) -> None:
        """Convert a pay-as-you-go instance to subscription billing."""

        self._client.post(
            f"{BASE_PATH}/gpu/instance/transToMonthlyInstance",
            json={"instanceId": instance_id, "month": month},
        )

    def save_image(self, request: SaveImageRequest) -> str:
        """Create an image from an instance and return the job ID."""

        response = self._client.post(
            f"{BASE_PATH}/job/save/image",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        payload = cast(dict[str, Any], response.json())
        return str(payload.get("jobId", ""))

    def get_ssh_endpoint(self, instance_id: str) -> SSHEndpoint:
        """Get SSH connection details for an instance.

        This method extracts SSH connection information from the instance details.
        It first tries to use connect_component_ssh fields, then falls back to
        parsing port_mappings for port 22.

        Args:
            instance_id: Instance ID to get SSH endpoint for

        Returns:
            SSHEndpoint with user, host, port, and optional command

        Raises:
            NotFoundError: If instance doesn't exist or has no SSH access
            ValueError: If SSH connection details cannot be determined
        """
        instance = self.get(instance_id)
        return _extract_ssh_endpoint(instance)


class AsyncInstances(AsyncBaseResource):
    """Asynchronous GPU instances management resource."""

    async def create(self, request: CreateInstanceRequest) -> CreateInstanceResponse:
        """Create a new GPU instance."""

        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/create",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return CreateInstanceResponse.model_validate(response.json())

    async def list(
        self,
        *,
        page_size: int | None = None,
        page_num: int | None = None,
        name: str | None = None,
        product_name: str | None = None,
        status: str | None = None,
    ) -> list[InstanceInfo]:
        """List GPU instances with optional filters."""

        params = _build_list_filters(page_size, page_num, name, product_name, status)
        response = await self._client.get(
            f"{BASE_PATH}/gpu/instances",
            params=params or None,
        )
        parsed = ListInstancesResponse.model_validate(response.json())
        return parsed.instances

    async def get(self, instance_id: str) -> InstanceInfo:
        """Fetch details for a specific instance."""

        response = await self._client.get(
            f"{BASE_PATH}/gpu/instance",
            params={"instanceId": instance_id},
        )
        return InstanceInfo.model_validate(response.json())

    async def edit(self, request: EditInstanceRequest) -> None:
        """Edit instance ports or root disk."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/edit",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    async def start(self, instance_id: str) -> None:
        """Start an instance."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/start",
            json={"instanceId": instance_id},
        )

    async def stop(self, instance_id: str) -> None:
        """Stop an instance."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/stop",
            json={"instanceId": instance_id},
        )

    async def delete(self, instance_id: str) -> None:
        """Delete an instance."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/delete",
            json={"instanceId": instance_id},
        )

    async def restart(self, instance_id: str) -> None:
        """Restart an instance."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/restart",
            json={"instanceId": instance_id},
        )

    async def upgrade(self, request: UpgradeInstanceRequest) -> None:
        """Upgrade an instance with a new configuration."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/upgrade",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

    async def migrate(self, instance_id: str) -> None:
        """Migrate an instance to a different region."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/migrate",
            json={"instanceId": instance_id},
        )

    async def renew(self, instance_id: str, month: int) -> None:
        """Renew a subscription instance."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/renewInstance",
            json={"instanceId": instance_id, "month": month},
        )

    async def convert_to_monthly(self, instance_id: str, month: int) -> None:
        """Convert a pay-as-you-go instance to subscription billing."""

        await self._client.post(
            f"{BASE_PATH}/gpu/instance/transToMonthlyInstance",
            json={"instanceId": instance_id, "month": month},
        )

    async def save_image(self, request: SaveImageRequest) -> str:
        """Create an image from an instance and return the job ID."""

        response = await self._client.post(
            f"{BASE_PATH}/job/save/image",
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        payload = cast(dict[str, Any], response.json())
        return str(payload.get("jobId", ""))

    async def get_ssh_endpoint(self, instance_id: str) -> SSHEndpoint:
        """Get SSH connection details for an instance.

        This method extracts SSH connection information from the instance details.
        It first tries to use connect_component_ssh fields, then falls back to
        parsing port_mappings for port 22.

        Args:
            instance_id: Instance ID to get SSH endpoint for

        Returns:
            SSHEndpoint with user, host, port, and optional command

        Raises:
            NotFoundError: If instance doesn't exist or has no SSH access
            ValueError: If SSH connection details cannot be determined
        """
        instance = await self.get(instance_id)
        return _extract_ssh_endpoint(instance)
