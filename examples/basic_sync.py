"""Basic synchronous client usage example.

This example demonstrates:
- Client initialization with environment variable
- Creating a GPU instance
- Listing all instances
- Getting instance details
- Proper cleanup
"""

from novita import CreateInstanceRequest, InstanceType, NovitaClient


def main() -> None:
    """Run basic synchronous operations."""
    # Initialize client (uses NOVITA_API_KEY environment variable)
    client = NovitaClient()

    try:
        # List all instances
        print("\nListing all instances...")
        instances = client.gpu.instances.list()
        print(f"✓ Total instances: {instances.total}")
        for instance in instances.instances:
            print(f"  - {instance.name} ({instance.status})")

        # Get GPU product pricing
        print(f"\nGetting all GPU products...")
        list = client.gpu.products.list()
        print(f"✓ Total GPU products: {len(list.data)}")
        for product in list.data:
            print(f"  - {product.name} (${product.price/100000}/hour)")

    finally:
        # Always close the client
        client.close()


if __name__ == "__main__":
    main()
