"""GPU instances management resource."""

from __future__ import annotations

from typing import Any, cast

from novita.generated.models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    EditInstanceRequest,
    InstanceInfo,
    ListInstancesResponse,
    SaveImageRequest,
    UpgradeInstanceRequest,
)

from .base import BASE_PATH, AsyncBaseResource, BaseResource


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
