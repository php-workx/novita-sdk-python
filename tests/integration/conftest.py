"""Shared fixtures for integration tests."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

import pytest

from novita import NovitaClient


def _skip(reason: str) -> NoReturn:
    """Helper to satisfy type checker for pytest.skip."""
    pytest.skip(reason)


@pytest.fixture(scope="session")
def api_key() -> str:
    """Get API key from environment variable."""
    key = os.getenv("NOVITA_API_KEY")
    if not key:
        _skip("NOVITA_API_KEY environment variable not set")
    return key


@pytest.fixture(scope="session")
def client(api_key: str) -> NovitaClient:
    """Create a NovitaClient instance for integration tests."""
    return NovitaClient(api_key=api_key)


@pytest.fixture(scope="session")
def cluster_id(client: NovitaClient) -> str:
    """Get a valid cluster ID from the API."""
    clusters = client.gpu.clusters.list()
    if not clusters or len(clusters) == 0:
        _skip("No clusters available")
    return clusters[0].id


@pytest.fixture(scope="session")
def product_id(client: NovitaClient) -> str:
    """Get a valid GPU product ID from the API."""
    products = client.gpu.products.list()
    if not products or len(products) == 0:
        _skip("No GPU products available")
    # Find a product that's available for deployment
    for product in products:
        if product.available_deploy:
            return product.id
    _skip("No deployable GPU products available")


@pytest.fixture(scope="session")
def cpu_product_id(client: NovitaClient) -> str:
    """Get a valid CPU product ID from the API."""
    # Note: CPU products may not be available in this API version
    products = client.gpu.products.list()
    if not products or len(products) == 0:
        _skip("No products available")
    # Find a CPU product that's available for deployment
    for product in products:
        if hasattr(product, "kind") and product.kind == "cpu" and product.available_deploy:
            return product.id
    _skip("No deployable CPU products available")


@pytest.fixture(scope="session")
def resource_tracker() -> dict[str, list[str]]:
    """Track resources created during the test session.

    Returns:
        Dictionary mapping resource type to list of resource IDs
    """
    return {
        "instances": [],
        "endpoints": [],
        "templates": [],
        "networks": [],
        "storages": [],
        "registries": [],
        "prewarm_tasks": [],
    }


def pytest_sessionstart(session: pytest.Session) -> None:
    """Run cleanup before test session starts.

    This removes any leaked resources from previous test runs.
    """
    # Only run cleanup for integration tests
    if "integration" not in str(session.config.args):
        return

    # Only run if NOVITA_API_KEY is set
    if not os.getenv("NOVITA_API_KEY"):
        return

    print("\n" + "=" * 60)
    print("Running pre-test cleanup...")
    print("=" * 60)

    # Get path to cleanup script
    repo_root = Path(__file__).parent.parent.parent
    cleanup_script = repo_root / "scripts" / "cleanup_test_resources.py"

    if not cleanup_script.exists():
        print(f"Warning: Cleanup script not found at {cleanup_script}")
        return

    try:
        # Run cleanup script
        result = subprocess.run(
            [sys.executable, str(cleanup_script)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            print("Warning: Pre-test cleanup encountered errors")

    except subprocess.TimeoutExpired:
        print("Warning: Pre-test cleanup timed out")
    except Exception as e:
        print(f"Warning: Failed to run pre-test cleanup: {e}")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:  # noqa: ARG001
    """Run cleanup after test session finishes.

    This removes any resources created during the test session that weren't
    properly cleaned up (e.g., due to test failures or interruptions).
    """
    # Only run cleanup for integration tests
    if "integration" not in str(session.config.args):
        return

    # Only run if NOVITA_API_KEY is set
    if not os.getenv("NOVITA_API_KEY"):
        return

    print("\n" + "=" * 60)
    print("Running post-test cleanup...")
    print("=" * 60)

    # Get path to cleanup script
    repo_root = Path(__file__).parent.parent.parent
    cleanup_script = repo_root / "scripts" / "cleanup_test_resources.py"

    if not cleanup_script.exists():
        print(f"Warning: Cleanup script not found at {cleanup_script}")
        return

    try:
        # Run cleanup script
        result = subprocess.run(
            [sys.executable, str(cleanup_script)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            print("Warning: Post-test cleanup encountered errors")

    except subprocess.TimeoutExpired:
        print("Warning: Post-test cleanup timed out")
    except Exception as e:
        print(f"Warning: Failed to run post-test cleanup: {e}")
