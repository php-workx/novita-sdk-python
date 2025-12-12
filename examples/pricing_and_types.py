"""GPU pricing and instance types example."""

from __future__ import annotations

import os

from novita import NovitaClient


def display_pricing(client: NovitaClient) -> None:
    print("=" * 60)
    print("GPU Instance Pricing")
    print("=" * 60)

    products = client.gpu.products.list()

    print(f"\nTotal GPU types available: {len(products)}\n")

    sorted_pricing = sorted(products, key=lambda x: x.price or 0)

    print(f"{'Instance Type':<25} {'Price/Hour':<15} {'Available':<10}")
    print("-" * 60)

    for item in sorted_pricing:
        price = item.price or 0
        price_str = f"${price:.2f}"
        available_str = "✓ Yes" if item.available_deploy else "✗ No"
        print(f"{item.id:<25} {price_str:<15} {available_str:<10}")


def find_best_value(client: NovitaClient) -> None:
    print("=" * 60)
    print("Best Value Analysis")
    print("=" * 60 + "\n")

    products = client.gpu.products.list()
    available = [p for p in products if p.available_deploy]
    available.sort(key=lambda x: x.price or float("inf"))

    if not available:
        print("⚠ No GPU instances currently available")
        return

    cheapest = available[0]
    print("Recommendations:\n")
    print(f"💰 Most Economical: {cheapest.id}")
    print(f"   ${(cheapest.price or 0):.2f}/hour\n")

    if len(available) > 2:
        mid = available[len(available) // 2]
        print(f"⚖️  Balanced Option: {mid.id}")
        print(f"   ${(mid.price or 0):.2f}/hour\n")

    premium = available[-1]
    print(f"🚀 Maximum Performance: {premium.id}")
    print(f"   ${(premium.price or 0):.2f}/hour\n")


def estimate_costs(instance_type: str, price_per_hour: float) -> None:
    print(f"\nCost Estimates for {instance_type}:")
    print(f"  1 hour:   ${price_per_hour * 1:.2f}")
    print(f"  8 hours:  ${price_per_hour * 8:.2f}")
    print(f"  24 hours: ${price_per_hour * 24:.2f}")
    print(f"  1 week:   ${price_per_hour * 24 * 7:.2f}")
    print(f"  1 month:  ${price_per_hour * 24 * 30:.2f}")


def main() -> None:
    # Check for API key
    if not os.environ.get("NOVITA_API_KEY"):
        print("Error: NOVITA_API_KEY environment variable is not set")
        print("Please set it with: export NOVITA_API_KEY='your-api-key-here'")
        return

    with NovitaClient() as client:
        display_pricing(client)

        print()
        find_best_value(client)

        print("=" * 60)
        print("Cost Estimation Example")
        print("=" * 60)
        estimate_costs(instance_type="A100_80GB", price_per_hour=3.50)

        print("\n✓ Pricing analysis complete!")


if __name__ == "__main__":
    main()
