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

        print(f"✓ Total instances: {len(instances)}")
        print(f"✓ Available GPU types: {len(products)}")
        for product in products[:3]:  # Show first 3
            hourly = (product.price or 0) / 100000
            print(f"  - {product.name}: ${hourly:.2f}/hour")


if __name__ == "__main__":
    asyncio.run(main())
