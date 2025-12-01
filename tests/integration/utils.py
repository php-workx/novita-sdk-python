"""Utility functions for integration tests."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from novita import NovitaClient


def wait_for_condition(
    condition_func: Callable[[], bool],
    timeout: int = 300,
    interval: int = 5,
    error_message: str = "Timeout waiting for condition",
) -> None:
    """
    Wait for a condition to become true.

    Args:
        condition_func: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds (default: 300)
        interval: Time between checks in seconds (default: 5)
        error_message: Error message to raise if timeout occurs

    Raises:
        TimeoutError: If condition is not met within timeout period
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return
        time.sleep(interval)
    raise TimeoutError(error_message)


def wait_for_instance_status(
    client: NovitaClient,
    instance_id: str,
    target_status: str,
    timeout: int = 600,
    interval: int = 10,
) -> None:
    """
    Wait for an instance to reach a specific status.

    Args:
        client: NovitaClient instance
        instance_id: ID of the instance to monitor
        target_status: Target status to wait for
        timeout: Maximum time to wait in seconds (default: 600)
        interval: Time between checks in seconds (default: 10)

    Raises:
        TimeoutError: If instance doesn't reach target status within timeout
    """

    def check_status() -> bool:
        instance = client.gpu.instances.get(instance_id=instance_id)
        return str(instance.status) == target_status

    wait_for_condition(
        condition_func=check_status,
        timeout=timeout,
        interval=interval,
        error_message=f"Instance {instance_id} did not reach status '{target_status}' within {timeout}s",
    )


def wait_for_endpoint_status(
    client: NovitaClient,
    endpoint_id: str,
    target_status: str,
    timeout: int = 600,
    interval: int = 10,
) -> None:
    """
    Wait for an endpoint to reach a specific status.

    Args:
        client: NovitaClient instance
        endpoint_id: ID of the endpoint to monitor
        target_status: Target status to wait for
        timeout: Maximum time to wait in seconds (default: 600)
        interval: Time between checks in seconds (default: 10)

    Raises:
        TimeoutError: If endpoint doesn't reach target status within timeout
    """

    def check_status() -> bool:
        endpoint = client.gpu.endpoints.get(endpoint_id=endpoint_id)
        # EndpointDetail doesn't have status attribute, using type: ignore
        return endpoint.status == target_status  # type: ignore[attr-defined,no-any-return]

    wait_for_condition(
        condition_func=check_status,
        timeout=timeout,
        interval=interval,
        error_message=f"Endpoint {endpoint_id} did not reach status '{target_status}' within {timeout}s",
    )


def cleanup_instance(client: NovitaClient, instance_id: str, wait: bool = True) -> None:
    """
    Clean up an instance by deleting it.

    Args:
        client: NovitaClient instance
        instance_id: ID of the instance to delete
        wait: Whether to wait for deletion to complete (default: True)
    """
    try:
        client.gpu.instances.delete(instance_id=instance_id)
        if wait:
            # Wait for instance to be removed
            time.sleep(5)  # Initial delay
            wait_for_condition(
                condition_func=lambda: not _instance_exists(client, instance_id),
                timeout=300,
                interval=10,
                error_message=f"Instance {instance_id} was not deleted within timeout",
            )
    except Exception as e:
        print(f"Warning: Failed to cleanup instance {instance_id}: {e}")


def cleanup_endpoint(client: NovitaClient, endpoint_id: str) -> None:
    """
    Clean up an endpoint by deleting it.

    Args:
        client: NovitaClient instance
        endpoint_id: ID of the endpoint to delete
    """
    try:
        client.gpu.endpoints.delete(endpoint_id=endpoint_id)
        time.sleep(2)  # Allow time for deletion to process
    except Exception as e:
        print(f"Warning: Failed to cleanup endpoint {endpoint_id}: {e}")


def cleanup_network(client: NovitaClient, network_id: str) -> None:
    """
    Clean up a network by deleting it.

    Args:
        client: NovitaClient instance
        network_id: ID of the network to delete
    """
    try:
        client.gpu.networks.delete(network_id=network_id)
        time.sleep(2)  # Allow time for deletion to process
    except Exception as e:
        print(f"Warning: Failed to cleanup network {network_id}: {e}")


def cleanup_network_storage(client: NovitaClient, storage_id: str) -> None:
    """
    Clean up a network storage by deleting it.

    Args:
        client: NovitaClient instance
        storage_id: ID of the network storage to delete
    """
    try:
        client.gpu.storages.delete(storage_id=storage_id)
        time.sleep(2)  # Allow time for deletion to process
    except Exception as e:
        print(f"Warning: Failed to cleanup network storage {storage_id}: {e}")


def cleanup_template(client: NovitaClient, template_id: str) -> None:
    """
    Clean up a template by deleting it.

    Args:
        client: NovitaClient instance
        template_id: ID of the template to delete
    """
    try:
        client.gpu.templates.delete(template_id=template_id)
        time.sleep(2)  # Allow time for deletion to process
    except Exception as e:
        print(f"Warning: Failed to cleanup template {template_id}: {e}")


def _instance_exists(client: NovitaClient, instance_id: str) -> bool:
    """
    Check if an instance exists.

    Args:
        client: NovitaClient instance
        instance_id: ID of the instance to check

    Returns:
        True if instance exists, False otherwise
    """
    try:
        client.gpu.instances.get(instance_id=instance_id)
        return True
    except Exception:
        return False
