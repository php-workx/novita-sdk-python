"""GPU pricing and instance types example.

This example demonstrates:
- Getting pricing information
- Listing available instance types
- Comparing GPU options
- Making cost-effective choices
"""

from novita import InstanceType, NovitaClient


def display_pricing(client: NovitaClient) -> None:
    """Display pricing information for all GPU types."""
    print("=" * 60)
    print("GPU Instance Pricing")
    print("=" * 60)

    pricing = client.gpu.products.list()

    print(f"\nTotal GPU types available: {len(pricing.data)}\n")

    # Sort by price
    sorted_pricing = sorted(pricing.data, key=lambda x: x.price)

    print(f"{'Instance Type':<20} {'Price/Hour':<15} {'Available':<10}")
    print("-" * 60)

    for item in sorted_pricing:
        price_str = f"${item.price:.2f}"
        available_str = "✓ Yes" if item.available_deploy else "✗ No"
        print(f"{item.id:<20} {price_str:<15} {available_str:<10}")


def display_instance_types() -> None:
    """Display all available instance type enums."""
    print("\n" + "=" * 60)
    print("Available Instance Types (from SDK)")
    print("=" * 60 + "\n")

    types = [
        (InstanceType.A100_80GB, "NVIDIA A100 80GB - Flagship GPU for AI training"),
        (InstanceType.A100_40GB, "NVIDIA A100 40GB - High-performance AI GPU"),
        (InstanceType.A10, "NVIDIA A10 - Cost-effective inference GPU"),
        (InstanceType.L40, "NVIDIA L40 - Multi-workload GPU"),
        (InstanceType.RTX_4090, "NVIDIA RTX 4090 - Consumer-grade powerhouse"),
        (InstanceType.RTX_A6000, "NVIDIA RTX A6000 - Professional workstation GPU"),
    ]

    for gpu_type, description in types:
        print(f"• {gpu_type.value}")
        print(f"  {description}\n")


def find_best_value(client: NovitaClient) -> None:
    """Find the best value GPU based on price and availability."""
    print("=" * 60)
    print("Best Value Analysis")
    print("=" * 60 + "\n")

    pricing = client.gpu.products.list()

    # Filter available GPUs and sort by price
    available = [p for p in pricing.data if p.available_deploy]
    available.sort(key=lambda x: x.price)

    if not available:
        print("⚠ No GPU instances currently available")
        return

    print("Recommendations:\n")

    # Cheapest option
    cheapest = available[0]
    print(f"💰 Most Economical: {cheapest.id}")
    print(f"   ${cheapest.price:.2f}/hour\n")

    # Mid-range option
    if len(available) > 2:
        mid_idx = len(available) // 2
        mid_range = available[mid_idx]
        print(f"⚖️  Balanced Option: {mid_range.id}")
        print(f"   ${mid_range.price:.2f}/hour\n")

    # Premium option
    premium = available[-1]
    print(f"🚀 Maximum Performance: {premium.id}")
    print(f"   ${premium.price:.2f}/hour\n")


def estimate_costs(instance_type: str, price_per_hour: float) -> None:
    """Estimate costs for different time periods.

    Args:
        hours: Number of hours to estimate
        instance_type: Type of GPU instance
        price_per_hour: Hourly rate
    """
    print(f"\nCost Estimates for {instance_type}:")
    print(f"  1 hour:   ${price_per_hour * 1:.2f}")
    print(f"  8 hours:  ${price_per_hour * 8:.2f}")
    print(f"  24 hours: ${price_per_hour * 24:.2f}")
    print(f"  1 week:   ${price_per_hour * 24 * 7:.2f}")
    print(f"  1 month:  ${price_per_hour * 24 * 30:.2f}")


def main() -> None:
    """Run pricing and instance type examples."""
    with NovitaClient() as client:
        # Display available instance types
        display_instance_types()

        # Get and display pricing
        display_pricing(client)

        # Find best value options
        print()
        find_best_value(client)

        # Example cost estimation
        print("=" * 60)
        print("Cost Estimation Example")
        print("=" * 60)
        estimate_costs(
            hours=1,
            instance_type="A100_80GB",
            price_per_hour=3.50,  # Example price
        )

        print("\n✓ Pricing analysis complete!")


if __name__ == "__main__":
    main()
