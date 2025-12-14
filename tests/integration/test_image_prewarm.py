"""Integration tests for image prewarm endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestImagePrewarm:
    """Test image prewarm-related endpoints."""

    def test_list_image_prewarm_tasks(self, client: NovitaClient) -> None:
        """Test listing all image prewarm tasks."""
        tasks = client.gpu.image_prewarm.list()

        assert isinstance(tasks, list)

    def test_get_image_prewarm_quota(self, client: NovitaClient) -> None:
        """Test getting image prewarm quota."""
        quota = client.gpu.image_prewarm.get_quota()

        assert quota is not None
        # Quota should be a dictionary or object with quota information

    def test_image_prewarm_task_structure(self, client: NovitaClient) -> None:
        """Test that image prewarm tasks have all expected fields."""
        tasks = client.gpu.image_prewarm.list()

        if len(tasks) > 0:
            task = tasks[0]

            # Required fields
            assert hasattr(task, "id")
            assert hasattr(task, "image_url")
            assert hasattr(task, "state")

            # Verify data types
            assert isinstance(task.id, str)
            assert isinstance(task.image_url, str)

            # IDs and URLs should be non-empty
            assert len(task.id) > 0
            assert len(task.image_url) > 0

    def test_image_prewarm_tasks_have_unique_ids(self, client: NovitaClient) -> None:
        """Test that all image prewarm tasks have unique IDs."""
        tasks = client.gpu.image_prewarm.list()

        if len(tasks) > 1:
            ids = [task.id for task in tasks]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.integration
@pytest.mark.invasive
@pytest.mark.skip(
    reason="Image prewarm API endpoint returns 500 error - appears to be a server-side issue"
)
class TestImagePrewarmLifecycle:
    """Test full image prewarm lifecycle (create, update, delete).

    Note: This test is currently skipped due to API issues with the image prewarm endpoint.
    The endpoint returns a 500 Internal Server Error when attempting to create prewarm tasks,
    which appears to be a server-side issue that needs to be resolved by the Novita team.
    """

    def test_create_delete_prewarm_task(self, client: NovitaClient, cluster_id: str) -> None:
        """
        Test full image prewarm task lifecycle.

        This test will:
        1. Create a new image prewarm task for ubuntu:22.04 on RTX 4090
        2. Verify it appears in the list
        3. Delete the prewarm task
        4. Verify it's removed from the list

        Note: Currently skipped due to API endpoint returning 500 errors.
        """
        # Find RTX 4090 products
        products = client.gpu.products.list(product_name="4090")
        if not products:
            pytest.skip("No RTX 4090 products found")

        # Get product IDs for RTX 4090
        product_ids = [p.id for p in products[:2]]  # Use up to 2 products

        # Small ubuntu minimal image (use full Docker Hub URL)
        test_image = "docker.io/library/ubuntu:22.04"
        task_id = None

        try:
            # Step 1: Create a new image prewarm task
            response = client.gpu.image_prewarm.create(
                imageUrl=test_image,
                clusterId=cluster_id,
                productIds=product_ids,
                note="Integration test prewarm task",
            )
            assert response.id is not None
            task_id = response.id

            # Step 2: Verify it appears in the list
            tasks = client.gpu.image_prewarm.list()
            found_task = next((t for t in tasks if t.id == task_id), None)
            assert (
                found_task is not None
            ), f"Prewarm task {task_id} not found in list after creation"
            assert found_task.image_url == test_image
            assert found_task.cluster_id == cluster_id

            # Step 3: Delete the prewarm task
            client.gpu.image_prewarm.delete(task_id)

            # Step 4: Verify it's removed from the list
            tasks_after_delete = client.gpu.image_prewarm.list()
            deleted_task = next((t for t in tasks_after_delete if t.id == task_id), None)
            assert deleted_task is None, f"Prewarm task {task_id} still exists after deletion"

        finally:
            # Cleanup: ensure the prewarm task is deleted even if test fails
            if task_id is not None:
                try:
                    tasks = client.gpu.image_prewarm.list()
                    if any(t.id == task_id for t in tasks):
                        client.gpu.image_prewarm.delete(task_id)
                except Exception as e:
                    # Log cleanup errors but don't fail the test
                    import warnings

                    warnings.warn(
                        f"Failed to cleanup prewarm task {task_id}: {e}",
                        ResourceWarning,
                        stacklevel=2,
                    )
