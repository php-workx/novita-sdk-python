"""Smoke tests for package imports and public API surface."""


def test_import_novita():
    """Test that the novita package can be imported."""
    import novita

    assert hasattr(novita, "__version__")
    assert hasattr(novita, "__all__")


def test_import_clients():
    """Test that clients can be imported from top-level."""
    from novita import AsyncNovitaClient, NovitaClient

    assert NovitaClient is not None
    assert AsyncNovitaClient is not None


def test_import_exceptions():
    """Test that exceptions can be imported from top-level."""
    from novita import (
        APIError,
        AuthenticationError,
        BadRequestError,
        NotFoundError,
        NovitaError,
        RateLimitError,
        TimeoutError,
    )

    # All exceptions inherit from the base NovitaError
    assert issubclass(AuthenticationError, NovitaError)
    assert issubclass(RateLimitError, NovitaError)
    assert issubclass(BadRequestError, NovitaError)
    assert issubclass(NotFoundError, NovitaError)
    assert issubclass(TimeoutError, NovitaError)
    assert issubclass(APIError, NovitaError)


def test_import_generated_models():
    """Test that generated models can be imported."""
    from novita.generated.models import GPUProduct, InstanceInfo

    assert GPUProduct is not None
    assert InstanceInfo is not None
    # Verify GPUProduct has expected fields
    assert "id" in GPUProduct.model_fields
    assert "name" in GPUProduct.model_fields
    assert "regions" in GPUProduct.model_fields
    assert "cpu_per_gpu" in GPUProduct.model_fields
    assert "memory_per_gpu" in GPUProduct.model_fields
    assert "available_deploy" in GPUProduct.model_fields


def test_import_models_from_toplevel():
    """Test that commonly used models are re-exported at top level."""
    from novita import (
        CreateInstanceRequest,
        GPUProduct,
        InstanceInfo,
        Kind,
    )

    assert GPUProduct is not None
    assert InstanceInfo is not None
    assert CreateInstanceRequest is not None
    assert Kind is not None


def test_client_has_resource_tree():
    """Test that client has expected resource tree structure."""
    from novita import NovitaClient

    client = NovitaClient(api_key="test-key")
    try:
        # Verify resource tree
        assert hasattr(client, "gpu")
        assert hasattr(client.gpu, "clusters")
        assert hasattr(client.gpu, "endpoints")
        assert hasattr(client.gpu, "image_prewarm")
        assert hasattr(client.gpu, "instances")
        assert hasattr(client.gpu, "jobs")
        assert hasattr(client.gpu, "metrics")
        assert hasattr(client.gpu, "networks")
        assert hasattr(client.gpu, "products")
        assert hasattr(client.gpu, "registries")
        assert hasattr(client.gpu, "storages")
        assert hasattr(client.gpu, "templates")
        # Spot-check a few methods to ensure resources are initialized
        assert hasattr(client.gpu.products, "list")
        assert hasattr(client.gpu.instances, "list")
        assert hasattr(client.gpu.instances, "create")
    finally:
        client.close()


async def test_async_client_context_manager():
    """Test that AsyncNovitaClient supports async context manager."""
    from novita import AsyncNovitaClient

    async with AsyncNovitaClient(api_key="test-key") as client:
        assert hasattr(client, "gpu")
        assert hasattr(client.gpu, "clusters")
        assert hasattr(client.gpu, "endpoints")
        assert hasattr(client.gpu, "image_prewarm")
        assert hasattr(client.gpu, "instances")
        assert hasattr(client.gpu, "jobs")
        assert hasattr(client.gpu, "metrics")
        assert hasattr(client.gpu, "networks")
        assert hasattr(client.gpu, "products")
        assert hasattr(client.gpu, "registries")
        assert hasattr(client.gpu, "storages")
        assert hasattr(client.gpu, "templates")
        # Spot-check a method to ensure resources are initialized
        assert hasattr(client.gpu.products, "list")


def test_py_typed_marker_exists():
    """Test that py.typed marker exists for type checking support."""
    import importlib.resources

    import novita

    # Check py.typed exists in the package
    files = importlib.resources.files(novita)
    py_typed = files.joinpath("py.typed")
    assert py_typed.is_file(), "py.typed marker should exist for PEP 561 compliance"
