"""Utility functions for integration tests."""

from __future__ import annotations

from datetime import datetime


def generate_test_name(prefix: str = "test") -> str:
    """Generate a timestamped test resource name.

    Format: {prefix}-YYYYMMDD-HHMMSS

    Args:
        prefix: Prefix for the resource name (default: "test")

    Returns:
        Timestamped resource name

    Examples:
        >>> generate_test_name("instance")
        'test-instance-20241214-153022'
        >>> generate_test_name("endpoint")
        'test-endpoint-20241214-153022'
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"test-{prefix}-{timestamp}"
