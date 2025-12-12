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
        response = client.gpu.image_registry.list_auths()  # type: ignore[attr-defined]

        assert response is not None
        assert hasattr(response, "data")
        assert isinstance(response.data, list)

    def test_repository_auth_structure(self, client: NovitaClient) -> None:
        """Test that repository auths have all expected fields."""
        auths = client.gpu.image_registry.list_auths()  # type: ignore[attr-defined]

        if len(auths.data) > 0:
            auth = auths.data[0]

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
        auths = client.gpu.image_registry.list_auths()  # type: ignore[attr-defined]

        if len(auths.data) > 1:
            ids = [auth.id for auth in auths.data]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.integration
@pytest.mark.invasive
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
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

        TODO: Implement this test sequence
        """
        pass
