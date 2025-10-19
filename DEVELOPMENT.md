# Development Guide

## Project Structure

```
novita-sdk-python/
├── src/novita/              # Main package source
│   ├── __init__.py          # Package exports
│   ├── client.py            # Sync/Async clients
│   ├── exceptions.py        # Custom exceptions
│   ├── api/                 # API resource modules
│   │   ├── __init__.py
│   │   └── gpu.py           # GPU instance management
│   └── models/              # Pydantic models
│       ├── __init__.py
│       ├── common.py        # Common types and enums
│       └── gpu.py           # GPU-specific models
├── tests/                   # Test suite
│   ├── test_client.py       # Client tests
│   └── test_gpu_api.py      # GPU API tests
├── .devcontainer/           # Development container
│   ├── devcontainer.json
│   └── Dockerfile
├── .github/workflows/       # CI/CD pipeline
│   └── ci.yaml
├── pyproject.toml           # Project configuration
├── LICENSE                  # MIT License
└── README.md                # User documentation
```

## Features Implemented

### ✅ GPU Instance Management API
- `create_instance()` - Create new GPU instances
- `list_instances()` - List all instances
- `get_instance()` - Get instance details
- `update_instance()` - Update instance configuration
- `start_instance()` - Start stopped instances
- `stop_instance()` - Stop running instances
- `delete_instance()` - Delete instances
- `get_pricing()` - Get pricing information

### ✅ Client Architecture
- **Synchronous Client** (`NovitaClient`)
- **Asynchronous Client** (`AsyncNovitaClient`)
- Context manager support for both
- Environment variable authentication
- Custom base URL and timeout configuration

### ✅ Error Handling
- `AuthenticationError` (401)
- `BadRequestError` (400)
- `NotFoundError` (404)
- `RateLimitError` (429)
- `APIError` (5xx and other errors)
- `TimeoutError` (request timeouts)

### ✅ Type Safety
- Full type hints throughout codebase
- Pydantic V2 models for validation
- MyPy strict mode compliance
- IDE autocomplete support

### ✅ Testing
- 20 comprehensive tests
- 100% passing test suite
- Mocked HTTP requests (no real API calls)
- Tests for all endpoints and error conditions

### ✅ Code Quality
- Ruff linting and formatting
- MyPy strict type checking
- Python 3.11+ support
- Clean, idiomatic Python code

### ✅ CI/CD
- GitHub Actions workflow
- Matrix testing (Python 3.11, 3.12, 3.13)
- Linting, type checking, and testing jobs
- Code coverage reporting

### ✅ Developer Experience
- Devcontainer configuration
- Comprehensive README
- Inline documentation
- Example code snippets

## Quick Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check src/ tests/

# Run formatting
ruff format src/ tests/

# Run type checking
mypy src/

# Run all checks (as CI does)
ruff check src/ tests/ && \
ruff format --check src/ tests/ && \
mypy src/ && \
pytest tests/ -v
```

## Testing Guidelines

All tests use `pytest-httpx` to mock HTTP requests. Tests verify:

1. **Correct HTTP method and URL** are called
2. **Authorization header** is present
3. **Request body** matches expected Pydantic model
4. **Response** is correctly deserialized
5. **Errors** raise appropriate exceptions

Example test pattern:

```python
def test_create_instance(httpx_mock: HTTPXMock) -> None:
    # Mock the API response
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/v1/gpu/instances",
        json={"instance_id": "inst-123", "status": "PENDING"},
    )

    client = NovitaClient(api_key="test-key")
    request = CreateInstanceRequest(
        name="test-instance",
        instance_type=InstanceType.A100_80GB
    )

    response = client.gpu.create_instance(request)

    assert response.instance_id == "inst-123"
    assert response.status == "PENDING"

    # Verify request was made correctly
    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    assert "Bearer test-key" in request_made.headers["authorization"]

    client.close()
```

## API Coverage

### GPU Instance Endpoints ✅

All GPU instance management endpoints are fully implemented:

- `POST /v1/gpu/instances` - Create instance
- `GET /v1/gpu/instances` - List instances
- `GET /v1/gpu/instances/{id}` - Get instance
- `PATCH /v1/gpu/instances/{id}` - Update instance
- `POST /v1/gpu/instances/{id}/start` - Start instance
- `POST /v1/gpu/instances/{id}/stop` - Stop instance
- `DELETE /v1/gpu/instances/{id}` - Delete instance
- `GET /v1/gpu/pricing` - Get pricing

## Next Steps (Future Enhancements)

If you want to extend the SDK:

1. **Model APIs**: Add text-to-image, image-to-image, etc.
2. **Utility APIs**: Add account info, balance checking, etc.
3. **Webhooks**: Add webhook support for async operations
4. **Pagination**: Add pagination helpers for list operations
5. **Retry Logic**: Add automatic retry with exponential backoff
6. **Rate Limiting**: Add client-side rate limiting

## Contributing

1. Create a feature branch
2. Implement changes with tests
3. Run all quality checks
4. Submit a pull request

All PRs must pass:
- ✅ Ruff linting
- ✅ Ruff formatting
- ✅ MyPy type checking
- ✅ Pytest (all tests passing)

## Version

Current version: **0.1.0**

## License

MIT License - see LICENSE file
