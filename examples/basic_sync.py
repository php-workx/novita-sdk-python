"""Basic synchronous client usage example.

This example demonstrates:
- Client initialization with environment variable
- Creating a GPU instance
- Listing all instances
- Getting instance details
- Proper cleanup
"""

from novita import NovitaClient


def main() -> None:
    """Run basic synchronous operations."""
    # Initialize client (uses NOVITA_API_KEY environment variable)
    client = NovitaClient()

    try:
        # List all instances
        print("\nListing all instances...")
        instances = client.gpu.instances.list()
        print(f"✓ Total instances: {len(instances)}")
        for instance in instances:
            print(f"  - {instance.name} ({instance.status.value})")

        # Get GPU product pricing
        print("\nGetting all GPU products...")
        products = client.gpu.products.list()
        print(f"✓ Total GPU products: {len(products)}")
        for product in products:
            price_str = f"${product.price:.2f}" if product.price is not None else "N/A"
            print(f"  - {product.name} ({price_str}/hour)")

    finally:
        # Always close the client
        client.close()


if __name__ == "__main__":
    main()
