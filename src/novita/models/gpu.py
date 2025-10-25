"""Pydantic models for GPU instance management."""

from pydantic import BaseModel, Field

from novita.models.common import EndpointStatus, InstanceType


class CreateInstanceRequest(BaseModel):
    """Request model for creating a GPU instance."""

    name: str = Field(..., description="Name for the instance")
    instance_type: str | InstanceType = Field(..., description="Type of GPU instance")
    disk_size: int = Field(default=50, description="Disk size in GB", ge=20, le=1000)
    ssh_key: str | None = Field(None, description="SSH public key for access")


class UpdateInstanceRequest(BaseModel):
    """Request model for updating a GPU instance."""

    name: str | None = Field(None, description="New name for the instance")
    disk_size: int | None = Field(None, description="New disk size in GB", ge=20, le=1000)


class InstanceInfo(BaseModel):
    """Model for GPU instance information."""

    instance_id: str = Field(..., description="Unique identifier for the instance")
    name: str = Field(..., description="Instance name")
    instance_type: str = Field(..., description="GPU instance type")
    status: str | EndpointStatus = Field(..., description="Current status of the instance")
    disk_size: int = Field(..., description="Disk size in GB")
    created_at: int = Field(..., description="Creation timestamp")
    ssh_host: str | None = Field(None, description="SSH host address")
    ssh_port: int | None = Field(None, description="SSH port")
    jupyter_url: str | None = Field(None, description="Jupyter notebook URL if available")


class CreateInstanceResponse(BaseModel):
    """Response model for instance creation."""

    instance_id: str = Field(..., description="ID of the created instance")
    status: str = Field(..., description="Initial status of the instance")


class ListInstancesResponse(BaseModel):
    """Response model for listing instances."""

    instances: list[InstanceInfo] = Field(..., description="List of instances")
    total: int = Field(..., description="Total number of instances")


class InstanceActionResponse(BaseModel):
    """Response model for instance actions (start/stop/delete)."""

    instance_id: str = Field(..., description="Instance ID")
    success: bool = Field(..., description="Whether the action succeeded")
    message: str | None = Field(None, description="Optional message")


class SubscriptionPrice(BaseModel):
    """Model for monthly subscription pricing."""

    price: int = Field(..., description="Unit price for the subscription instance")
    month: int = Field(..., description="Subscription duration, in months")


class GPUProduct(BaseModel):
    """Model for GPU product information."""

    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    cpu_per_gpu: int = Field(..., alias="cpuPerGpu", description="Number of CPU cores per GPU")
    memory_per_gpu: int = Field(..., alias="memoryPerGpu", description="Memory size per GPU (GB)")
    disk_per_gpu: int = Field(..., alias="diskPerGpu", description="Disk size per GPU (GB)")
    available_deploy: bool = Field(
        ...,
        alias="availableDeploy",
        description="Whether this product can be used to create an instance",
    )
    min_root_fs: int = Field(
        ..., alias="minRootFS", description="Minimum available root filesystem size (GB)"
    )
    max_root_fs: int = Field(
        ..., alias="maxRootFS", description="Maximum available root filesystem size (GB)"
    )
    min_local_storage: int = Field(
        ..., alias="minLocalStorage", description="Minimum available local storage size (GB)"
    )
    max_local_storage: int = Field(
        ..., alias="maxLocalStorage", description="Maximum available local storage size (GB)"
    )
    regions: list[str] = Field(
        ...,
        description="Available clusters. Indicates that this product is only available in the specified clusters. If the list is empty, the product is available in all clusters.",
    )
    price: int = Field(
        ..., description="Price for creating a pay-as-you-go instance with this product"
    )
    monthly_price: list[SubscriptionPrice] = Field(
        ...,
        alias="monthlyPrice",
        description="Price for creating a subscription (monthly or yearly) instance with this product",
    )
    billing_methods: list[str] = Field(
        ...,
        alias="billingMethods",
        description="The billing methods supported by this product. Valid values: onDemand, monthly, spot",
    )
    spot_price: str = Field(..., alias="spotPrice", description="Spot billing instance price")


class ListGPUProductsResponse(BaseModel):
    """Response model for listing GPU products."""

    data: list[GPUProduct] = Field(..., description="List of GPU product information")
