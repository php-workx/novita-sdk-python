"""Integration tests for network endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient

from novita.generated.models import CreateNetworkRequest, UpdateNetworkRequest


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

    def test_create_update_delete_network(self, client: NovitaClient, cluster_id: str) -> None:
        """
        Test full network lifecycle.

        This test will:
        1. Create a new VPC network
        2. Find the network by name (API doesn't return ID on create)
        3. Update the network (rename)
        4. Verify the update
        5. Delete the network
        6. Verify the network was deleted
        """
        import time

        from novita.exceptions import BadRequestError, NotFoundError

        from .test_utils import generate_test_name

        # Generate unique test names (max 30 chars for networks)
        # Format: test-net-YYYYMMDD-HHMMSS (27 chars)
        initial_name = generate_test_name("net")
        network_id = None

        try:
            # Step 1: Create a new VPC network
            client.gpu.networks.create(
                CreateNetworkRequest(
                    cluster_id=cluster_id,
                    name=initial_name,
                )
            )

            # Step 2: Find the network in the list by name (API doesn't return ID on create)
            time.sleep(1)  # Give API a moment to process
            networks = client.gpu.networks.list()
            found_network = next((n for n in networks if n.name == initial_name), None)
            assert (
                found_network is not None
            ), f"Network '{initial_name}' not found in list after creation"
            network_id = found_network.id
            assert network_id is not None

            # Step 3: Update the network (rename with new timestamp)
            updated_name = generate_test_name("net")
            client.gpu.networks.update(
                UpdateNetworkRequest(
                    network_id=network_id,
                    name=updated_name,
                )
            )

            # Step 4: Verify the update
            networks_after_update = client.gpu.networks.list()
            updated_in_list = next((n for n in networks_after_update if n.id == network_id), None)
            assert updated_in_list is not None
            assert (
                updated_in_list.name == updated_name
            ), f"Expected {updated_name}, got {updated_in_list.name}"

            # Step 5: Delete the network
            client.gpu.networks.delete(network_id)

            # Step 6: Verify deletion - network should no longer exist
            try:
                client.gpu.networks.get(network_id=network_id)
                # If we get here, network still exists
                raise AssertionError(f"Network {network_id} still exists after deletion")
            except (NotFoundError, BadRequestError) as e:
                # Expected - network should not exist anymore
                if "not found" in str(e).lower():
                    pass
                else:
                    raise

        finally:
            # Cleanup: ensure the network is deleted even if test fails
            if network_id is not None:
                try:
                    # Always try to delete - API will handle if already deleted
                    client.gpu.networks.delete(network_id)
                except Exception as e:
                    # If network is already gone ("not found"), that's fine
                    error_msg = str(e).lower()
                    if "not found" not in error_msg and "not fount" not in error_msg:
                        # Log cleanup errors but don't fail the test
                        import warnings

                        warnings.warn(
                            f"Failed to cleanup network {network_id}: {e}",
                            ResourceWarning,
                            stacklevel=2,
                        )
