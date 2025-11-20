"""Example demonstrating the resource-based GPU API structure.

This example shows how to use API with resource-based organization.
All GPU functionality is organized into logical resource groups.
"""

from novita import NovitaClient


def main() -> None:
    """Demonstrate the resource-based GPU API structure."""
    # Initialize client (uses NOVITA_API_KEY environment variable)
    client = NovitaClient()

    try:
        # === Instance Management ===
        print("\n=== GPU Instances ===")

        # List all instances
        print("Listing all instances...")
        instances = client.gpu.instances.list()
        print(f"✓ Total instances: {len(instances)}")
        for instance in instances[:3]:  # Show first 3
            print(f"  - {instance.name} ({instance.status.value})")

        # Get pricing information
        print("\n=== GPU Products/Pricing ===")
        products = client.gpu.products.list()
        print(f"✓ Total GPU products: {len(products)}")
        for product in products[:3]:  # Show first 3
            hourly = (product.price or 0) / 100000
            print(f"  - {product.id}: ${hourly:.2f}/hour")

        # Demonstrate clusters
        print("\n=== Available Clusters ===")
        try:
            clusters = client.gpu.clusters.list()
            print(f"✓ Available clusters: {len(clusters) if clusters else 0}")
        except Exception as e:
            print(f"⚠ Clusters endpoint: {type(e).__name__}")

    finally:
        # Always close the client
        client.close()


if __name__ == "__main__":
    main()
