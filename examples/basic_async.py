"""Asynchronous client usage example.

This example demonstrates:
- Async client initialization
- Using async context manager
- Creating instances asynchronously
- Concurrent operations with asyncio.gather
"""

import asyncio

from novita import AsyncNovitaClient


async def main() -> None:
    """Run asynchronous operations."""
    # Use async context manager for automatic cleanup
    async with AsyncNovitaClient() as client:
        # List all instances concurrently with getting pricing
        print("\nFetching instances and pricing concurrently...")
        instances_task = client.gpu.instances.list()
        pricing_task = client.gpu.products.list()

        instances, products = await asyncio.gather(instances_task, pricing_task)

        print(f"✓ Total instances: {instances.total}")
        print(f"✓ Available GPU types: {len(products.data)}")
        for product in products.data[:3]:  # Show first 3
            print(f"  - {product.name}: ${product.price / 100000}/hour")


if __name__ == "__main__":
    asyncio.run(main())
