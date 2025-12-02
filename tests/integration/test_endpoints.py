"""Integration tests for serverless endpoint endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


class TestEndpoints:
    """Test serverless endpoint-related endpoints."""

    def test_list_endpoints(self, client: NovitaClient) -> None:
        """Test listing all serverless endpoints."""
        endpoints = client.gpu.endpoints.list()

        assert endpoints is not None
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

        assert limits is not None
        assert isinstance(limits, dict)

        # Verify required fields
        assert "min_rootfs_size" in limits
        assert "max_rootfs_size" in limits
        assert "free_rootfs_size" in limits
        assert "min_local_volume_size" in limits
        assert "max_local_volume_size" in limits
        assert "free_local_volume_size" in limits
        assert "min_worker_num" in limits
        assert "max_worker_num" in limits
        assert "min_free_timeout" in limits
        assert "max_free_timeout" in limits
        assert "min_concurrency_num" in limits
        assert "max_concurrency_num" in limits
        assert "min_queue_wait_time" in limits
        assert "max_queue_wait_time" in limits
        assert "min_request_num" in limits
        assert "max_request_num" in limits
        assert "min_gpu_num" in limits
        assert "max_gpu_num" in limits
        assert "cuda_version_list" in limits

        # Verify data types
        assert isinstance(limits["min_rootfs_size"], int)
        assert isinstance(limits["max_rootfs_size"], int)
        assert isinstance(limits["cuda_version_list"], list)

        # Verify logical constraints
        assert limits["min_rootfs_size"] <= limits["max_rootfs_size"]
        assert limits["min_local_volume_size"] <= limits["max_local_volume_size"]
        assert limits["min_worker_num"] <= limits["max_worker_num"]
        assert limits["min_gpu_num"] <= limits["max_gpu_num"]

    def test_get_endpoint_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific endpoint."""
        # First get list of endpoints
        endpoints = client.gpu.endpoints.list()

        if not endpoints:
            pytest.skip("No endpoints available to test endpoint details")

        endpoint_id = endpoints[0].id

        # Get detailed information
        endpoint = client.gpu.endpoints.get(endpoint_id)

        assert endpoint is not None
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
        assert endpoint.state is not None


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestEndpointLifecycle:
    """Test full endpoint lifecycle (create, update, delete)."""

    def test_create_update_delete_endpoint(self, client: NovitaClient, product_id: str) -> None:
        """
        Test full endpoint lifecycle.

        This test will:
        1. Create a new endpoint
        2. Wait for it to be running
        3. Update the endpoint
        4. Delete the endpoint

        TODO: Implement this test sequence
        """
        pass
