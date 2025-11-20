"""Integration tests for image prewarm endpoints."""

import pytest


class TestImagePrewarm:
    """Test image prewarm-related endpoints."""

    def test_list_image_prewarm_tasks(self, client):
        """Test listing all image prewarm tasks."""
        response = client.gpu.image_prewarm.list()

        assert response is not None
        assert hasattr(response, "data")
        assert isinstance(response.data, list)

    def test_get_image_prewarm_quota(self, client):
        """Test getting image prewarm quota."""
        quota = client.gpu.image_prewarm.get_quota()

        assert quota is not None
        # Quota should be a dictionary or object with quota information

    def test_image_prewarm_task_structure(self, client):
        """Test that image prewarm tasks have all expected fields."""
        tasks = client.gpu.image_prewarm.list()

        if len(tasks.data) > 0:
            task = tasks.data[0]

            # Required fields
            assert hasattr(task, "id")
            assert hasattr(task, "image_url")
            assert hasattr(task, "status")

            # Verify data types
            assert isinstance(task.id, str)
            assert isinstance(task.image_url, str)
            assert isinstance(task.status, str)

            # IDs and URLs should be non-empty
            assert len(task.id) > 0
            assert len(task.image_url) > 0

    def test_image_prewarm_tasks_have_unique_ids(self, client):
        """Test that all image prewarm tasks have unique IDs."""
        tasks = client.gpu.image_prewarm.list()

        if len(tasks.data) > 1:
            ids = [task.id for task in tasks.data]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestImagePrewarmLifecycle:
    """Test full image prewarm lifecycle (create, update, delete)."""

    def test_create_update_delete_prewarm_task(self, client, cluster_id):
        """
        Test full image prewarm task lifecycle.

        This test will:
        1. Create a new image prewarm task
        2. Verify it appears in the list
        3. Update the prewarm task
        4. Delete the prewarm task
        5. Verify it's removed from the list

        TODO: Implement this test sequence
        """
        pass
