"""Complete GPU instance lifecycle example."""

from __future__ import annotations

import time

from novita import CreateInstanceRequest, EditInstanceRequest, Kind, NovitaClient


def _pick_product(client: NovitaClient) -> tuple[str, int]:
    products = client.gpu.products.list()
    if not products:
        raise RuntimeError("No GPU products available")
    product = products[0]
    return product.id, product.min_root_fs or 50


def main() -> None:
    with NovitaClient() as client:
        product_id, min_rootfs = _pick_product(client)

        print("=" * 60)
        print("STEP 1: Creating GPU instance")
        print("=" * 60)
        request = CreateInstanceRequest(
            name="lifecycle-demo",
            product_id=product_id,
            gpu_num=1,
            rootfs_size=min_rootfs,
            image_url="docker.io/library/ubuntu:latest",
            kind=Kind.gpu,
        )
        response = client.gpu.instances.create(request)
        instance_id = response.id
        print(f"✓ Created instance: {instance_id}")

        print("\n" + "=" * 60)
        print("STEP 2: Getting instance details")
        print("=" * 60)
        instance = client.gpu.instances.get(instance_id)
        print(f"✓ Name: {instance.name}")
        print(f"  Status: {instance.status.value}")
        print(f"  Rootfs: {instance.rootfs_size}GB")

        print("\n" + "=" * 60)
        print("STEP 3: Updating instance configuration")
        print("=" * 60)
        update = EditInstanceRequest(
            instance_id=instance_id, expand_root_disk=instance.rootfs_size + 50
        )
        client.gpu.instances.edit(update)
        print("✓ Expansion request submitted")

        print("\n" + "=" * 60)
        print("STEP 4: Stopping instance")
        print("=" * 60)
        client.gpu.instances.stop(instance_id)
        print("✓ Stop initiated")
        time.sleep(2)

        print("\n" + "=" * 60)
        print("STEP 5: Starting instance")
        print("=" * 60)
        client.gpu.instances.start(instance_id)
        print("✓ Start initiated")

        print("\n" + "=" * 60)
        print("STEP 6: Deleting instance")
        print("=" * 60)
        client.gpu.instances.delete(instance_id)
        print("✓ Instance deletion requested")

        print("\n✓ Lifecycle demo complete!")


if __name__ == "__main__":
    main()
