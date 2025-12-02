"""Integration tests for cluster endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from novita import NovitaClient


class TestClusters:
    """Test cluster-related endpoints."""

    def test_list_clusters(self, client: NovitaClient) -> None:
        """Test listing all clusters."""
        clusters = client.gpu.clusters.list()

        assert clusters is not None
        assert isinstance(clusters, list)

        if len(clusters) > 0:
            cluster = clusters[0]
            # Verify cluster structure
            assert hasattr(cluster, "id")
            assert hasattr(cluster, "name")
            assert hasattr(cluster, "available_gpu_type")
            assert hasattr(cluster, "support_network_storage")
            assert hasattr(cluster, "support_instance_network")

            # Verify data types
            assert isinstance(cluster.id, str)
            assert isinstance(cluster.name, str)
            assert isinstance(cluster.available_gpu_type, list)
            assert isinstance(cluster.support_network_storage, bool)
            assert isinstance(cluster.support_instance_network, bool)

    def test_clusters_have_valid_gpu_types(self, client: NovitaClient) -> None:
        """Test that clusters have valid GPU type information."""
        clusters = client.gpu.clusters.list()

        if len(clusters) > 0:
            for cluster in clusters:
                # Each cluster should have at least some GPU types or be empty
                assert isinstance(cluster.available_gpu_type, list)

                # If GPU types are present, they should be non-empty strings
                for gpu_type in cluster.available_gpu_type:
                    assert isinstance(gpu_type, str)
                    assert len(gpu_type) > 0
