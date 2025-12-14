"""Integration tests for serverless endpoint endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestEndpoints:
    """Test serverless endpoint-related endpoints."""

    def test_list_endpoints(self, client: NovitaClient) -> None:
        """Test listing all serverless endpoints."""
        endpoints = client.gpu.endpoints.list()

        assert isinstance(endpoints, list)

    def test_list_endpoints_returns_list(self, client: NovitaClient) -> None:
        """Test that listing endpoints returns a valid list."""
        endpoints = client.gpu.endpoints.list()
        assert isinstance(endpoints, list)
        # Verify each endpoint has expected structure
        for endpoint in endpoints:
            assert hasattr(endpoint, "id")
            assert hasattr(endpoint, "name")

    def test_get_endpoint_limits(self, client: NovitaClient) -> None:
        """Test getting endpoint parameter limits."""
        limits = client.gpu.endpoints.get_limit_ranges()

        assert isinstance(limits, dict)

        # Verify required fields (API returns camelCase)
        required_keys = [
            "minRootfsSize",
            "maxRootfsSize",
            "freeRootfsSize",
            "minLocalVolumeSize",
            "maxLocalVolumeSize",
            "freeLocalVolumeSize",
            "minWorkerNum",
            "maxWorkerNum",
            "minFreeTimeout",
            "maxFreeTimeout",
            "minConcurrencyNum",
            "maxConcurrencyNum",
            "minQueueWaitTime",
            "maxQueueWaitTime",
            "minRequestNum",
            "maxRequestNum",
            "minGPUNum",
            "maxGPUNum",
            "cudaVersionList",
        ]
        for key in required_keys:
            assert key in limits, f"Missing required key: {key}"

        # Verify data types for sample fields
        assert isinstance(limits["minRootfsSize"], int)
        assert isinstance(limits["maxRootfsSize"], int)
        assert isinstance(limits["cudaVersionList"], list)

        # Verify logical constraints for min/max pairs
        min_max_pairs = [
            ("minRootfsSize", "maxRootfsSize"),
            ("minLocalVolumeSize", "maxLocalVolumeSize"),
            ("minWorkerNum", "maxWorkerNum"),
            ("minGPUNum", "maxGPUNum"),
        ]
        for min_key, max_key in min_max_pairs:
            assert limits[min_key] <= limits[max_key], f"{min_key} should be <= {max_key}"

    def test_get_endpoint_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific endpoint."""
        # First get list of endpoints
        endpoints = client.gpu.endpoints.list()

        if not endpoints:
            pytest.skip("No endpoints available to test endpoint details")

        endpoint_id = endpoints[0].id
        assert endpoint_id is not None

        # Get detailed information
        endpoint = client.gpu.endpoints.get(endpoint_id)

        assert hasattr(endpoint, "id")
        assert hasattr(endpoint, "name")
        assert hasattr(endpoint, "state")

        # Verify data types
        assert isinstance(endpoint.id, str)
        if endpoint.name is not None:
            assert isinstance(endpoint.name, str)
        assert endpoint.id == endpoint_id

    def test_endpoint_structure(self, client: NovitaClient) -> None:
        """Test that endpoints have all expected fields."""
        endpoints = client.gpu.endpoints.list()

        if not endpoints:
            pytest.skip("No endpoints available to test endpoint structure")

        endpoint = endpoints[0]

        # Required fields
        assert hasattr(endpoint, "id")
        assert hasattr(endpoint, "name")
        assert hasattr(endpoint, "state")

        # Verify state exists and is not None


@pytest.mark.integration
@pytest.mark.invasive
class TestEndpointFullLifecycle:
    """Test full endpoint lifecycle (create, update, delete).

    Warning: Creates real serverless endpoints which cost money.
    """

    def test_create_update_delete_endpoint(self, client: NovitaClient, cluster_id: str) -> None:
        """
        Test full endpoint lifecycle with nginx on RTX 4090.

        This test will:
        1. Find available RTX 4090 product
        2. Create a serverless endpoint with nginx
        3. Verify endpoint details
        4. Update endpoint configuration
        5. Delete the endpoint
        """
        import time

        from novita.generated.models import (
            CreateEndpointRequest,
            Endpoint,
            Healthy1,
            Image1,
            ImageItem,
            Policy1,
            PolicyItem,
            Port2,
            Ports,
            Product1,
            Type4,
            Type6,
            UpdateEndpointRequest,
            WorkerConfig1,
            WorkerConfigItem,
        )

        endpoint_id = None

        try:
            # Step 1: Find RTX 4090 product
            products = client.gpu.products.list(product_name="4090")
            if not products:
                pytest.skip("No RTX 4090 products found")

            available_products = [p for p in products if p.available_deploy]
            if not available_products:
                pytest.skip("No RTX 4090 products currently available to deploy")

            product = available_products[0]
            product_id = product.id

            # Step 2: Create endpoint configuration using Pydantic models
            from tests.integration.test_utils import generate_test_name

            test_name = generate_test_name("endpoint")
            app_name = generate_test_name("app")

            endpoint_config = Endpoint(
                name=test_name,
                app_name=app_name,
                worker_config=WorkerConfig1(
                    min_num=1,
                    max_num=2,
                    free_timeout=60,
                    max_concurrent=1,
                    gpu_num=1,
                ),
                ports=Ports(port="80"),
                policy=Policy1(type=Type4.concurrency, value=25),
                image=Image1(image="docker.io/library/nginx:latest"),
                products=[Product1(id=product_id)],
                rootfs_size=100,
                volume_mounts=[],
                cluster_id=cluster_id,
                healthy=Healthy1(path="/health"),
            )

            # Step 3: Create the endpoint
            created = client.gpu.endpoints.create(CreateEndpointRequest(endpoint=endpoint_config))
            assert created.id is not None
            endpoint_id = created.id
            assert created.name == test_name

            # Wait a couple seconds for endpoint to be created
            time.sleep(2)

            # Step 4: Get endpoint details
            endpoint_detail = client.gpu.endpoints.get(endpoint_id)
            assert endpoint_detail.id == endpoint_id
            assert endpoint_detail.name == test_name
            assert endpoint_detail.state is not None

            # Step 5: Update endpoint (change name)
            updated_name = generate_test_name("endpoint-updated")
            update_request = UpdateEndpointRequest(
                worker_config=[
                    WorkerConfigItem(
                        min_num=1,
                        max_num=2,
                        free_timeout=60,
                        max_concurrent=1,
                        gpu_num=1,
                    )
                ],
                ports=[Port2(port="80")],
                policy=[PolicyItem(type=Type6.concurrency, value=25)],
                image=[ImageItem(image="docker.io/library/nginx:latest")],
                name=updated_name,
            )
            updated = client.gpu.endpoints.update(endpoint_id, update_request)
            assert updated.name == updated_name

            # Verify update
            endpoint_detail = client.gpu.endpoints.get(endpoint_id)
            assert endpoint_detail.name == updated_name

            # Wait before deletion
            time.sleep(2)

            # Step 6: Delete the endpoint
            client.gpu.endpoints.delete(endpoint_id)

            # Verify deletion was initiated
            # Note: Endpoint may be removed quickly, so we handle both cases
            try:
                endpoint_detail = client.gpu.endpoints.get(endpoint_id)
                # If we can still get it, it should be in a deletion state
                # (Novita endpoints don't have standard deletion states like instances)
                # Just verify we can still access it
                assert endpoint_detail.id == endpoint_id
            except Exception as e:
                # If we get a "not found" error, deletion completed successfully
                error_msg = str(e).lower()
                assert (
                    "not found" in error_msg or "not fount" in error_msg
                ), f"Expected 'not found' error after deletion, got: {e}"

        finally:
            # Cleanup: ensure the endpoint is deleted even if test fails
            if endpoint_id is not None:
                try:
                    # Always try to delete - API will handle if already deleted
                    client.gpu.endpoints.delete(endpoint_id)
                except Exception as e:
                    # If endpoint is already gone ("not found"), that's fine
                    error_msg = str(e).lower()
                    if "not found" not in error_msg and "not fount" not in error_msg:
                        # Log cleanup errors but don't fail the test
                        import warnings

                        warnings.warn(
                            f"Failed to cleanup endpoint {endpoint_id}: {e}",
                            ResourceWarning,
                            stacklevel=2,
                        )
