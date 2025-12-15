"""GPU API resources."""

from .base import AsyncBaseResource, BaseResource
from .clusters import AsyncClusters, Clusters
from .endpoints import AsyncEndpoints, Endpoints
from .image_prewarm import AsyncImagePrewarm, ImagePrewarm
from .instances import AsyncInstances, Instances
from .jobs import AsyncJobs, Jobs
from .metrics import AsyncMetrics, Metrics
from .networks import AsyncNetworks, Networks
from .products import AsyncProducts, Products
from .registries import AsyncRegistries, Registries
from .ssh_keys import AsyncSSHKeys, SSHKeys
from .storages import AsyncStorages, Storages
from .templates import AsyncTemplates, Templates

__all__ = [
    "BaseResource",
    "AsyncBaseResource",
    "Clusters",
    "AsyncClusters",
    "Endpoints",
    "AsyncEndpoints",
    "ImagePrewarm",
    "AsyncImagePrewarm",
    "Instances",
    "AsyncInstances",
    "Jobs",
    "AsyncJobs",
    "Metrics",
    "AsyncMetrics",
    "Networks",
    "AsyncNetworks",
    "Products",
    "AsyncProducts",
    "Registries",
    "AsyncRegistries",
    "SSHKeys",
    "AsyncSSHKeys",
    "Storages",
    "AsyncStorages",
    "Templates",
    "AsyncTemplates",
]
