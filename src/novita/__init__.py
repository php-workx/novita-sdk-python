"""Novita AI SDK for Python."""

from novita.client import AsyncNovitaClient, NovitaClient
from novita.exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    NovitaError,
    RateLimitError,
    TimeoutError,
)
from novita.models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    EndpointStatus,
    InstanceActionResponse,
    InstanceInfo,
    GPUProduct,
    InstanceType,
    ListInstancesResponse,
    ListGPUProductsResponse,
    UpdateInstanceRequest,
)

__version__ = "0.1.0"

__all__ = [
    # Clients
    "NovitaClient",
    "AsyncNovitaClient",
    # Exceptions
    "NovitaError",
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
    "TimeoutError",
    # Models
    "CreateInstanceRequest",
    "CreateInstanceResponse",
    "UpdateInstanceRequest",
    "InstanceInfo",
    "ListInstancesResponse",
    "InstanceActionResponse",
    "GPUProduct",
    "ListGPUProductsResponse",
    "InstanceType",
    "EndpointStatus",
]
