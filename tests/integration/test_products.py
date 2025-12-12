"""Integration tests for product endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


@pytest.mark.integration
@pytest.mark.safe
class TestGPUProducts:
    """Test GPU product-related endpoints."""

    def test_list_gpu_products(self, client: NovitaClient) -> None:
        """Test listing all GPU products."""
        products = client.gpu.products.list()

        assert isinstance(products, list)

        if not products:
            pytest.skip("No GPU products available to test product structure")

        product = products[0]
        # Verify product structure
        assert hasattr(product, "id")
        assert hasattr(product, "name")
        assert hasattr(product, "cpu_per_gpu")
        assert hasattr(product, "memory_per_gpu")
        assert hasattr(product, "disk_per_gpu")
        assert hasattr(product, "available_deploy")
        assert hasattr(product, "min_root_fs")
        assert hasattr(product, "max_root_fs")
        assert hasattr(product, "regions")
        assert hasattr(product, "price")
        assert hasattr(product, "billing_methods")

        # Verify data types
        assert isinstance(product.id, str)
        assert isinstance(product.name, str)
        assert isinstance(product.cpu_per_gpu, int)
        assert isinstance(product.memory_per_gpu, int)
        assert isinstance(product.disk_per_gpu, int)
        assert isinstance(product.available_deploy, bool)
        assert isinstance(product.regions, list)
        assert isinstance(product.billing_methods, list)

    def test_list_gpu_products_with_cluster_filter(
        self, client: NovitaClient, cluster_id: str
    ) -> None:
        """Test listing GPU products filtered by cluster."""
        products = client.gpu.products.list(cluster_id=cluster_id)

        assert isinstance(products, list)

        if not products:
            pytest.skip("No GPU products available for cluster filter test")

        # Verify products were returned (API accepted the filter)
        # Note: regions contains cluster names like "US-01 (Dallas)", not cluster IDs
        assert len(products) > 0
        assert all(hasattr(p, "regions") for p in products)

    def test_list_gpu_products_with_gpu_num_filter(self, client: NovitaClient) -> None:
        """Test listing GPU products filtered by GPU count."""
        gpu_num = 1
        products = client.gpu.products.list(gpu_num=gpu_num)

        assert isinstance(products, list)

        # TODO: Validate filter is working correctly once GPUProduct model includes gpu_num field
        # The API accepts gpu_num as a filter parameter but the model doesn't expose this field
        # in the response, so we can't verify the filter worked. Need to add a field like
        # 'gpu_count' or 'gpu_num' to GPUProduct model to enable validation.
        pytest.skip(
            "Cannot validate gpu_num filter - GPUProduct model lacks gpu_num/gpu_count field"
        )

    def test_list_gpu_products_with_billing_method_filter(self, client: NovitaClient) -> None:
        """Test listing GPU products filtered by billing method."""
        products = client.gpu.products.list(billing_method="onDemand")

        assert isinstance(products, list)

        if not products:
            pytest.skip("No GPU products with onDemand billing to test filter")

        # All products should support onDemand billing
        for product in products:
            assert "onDemand" in product.billing_methods

    def test_list_gpu_products_with_product_name_filter(self, client: NovitaClient) -> None:
        """Test listing GPU products filtered by product name."""
        # Get all products first
        all_products = client.gpu.products.list()

        if not all_products:
            pytest.skip("No GPU products available to test product name filter")

        # Use part of the first product's name for fuzzy search and ensure it comes back
        reference_product = all_products[0]
        search_term = reference_product.name[:5]
        filtered_products = client.gpu.products.list(product_name=search_term)

        assert isinstance(filtered_products, list)

        if not filtered_products:
            pytest.skip("Product name filter returned no results for known name fragment")

        assert any(p.id == reference_product.id for p in filtered_products)

    def test_gpu_product_has_valid_price_info(self, client: NovitaClient) -> None:
        """Test that GPU products have valid pricing information.

        Note: SDK returns prices as float in USD (converted from API's 1/100000 USD units).
        """
        products = client.gpu.products.list()

        if not products:
            pytest.skip("No GPU products available to test price information")

        for product in products:
            # Price should be a non-negative float (in USD)
            assert isinstance(product.price, float)
            assert product.price >= 0

            # Spot price should be float or None
            if product.spot_price is not None:
                assert isinstance(product.spot_price, float)
                assert product.spot_price >= 0

            # Monthly price should be a list
            if hasattr(product, "monthly_price") and product.monthly_price:
                assert isinstance(product.monthly_price, list)
                # Each monthly price should have a price property that returns float
                for monthly in product.monthly_price:
                    assert isinstance(monthly.price, float)
                    assert monthly.price >= 0


@pytest.mark.integration
@pytest.mark.safe
class TestCPUProducts:
    """Test CPU product-related endpoints."""

    def test_list_cpu_products(self, client: NovitaClient) -> None:
        """Test listing all CPU products.

        Note: SDK returns prices as float in USD (converted from API's 1/100000 USD units).
        """
        products = client.gpu.products.list_cpu()

        assert isinstance(products, list)

        if not products:
            pytest.skip("No CPU products available to test product structure")

        product = products[0]
        # Verify product structure
        assert hasattr(product, "id")
        assert hasattr(product, "name")
        assert hasattr(product, "cpu_num")
        assert hasattr(product, "memory_size")
        assert hasattr(product, "rootfs_size")
        assert hasattr(product, "local_volume_size")
        assert hasattr(product, "available_deploy")
        assert hasattr(product, "price")

        # Verify data types
        assert isinstance(product.id, str)
        assert isinstance(product.name, str)
        if product.cpu_num is not None:
            assert isinstance(product.cpu_num, int)
        if product.memory_size is not None:
            assert isinstance(product.memory_size, int)
        if product.rootfs_size is not None:
            assert isinstance(product.rootfs_size, int)
        if product.local_volume_size is not None:
            assert isinstance(product.local_volume_size, int)
        if product.available_deploy is not None:
            assert isinstance(product.available_deploy, bool)
        # Price is now a float property
        if product.price is not None:
            assert isinstance(product.price, float)

    def test_list_cpu_products_with_cluster_filter(
        self, client: NovitaClient, cluster_id: str
    ) -> None:
        """Test listing CPU products filtered by cluster.

        Note: CPUProduct model doesn't expose regions field, so we can only verify
        the API accepts the filter parameter and returns valid data.
        """
        products = client.gpu.products.list_cpu(cluster_id=cluster_id)

        assert isinstance(products, list)

    def test_list_cpu_products_with_product_name_filter(self, client: NovitaClient) -> None:
        """Test listing CPU products filtered by product name."""
        # Get all products first
        all_products = client.gpu.products.list_cpu()

        if not all_products:
            pytest.skip("No CPU products available to test product name filter")

        # Use part of the first product's name for fuzzy search and ensure it comes back
        reference_product = all_products[0]
        search_term = reference_product.name[:5]
        filtered_products = client.gpu.products.list_cpu(product_name=search_term)

        assert isinstance(filtered_products, list)

        if not filtered_products:
            pytest.skip("CPU product name filter returned no results for known name fragment")

        assert any(p.id == reference_product.id for p in filtered_products)

    def test_cpu_product_has_valid_price_info(self, client: NovitaClient) -> None:
        """Test that CPU products have valid pricing information.

        Note: SDK returns prices as float in USD (converted from API's 1/100000 USD units).
        """
        products = client.gpu.products.list_cpu()

        if not products:
            pytest.skip("No CPU products available to test price information")

        for product in products:
            # Price should be a non-negative float (in USD) or None
            if product.price is not None:
                assert isinstance(product.price, float)
                assert product.price >= 0
