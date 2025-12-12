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

        # Verify required fields (API returns camelCase)
        assert "minRootfsSize" in limits
        assert "maxRootfsSize" in limits
        assert "freeRootfsSize" in limits
        assert "minLocalVolumeSize" in limits
        assert "maxLocalVolumeSize" in limits
        assert "freeLocalVolumeSize" in limits
        assert "minWorkerNum" in limits
        assert "maxWorkerNum" in limits
        assert "minFreeTimeout" in limits
        assert "maxFreeTimeout" in limits
        assert "minConcurrencyNum" in limits
        assert "maxConcurrencyNum" in limits
        assert "minQueueWaitTime" in limits
        assert "maxQueueWaitTime" in limits
        assert "minRequestNum" in limits
        assert "maxRequestNum" in limits
        assert "minGPUNum" in limits
        assert "maxGPUNum" in limits
        assert "cudaVersionList" in limits

        # Verify data types
        assert isinstance(limits["minRootfsSize"], int)
        assert isinstance(limits["maxRootfsSize"], int)
        assert isinstance(limits["cudaVersionList"], list)

        # Verify logical constraints
        assert limits["minRootfsSize"] <= limits["maxRootfsSize"]
        assert limits["minLocalVolumeSize"] <= limits["maxLocalVolumeSize"]
        assert limits["minWorkerNum"] <= limits["maxWorkerNum"]
        assert limits["minGPUNum"] <= limits["maxGPUNum"]

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
@pytest.mark.integration
@pytest.mark.invasive
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
