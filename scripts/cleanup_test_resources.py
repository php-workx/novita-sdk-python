#!/usr/bin/env python3
"""Clean up test resources created during integration tests.

This script deletes all resources with names starting with 'test-' prefix.
Run this before integration tests to clean up any leaked resources from previous runs.

By default, deletes all test resources. Use --min-age to only delete older resources.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from novita import NovitaClient


def parse_timestamp_from_name(name: str) -> datetime | None:
    """Extract timestamp from resource name.

    Resource names are expected to be in format: test-{type}-YYYYMMDD-HHMMSS

    Args:
        name: Resource name

    Returns:
        datetime object if timestamp found, None otherwise
    """
    # Pattern: test-{type}-YYYYMMDD-HHMMSS
    pattern = r"test-\w+-(\d{8})-(\d{6})"
    match = re.search(pattern, name)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        try:
            return datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S").replace(tzinfo=UTC)
        except ValueError:
            return None
    return None


def is_old_enough(name: str, min_age_hours: float) -> bool:
    """Check if resource is old enough to delete.

    Args:
        name: Resource name
        min_age_hours: Minimum age in hours (0.0 means delete all)

    Returns:
        True if resource should be deleted
    """
    if min_age_hours == 0:
        return True

    timestamp = parse_timestamp_from_name(name)
    if timestamp is None:
        # If we can't parse timestamp, delete it (legacy format or corrupted)
        return True

    age = datetime.now(UTC) - timestamp
    return age >= timedelta(hours=min_age_hours)


def cleanup_instances(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test instances.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        instances = client.gpu.instances.list()
        test_instances = [
            i
            for i in instances
            if i.name and i.name.startswith("test-") and is_old_enough(i.name, min_age_hours)
        ]

        for instance in test_instances:
            try:
                print(f"Deleting instance: {instance.id} ({instance.name})")
                client.gpu.instances.delete(instance.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete instance {instance.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list instances: {e}")
        errors += 1

    return deleted, errors


def cleanup_endpoints(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test endpoints.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        endpoints = client.gpu.endpoints.list()
        test_endpoints = [
            e
            for e in endpoints
            if e.name and e.name.startswith("test-") and is_old_enough(e.name, min_age_hours)
        ]

        for endpoint in test_endpoints:
            try:
                print(f"Deleting endpoint: {endpoint.id} ({endpoint.name})")
                client.gpu.endpoints.delete(endpoint.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete endpoint {endpoint.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list endpoints: {e}")
        errors += 1

    return deleted, errors


def cleanup_templates(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test templates.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        templates = client.gpu.templates.list()
        test_templates = [
            t
            for t in templates
            if t.name and t.name.startswith("test-") and is_old_enough(t.name, min_age_hours)
        ]

        for template in test_templates:
            try:
                print(f"Deleting template: {template.id} ({template.name})")
                client.gpu.templates.delete(template.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete template {template.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list templates: {e}")
        errors += 1

    return deleted, errors


def cleanup_networks(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test networks.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        networks = client.gpu.networks.list()
        test_networks = [
            n
            for n in networks
            if n.name and n.name.startswith("test-") and is_old_enough(n.name, min_age_hours)
        ]

        for network in test_networks:
            try:
                print(f"Deleting network: {network.id} ({network.name})")
                client.gpu.networks.delete(network.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete network {network.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list networks: {e}")
        errors += 1

    return deleted, errors


def cleanup_storages(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test network storages.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        storages = client.gpu.storages.list()
        test_storages = [
            s
            for s in storages
            if s.storage_name
            and s.storage_name.startswith("test-")
            and is_old_enough(s.storage_name, min_age_hours)
        ]

        for storage in test_storages:
            try:
                print(f"Deleting storage: {storage.storage_id} ({storage.storage_name})")
                client.gpu.storages.delete(storage.storage_id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete storage {storage.storage_id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list storages: {e}")
        errors += 1

    return deleted, errors


def cleanup_registries(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test image registry authentications.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        auths = client.gpu.registries.list()
        test_auths = [
            a
            for a in auths
            if a.registry
            and a.registry.startswith("test-")
            and is_old_enough(a.registry, min_age_hours)
        ]

        for auth in test_auths:
            try:
                print(f"Deleting registry auth: {auth.id} ({auth.registry})")
                client.gpu.registries.delete(auth.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete registry auth {auth.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list registry auths: {e}")
        errors += 1

    return deleted, errors


def cleanup_image_prewarm(client: NovitaClient, min_age_hours: float = 0) -> tuple[int, int]:
    """Clean up test image prewarm tasks.

    Args:
        client: NovitaClient instance
        min_age_hours: Only delete resources older than this many hours (0.0 = all)

    Returns:
        Tuple of (deleted_count, error_count)
    """
    deleted = 0
    errors = 0

    try:
        tasks = client.gpu.image_prewarm.list()
        # For image prewarm, check if the image contains test- tag
        test_tasks = [
            t
            for t in tasks
            if t.image and "test-" in t.image and is_old_enough(t.image, min_age_hours)
        ]

        for task in test_tasks:
            try:
                print(f"Deleting prewarm task: {task.id} ({task.image})")
                client.gpu.image_prewarm.delete(task.id)
                deleted += 1
            except Exception as e:
                print(f"  Failed to delete prewarm task {task.id}: {e}")
                errors += 1
    except Exception as e:
        print(f"Failed to list prewarm tasks: {e}")
        errors += 1

    return deleted, errors


def main() -> int:
    """Main cleanup function.

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    parser = argparse.ArgumentParser(
        description="Clean up test resources from Novita API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Delete all test resources
  %(prog)s

  # Delete only resources older than 2 hours
  %(prog)s --min-age 2

  # Delete only resources older than 30 minutes
  %(prog)s --min-age 0.5
        """,
    )
    parser.add_argument(
        "--min-age",
        type=float,
        default=0,
        help="Only delete resources older than this many hours (default: 0.0 = delete all)",
    )
    args = parser.parse_args()

    api_key = os.getenv("NOVITA_API_KEY")
    if not api_key:
        print("Error: NOVITA_API_KEY environment variable not set")
        return 1

    # Import here to avoid import errors if package not installed
    try:
        from novita import NovitaClient
    except ImportError:
        print("Error: novita package not installed")
        return 1

    client = NovitaClient(api_key=api_key)

    print("=" * 60)
    if args.min_age > 0:
        print(f"Cleaning up test resources older than {args.min_age} hours...")
    else:
        print("Cleaning up all test resources...")
    print("=" * 60)

    total_deleted = 0
    total_errors = 0

    # Cleanup each resource type
    resource_types = [
        ("instances", cleanup_instances),
        ("endpoints", cleanup_endpoints),
        ("templates", cleanup_templates),
        ("networks", cleanup_networks),
        ("storages", cleanup_storages),
        ("registry auths", cleanup_registries),
        ("prewarm tasks", cleanup_image_prewarm),
    ]

    for resource_name, cleanup_func in resource_types:
        print(f"\nCleaning up {resource_name}...")
        deleted, errors = cleanup_func(client, min_age_hours=args.min_age)
        total_deleted += deleted
        total_errors += errors

        if deleted > 0:
            print(f"  Deleted {deleted} {resource_name}")
        if errors > 0:
            print(f"  Encountered {errors} errors")

    print("\n" + "=" * 60)
    print(f"Cleanup complete: {total_deleted} resources deleted, {total_errors} errors")
    print("=" * 60)

    client.close()

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
