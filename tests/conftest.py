"""Pytest configuration for test suite.

This configuration ensures that:
1. All HTTP requests are mocked using pytest-httpx
2. Tests fail if they attempt real HTTP requests
3. Common test fixtures are available
"""

import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(autouse=True)
def _enforce_httpx_mock(httpx_mock: HTTPXMock) -> None:
    """Automatically enforce that all HTTP requests are mocked.
    This fixture is automatically used for all tests (autouse=True).
    It ensures that pytest-httpx is active, which will raise an exception
    if any test tries to make a real HTTP request without a corresponding mock.
    Args:
        httpx_mock: The httpx mock fixture from pytest-httpx
    """
    # Just by including httpx_mock as a fixture parameter,
    # pytest-httpx will intercept all httpx requests.
    # Any unmocked request will raise httpx.TimeoutException
    pass


@pytest.fixture
def api_key() -> str:
    """Provide a test API key for test fixtures.
    Returns:
        A fake API key to use in tests
    """
    return "test-api-key-12345"
