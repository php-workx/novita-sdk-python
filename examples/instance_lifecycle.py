"""Complete GPU instance lifecycle example.

This example demonstrates:
- Creating an instance
- Updating instance configuration
- Starting and stopping instances
- Deleting instances
- Full lifecycle management
"""

import time

from novita import CreateInstanceRequest, InstanceType, NovitaClient, UpdateInstanceRequest


def main() -> None:
    """Demonstrate full instance lifecycle."""
    with NovitaClient() as client:
        # Step 1: Create instance
        print("=" * 60)
        print("STEP 1: Creating GPU instance")
        print("=" * 60)
        request = CreateInstanceRequest(
            name="lifecycle-demo",
            instance_type=InstanceType.A10,
            disk_size=50,
        )
        response = client.gpu.instances.create(request)
        instance_id = response.instance_id
        print(f"✓ Created instance: {instance_id}")
        print(f"  Initial status: {response.status}")

        # Step 2: Get instance details
        print("\n" + "=" * 60)
        print("STEP 2: Getting instance details")
        print("=" * 60)
        instance = client.gpu.instances.get(instance_id)
        print(f"✓ Name: {instance.name}")
        print(f"  Type: {instance.instance_type}")
        print(f"  Status: {instance.status}")
        print(f"  Disk: {instance.disk_size}GB")

        # Step 3: Update instance
        print("\n" + "=" * 60)
        print("STEP 3: Updating instance configuration")
        print("=" * 60)
        update = UpdateInstanceRequest(name="lifecycle-demo-updated", disk_size=100)
        updated = client.gpu.instances.edit(instance_id, update)
        print(f"✓ Updated name: {updated.name}")
        print(f"  Updated disk: {updated.disk_size}GB")

        # Step 4: Stop instance (if running)
        print("\n" + "=" * 60)
        print("STEP 4: Stopping instance")
        print("=" * 60)
        stop_response = client.gpu.instances.stop(instance_id)
        print(f"✓ Stop initiated: {stop_response.success}")
        if stop_response.message:
            print(f"  Message: {stop_response.message}")

        # Wait a moment
        print("  Waiting 2 seconds...")
        time.sleep(2)

        # Step 5: Start instance
        print("\n" + "=" * 60)
        print("STEP 5: Starting instance")
        print("=" * 60)
        start_response = client.gpu.instances.start(instance_id)
        print(f"✓ Start initiated: {start_response.success}")
        if start_response.message:
            print(f"  Message: {start_response.message}")

        # Step 6: Delete instance
        print("\n" + "=" * 60)
        print("STEP 6: Deleting instance")
        print("=" * 60)
        delete_response = client.gpu.instances.delete(instance_id)
        print(f"✓ Deletion initiated: {delete_response.success}")
        print("\n✓ Lifecycle demo complete!")


if __name__ == "__main__":
    main()
