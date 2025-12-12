"""Complete GPU instance lifecycle example."""

from __future__ import annotations

import os
import time

from novita import (
    APIError,
    BadRequestError,
    BillingMode,
    CreateInstanceRequest,
    EditInstanceRequest,
    Kind,
    NovitaClient,
)


def main() -> None:
    # Check for API key
    if not os.environ.get("NOVITA_API_KEY"):
        print("Error: NOVITA_API_KEY environment variable is not set")
        print("Please set it with: export NOVITA_API_KEY='your-api-key-here'")
        return

    with NovitaClient() as client:
        print("=" * 60)
        print("STEP 1: Pick an RTX 4090 (Prefer Spot Pricing)")
        print("=" * 60)
        # Use API filtering to find available RTX 4090 products
        # Note: API doesn't support filtering by availability, so we filter client-side
        products = client.gpu.products.list(
            product_name="4090",  # Fuzzy match for RTX 4090
        )
        if not products:
            raise RuntimeError("No RTX 4090 products available")

        # Filter for available products and prefer spot pricing
        available_products = [p for p in products if p.available_deploy]
        if not available_products:
            raise RuntimeError(
                f"Found {len(products)} RTX 4090 products, "
                "but none are currently available to deploy"
            )

        # Prefer spot pricing if available
        spot_products = [
            p
            for p in available_products
            if "spot" in [m.lower() for m in (p.billing_methods or [])]
        ]
        product = spot_products[0] if spot_products else available_products[0]

        # Determine billing mode based on what's supported
        billing_mode = BillingMode.spot if spot_products else BillingMode.on_demand

        product_id = product.id
        min_rootfs = product.min_root_fs or 50
        print(f"✓ Selected {product.name} (ID: {product_id})")
        print(f"  Billing mode: {billing_mode.value}")
        inventory_state = product.inventory_state.value if product.inventory_state else "unknown"
        print(f"  Inventory: {inventory_state}")

        print("\n" + "=" * 60)
        print("STEP 2: Creating GPU instance")
        print("=" * 60)
        request = CreateInstanceRequest(
            name="lifecycle-demo",
            product_id=product_id,
            gpu_num=1,
            rootfs_size=min_rootfs,
            image_url="ubuntu:22.04",
            kind=Kind.gpu,
            billing_mode=billing_mode,
        )

        try:
            response = client.gpu.instances.create(request)
            instance_id = response.id
            print(f"✓ Created instance: {instance_id}")
        except BadRequestError as e:
            print(f"✗ Failed to create instance: {e}")
            if e.details:
                print(f"  Details: {e.details}")
            return
        except APIError as e:
            print(f"✗ API error: {e}")
            if e.status_code:
                print(f"  Status code: {e.status_code}")
            if e.response_body:
                print(f"  Response: {e.response_body}")
            return

        print("\n" + "=" * 60)
        print("STEP 3: Getting instance details")
        print("=" * 60)
        instance = client.gpu.instances.get(instance_id)
        print(f"✓ Name: {instance.name}")
        print(f"  Status: {instance.status.value}")
        print(f"  Rootfs: {instance.rootfs_size}GB")

        print("\n" + "=" * 60)
        print("STEP 4: Updating instance configuration")
        print("=" * 60)
        update = EditInstanceRequest(
            instance_id=instance_id, expand_root_disk=instance.rootfs_size + 50
        )
        client.gpu.instances.edit(update)
        print("✓ Expansion request submitted")

        print("\n" + "=" * 60)
        print("STEP 5: Stopping instance")
        print("=" * 60)
        client.gpu.instances.stop(instance_id)
        print("✓ Stop initiated")

        # Poll for stopped status
        for _ in range(30):  # ~60 second timeout (30 * 2s)
            instance = client.gpu.instances.get(instance_id)
            if instance.status.value == "exited":
                print("✓ Instance stopped successfully")
                break
            time.sleep(2)
        else:
            # Timeout reached without instance stopping
            print("⚠ Warning: Instance did not stop within 60 seconds")
            print(f"  Instance ID: {instance_id}")
            print(f"  Current status: {instance.status.value}")
            print("  Proceeding with deletion anyway...")

        print("\n" + "=" * 60)
        print("STEP 6: Deleting instance")
        print("=" * 60)
        client.gpu.instances.delete(instance_id)
        print("✓ Instance deletion requested")

        print("\n✓ Lifecycle demo complete!")


if __name__ == "__main__":
    main()
