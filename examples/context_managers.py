"""Context manager usage patterns.

This example demonstrates:
- Using context managers for automatic cleanup
- Sync and async context manager patterns
- Best practices for resource management
- Error handling within context managers
"""

import asyncio

from novita import AsyncNovitaClient, CreateInstanceRequest, InstanceType, NovitaClient


def sync_context_manager_basic() -> None:
    """Basic synchronous context manager usage."""
    print("=" * 60)
    print("Synchronous Context Manager - Basic")
    print("=" * 60 + "\n")

    # Client automatically closed when exiting the context
    with NovitaClient() as client:
        instances = client.gpu.list_instances()
        print(f"✓ Found {instances.total} instances")
        print("✓ Client will be automatically closed")


def sync_context_manager_with_error() -> None:
    """Context manager with error handling."""
    print("\n" + "=" * 60)
    print("Synchronous Context Manager - With Error Handling")
    print("=" * 60 + "\n")

    try:
        with NovitaClient() as client:
            print("✓ Client initialized")

            # This might raise an error
            request = CreateInstanceRequest(
                name="test-instance",
                instance_type=InstanceType.A100_80GB,
            )
            response = client.gpu.create_instance(request)
            print(f"✓ Created instance: {response.instance_id}")

    except Exception as e:
        print(f"✗ Error occurred: {e}")
        print("✓ Client still properly closed despite error")


async def async_context_manager_basic() -> None:
    """Basic asynchronous context manager usage."""
    print("\n" + "=" * 60)
    print("Asynchronous Context Manager - Basic")
    print("=" * 60 + "\n")

    # Async client automatically closed when exiting
    async with AsyncNovitaClient() as client:
        instances = await client.gpu.list_instances()
        print(f"✓ Found {instances.total} instances")
        print("✓ Async client will be automatically closed")


async def async_context_manager_concurrent() -> None:
    """Async context manager with concurrent operations."""
    print("\n" + "=" * 60)
    print("Asynchronous Context Manager - Concurrent Operations")
    print("=" * 60 + "\n")

    async with AsyncNovitaClient() as client:
        # Run multiple operations concurrently
        instances_task = client.gpu.list_instances()
        pricing_task = client.gpu.get_pricing()

        instances, pricing = await asyncio.gather(instances_task, pricing_task)

        print(f"✓ Instances: {instances.total}")
        print(f"✓ GPU types: {len(pricing.pricing)}")
        print("✓ All operations completed, client auto-closed")


def manual_cleanup_pattern() -> None:
    """Manual cleanup pattern (not recommended)."""
    print("\n" + "=" * 60)
    print("Manual Cleanup Pattern (Not Recommended)")
    print("=" * 60 + "\n")

    client = NovitaClient()
    try:
        instances = client.gpu.list_instances()
        print(f"✓ Found {instances.total} instances")
    finally:
        # Must remember to close manually
        client.close()
        print("✓ Manually closed client")

    print("⚠ Using context managers is preferred!")


def nested_context_managers() -> None:
    """Using nested context managers (multiple clients)."""
    print("\n" + "=" * 60)
    print("Nested Context Managers (Multiple Clients)")
    print("=" * 60 + "\n")

    # You can create multiple clients if needed
    # (though usually one is sufficient)
    with NovitaClient(api_key="key1") as client1:
        with NovitaClient(api_key="key2") as client2:
            print("✓ Both clients initialized")
            # Use both clients...
            print("✓ Both clients will be cleaned up in reverse order")


async def main_async() -> None:
    """Run async examples."""
    await async_context_manager_basic()
    await async_context_manager_concurrent()


def main() -> None:
    """Run all context manager examples."""
    # Synchronous examples
    sync_context_manager_basic()
    sync_context_manager_with_error()
    manual_cleanup_pattern()
    nested_context_managers()

    # Asynchronous examples
    print("\n" + "=" * 60)
    print("Running Async Examples")
    print("=" * 60)
    asyncio.run(main_async())

    print("\n✓ All context manager examples complete!")


if __name__ == "__main__":
    main()
