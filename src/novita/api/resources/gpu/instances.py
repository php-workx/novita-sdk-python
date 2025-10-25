"""GPU instances management resource."""

from typing import TYPE_CHECKING

from novita.models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    InstanceActionResponse,
    InstanceInfo,
    ListInstancesResponse,
    UpdateInstanceRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    pass


class Instances(BaseResource):
    """Synchronous GPU instances management resource."""

    def create(self, request: CreateInstanceRequest) -> CreateInstanceResponse:
        """Create a new GPU instance.

        Args:
            request: Instance creation parameters

        Returns:
            Response containing the created instance ID and status

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/create", json=request.model_dump(exclude_none=True)
        )
        return CreateInstanceResponse.model_validate(response.json())

    def list(self) -> ListInstancesResponse:
        """List all GPU instances.

        Returns:
            Response containing list of instances

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = self._client.get(f"{BASE_PATH}/gpu/instances")
        return ListInstancesResponse.model_validate(response.json())

    def get(self, instance_id: str) -> InstanceInfo:
        """Get details of a specific GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Detailed information about the instance

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.get(
            f"{BASE_PATH}/gpu/instance", params={"instance_id": instance_id}
        )
        return InstanceInfo.model_validate(response.json())

    def edit(self, instance_id: str, request: UpdateInstanceRequest) -> InstanceInfo:
        """Update a GPU instance.

        Args:
            instance_id: The ID of the instance
            request: Update parameters

        Returns:
            Updated instance information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"instance_id": instance_id, **request.model_dump(exclude_none=True)}
        response = self._client.post(f"{BASE_PATH}/gpu/instance/edit", json=data)
        return InstanceInfo.model_validate(response.json())

    def start(self, instance_id: str) -> InstanceActionResponse:
        """Start a stopped GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/start", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    def stop(self, instance_id: str) -> InstanceActionResponse:
        """Stop a running GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/stop", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    def delete(self, instance_id: str) -> InstanceActionResponse:
        """Delete a GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/delete", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    def restart(self, instance_id: str) -> InstanceActionResponse:
        """Restart a GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/restart", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    def upgrade(self, instance_id: str, new_instance_type: str) -> InstanceActionResponse:
        """Upgrade a GPU instance to a different instance type.

        Args:
            instance_id: The ID of the instance
            new_instance_type: The new instance type to upgrade to

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the upgrade is not valid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/upgrade",
            json={"instance_id": instance_id, "instance_type": new_instance_type},
        )
        return InstanceActionResponse.model_validate(response.json())

    def migrate(self, instance_id: str, target_region: str) -> InstanceActionResponse:
        """Migrate a GPU instance to a different region.

        Args:
            instance_id: The ID of the instance
            target_region: The target region to migrate to

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the migration is not valid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/migrate",
            json={"instance_id": instance_id, "target_region": target_region},
        )
        return InstanceActionResponse.model_validate(response.json())

    def renew(self, instance_id: str, duration_hours: int) -> InstanceActionResponse:
        """Renew a GPU instance for additional time.

        Args:
            instance_id: The ID of the instance
            duration_hours: Number of hours to renew for

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the renewal is not valid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/renewInstance",
            json={"instance_id": instance_id, "duration_hours": duration_hours},
        )
        return InstanceActionResponse.model_validate(response.json())

    def convert_to_monthly(self, instance_id: str) -> InstanceActionResponse:
        """Convert an hourly instance to monthly billing.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the conversion is not valid
            APIError: If the API returns an error
        """
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/transToMonthlyInstance", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())


class AsyncInstances(AsyncBaseResource):
    """Asynchronous GPU instances management resource."""

    async def create(self, request: CreateInstanceRequest) -> CreateInstanceResponse:
        """Create a new GPU instance.

        Args:
            request: Instance creation parameters

        Returns:
            Response containing the created instance ID and status

        Raises:
            AuthenticationError: If API key is invalid
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/create", json=request.model_dump(exclude_none=True)
        )
        return CreateInstanceResponse.model_validate(response.json())

    async def list(self) -> ListInstancesResponse:
        """List all GPU instances.

        Returns:
            Response containing list of instances

        Raises:
            AuthenticationError: If API key is invalid
            APIError: If the API returns an error
        """
        response = await self._client.get(f"{BASE_PATH}/gpu/instances")
        return ListInstancesResponse.model_validate(response.json())

    async def get(self, instance_id: str) -> InstanceInfo:
        """Get details of a specific GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Detailed information about the instance

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.get(
            f"{BASE_PATH}/gpu/instance", params={"instance_id": instance_id}
        )
        return InstanceInfo.model_validate(response.json())

    async def edit(self, instance_id: str, request: UpdateInstanceRequest) -> InstanceInfo:
        """Update a GPU instance.

        Args:
            instance_id: The ID of the instance
            request: Update parameters

        Returns:
            Updated instance information

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If request parameters are invalid
            APIError: If the API returns an error
        """
        data = {"instance_id": instance_id, **request.model_dump(exclude_none=True)}
        response = await self._client.post(f"{BASE_PATH}/gpu/instance/edit", json=data)
        return InstanceInfo.model_validate(response.json())

    async def start(self, instance_id: str) -> InstanceActionResponse:
        """Start a stopped GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/start", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    async def stop(self, instance_id: str) -> InstanceActionResponse:
        """Stop a running GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/stop", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    async def delete(self, instance_id: str) -> InstanceActionResponse:
        """Delete a GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/delete", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    async def restart(self, instance_id: str) -> InstanceActionResponse:
        """Restart a GPU instance.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/restart", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())

    async def upgrade(self, instance_id: str, new_instance_type: str) -> InstanceActionResponse:
        """Upgrade a GPU instance to a different instance type.

        Args:
            instance_id: The ID of the instance
            new_instance_type: The new instance type to upgrade to

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the upgrade is not valid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/upgrade",
            json={"instance_id": instance_id, "instance_type": new_instance_type},
        )
        return InstanceActionResponse.model_validate(response.json())

    async def migrate(self, instance_id: str, target_region: str) -> InstanceActionResponse:
        """Migrate a GPU instance to a different region.

        Args:
            instance_id: The ID of the instance
            target_region: The target region to migrate to

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the migration is not valid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/migrate",
            json={"instance_id": instance_id, "target_region": target_region},
        )
        return InstanceActionResponse.model_validate(response.json())

    async def renew(self, instance_id: str, duration_hours: int) -> InstanceActionResponse:
        """Renew a GPU instance for additional time.

        Args:
            instance_id: The ID of the instance
            duration_hours: Number of hours to renew for

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the renewal is not valid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/renewInstance",
            json={"instance_id": instance_id, "duration_hours": duration_hours},
        )
        return InstanceActionResponse.model_validate(response.json())

    async def convert_to_monthly(self, instance_id: str) -> InstanceActionResponse:
        """Convert an hourly instance to monthly billing.

        Args:
            instance_id: The ID of the instance

        Returns:
            Response indicating success or failure

        Raises:
            AuthenticationError: If API key is invalid
            NotFoundError: If instance doesn't exist
            BadRequestError: If the conversion is not valid
            APIError: If the API returns an error
        """
        response = await self._client.post(
            f"{BASE_PATH}/gpu/instance/transToMonthlyInstance", json={"instance_id": instance_id}
        )
        return InstanceActionResponse.model_validate(response.json())
