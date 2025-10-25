"""GPU API resources."""

from .base import BaseResource, AsyncBaseResource
from .clusters import Clusters, AsyncClusters
from .endpoints import Endpoints, AsyncEndpoints
from .images import Images, AsyncImages
from .instances import Instances, AsyncInstances
from .jobs import Jobs, AsyncJobs
from .metrics import Metrics, AsyncMetrics
from .networks import Networks, AsyncNetworks
from .products import Products, AsyncProducts
from .registries import Registries, AsyncRegistries
from .storages import Storages, AsyncStorages
from .templates import Templates, AsyncTemplates

__all__ = [
    "BaseResource",
    "AsyncBaseResource",
    "Clusters",
    "AsyncClusters",
    "Endpoints",
    "AsyncEndpoints", 
    "Images",
    "AsyncImages",
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
    "Storages",
    "AsyncStorages",
    "Templates",
    "AsyncTemplates",
]