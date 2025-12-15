"""GPU API client with resource-based structure."""

from typing import TYPE_CHECKING

from .resources.gpu import (
    AsyncClusters,
    AsyncEndpoints,
    AsyncImagePrewarm,
    AsyncInstances,
    AsyncJobs,
    AsyncMetrics,
    AsyncNetworks,
    AsyncProducts,
    AsyncRegistries,
    AsyncSSHKeys,
    AsyncStorages,
    AsyncTemplates,
    Clusters,
    Endpoints,
    ImagePrewarm,
    Instances,
    Jobs,
    Metrics,
    Networks,
    Products,
    Registries,
    SSHKeys,
    Storages,
    Templates,
)

if TYPE_CHECKING:
    import httpx


class GpuClient:
    """Synchronous GPU API client with resource-based structure."""

    def __init__(self, client: "httpx.Client") -> None:
        """Initialize the GPU client with all resources.

        Args:
            client: The httpx client instance
        """
        # Initialize all GPU API resources
        self.clusters = Clusters(client)
        self.endpoints = Endpoints(client)
        self.image_prewarm = ImagePrewarm(client)
        self.instances = Instances(client)
        self.jobs = Jobs(client)
        self.metrics = Metrics(client)
        self.networks = Networks(client)
        self.products = Products(client)
        self.registries = Registries(client)
        self.ssh_keys = SSHKeys(client)
        self.storages = Storages(client)
        self.templates = Templates(client)


class AsyncGpuClient:
    """Asynchronous GPU API client with resource-based structure."""

    def __init__(self, client: "httpx.AsyncClient") -> None:
        """Initialize the async GPU client with all resources.

        Args:
            client: The httpx async client instance
        """
        # Initialize all async GPU API resources
        self.clusters = AsyncClusters(client)
        self.endpoints = AsyncEndpoints(client)
        self.image_prewarm = AsyncImagePrewarm(client)
        self.instances = AsyncInstances(client)
        self.jobs = AsyncJobs(client)
        self.metrics = AsyncMetrics(client)
        self.networks = AsyncNetworks(client)
        self.products = AsyncProducts(client)
        self.registries = AsyncRegistries(client)
        self.ssh_keys = AsyncSSHKeys(client)
        self.storages = AsyncStorages(client)
        self.templates = AsyncTemplates(client)
