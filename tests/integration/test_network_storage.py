"""Integration tests for network storage endpoints."""

import pytest


class TestNetworkStorage:
    """Test network storage-related endpoints."""

    def test_list_network_storages(self, client):
        """Test listing all network storage volumes."""
        response = client.gpu.network_storage.list()

        assert response is not None
        assert hasattr(response, "data")
        assert isinstance(response.data, list)

    def test_network_storage_structure(self, client):
        """Test that network storages have all expected fields."""
        storages = client.gpu.network_storage.list()

        if len(storages.data) > 0:
            storage = storages.data[0]

            # Required fields
            assert hasattr(storage, "id")
            assert hasattr(storage, "name")
            assert hasattr(storage, "size")
            assert hasattr(storage, "cluster_id")

            # Verify data types
            assert isinstance(storage.id, str)
            assert isinstance(storage.name, str)
            assert isinstance(storage.size, int)
            assert isinstance(storage.cluster_id, str)

            # Size should be positive
            assert storage.size > 0

            # IDs should be non-empty
            assert len(storage.id) > 0
            assert len(storage.cluster_id) > 0

    def test_network_storages_have_valid_sizes(self, client):
        """Test that network storages have valid size values."""
        storages = client.gpu.network_storage.list()

        for storage in storages.data:
            # Size should be a positive integer
            assert isinstance(storage.size, int)
            assert storage.size > 0
            # Size should be within reasonable bounds (10GB to 10TB)
            assert 10 <= storage.size <= 10240

    def test_network_storages_have_unique_ids(self, client):
        """Test that all network storages have unique IDs."""
        storages = client.gpu.network_storage.list()

        if len(storages.data) > 1:
            ids = [storage.id for storage in storages.data]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestNetworkStorageLifecycle:
    """Test full network storage lifecycle (create, update, delete)."""

    def test_create_update_delete_network_storage(self, client, cluster_id):
        """
        Test full network storage lifecycle.

        This test will:
        1. Create a new network storage volume
        2. Verify it appears in the list
        3. Update the storage (resize)
        4. Delete the storage
        5. Verify it's removed from the list

        TODO: Implement this test sequence
        """
        pass
