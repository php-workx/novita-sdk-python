"""Integration tests for network endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


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


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.integration
@pytest.mark.invasive
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestNetworkLifecycle:
    """Test full network lifecycle (create, update, delete)."""

    def test_create_update_delete_network(self, client: NovitaClient, cluster_id: str) -> None:
        """
        Test full network lifecycle.

        This test will:
        1. Create a new network
        2. Verify it appears in the list
        3. Update the network
        4. Delete the network
        5. Verify it's removed from the list

        TODO: Implement this test sequence
        """
        pass
