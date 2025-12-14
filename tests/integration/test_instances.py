"""Integration tests for instance endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestInstances:
    """Test instance-related endpoints."""

    def test_list_instances(self, client: NovitaClient) -> None:
        """Test listing all instances."""
        instances = client.gpu.instances.list(page_size=10, page_num=0)

        assert isinstance(instances, list)

    def test_list_instances_with_pagination(self, client: NovitaClient) -> None:
        """Test listing instances with different pagination parameters."""
        # Get first page
        page1 = client.gpu.instances.list(page_size=5, page_num=0)
        assert len(page1) <= 5

        # Get second page
        page2 = client.gpu.instances.list(page_size=5, page_num=1)
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
                assert isinstance(filtered, list)

    def test_list_instances_with_status_filter(self, client: NovitaClient) -> None:
        """Test listing instances filtered by status."""
        # Test with a common status
        instances = client.gpu.instances.list(page_size=10, page_num=0, status="running")
        # All returned instances should have running status
        for instance in instances:
            assert str(instance.status) == "running"

    def test_list_instances_with_product_name_filter(self, client: NovitaClient) -> None:
        """Test listing instances filtered by product name."""
        instances = client.gpu.instances.list(page_size=10, page_num=0, product_name="RTX")
        assert isinstance(instances, list)

    def test_get_instance_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific instance."""
        # First get list of instances
        instances = client.gpu.instances.list(page_size=1, page_num=0)
        if len(instances) > 0:
            instance_id = instances[0].id

            # Get detailed information
            instance = client.gpu.instances.get(instance_id=instance_id)

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


@pytest.mark.integration
@pytest.mark.invasive
class TestInstanceLifecycle:
    """Test full instance lifecycle (create, update, delete)."""

    def test_create_stop_delete_instance(self, client: NovitaClient) -> None:
        """
        Test instance lifecycle with RTX 4090.

        This test will:
        1. Find an available RTX 4090 product
        2. Create a new instance
        3. Get instance details
        4. Delete the instance (instances are deleted regardless of status)

        Note: We skip waiting for the instance to start since GPU instances can take
        several minutes to provision. Deletion works in any state.
        """
        from novita import CreateInstanceRequest, Kind

        instance_id = None

        try:
            # Step 1: Find RTX 4090 product
            products = client.gpu.products.list(product_name="4090")
            if not products:
                pytest.skip("No RTX 4090 products found")

            available_products = [p for p in products if p.available_deploy]
            if not available_products:
                pytest.skip("No RTX 4090 products currently available to deploy")

            # Use first available product
            product = available_products[0]
            product_id = product.id
            min_rootfs = max(product.min_root_fs or 50, 50)  # Use at least 50GB

            # Step 2: Create a new instance
            # Note: We don't specify billing_mode to use the default for the product
            from tests.integration.test_utils import generate_test_name

            test_name = generate_test_name("instance")
            request = CreateInstanceRequest(
                name=test_name,
                product_id=product_id,
                gpu_num=1,
                rootfs_size=min_rootfs,
                image_url="docker.io/library/ubuntu:22.04",
                kind=Kind.gpu,
            )

            response = client.gpu.instances.create(request)
            assert response.id is not None
            instance_id = response.id

            # Step 3: Get instance details
            instance = client.gpu.instances.get(instance_id)
            assert instance.name == test_name
            assert instance.id == instance_id
            assert instance.status is not None

            # Wait a couple seconds before deletion
            import time

            time.sleep(2)

            # Step 4: Delete the instance (works in any state)
            client.gpu.instances.delete(instance_id)

            # Verify deletion was initiated or completed
            # Note: Instance may be removed so quickly that get() returns 404
            try:
                instance = client.gpu.instances.get(instance_id)
                assert instance.status.value in [
                    "toRemove",
                    "removing",
                    "removed",
                ], f"Unexpected status after delete: {instance.status.value}"
            except Exception as e:
                # If we get a "not found" error, that means deletion completed successfully
                assert (
                    "not found" in str(e).lower() or "not fount" in str(e).lower()
                ), f"Expected 'not found' error after deletion, got: {e}"

        finally:
            # Cleanup: ensure the instance is deleted even if test fails
            if instance_id is not None:
                try:
                    # Always try to delete - API will handle if already deleted
                    client.gpu.instances.delete(instance_id)
                except Exception as e:
                    # If instance is already gone ("not found"), that's fine
                    error_msg = str(e).lower()
                    if "not found" not in error_msg and "not fount" not in error_msg:
                        # Log cleanup errors but don't fail the test
                        import warnings

                        warnings.warn(
                            f"Failed to cleanup instance {instance_id}: {e}",
                            ResourceWarning,
                            stacklevel=2,
                        )
