"""Integration tests for network storage endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


class TestNetworkStorage:
    """Test network storage-related endpoints."""

    def test_list_network_storages(self, client: NovitaClient) -> None:
        """Test listing all network storage volumes."""
        storages = client.gpu.storages.list()

        assert storages is not None
        assert isinstance(storages, list)

    def test_network_storage_structure(self, client: NovitaClient) -> None:
        """Test that network storages have all expected fields."""
        storages = client.gpu.storages.list()

        if len(storages) > 0:
            storage = storages[0]

            # Required fields
            assert hasattr(storage, "storage_id")
            assert hasattr(storage, "storage_name")
            assert hasattr(storage, "storage_size")
            assert hasattr(storage, "cluster_id")

            # Verify data types
            if storage.storage_id is not None:
                assert isinstance(storage.storage_id, str)
                assert len(storage.storage_id) > 0
            if storage.storage_name is not None:
                assert isinstance(storage.storage_name, str)
            if storage.storage_size is not None:
                assert isinstance(storage.storage_size, int)
                assert storage.storage_size > 0
            if storage.cluster_id is not None:
                assert isinstance(storage.cluster_id, str)
                assert len(storage.cluster_id) > 0

    def test_network_storages_have_valid_sizes(self, client: NovitaClient) -> None:
        """Test that network storages have valid size values."""
        storages = client.gpu.storages.list()

        for storage in storages:
            if storage.storage_size is not None:
                # Size should be a positive integer
                assert isinstance(storage.storage_size, int)
                assert storage.storage_size > 0
                # Size should be within reasonable bounds (10GB to 10TB)
                assert 10 <= storage.storage_size <= 10240

    def test_network_storages_have_unique_ids(self, client: NovitaClient) -> None:
        """Test that all network storages have unique IDs."""
        storages = client.gpu.storages.list()

        if len(storages) > 1:
            ids = [storage.storage_id for storage in storages if storage.storage_id is not None]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestNetworkStorageLifecycle:
    """Test full network storage lifecycle (create, update, delete)."""

    def test_create_update_delete_network_storage(
        self, client: NovitaClient, cluster_id: str
    ) -> None:
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
