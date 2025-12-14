"""Integration tests for network storage endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestNetworkStorage:
    """Test network storage-related endpoints."""

    def test_list_network_storages(self, client: NovitaClient) -> None:
        """Test listing all network storage volumes."""
        storages = client.gpu.storages.list()

        assert isinstance(storages, list)

    def test_network_storage_structure(self, client: NovitaClient) -> None:
        """Test that network storages have all expected fields."""
        storages = client.gpu.storages.list()

        if not storages:
            pytest.skip("No network storages available to test structure")

        storage = storages[0]

        # Check field presence
        assert hasattr(storage, "storage_id")
        assert hasattr(storage, "storage_name")
        assert hasattr(storage, "storage_size")
        assert hasattr(storage, "cluster_id")

        # Verify data types (fields may be optional based on API contract)
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

        if len(storages) <= 1:
            pytest.skip("Need at least two network storages to check ID uniqueness")

        ids = [storage.storage_id for storage in storages if storage.storage_id is not None]
        # Check for uniqueness
        assert len(ids) == len(set(ids))


@pytest.mark.integration
@pytest.mark.invasive
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
        3. Update the storage (rename)
        4. Delete the storage
        5. Verify it's removed from the list
        """
        from .test_utils import generate_test_name

        # Generate unique test storage name
        test_name = generate_test_name("storage")
        updated_name = generate_test_name("storage-updated")
        test_size = 10  # Small volume size in GB
        storage_id = None

        try:
            # Step 1: Create a new network storage volume
from novita.generated.models import (
    CreateNetworkStorageRequest,
    UpdateNetworkStorageRequest,
)

            created_storage = client.gpu.storages.create(
                CreateNetworkStorageRequest(
                    cluster_id=cluster_id,
                    storage_name=test_name,
                    storage_size=test_size,
                )
            )
            assert created_storage.storage_id is not None
            assert created_storage.storage_name == test_name
            assert created_storage.storage_size == test_size
            storage_id = created_storage.storage_id

            # Step 2: Verify it appears in the list
            storages = client.gpu.storages.list()
            found_storage = next((s for s in storages if s.storage_id == storage_id), None)
            assert (
                found_storage is not None
            ), f"Storage {storage_id} not found in list after creation"
            assert found_storage.storage_name == test_name

            # Step 3: Update the storage (rename and resize)
            client.gpu.storages.update(
                UpdateNetworkStorageRequest(
                    storage_id=storage_id,
                    storage_name=updated_name,
                    storage_size=test_size + 2,
                )
            )

            # Verify the update in the list
            storages_after_update = client.gpu.storages.list()
            updated_in_list = next(
                (s for s in storages_after_update if s.storage_id == storage_id), None
            )
            assert updated_in_list is not None
            assert updated_in_list.storage_name == updated_name
            assert updated_in_list.storage_size == test_size + 2

            # Step 4: Delete the storage
            client.gpu.storages.delete(storage_id)

            # Step 5: Verify it's removed from the list
            storages_after_delete = client.gpu.storages.list()
            deleted_storage = next(
                (s for s in storages_after_delete if s.storage_id == storage_id), None
            )
            assert deleted_storage is None, f"Storage {storage_id} still exists after deletion"

        finally:
            # Cleanup: ensure the storage is deleted even if test fails
            if storage_id is not None:
                try:
                    # Always try to delete - API will handle if already deleted
                    client.gpu.storages.delete(storage_id)
                except Exception as e:
                    # If storage is already gone ("not found"), that's fine
                    error_msg = str(e).lower()
                    if "not found" not in error_msg and "not fount" not in error_msg:
                        # Log cleanup errors but don't fail the test
                        import warnings

                        warnings.warn(
                            f"Failed to cleanup storage {storage_id}: {e}",
                            ResourceWarning,
                            stacklevel=2,
                        )
