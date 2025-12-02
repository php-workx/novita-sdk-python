"""Shared fixtures for integration tests."""

from __future__ import annotations

import os
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
