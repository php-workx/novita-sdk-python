"""Shared fixtures for integration tests."""

import os

import pytest

from novita import NovitaClient


@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment variable."""
    key = os.getenv("NOVITA_API_KEY")
    if not key:
        pytest.skip("NOVITA_API_KEY environment variable not set")
    return key


@pytest.fixture(scope="session")
def client(api_key):
    """Create a NovitaClient instance for integration tests."""
    return NovitaClient(api_key=api_key)


@pytest.fixture(scope="session")
def cluster_id(client):
    """Get a valid cluster ID from the API."""
    clusters = client.gpu.clusters.list()
    if not clusters or len(clusters) == 0:
        pytest.skip("No clusters available")
    return clusters[0].id


@pytest.fixture(scope="session")
def product_id(client):
    """Get a valid GPU product ID from the API."""
    products = client.gpu.products.list()
    if not products or len(products) == 0:
        pytest.skip("No GPU products available")
    # Find a product that's available for deployment
    for product in products:
        if product.available_deploy:
            return product.id
    pytest.skip("No deployable GPU products available")


@pytest.fixture(scope="session")
def cpu_product_id(client):
    """Get a valid CPU product ID from the API."""
    products = client.gpu.cpu_products.list()
    if not products or len(products) == 0:
        pytest.skip("No CPU products available")
    # Find a product that's available for deployment
    for product in products:
        if product.available_deploy:
            return product.id
    pytest.skip("No deployable CPU products available")
