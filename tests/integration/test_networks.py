"""Integration tests for network endpoints."""

from __future__ import annotations

import time
import warnings
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient

from novita.exceptions import BadRequestError, NotFoundError
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
@pytest.mark.invasive
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
            # Poll for up to 10 seconds to handle slow API responses
            max_wait = 10
            poll_interval = 0.5
            start_time = time.time()
            found_network = None

            while time.time() - start_time < max_wait:
                networks = client.gpu.networks.list()
                found_network = next((n for n in networks if n.name == initial_name), None)
                if found_network is not None:
                    break
                time.sleep(poll_interval)

            assert (
                found_network is not None
            ), f"Network '{initial_name}' not found in list after {max_wait}s"
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
                except (NotFoundError, BadRequestError):
                    # If network is already gone, that's fine
                    pass
                except Exception as e:
                    # Log unexpected cleanup errors but don't fail the test
                    warnings.warn(
                        f"Failed to cleanup network {network_id}: {e}",
                        ResourceWarning,
                        stacklevel=2,
                    )
