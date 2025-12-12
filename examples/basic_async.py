"""Asynchronous client usage example.

This example demonstrates:
- Async client initialization
- Using async context manager
- Creating instances asynchronously
- Concurrent operations with asyncio.gather
"""

import asyncio
import os

from novita import AsyncNovitaClient


async def main() -> None:
    """Run asynchronous operations."""
    # Check for API key
    if not os.environ.get("NOVITA_API_KEY"):
        print("Error: NOVITA_API_KEY environment variable is not set")
        print("Please set it with: export NOVITA_API_KEY='your-api-key-here'")
        return

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
            price_str = f"${product.price:.2f}" if product.price is not None else "N/A"
            print(f"  - {product.name}: {price_str}/hour")


if __name__ == "__main__":
    asyncio.run(main())
