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
from novita.generated.models import (
    BillingMode,
    CreateInstanceRequest,
    CreateInstanceResponse,
    CreateSSHKeyRequest,
    EditInstanceRequest,
    GPUProduct,
    InstanceInfo,
    Kind,
    ListGPUProductsResponse,
    ListInstancesResponse,
    ListSSHKeysResponse,
    Port,
    SaveImageRequest,
    SSHEndpoint,
    SSHKey,
    Type,
    UpgradeInstanceRequest,
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
    # SSH Keys
    "SSHKey",
    "SSHEndpoint",
    "CreateSSHKeyRequest",
    "ListSSHKeysResponse",
]
