"""Integration tests for instance endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


class TestInstances:
    """Test instance-related endpoints."""

    def test_list_instances(self, client: NovitaClient) -> None:
        """Test listing all instances."""
        instances = client.gpu.instances.list(page_size=10, page_num=0)

        assert instances is not None
        assert isinstance(instances, list)

    def test_list_instances_with_pagination(self, client: NovitaClient) -> None:
        """Test listing instances with different pagination parameters."""
        # Get first page
        page1 = client.gpu.instances.list(page_size=5, page_num=0)
        assert page1 is not None
        assert len(page1) <= 5

        # Get second page
        page2 = client.gpu.instances.list(page_size=5, page_num=1)
        assert page2 is not None
        assert len(page2) <= 5

    def test_list_instances_with_name_filter(self, client: NovitaClient) -> None:
        """Test listing instances filtered by name."""
        # Get all instances first
        all_instances = client.gpu.instances.list(page_size=100, page_num=0)
        if len(all_instances) > 0:
            # Use part of the first instance's name for fuzzy search
            first_instance = all_instances[0]
            if hasattr(first_instance, "name") and first_instance.name:
                search_term = first_instance.name[:5]
                filtered = client.gpu.instances.list(page_size=10, page_num=0, name=search_term)
                assert filtered is not None

    def test_list_instances_with_status_filter(self, client: NovitaClient) -> None:
        """Test listing instances filtered by status."""
        # Test with a common status
        instances = client.gpu.instances.list(page_size=10, page_num=0, status="running")
        assert instances is not None
        # All returned instances should have running status
        for instance in instances:
            assert str(instance.status) == "running"

    def test_list_instances_with_product_name_filter(self, client: NovitaClient) -> None:
        """Test listing instances filtered by product name."""
        instances = client.gpu.instances.list(page_size=10, page_num=0, product_name="RTX")
        assert instances is not None

    def test_get_instance_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific instance."""
        # First get list of instances
        instances = client.gpu.instances.list(page_size=1, page_num=0)
        if len(instances) > 0:
            instance_id = instances[0].id

            # Get detailed information
            instance = client.gpu.instances.get(instance_id=instance_id)

            assert instance is not None
            assert hasattr(instance, "id")
            assert hasattr(instance, "name")
            assert hasattr(instance, "status")
            assert hasattr(instance, "cluster_id")

            # Verify data types
            assert isinstance(instance.id, str)
            assert isinstance(instance.status, str)
            assert instance.id == instance_id

    def test_instance_structure(self, client: NovitaClient) -> None:
        """Test that instances have all expected fields."""
        instances = client.gpu.instances.list(page_size=1, page_num=0)
        if len(instances) > 0:
            instance = instances[0]

            # Required fields
            assert hasattr(instance, "id")
            assert hasattr(instance, "name")
            assert hasattr(instance, "status")
            assert hasattr(instance, "cluster_id")

            # Verify status is valid
            valid_statuses = [
                "toCreate",
                "creating",
                "pulling",
                "running",
                "toStart",
                "starting",
                "toStop",
                "stopping",
                "exited",
                "toRestart",
                "restarting",
                "toRemove",
                "removing",
                "removed",
                "toReset",
                "resetting",
                "migrating",
                "freezing",
            ]
            assert str(instance.status) in valid_statuses


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestInstanceLifecycle:
    """Test full instance lifecycle (create, update, delete)."""

    def test_create_update_delete_instance(
        self, client: NovitaClient, product_id: str, cluster_id: str
    ) -> None:
        """
        Test full instance lifecycle.

        This test will:
        1. Create a new instance
        2. Wait for it to be running
        3. Update the instance
        4. Stop the instance
        5. Delete the instance

        TODO: Implement this test sequence
        """
        pass

    def test_create_start_stop_delete_instance(
        self, client: NovitaClient, product_id: str, cluster_id: str
    ) -> None:
        """
        Test instance start/stop lifecycle.

        TODO: Implement this test sequence
        """
        pass
