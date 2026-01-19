"""Novita AI SDK for Python."""

from importlib.metadata import version

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
from novita.generated.models import (
    BillingMode,
    CreateInstanceRequest,
    CreateInstanceResponse,
    EditInstanceRequest,
    GPUProduct,
    InstanceInfo,
    Kind,
    ListGPUProductsResponse,
    ListInstancesResponse,
    Port,
    SaveImageRequest,
    Type,
    UpgradeInstanceRequest,
)

__version__ = version("novita-sdk")

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
    "EditInstanceRequest",
    "UpgradeInstanceRequest",
    "SaveImageRequest",
    "InstanceInfo",
    "ListInstancesResponse",
    "GPUProduct",
    "ListGPUProductsResponse",
    "Kind",
    "BillingMode",
    "Port",
    "Type",
]
