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
        response = client.gpu.endpoints.list(page_size=10, page_num=0)  # type: ignore[call-arg]

        assert response is not None
        assert hasattr(response, "data")
        assert hasattr(response, "total")
        assert isinstance(response.data, list)
        assert isinstance(response.total, int)

    def test_list_endpoints_with_pagination(self, client: NovitaClient) -> None:
        """Test listing endpoints with different pagination parameters."""
        # Get first page
        page1 = client.gpu.endpoints.list(page_size=5, page_num=0)  # type: ignore[call-arg]
        assert page1 is not None
        assert len(page1.data) <= 5  # type: ignore[attr-defined]

        # Get second page
        page2 = client.gpu.endpoints.list(page_size=5, page_num=1)  # type: ignore[call-arg]
        assert page2 is not None
        assert len(page2.data) <= 5  # type: ignore[attr-defined]

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
        endpoints = client.gpu.endpoints.list(page_size=1, page_num=0)  # type: ignore[call-arg]

        if len(endpoints.data) > 0:  # type: ignore[attr-defined]
            endpoint_id = endpoints.data[0].id  # type: ignore[attr-defined]

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
        endpoints = client.gpu.endpoints.list(page_size=1, page_num=0)  # type: ignore[call-arg]

        if len(endpoints.data) > 0:  # type: ignore[attr-defined]
            endpoint = endpoints.data[0]  # type: ignore[attr-defined]

            # Required fields
            assert hasattr(endpoint, "id")
            assert hasattr(endpoint, "name")
            assert hasattr(endpoint, "status")

            # Verify status is valid
            valid_statuses = ["pending", "running", "stopped", "error"]
            assert endpoint.status in valid_statuses


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
