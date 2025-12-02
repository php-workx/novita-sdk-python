"""Integration tests for metrics endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


class TestMetrics:
    """Test metrics-related endpoints."""

    def test_get_instance_metrics(self, client: NovitaClient) -> None:
        """Test fetching instance monitor metrics."""
        # First get list of instances
        instances = client.gpu.instances.list(page_size=1, page_num=0)

        if len(instances) > 0:
            instance_id = instances[0].id

            # Get metrics for the instance
            metrics = client.gpu.metrics.get(instance_id=instance_id)

            assert metrics is not None
            # Metrics should be a dictionary or object with metric data

    def test_get_instance_metrics_for_running_instance(self, client: NovitaClient) -> None:
        """Test fetching metrics for a running instance."""
        # Get running instances
        instances = client.gpu.instances.list(page_size=10, page_num=0, status="running")

        if len(instances) > 0:
            instance_id = instances[0].id

            # Get metrics for the running instance
            metrics = client.gpu.metrics.get(instance_id=instance_id)

            assert metrics is not None
            # Running instances should have more comprehensive metrics

    def test_get_instance_metrics_invalid_id(self, client: NovitaClient) -> None:
        """Test fetching metrics with an invalid instance ID."""
        from novita import NotFoundError

        with pytest.raises(NotFoundError):
            # This should raise an error (404 or similar)
            client.gpu.metrics.get(instance_id="invalid-id-12345")
