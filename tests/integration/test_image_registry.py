"""Integration tests for image registry authentication endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestImageRegistry:
    """Test image registry authentication-related endpoints."""

    def test_list_repository_auths(self, client: NovitaClient) -> None:
        """Test listing all container registry authentications."""
        auths = client.gpu.registries.list()

        assert isinstance(auths, list)

    def test_repository_auth_structure(self, client: NovitaClient) -> None:
        """Test that repository auths have all expected fields."""
        auths = client.gpu.registries.list()

        if len(auths) > 0:
            auth = auths[0]

            # Required fields
            assert hasattr(auth, "id")
            assert hasattr(auth, "registry")

            # Verify data types
            assert isinstance(auth.id, str)
            assert isinstance(auth.registry, str)

            # Registry should be a valid URL or domain
            assert len(auth.registry) > 0

    def test_repository_auths_have_unique_ids(self, client: NovitaClient) -> None:
        """Test that all repository auths have unique IDs."""
        auths = client.gpu.registries.list()

        if len(auths) > 1:
            ids = [auth.id for auth in auths]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


@pytest.mark.integration
@pytest.mark.safe
class TestImageRegistryLifecycle:
    """Test full image registry auth lifecycle (create, delete)."""

    def test_create_delete_repository_auth(self, client: NovitaClient) -> None:
        """
        Test full repository auth lifecycle.

        This test will:
        1. Create a new repository auth
        2. Verify it appears in the list
        3. Delete the repository auth
        4. Verify it's removed from the list
        """
        import uuid

        # Generate unique test registry name
        test_registry = f"test-registry-{uuid.uuid4().hex[:8]}.example.com"
        test_username = "test-user"
        test_password = "test-password"
        auth_id = None

        try:
            # Step 1: Create a new repository auth
            client.gpu.registries.create(
                name=test_registry,
                username=test_username,
                password=test_password,
            )

            # Step 2: Verify it appears in the list
            auths = client.gpu.registries.list()
            created_auth = next((auth for auth in auths if auth.name == test_registry), None)
            assert (
                created_auth is not None
            ), f"Registry {test_registry} not found in list after creation"
            assert created_auth.username == test_username
            auth_id = created_auth.id

            # Step 3: Delete the repository auth
            client.gpu.registries.delete(auth_id)

            # Step 4: Verify it's removed from the list
            auths_after_delete = client.gpu.registries.list()
            deleted_auth = next((auth for auth in auths_after_delete if auth.id == auth_id), None)
            assert deleted_auth is None, f"Registry {test_registry} still exists after deletion"

        finally:
            # Cleanup: ensure the auth is deleted even if test fails
            if auth_id is not None:
                try:
                    auths = client.gpu.registries.list()
                    if any(auth.id == auth_id for auth in auths):
                        client.gpu.registries.delete(auth_id)
                except Exception as e:
                    # Log cleanup errors but don't fail the test
                    import warnings

                    warnings.warn(
                        f"Failed to cleanup registry auth {auth_id}: {e}",
                        ResourceWarning,
                        stacklevel=2,
                    )
