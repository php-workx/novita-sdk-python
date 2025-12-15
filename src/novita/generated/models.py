from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Literal, Optional

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    computed_field,
    field_validator,
)


class Cluster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Cluster ID")]
    name: Annotated[str, Field(description="Cluster name")]
    available_gpu_type: Annotated[
        list[str], Field(alias="availableGpuType", description="Supported GPU types in the cluster")
    ]
    support_network_storage: Annotated[
        bool,
        Field(
            alias="supportNetworkStorage", description="Whether cloud storage creation is supported"
        ),
    ]
    support_instance_network: Annotated[
        bool,
        Field(
            alias="supportInstanceNetwork", description="Whether VPC network creation is supported"
        ),
    ]


class Kind(StrEnum):
    """
    Instance type
    """

    gpu = "gpu"
    cpu = "cpu"


class Env(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: str
    value: str


class Tool(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str | None = None
    port: str | None = None
    type: str | None = None


class NetworkStorage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(alias="Id")] = None
    mount_point: Annotated[str | None, Field(alias="mountPoint")] = None


class BillingMode(StrEnum):
    """
    Billing mode
    """

    on_demand = "onDemand"
    monthly = "monthly"
    spot = "spot"


class CreateInstanceRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[
        str | None, Field(description="Name for the instance", max_length=255, min_length=0)
    ] = None
    product_id: Annotated[
        str,
        Field(
            alias="productId", description="GPU product identifier", max_length=255, min_length=1
        ),
    ]
    gpu_num: Annotated[int, Field(alias="gpuNum", description="Number of GPUs", ge=1, le=8)]
    rootfs_size: Annotated[
        int, Field(alias="rootfsSize", description="Root filesystem size in GB", ge=10, le=6144)
    ]
    image_url: Annotated[
        str,
        Field(alias="imageUrl", description="Container image URL", max_length=500, min_length=1),
    ]
    kind: Annotated[Kind, Field(description="Instance type")]
    image_auth: Annotated[
        str | None, Field(alias="imageAuth", description="Registry credentials")
    ] = None
    image_auth_id: Annotated[
        str | None, Field(alias="imageAuthId", description="Authentication reference ID")
    ] = None
    ports: Annotated[str | None, Field(description="Exposed ports with protocols")] = None
    envs: Annotated[
        list[Env] | None, Field(description="Environment variables", max_length=100)
    ] = None
    tools: Annotated[list[Tool] | None, Field(description="Tool configuration (e.g., Jupyter)")] = (
        None
    )
    command: Annotated[
        str | None, Field(description="Startup command", max_length=2047, min_length=0)
    ] = None
    cluster_id: Annotated[
        str | None, Field(alias="clusterId", description="Cluster placement specification")
    ] = None
    network_storages: Annotated[
        list[NetworkStorage] | None,
        Field(alias="networkStorages", description="Cloud storage mounts", max_length=30),
    ] = None
    network_id: Annotated[
        str | None, Field(alias="networkId", description="VPC network reference")
    ] = None
    month: Annotated[int | None, Field(description="Subscription duration in months")] = None
    billing_mode: Annotated[
        BillingMode | None, Field(alias="billingMode", description="Billing mode")
    ] = None


class VolumeMount(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Literal["network"], Field(description='Must be "network"')]
    id: Annotated[str, Field(description="Storage identifier")]
    mount_path: Annotated[
        str,
        Field(alias="mountPath", description="Attachment location", max_length=4095, min_length=1),
    ]


class NetworkVolume(BaseModel):
    """
    Cloud storage configuration
    """

    model_config = ConfigDict(populate_by_name=True)
    volume_mounts: Annotated[
        list[VolumeMount],
        Field(
            alias="volumeMounts",
            description="Cloud storage mounts (max 30, use empty array to remove all)",
            max_length=30,
        ),
    ]


class UpgradeInstanceRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    instance_id: Annotated[
        str, Field(alias="instanceId", description="Identifier for the instance being upgraded")
    ]
    image_url: Annotated[
        str,
        Field(
            alias="imageUrl", description="Container image location", max_length=500, min_length=1
        ),
    ]
    image_auth_id: Annotated[
        str | None, Field(alias="imageAuthId", description="Registry authentication credential")
    ] = None
    envs: Annotated[list[Env], Field(description="Environment variable pairs", max_length=100)]
    command: Annotated[
        str, Field(description="Container startup instruction", max_length=2047, min_length=0)
    ]
    save: Annotated[bool, Field(description="Whether to retain data from the previous instance")]
    network_volume: Annotated[
        NetworkVolume, Field(alias="networkVolume", description="Cloud storage configuration")
    ]


class Type(StrEnum):
    """
    Protocol type.
    """

    tcp = "tcp"
    http = "http"


class Port(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port: Annotated[
        int, Field(description="Port number (1-65535, excluding 2222/2223/2224).", ge=1, le=65535)
    ]
    type: Annotated[Type, Field(description="Protocol type.")]


class EditInstanceRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    instance_id: Annotated[
        str, Field(alias="instanceId", description="ID of the instance to edit.")
    ]
    ports: Annotated[
        list[Port] | None,
        Field(description="Ports to expose (ports + tools must not exceed 15).", max_length=15),
    ] = None
    expand_root_disk: Annotated[
        int | None,
        Field(
            alias="expandRootDisk",
            description="Size to expand the root disk (GB). Set to 0 if no expansion is needed.",
            ge=0,
        ),
    ] = None


class CreateInstanceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Created instance ID.")]


class Status(StrEnum):
    """
    Instance status.
    """

    pending = "pending"
    to_create = "toCreate"
    creating = "creating"
    pulling = "pulling"
    running = "running"
    to_start = "toStart"
    starting = "starting"
    to_stop = "toStop"
    stopping = "stopping"
    exited = "exited"
    to_restart = "toRestart"
    restarting = "restarting"
    to_remove = "toRemove"
    removing = "removing"
    removed = "removed"
    to_reset = "toReset"
    resetting = "resetting"
    migrating = "migrating"
    freezing = "freezing"


class PortMapping(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port: Annotated[int | None, Field(description="Port number.")] = None
    endpoint: Annotated[str | None, Field(description="Port endpoint URL.")] = None
    type: Annotated[str | None, Field(description="Protocol type.")] = None


class Type1(StrEnum):
    """
    Storage type.
    """

    network = "network"
    local = "local"


class VolumeMount1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type1 | None, Field(description="Storage type.")] = None
    size: Annotated[str | None, Field(description="Storage capacity.")] = None
    id: Annotated[
        str | None, Field(description="Cloud storage ID (present when type=network).")
    ] = None
    mount_path: Annotated[
        str | None, Field(alias="mountPath", description="Storage mount path.")
    ] = None


class StatusError(BaseModel):
    """
    Error information when the instance fails.
    """

    model_config = ConfigDict(populate_by_name=True)
    state: Annotated[str | None, Field(description="Abnormal instance status.")] = None
    message: Annotated[str | None, Field(description="Error message.")] = None


class Env2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: Annotated[str | None, Field(description="Environment variable name.")] = None
    value: Annotated[str | None, Field(description="Environment variable value.")] = None


class BillingMode1(StrEnum):
    """
    Billing mode for the instance.
    """

    on_demand = "onDemand"
    monthly = "monthly"
    spot = "spot"


class SpotStatus(StrEnum):
    """
    Spot instance status.
    """

    running = "running"
    notified = "notified"
    reclaiming = "reclaiming"
    terminated = "terminated"


class Network(BaseModel):
    """
    VPC network information.
    """

    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(description="Network ID.")] = None
    ip: Annotated[str | None, Field(description="Instance IP in the VPC network.")] = None


class ConnectComponentSsh(BaseModel):
    """
    SSH connection credentials and command.
    """

    model_config = ConfigDict(populate_by_name=True)
    user: str | None = None
    password: str | None = None
    command: str | None = None


class ConnectComponentWebTerminal(BaseModel):
    """
    Web-based terminal access details.
    """

    model_config = ConfigDict(populate_by_name=True)
    url: str | None = None


class ConnectComponentJupyter(BaseModel):
    """
    Jupyter connection information.
    """

    model_config = ConfigDict(populate_by_name=True)
    url: str | None = None
    token: str | None = None


class ConnectComponentLog(BaseModel):
    """
    Log streaming addresses.
    """

    model_config = ConfigDict(populate_by_name=True)
    url: str | None = None


class Node(BaseModel):
    """
    Node metadata.
    """

    model_config = ConfigDict(populate_by_name=True)
    max_rootfs_size: Annotated[
        int | None, Field(alias="maxRootfsSize", description="Maximum root filesystem size.")
    ] = None


class Job(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(description="Job ID.")] = None
    type: Annotated[str | None, Field(description="Job type.")] = None


class InstanceInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Instance ID.")]
    name: Annotated[str, Field(description="Instance name.")]
    cluster_id: Annotated[str, Field(alias="clusterId", description="Cluster ID.")]
    cluster_name: Annotated[str | None, Field(alias="clusterName", description="Cluster name.")] = (
        None
    )
    status: Annotated[Status, Field(description="Instance status.")]
    image_url: Annotated[str, Field(alias="imageUrl", description="Container image URL.")]
    image_auth_id: Annotated[
        str | None,
        Field(alias="imageAuthId", description="Image registry authentication information."),
    ] = None
    command: Annotated[str | None, Field(description="Container startup command.")] = None
    cpu_num: Annotated[str, Field(alias="cpuNum", description="Number of CPU cores.")]
    memory: Annotated[str, Field(description="Memory size (GB).")]
    gpu_num: Annotated[str, Field(alias="gpuNum", description="Number of GPUs.")]
    port_mappings: Annotated[
        list[PortMapping] | None,
        Field(alias="portMappings", description="Instance port information."),
    ] = None
    product_id: Annotated[
        str, Field(alias="productId", description="Product ID used to deploy the instance.")
    ]
    product_name: Annotated[
        str, Field(alias="productName", description="Product name used to deploy the instance.")
    ]
    rootfs_size: Annotated[int, Field(alias="rootfsSize", description="Root filesystem size (GB).")]
    volume_mounts: Annotated[
        list[VolumeMount1] | None,
        Field(alias="volumeMounts", description="Instance storage configuration."),
    ] = None
    status_error: Annotated[
        StatusError | None,
        Field(alias="statusError", description="Error information when the instance fails."),
    ] = None
    envs: Annotated[
        list[Env2] | None, Field(description="Instance environment variable information.")
    ] = None
    kind: Annotated[str | None, Field(description="Instance type.")] = None
    billing_mode: Annotated[
        BillingMode1 | None,
        Field(alias="billingMode", description="Billing mode for the instance."),
    ] = None
    end_time: Annotated[
        str | None,
        Field(
            alias="endTime",
            description="Expiration time for subscription instances (pay-as-you-go returns -1).",
        ),
    ] = None
    spot_status: Annotated[
        SpotStatus | None, Field(alias="spotStatus", description="Spot instance status.")
    ] = None
    spot_reclaim_time: Annotated[
        str | None,
        Field(
            alias="spotReclaimTime",
            description='Spot instance reclaim time ("0" when reclaim has not started).',
        ),
    ] = None
    network: Annotated[Network | None, Field(description="VPC network information.")] = None
    connect_component_ssh: Annotated[
        ConnectComponentSsh | None,
        Field(alias="connectComponentSSH", description="SSH connection credentials and command."),
    ] = None
    connect_component_web_terminal: Annotated[
        ConnectComponentWebTerminal | None,
        Field(
            alias="connectComponentWebTerminal", description="Web-based terminal access details."
        ),
    ] = None
    connect_component_jupyter: Annotated[
        ConnectComponentJupyter | None,
        Field(alias="connectComponentJupyter", description="Jupyter connection information."),
    ] = None
    connect_component_log: Annotated[
        ConnectComponentLog | None,
        Field(alias="connectComponentLog", description="Log streaming addresses."),
    ] = None
    node: Annotated[Node | None, Field(description="Node metadata.")] = None
    free_storage_size: Annotated[
        int | None,
        Field(alias="freeStorageSize", description="Available system disk space in GB."),
    ] = None
    keep_data_day: Annotated[
        int | None,
        Field(alias="keepDataDay", description="Data retention duration post-shutdown."),
    ] = None
    jobs: Annotated[
        list[Job] | None, Field(description="Tasks currently running on the instance.")
    ] = None

    @field_validator("spot_status", "billing_mode", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        """Convert empty string to None for spot_status and billing_mode fields."""
        if v == "":
            return None
        return v


class ListInstancesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    instances: list[InstanceInfo]
    total: Annotated[int, Field(description="Total number of instances")]


class SubscriptionPrice(BaseModel):
    """Subscription pricing information.

    Note: Prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD. For example, an API value of 350000 represents $3.50.
    """

    model_config = ConfigDict(populate_by_name=True)
    price_raw: Annotated[
        int, Field(alias="price", description="Unit price for the subscription instance")
    ]
    month: Annotated[int, Field(description="Subscription duration, in months")]

    @computed_field()
    @property
    def price(self) -> float | None:
        """Get subscription price in USD.

        Returns:
            Price in USD (converted from raw API value in 1/100000 USD units), or None if not available
        """
        return None if self.price_raw is None else self.price_raw / 100000


class InventoryState(StrEnum):
    """
    Stock status
    """

    none = "none"
    low = "low"
    normal = "normal"
    high = "high"


class GPUProduct(BaseModel):
    """GPU product information.

    Note: All prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD per hour. For example, an API value of 35000 represents $0.35/hour.
    """

    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Product ID")]
    name: Annotated[str, Field(description="Product name")]
    cpu_per_gpu: Annotated[int, Field(alias="cpuPerGpu", description="Number of CPU cores per GPU")]
    memory_per_gpu: Annotated[
        int, Field(alias="memoryPerGpu", description="Memory size per GPU (GB)")
    ]
    disk_per_gpu: Annotated[int, Field(alias="diskPerGpu", description="Disk size per GPU (GB)")]
    available_deploy: Annotated[
        bool,
        Field(
            alias="availableDeploy",
            description="Whether this product can be used to create an instance",
        ),
    ]
    min_root_fs: Annotated[
        int, Field(alias="minRootFS", description="Minimum available root filesystem size (GB)")
    ]
    max_root_fs: Annotated[
        int, Field(alias="maxRootFS", description="Maximum available root filesystem size (GB)")
    ]
    min_local_storage: Annotated[
        int, Field(alias="minLocalStorage", description="Minimum available local storage size (GB)")
    ]
    max_local_storage: Annotated[
        int, Field(alias="maxLocalStorage", description="Maximum available local storage size (GB)")
    ]
    regions: Annotated[list[str], Field(description="Available clusters")]
    price_raw: Annotated[
        int, Field(alias="price", description="Price for creating a pay-as-you-go instance")
    ]
    monthly_price: Annotated[
        list[SubscriptionPrice],
        Field(alias="monthlyPrice", description="Price for creating a subscription instance"),
    ]
    billing_methods: Annotated[
        list[str], Field(alias="billingMethods", description="Supported billing methods")
    ]
    spot_price_raw: Annotated[
        int | None,
        Field(
            alias="spotPrice", description="Spot billing instance price (in units of 1/100000 USD)"
        ),
    ] = None
    inventory_state: Annotated[
        InventoryState | None, Field(alias="inventoryState", description="Stock status")
    ] = None

    @computed_field()
    @property
    def price(self) -> float | None:
        """Get on-demand price in USD per hour.

        Returns:
            Price in USD per hour (converted from raw API value in 1/100000 USD units), or None if not available
        """
        return None if self.price_raw is None else self.price_raw / 100000

    @computed_field()
    @property
    def spot_price(self) -> float | None:
        """Get spot price in USD per hour.

        Returns:
            Spot price in USD per hour, or None if spot pricing is not available
        """
        return self.spot_price_raw / 100000 if self.spot_price_raw is not None else None


class ListGPUProductsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[list[GPUProduct], Field(description="List of GPU product information")]


class CPUProduct(BaseModel):
    """CPU product information.

    Note: Prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD per hour.
    """

    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Unique product identifier")]
    name: Annotated[str, Field(description="Product display name")]
    cpu_num: Annotated[int | None, Field(alias="cpuNum", description="Number of CPU cores")] = None
    memory_size: Annotated[
        int | None, Field(alias="memorySize", description="RAM allocation in GB")
    ] = None
    rootfs_size: Annotated[
        int | None, Field(alias="rootfsSize", description="Root filesystem capacity in GB")
    ] = None
    local_volume_size: Annotated[
        int | None, Field(alias="localVolumeSize", description="Local storage in GB")
    ] = None
    available_deploy: Annotated[
        bool | None,
        Field(
            alias="availableDeploy",
            description="Whether this product can be used to create an instance",
        ),
    ] = None
    price_raw: Annotated[int | None, Field(alias="price", description="Product unit cost")] = None

    @computed_field()
    @property
    def price(self) -> float | None:
        """Get price in USD per hour.

        Returns:
            Price in USD per hour, or None if pricing is not available
        """
        return self.price_raw / 100000 if self.price_raw is not None else None


class ListCPUProductsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[list[CPUProduct], Field(description="List of CPU product information")]


class ErrorResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    message: str
    details: dict[str, Any] | None = None


class State(BaseModel):
    """
    Status details
    """

    model_config = ConfigDict(populate_by_name=True)
    state: Annotated[
        str | None, Field(description='Status value (e.g., "serving" when available)')
    ] = None
    error: Annotated[str | None, Field(description="Error code if applicable")] = None
    message: Annotated[str | None, Field(description="Status message")] = None


class WorkerConfig(BaseModel):
    """
    Worker scaling configuration
    """

    model_config = ConfigDict(populate_by_name=True)
    min_num: Annotated[int | None, Field(alias="minNum", description="Minimum worker count")] = None
    max_num: Annotated[int | None, Field(alias="maxNum", description="Maximum worker count")] = None
    free_timeout: Annotated[
        int | None, Field(alias="freeTimeout", description="Idle timeout in seconds")
    ] = None
    max_concurrent: Annotated[
        int | None, Field(alias="maxConcurrent", description="Request concurrency limit")
    ] = None
    gpu_num: Annotated[
        int | None, Field(alias="gpuNum", description="GPUs allocated per worker")
    ] = None
    cuda_version: Annotated[str | None, Field(alias="cudaVersion", description="CUDA version")] = (
        None
    )


class Type2(StrEnum):
    """
    Scaling strategy (queue or concurrency)
    """

    queue = "queue"
    concurrency = "concurrency"


class Policy(BaseModel):
    """
    Auto-scaling rules
    """

    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type2 | None, Field(description="Scaling strategy (queue or concurrency)")] = (
        None
    )
    value: Annotated[
        int | None,
        Field(description="Threshold value (seconds for queue, request count for concurrency)"),
    ] = None


class Image(BaseModel):
    """
    Container specifications
    """

    model_config = ConfigDict(populate_by_name=True)
    image: Annotated[str | None, Field(description="Container image URL")] = None
    auth_id: Annotated[str | None, Field(alias="authId", description="Registry credentials ID")] = (
        None
    )
    command: Annotated[str | None, Field(description="Startup command")] = None


class Type3(StrEnum):
    """
    Storage type (local or network)
    """

    local = "local"
    network = "network"


class VolumeMount2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type3 | None, Field(description="Storage type (local or network)")] = None
    id: Annotated[str | None, Field(description="Storage identifier (for network storage)")] = None
    size: Annotated[int | None, Field(description="Storage size in GB (for local storage)")] = None
    mount_path: Annotated[str | None, Field(alias="mountPath", description="Mount path")] = None


class Env3(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: str | None = None
    value: str | None = None


class Port1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port: Annotated[str | None, Field(description="Port number")] = None


class Worker(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(description="Worker identifier")] = None
    state: Annotated[dict[str, Any] | None, Field(description="Worker state information")] = None
    log: Annotated[str | None, Field(description="Worker log path")] = None
    metrics: Annotated[dict[str, Any] | None, Field(description="Worker metrics")] = None
    health: Annotated[dict[str, Any] | None, Field(description="Worker health status")] = None


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(description="Product identifier")] = None


class Healthy(BaseModel):
    """
    Health check settings
    """

    model_config = ConfigDict(populate_by_name=True)
    path: Annotated[str | None, Field(description="Health check endpoint path")] = None


class EndpointDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str | None, Field(description="Unique endpoint identifier")] = None
    name: Annotated[str | None, Field(description="Display name for the endpoint")] = None
    app_name: Annotated[
        str | None, Field(alias="appName", description="Associated application name")
    ] = None
    url: Annotated[
        str | None,
        Field(description="Endpoint URL. You can access your HTTP service via this URL"),
    ] = None
    state: Annotated[State | None, Field(description="Status details")] = None
    worker_config: Annotated[
        WorkerConfig | None,
        Field(alias="workerConfig", description="Worker scaling configuration"),
    ] = None
    policy: Annotated[Policy | None, Field(description="Auto-scaling rules")] = None
    image: Annotated[Image | None, Field(description="Container specifications")] = None
    rootfs_size: Annotated[
        int | None, Field(alias="rootfsSize", description="System disk size in GB")
    ] = None
    volume_mounts: Annotated[
        list[VolumeMount2] | None, Field(alias="volumeMounts", description="Storage mounts")
    ] = None
    envs: Annotated[list[Env3] | None, Field(description="Environment variables")] = None
    ports: Annotated[list[Port1] | None, Field(description="HTTP port configurations")] = None
    workers: Annotated[list[Worker] | None, Field(description="Active worker details")] = None
    products: Annotated[list[Product] | None, Field(description="Associated product IDs")] = None
    healthy: Annotated[Healthy | None, Field(description="Health check settings")] = None
    cluster_id: Annotated[
        str | None, Field(alias="clusterID", description="Cluster location for cloud storage")
    ] = None
    log: Annotated[str | None, Field(description="Endpoint logging path")] = None


class WorkerConfig1(BaseModel):
    """
    Worker scaling specification
    """

    model_config = ConfigDict(populate_by_name=True)
    min_num: Annotated[int, Field(alias="minNum", description="Minimum worker count")]
    max_num: Annotated[int, Field(alias="maxNum", description="Maximum worker count")]
    free_timeout: Annotated[int, Field(alias="freeTimeout", description="Idle timeout in seconds")]
    max_concurrent: Annotated[
        int, Field(alias="maxConcurrent", description="Request concurrency limit")
    ]
    gpu_num: Annotated[int, Field(alias="gpuNum", description="GPUs per worker")]


class Ports(BaseModel):
    """
    HTTP port configuration (1-65535, excluding 2222-2224)
    """

    model_config = ConfigDict(populate_by_name=True)
    port: Annotated[str, Field(description="Port number")]


class Type4(StrEnum):
    """
    Scaling strategy
    """

    queue = "queue"
    concurrency = "concurrency"


class Policy1(BaseModel):
    """
    Auto-scaling rules
    """

    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type4, Field(description="Scaling strategy")]
    value: Annotated[
        int, Field(description="Threshold value (seconds for queue, request count for concurrency)")
    ]


class Image1(BaseModel):
    """
    Container image details
    """

    model_config = ConfigDict(populate_by_name=True)
    image: Annotated[str, Field(description="Container image URL", max_length=511)]
    auth_id: Annotated[
        str | None,
        Field(alias="authId", description="Private registry credentials ID", max_length=255),
    ] = None
    command: Annotated[
        str | None, Field(description="Container startup command", max_length=2047)
    ] = None


class Product1(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Product ID")]


class Type5(StrEnum):
    """
    Storage type
    """

    local = "local"
    network = "network"


class VolumeMount3(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type5, Field(description="Storage type")]
    size: Annotated[int | None, Field(description="Local storage only, fixed at 30 GB")] = None
    id: Annotated[str | None, Field(description="Network storage only")] = None
    mount_path: Annotated[str, Field(alias="mountPath", description="Mount path", max_length=255)]


class Env4(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: str
    value: str


class Healthy1(BaseModel):
    """
    Health check configuration
    """

    model_config = ConfigDict(populate_by_name=True)
    path: Annotated[str, Field(description="HTTP health check endpoint")]


class Endpoint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str | None, Field(description="Endpoint identifier", max_length=220)] = None
    app_name: Annotated[
        str | None,
        Field(alias="appName", description="URL component (defaults to Endpoint ID if omitted)"),
    ] = None
    worker_config: Annotated[
        WorkerConfig1, Field(alias="workerConfig", description="Worker scaling specification")
    ]
    ports: Annotated[
        Ports, Field(description="HTTP port configuration (1-65535, excluding 2222-2224)")
    ]
    policy: Annotated[Policy1, Field(description="Auto-scaling rules")]
    image: Annotated[Image1, Field(description="Container image details")]
    products: Annotated[list[Product1], Field(description="Product identifiers")]
    rootfs_size: Annotated[
        int, Field(alias="rootfsSize", description="System disk size in GB (fixed at 100)")
    ]
    volume_mounts: Annotated[
        list[VolumeMount3], Field(alias="volumeMounts", description="Storage configuration")
    ]
    cluster_id: Annotated[
        str | None, Field(alias="clusterID", description="Required for cloud storage mounting")
    ] = None
    envs: Annotated[list[Env4] | None, Field(description="Environment variable pairs")] = None
    healthy: Annotated[Healthy1, Field(description="Health check configuration")]


class CreateEndpointRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    endpoint: Endpoint


class WorkerConfigItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    min_num: Annotated[int, Field(alias="minNum", description="Minimum worker count")]
    max_num: Annotated[int, Field(alias="maxNum", description="Maximum worker count")]
    free_timeout: Annotated[int, Field(alias="freeTimeout", description="Idle timeout (seconds)")]
    max_concurrent: Annotated[
        int, Field(alias="maxConcurrent", description="Request concurrency limit")
    ]
    gpu_num: Annotated[int, Field(alias="gpuNum", description="GPUs allocated per worker")]


class Port2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port: Annotated[str, Field(description="Port number")]


class Type6(StrEnum):
    """
    Scaling strategy
    """

    queue = "queue"
    concurrency = "concurrency"


class PolicyItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type6, Field(description="Scaling strategy")]
    value: Annotated[
        int, Field(description="Threshold value (seconds for queue, request count for concurrency)")
    ]


class ImageItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    image: Annotated[str, Field(description="Container image URL", max_length=511)]
    auth_id: Annotated[
        str | None,
        Field(alias="authId", description="Private registry credentials ID", max_length=255),
    ] = None
    command: Annotated[
        str | None, Field(description="Container startup command", max_length=2047)
    ] = None


class Type7(StrEnum):
    """
    Storage type
    """

    local = "local"
    network = "network"


class VolumeMount4(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type7, Field(description="Storage type")]
    size: Annotated[int | None, Field(description="Local storage size (fixed at 30 GB)")] = None
    id: Annotated[str | None, Field(description="Network storage identifier")] = None
    mount_path: Annotated[str, Field(alias="mountPath", description="Mount path", max_length=255)]


class HealthyItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    path: Annotated[str, Field(description="Health verification endpoint path")]


class UpdateEndpointRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str | None, Field(description="Display name for the endpoint")] = None
    cluster_id: Annotated[
        str | None,
        Field(
            alias="clusterID",
            description="Cluster information (required when mounting cloud storage)",
            max_length=255,
        ),
    ] = None
    worker_config: Annotated[
        list[WorkerConfigItem],
        Field(alias="workerConfig", description="Worker scaling configuration"),
    ]
    ports: Annotated[
        list[Port2], Field(description="HTTP port (range 1-65535, excluding 2222-2224)")
    ]
    policy: Annotated[list[PolicyItem], Field(description="Auto-scaling policy")]
    image: Annotated[list[ImageItem], Field(description="Container image configuration")]
    volume_mounts: Annotated[
        list[VolumeMount4] | None, Field(alias="volumeMounts", description="Storage mounts")
    ] = None
    envs: Annotated[list[Env4] | None, Field(description="Environment variables")] = None
    healthy: Annotated[
        list[HealthyItem] | None, Field(description="Health check configuration")
    ] = None


class Type8(StrEnum):
    """
    Job category
    """

    save_image = "saveImage"
    instance_migrate = "instanceMigrate"
    auto_instance_migrate = "autoInstanceMigrate"


class Env6(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: str | None = None
    value: str | None = None


class State1(BaseModel):
    """
    Status information
    """

    model_config = ConfigDict(populate_by_name=True)
    state: Annotated[str | None, Field(description="Job state")] = None
    error: Annotated[str | None, Field(description="Error code")] = None
    message: Annotated[str | None, Field(description="Error message")] = None


class JobModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(alias="Id", description="Unique job identifier")]
    user: Annotated[str, Field(description="User ID who created the job")]
    type: Annotated[Type8, Field(description="Job category")]
    envs: Annotated[list[Env6] | None, Field(description="Environmental variables")] = None
    state: Annotated[State1, Field(description="Status information")]
    log_address: Annotated[
        str | None, Field(alias="logAddress", description="URL for accessing execution logs")
    ] = None
    created_at: Annotated[
        str, Field(alias="createdAt", description="Job creation timestamp (Unix seconds)")
    ]
    instance_id: Annotated[
        str, Field(alias="instanceId", description="Associated GPU instance identifier")
    ]


class SaveImageRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    instance_id: Annotated[
        str,
        Field(
            alias="instanceId",
            description="The identifier for the compute instance",
            max_length=255,
            min_length=1,
        ),
    ]
    image: Annotated[
        str,
        Field(
            description="Complete image reference with registry, repository, and tag",
            max_length=4095,
            min_length=1,
        ),
    ]
    registry_auth_id: Annotated[
        str | None,
        Field(
            alias="registryAuthId",
            description="Authentication credentials for private registries (omit for public or platform registries)",
        ),
    ] = None


class State2(StrEnum):
    """
    Task state.
    """

    pending = "Pending"
    running = "Running"
    succeeded = "Succeeded"
    failed = "Failed"


class ImagePrewarmProduct(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    product_id: Annotated[str, Field(alias="productId", description="Product ID.")]
    product_name: Annotated[str, Field(alias="productName", description="Product name.")]


class CreateImagePrewarmRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    image_url: Annotated[
        str,
        Field(
            alias="imageUrl", description="Image address to prewarm.", max_length=500, min_length=1
        ),
    ]
    repository_auth: Annotated[
        str | None,
        Field(
            alias="repositoryAuth",
            description="Image registry authentication ID (required for private registries).",
        ),
    ] = None
    cluster_id: Annotated[
        str, Field(alias="clusterId", description="Cluster ID where the image should be prewarmed.")
    ]
    product_ids: Annotated[
        list[str] | None,
        Field(
            alias="productIds",
            description="Product IDs to prewarm on. Leave empty to prewarm globally in the cluster.",
        ),
    ] = None
    note: Annotated[str | None, Field(description="Task note or description.")] = None


class CreateImagePrewarmResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Created prewarm task ID.")]


class UpdateImagePrewarmRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Prewarm task ID.")]
    note: Annotated[str | None, Field(description="Task note.")] = None


class DeleteImagePrewarmRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ids: Annotated[list[str], Field(description="IDs of prewarm tasks to delete.", min_length=1)]


class RepositoryAuth(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Authentication identifier")]
    name: Annotated[str, Field(description="Registry name/URL")]
    username: Annotated[str, Field(description="Registry username")]
    password: Annotated[SecretStr, Field(description="Registry password (returned as masked)")]


class CreateRepositoryAuthRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str, Field(description="Registry name/URL", max_length=500, min_length=1)]
    username: Annotated[str, Field(description="Registry username", max_length=500, min_length=1)]
    password: Annotated[
        SecretStr,
        Field(
            description="Registry password (stored securely, not logged)",
            max_length=500,
            min_length=1,
        ),
    ]


class DeleteRepositoryAuthRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Authentication ID to delete")]


class State4(StrEnum):
    """
    Network status
    """

    creating = "creating"
    ready = "ready"


class State3(BaseModel):
    """
    Network operational status
    """

    model_config = ConfigDict(populate_by_name=True)
    state: Annotated[State4, Field(description="Network status")]
    error: Annotated[str | None, Field(description="Error details if creation fails")] = None


class Address(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(alias="Id", description="Instance identifier")]
    ip: Annotated[str, Field(alias="Ip", description="Instance IP address")]


class NetworkModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(alias="Id", description="VPC network identifier")]
    user: Annotated[str, Field(description="User account ID")]
    name: Annotated[str, Field(description="VPC network name")]
    state: Annotated[State3, Field(description="Network operational status")]
    segment: Annotated[str, Field(description="VPC network segment designation")]
    cluster_id: Annotated[
        str, Field(alias="clusterId", description="Associated cluster identifier")
    ]
    addresses: Annotated[
        list[Address], Field(alias="Addresses", description="Instances within the VPC network")
    ]
    create_time: Annotated[
        str,
        Field(alias="createTime", description="VPC network creation time (Unix timestamp format)"),
    ]


class CreateNetworkRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cluster_id: Annotated[
        str,
        Field(
            alias="clusterId",
            description="Target cluster ID (obtain via List Clusters API)",
            max_length=255,
            min_length=1,
        ),
    ]
    name: Annotated[
        str | None, Field(description="Custom VPC network name", max_length=30, min_length=0)
    ] = None


class UpdateNetworkRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    network_id: Annotated[
        str,
        Field(
            alias="networkId", description="VPC network ID to update", max_length=255, min_length=1
        ),
    ]
    name: Annotated[
        str | None, Field(description="Custom network name", max_length=30, min_length=1)
    ] = None


class DeleteNetworkRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    network_id: Annotated[
        str,
        Field(
            alias="networkId",
            description="VPC network ID to delete (ensure no instances are under this VPC network before deletion)",
            max_length=255,
            min_length=1,
        ),
    ]


class NetworkStorageModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    storage_id: Annotated[
        str | None, Field(alias="storageId", description="Unique storage identifier")
    ] = None
    storage_name: Annotated[
        str | None, Field(alias="storageName", description="User-defined storage name")
    ] = None
    storage_size: Annotated[
        int | None, Field(alias="storageSize", description="Storage capacity measurement")
    ] = None
    cluster_id: Annotated[
        str | None, Field(alias="clusterId", description="Associated cluster identifier")
    ] = None
    cluster_name: Annotated[
        str | None, Field(alias="clusterName", description="Associated cluster name")
    ] = None
    price: Annotated[str | None, Field(description="Storage pricing information")] = None


class CreateNetworkStorageRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cluster_id: Annotated[str, Field(alias="clusterId", description="Identifier for the cluster")]
    storage_name: Annotated[
        str, Field(alias="storageName", description="Name assigned to the storage resource")
    ]
    storage_size: Annotated[
        int, Field(alias="storageSize", description="Capacity allocation for storage")
    ]


class UpdateNetworkStorageRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    storage_id: Annotated[
        str,
        Field(
            alias="storageId", description="Unique identifier distinguishing the storage resource"
        ),
    ]
    storage_name: Annotated[
        str, Field(alias="storageName", description="The display name assigned to the storage")
    ]
    storage_size: Annotated[
        int, Field(alias="storageSize", description="Capacity measurement in appropriate units")
    ]


class DeleteNetworkStorageRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    storage_id: Annotated[
        str,
        Field(alias="storageId", description="Identifier for the network storage to be removed"),
    ]


class Channel(StrEnum):
    """
    Template channel.
    """

    private = "private"
    official = "official"
    community = "community"


class TemplateVolume(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[str, Field(description="Volume type.")]
    size: Annotated[int, Field(description="Volume size (GB).")]
    mount_path: Annotated[str, Field(alias="mountPath", description="Volume mount path.")]


class Type9(StrEnum):
    """
    Exposed port type.
    """

    http = "http"
    tcp = "tcp"


class TemplatePort(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Annotated[Type9, Field(description="Exposed port type.")]
    ports: Annotated[
        list[int], Field(description="Exposed ports (maximum of 10 per entry).", max_length=10)
    ]


class TemplateEnvironmentVariable(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    key: Annotated[str, Field(description="Environment variable key.")]
    value: Annotated[str, Field(description="Environment variable value.")]


class Type10(StrEnum):
    """
    Tool type.
    """

    http = "http"
    tcp = "tcp"


class TemplateTool(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str, Field(description='Tool name (e.g., "Jupyter").')]
    describe: Annotated[str | None, Field(description="Tool description.")] = None
    port: Annotated[int, Field(description="Port number for the tool.")]
    type: Annotated[Type10, Field(description="Tool type.")]


class TemplateCreatePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str, Field(description="Template name.")]
    readme: Annotated[str, Field(description="Template README content (Markdown).")]
    type: Annotated[Literal["instance"], Field(description="Template type.")]
    channel: Annotated[Channel, Field(description="Template channel.")]
    image: Annotated[str, Field(description="Docker image address for instance startup.")]
    start_command: Annotated[
        str, Field(alias="startCommand", description="Startup command for the instance.")
    ]
    rootfs_size: Annotated[
        int, Field(alias="rootfsSize", description="Root filesystem storage size (GB).")
    ]
    ports: Annotated[list[TemplatePort], Field(description="Exposed port settings.")]
    volumes: Annotated[list[TemplateVolume], Field(description="Volume settings.")]
    envs: Annotated[
        list[TemplateEnvironmentVariable],
        Field(description="Environment variables injected into the instance."),
    ]


class CreateTemplateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template_id: Annotated[
        str, Field(alias="templateId", description="ID of the created template.")
    ]


class DeleteTemplateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template_id: Annotated[str, Field(alias="templateId", description="Template ID to delete.")]


class DeleteTemplateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template_id: Annotated[
        str, Field(alias="templateId", description="ID of the deleted template.")
    ]


class SSHKey(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="SSH key ID")]
    name: Annotated[str, Field(description="SSH key name")]
    public_key: Annotated[str, Field(alias="publicKey", description="SSH public key content")]
    created_at: Annotated[
        str | None, Field(alias="createdAt", description="Creation timestamp")
    ] = None


class ListSSHKeysResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[list[SSHKey], Field(description="List of SSH keys")]


class CreateSSHKeyRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[str, Field(description="SSH key name", max_length=255, min_length=1)]
    public_key: Annotated[
        str, Field(alias="publicKey", description="SSH public key content", min_length=1)
    ]


class SSHEndpoint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user: Annotated[str, Field(description="SSH username")]
    host: Annotated[str, Field(description="SSH host address")]
    port: Annotated[int, Field(description="SSH port number")]
    command: Annotated[str | None, Field(description="Full SSH command")] = None


class ListEndpointsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    endpoints: Annotated[
        list[EndpointDetail], Field(description="Collection of endpoint configurations")
    ]
    total: Annotated[int, Field(description="Count of all available results")]


class ListJobsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    jobs: Annotated[list[JobModel], Field(description="Collection of job records")]
    total: Annotated[int, Field(description="Count of matching jobs")]


class ImagePrewarmTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(description="Prewarm task ID.")]
    image_name: Annotated[
        str,
        Field(
            alias="imageName",
            description="Image name (last segment of the image URL without the tag).",
        ),
    ]
    image_url: Annotated[str, Field(alias="imageUrl", description="Image URL.")]
    repository_auth: Annotated[
        str | None,
        Field(alias="repositoryAuth", description="Image registry authentication ID."),
    ] = None
    cluster_id: Annotated[str, Field(alias="clusterId", description="Cluster ID.")]
    cluster_name: Annotated[str, Field(alias="clusterName", description="Cluster name.")]
    products: Annotated[list[ImagePrewarmProduct], Field(description="Products to prewarm.")]
    image_size: Annotated[
        str | None, Field(alias="imageSize", description="Image size in bytes.")
    ] = None
    create_time: Annotated[
        str,
        Field(alias="createTime", description="Task creation time (Unix timestamp in seconds)."),
    ]
    state: Annotated[State2, Field(description="Task state.")]
    complete_time: Annotated[
        str | None,
        Field(
            alias="completeTime", description="Task completion time (Unix timestamp in seconds)."
        ),
    ] = None
    note: Annotated[str | None, Field(description="Task note.")] = None
    reason: Annotated[
        list[str] | None, Field(description="Reason messages when the task fails.")
    ] = None


class ListRepositoryAuthsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[
        list[RepositoryAuth], Field(description="List of container registry authentications")
    ]


class ListNetworksResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    networks: Annotated[list[NetworkModel], Field(description="List of VPC networks")]
    total: Annotated[int, Field(description="Total count of VPC networks")]


class ListNetworkStoragesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[
        list[NetworkStorageModel] | None, Field(description="Collection of storage records")
    ] = None
    total: Annotated[int | None, Field(description="Total count of matching storages")] = None


class Template(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Annotated[str, Field(alias="Id", description="Unique template identifier.")]
    create_time: Annotated[
        AwareDatetime | None, Field(alias="createTime", description="Template creation time.")
    ] = None
    user: Annotated[str | None, Field(description="ID of the user who created the template.")] = (
        None
    )
    tools: Annotated[
        list[TemplateTool] | None, Field(description="Tools enabled for the template.")
    ] = None
    name: Annotated[str, Field(description="Template name.")]
    readme: Annotated[str | None, Field(description="Template README content (Markdown).")] = None
    type: Annotated[Literal["instance"], Field(description="Template type.")]
    channel: Annotated[Channel, Field(description="Template channel.")]
    image: Annotated[str, Field(description="Docker image address for instance startup.")]
    image_auth: Annotated[
        str | None,
        Field(
            alias="imageAuth",
            description="Credentials for the Docker image registry to pull private images.",
        ),
    ] = None
    start_command: Annotated[
        str, Field(alias="startCommand", description="Startup command for the instance.")
    ]
    rootfs_size: Annotated[
        int, Field(alias="rootfsSize", description="Root filesystem storage size (GB).")
    ]
    volumes: Annotated[list[TemplateVolume] | None, Field(description="Volume settings.")] = None
    ports: Annotated[list[TemplatePort] | None, Field(description="Exposed port settings.")] = None
    envs: Annotated[
        list[TemplateEnvironmentVariable] | None,
        Field(description="Environment variables injected into the instance."),
    ] = None


class CreateTemplateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template: Annotated[TemplateCreatePayload, Field(description="Template settings.")]


class ListImagePrewarmTasksResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Annotated[list[ImagePrewarmTask], Field(description="List of prewarm tasks.")]
    total: Annotated[int, Field(description="Total number of tasks.")]


class ListTemplatesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template: Annotated[list[Template], Field(description="List of templates.")]
    page_size: Annotated[
        int, Field(alias="pageSize", description="Maximum number of entries returned on one page.")
    ]
    page_num: Annotated[int, Field(alias="pageNum", description="Current page index.")]
    total: Annotated[int, Field(description="Total number of templates.")]


class GetTemplateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template: Annotated[Template, Field(description="Template details.")]
