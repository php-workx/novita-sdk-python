# Test Suite

## HTTP Mocking Strategy

**All tests use `pytest-httpx` to mock HTTP requests - NO real API calls are made.**

### Automatic HTTP Interception

The test suite uses an automatic fixture (`conftest.py`) that ensures:
- ✅ All HTTP requests are intercepted by `pytest-httpx`
- ✅ Any unmocked HTTP request will cause the test to **FAIL** with `httpx.TimeoutException`
- ✅ No accidental real API calls during testing

### How It Works

```python
# tests/conftest.py
@pytest.fixture(autouse=True)
def _enforce_httpx_mock(httpx_mock: HTTPXMock) -> None:
    """Automatically enforce that all HTTP requests are mocked."""
    pass  # Just including httpx_mock activates interception
```

This fixture is **automatically** applied to all tests (`autouse=True`).

### Writing Tests

Always use `httpx_mock` to set up expected HTTP responses:

```python
def test_create_instance(httpx_mock: HTTPXMock) -> None:
    # Mock the HTTP response
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/gpu/instance/create",
        json={"instance_id": "inst-123", "status": "PENDING"}
    )
    
    # Make the API call (will use the mock)
    client = NovitaClient(api_key="test-key")
    response = client.gpu.instances.create(request)
    
    # Assert the results
    assert response.instance_id == "inst-123"
```

### ⚠️ Important: Use Real API Documentation

When writing tests, **ALWAYS** check the official Novita API documentation first:
- https://novita.ai/docs/api-reference/

The mock responses should match the **actual** API response structure, not what you think it should be.

**Example:**
```python
# ❌ WRONG - Don't guess the API structure
httpx_mock.add_response(
    url=".../products",
    json={"products": [...]}  # Wrong field name!
)

# ✅ CORRECT - Check API docs first
# According to https://novita.ai/docs/api-reference/gpu-instance-list-products
httpx_mock.add_response(
    url=".../products",
    json={"data": [...]}  # Correct - matches actual API
)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_gpu_api.py

# Run specific test
pytest tests/test_gpu_api.py::test_create_instance

# Run with coverage
make test-cov
```

### Test Failures

If you see `httpx.TimeoutException`, it means:
1. A test tried to make a real HTTP request
2. The request URL didn't match any mocked response
3. The mock setup is incorrect or missing

**Solution:** Add or fix the `httpx_mock.add_response()` call to match the exact URL being requested.

### Benefits of This Approach

✅ **Fast** - No network latency  
✅ **Reliable** - No flaky tests from network issues  
✅ **Isolated** - Tests don't depend on external services  
✅ **Safe** - Can't accidentally hit production API  
✅ **Predictable** - Same results every time  
✅ **Free** - No API quota usage during testing  

### Test Organization

```
tests/
├── conftest.py              # Global test configuration
├── test_client.py           # Client initialization tests
└── test_gpu_api.py          # GPU API endpoint tests
```

### Common Patterns

#### Testing Error Responses

```python
def test_authentication_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="...",
        status_code=401,
        json={"error": "Unauthorized"}
    )
    
    client = NovitaClient(api_key="invalid")
    with pytest.raises(AuthenticationError):
        client.gpu.instances.list()
```

#### Testing with Request Body

```python
def test_with_request_body(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="...",
        json={"success": True}
    )
    
    # The mock will match regardless of request body
    # unless you specifically check it
    client.gpu.instances.create(request)
```

### Debugging Tests

If a test fails with URL mismatch:

```python
# The error shows:
# httpx.TimeoutException: No response can be found for GET request on 
# https://api.novita.ai/gpu-instance/openapi/v1/products amongst:
#   - Match GET request on https://api.novita.ai/gpu-instance/openapi/v1/gpu/pricing

# This means:
# - Test is calling /products
# - Mock is set up for /gpu/pricing
# - Fix: Update either the code or the mock to match
```

### Best Practices

1. **Check API docs first** - Don't guess the API structure
2. **Use exact URLs** - Include full URL with query parameters if needed
3. **Match HTTP methods** - GET, POST, PUT, DELETE must match
4. **Real response structure** - Use actual API response format
5. **One test, one thing** - Test one endpoint behavior at a time
6. **Clean up** - Use `client.close()` or context managers

### CI/CD

Tests run automatically in CI without any special configuration:
- No API keys needed
- No network access required  
- Fast execution (<1 second for all tests)

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: pytest tests/ -v
```

That's it! The test suite is fully isolated and will never make real HTTP requests.