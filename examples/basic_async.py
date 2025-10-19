"""Asynchronous client usage example.

This example demonstrates:
- Async client initialization
- Using async context manager
- Creating instances asynchronously
- Concurrent operations with asyncio.gather
"""

import asyncio

from novita import AsyncNovitaClient, CreateInstanceRequest, InstanceType


async def main() -> None:
    """Run asynchronous operations."""
    # Use async context manager for automatic cleanup
    async with AsyncNovitaClient() as client:
        # Create instance
        print("Creating GPU instance...")
        request = CreateInstanceRequest(
            name="my-async-instance",
            instance_type=InstanceType.A100_80GB,
            disk_size=50,
        )
        response = await client.gpu.create_instance(request)
        print(f"✓ Created: {response.instance_id}")
        instance_id = response.instance_id

        # Get instance details
        print(f"\nFetching instance details...")
        instance = await client.gpu.get_instance(instance_id)
        print(f"✓ Status: {instance.status}")

        # List all instances concurrently with getting pricing
        print("\nFetching instances and pricing concurrently...")
        instances_task = client.gpu.list_instances()
        pricing_task = client.gpu.get_pricing()

        instances, pricing = await asyncio.gather(instances_task, pricing_task)

        print(f"✓ Total instances: {instances.total}")
        print(f"✓ Available GPU types: {len(pricing.pricing)}")
        for price in pricing.pricing[:3]:  # Show first 3
            print(f"  - {price.instance_type}: ${price.price_per_hour}/hour")


if __name__ == "__main__":
    asyncio.run(main())
