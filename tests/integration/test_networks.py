"""Integration tests for network endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient

from novita.generated.models import UpdateNetworkRequest


@pytest.mark.integration
@pytest.mark.safe
class TestNetworks:
    """Test VPC network-related endpoints."""

    def test_list_networks(self, client: NovitaClient) -> None:
        """Test listing all VPC networks."""
        networks = client.gpu.networks.list()

        assert isinstance(networks, list)

    def test_network_structure(self, client: NovitaClient) -> None:
        """Test that networks have all expected fields."""
        networks = client.gpu.networks.list()

        if len(networks) > 0:
            network = networks[0]

            # Required fields
            assert hasattr(network, "id")
            assert hasattr(network, "name")
            assert hasattr(network, "cluster_id")

            # Verify data types
            assert isinstance(network.id, str)
            assert isinstance(network.name, str)
            assert isinstance(network.cluster_id, str)

            # IDs should be non-empty
            assert len(network.id) > 0
            assert len(network.cluster_id) > 0

    def test_get_network_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific network."""
        # First get list of networks
        networks = client.gpu.networks.list()

        if len(networks) > 0:
            network_id = networks[0].id

            # Get detailed information
            network = client.gpu.networks.get(network_id=network_id)
            assert network is not None

    def test_networks_have_unique_ids(self, client: NovitaClient) -> None:
        """Test that all networks have unique IDs."""
        networks = client.gpu.networks.list()

        if len(networks) > 1:
            ids = [network.id for network in networks]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


@pytest.mark.integration
@pytest.mark.safe
class TestNetworkLifecycle:
    """Test full network lifecycle (create, update, delete)."""

    def test_create_update_delete_network(self, client: NovitaClient) -> None:
        """
        Test full network lifecycle.

        This test will:
        1. Use an existing network or skip if network limit reached
        2. Update the network (rename)
        3. Verify the update
        4. Restore the original name

        Note: This test doesn't create/delete networks due to account limits.
        It tests update functionality using an existing network.
        """
        # Get existing networks
        networks = client.gpu.networks.list()

        if not networks:
            pytest.skip("No networks available for testing")

        # Use the first network for testing
        test_network = networks[0]
        network_id = test_network.id
        original_name = test_network.name

        # Generate a test name
        import uuid

        test_name = f"test-update-{uuid.uuid4().hex[:6]}"

        try:
            # Step 1: Update the network (rename)
            client.gpu.networks.update(
                UpdateNetworkRequest(
                    network_id=network_id,
                    name=test_name,
                )
            )

            # Step 2: Verify the update in the list
            networks_after_update = client.gpu.networks.list()
            updated_in_list = next((n for n in networks_after_update if n.id == network_id), None)
            assert updated_in_list is not None
            assert (
                updated_in_list.name == test_name
            ), f"Expected {test_name}, got {updated_in_list.name}"

        finally:
            # Restore original name
            try:
                client.gpu.networks.update(
                    UpdateNetworkRequest(
                        network_id=network_id,
                        name=original_name,
                    )
                )
            except Exception as e:
                # Log restore errors but don't fail the test
                import warnings

                warnings.warn(
                    f"Failed to restore network name for {network_id}: {e}",
                    ResourceWarning,
                    stacklevel=2,
                )
