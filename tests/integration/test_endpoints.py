"""Integration tests for serverless endpoint endpoints."""

import pytest


class TestEndpoints:
    """Test serverless endpoint-related endpoints."""

    def test_list_endpoints(self, client):
        """Test listing all serverless endpoints."""
        response = client.gpu.endpoints.list(page_size=10, page_num=0)

        assert response is not None
        assert hasattr(response, "data")
        assert hasattr(response, "total")
        assert isinstance(response.data, list)
        assert isinstance(response.total, int)

    def test_list_endpoints_with_pagination(self, client):
        """Test listing endpoints with different pagination parameters."""
        # Get first page
        page1 = client.gpu.endpoints.list(page_size=5, page_num=0)
        assert page1 is not None
        assert len(page1.data) <= 5

        # Get second page
        page2 = client.gpu.endpoints.list(page_size=5, page_num=1)
        assert page2 is not None
        assert len(page2.data) <= 5

    def test_get_endpoint_limits(self, client):
        """Test getting endpoint parameter limits."""
        limits = client.gpu.endpoints.get_limits()

        assert limits is not None

        # Verify required fields
        assert hasattr(limits, "min_rootfs_size")
        assert hasattr(limits, "max_rootfs_size")
        assert hasattr(limits, "free_rootfs_size")
        assert hasattr(limits, "min_local_volume_size")
        assert hasattr(limits, "max_local_volume_size")
        assert hasattr(limits, "free_local_volume_size")
        assert hasattr(limits, "min_worker_num")
        assert hasattr(limits, "max_worker_num")
        assert hasattr(limits, "min_free_timeout")
        assert hasattr(limits, "max_free_timeout")
        assert hasattr(limits, "min_concurrency_num")
        assert hasattr(limits, "max_concurrency_num")
        assert hasattr(limits, "min_queue_wait_time")
        assert hasattr(limits, "max_queue_wait_time")
        assert hasattr(limits, "min_request_num")
        assert hasattr(limits, "max_request_num")
        assert hasattr(limits, "min_gpu_num")
        assert hasattr(limits, "max_gpu_num")
        assert hasattr(limits, "cuda_version_list")

        # Verify data types
        assert isinstance(limits.min_rootfs_size, int)
        assert isinstance(limits.max_rootfs_size, int)
        assert isinstance(limits.cuda_version_list, list)

        # Verify logical constraints
        assert limits.min_rootfs_size <= limits.max_rootfs_size
        assert limits.min_local_volume_size <= limits.max_local_volume_size
        assert limits.min_worker_num <= limits.max_worker_num
        assert limits.min_gpu_num <= limits.max_gpu_num

    def test_get_endpoint_details(self, client):
        """Test getting details of a specific endpoint."""
        # First get list of endpoints
        endpoints = client.gpu.endpoints.list(page_size=1, page_num=0)

        if len(endpoints.data) > 0:
            endpoint_id = endpoints.data[0].id

            # Get detailed information
            endpoint = client.gpu.endpoints.get(id=endpoint_id)

            assert endpoint is not None
            assert hasattr(endpoint, "id")
            assert hasattr(endpoint, "name")
            assert hasattr(endpoint, "status")

            # Verify data types
            assert isinstance(endpoint.id, str)
            assert isinstance(endpoint.name, str)
            assert isinstance(endpoint.status, str)
            assert endpoint.id == endpoint_id

    def test_endpoint_structure(self, client):
        """Test that endpoints have all expected fields."""
        endpoints = client.gpu.endpoints.list(page_size=1, page_num=0)

        if len(endpoints.data) > 0:
            endpoint = endpoints.data[0]

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

    def test_create_update_delete_endpoint(self, client, product_id):
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
