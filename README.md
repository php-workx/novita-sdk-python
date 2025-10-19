# (Unofficial) Novita AI Python SDK

[![CI](https://github.com/novita-ai/novita-sdk-python/actions/workflows/ci.yaml/badge.svg)](https://github.com/novita-ai/novita-sdk-python/actions/workflows/ci.yaml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

(Unofficial,) Modern, fully type-safe Python SDK for the [Novita AI API](https://novita.ai/). Built with Pydantic v2 and httpx.

## Features

- **Fully Type-Safe**: Complete type hints for excellent IDE support
- **Async & Sync**: Both synchronous and asynchronous clients
- **Pydantic Models**: Request/response validation with Pydantic v2
- **Modern Stack**: Built on httpx and modern Python practices

## Installation

```bash
pip install novita-sdk-python
```

## Quick Start

### Authentication

Set your API key as an environment variable:

```bash
export NOVITA_API_KEY="your-api-key-here"
```

Or pass it directly to the client:

```python
from novita import NovitaClient

client = NovitaClient(api_key="your-api-key-here")
```

### Synchronous Client

```python
from novita import NovitaClient, CreateInstanceRequest, InstanceType

# Initialize client
client = NovitaClient()

# Create a GPU instance
request = CreateInstanceRequest(
    name="my-gpu-instance",
    instance_type=InstanceType.A100_80GB,
    disk_size=100
)
response = client.gpu.create_instance(request)
print(f"Created instance: {response.instance_id}")

# List all instances
instances = client.gpu.list_instances()
for instance in instances.instances:
    print(f"{instance.name}: {instance.status}")

# Clean up
client.close()
```

```

### Asynchronous Client

```python
import asyncio
from novita import AsyncNovitaClient, CreateInstanceRequest, InstanceType

async def main():
    # Use async context manager
    async with AsyncNovitaClient() as client:
        # Create instance
        request = CreateInstanceRequest(
            name="my-async-instance",
            instance_type=InstanceType.A100_80GB
        )
        response = await client.gpu.create_instance(request)
        print(f"Created: {response.instance_id}")
        
        # Get instance details
        instance = await client.gpu.get_instance(response.instance_id)
        print(f"Status: {instance.status}")

asyncio.run(main())
```

## 📚 Examples

For more detailed examples and use cases, check out the [`examples/`](./examples) directory:

- **[basic_sync.py](./examples/basic_sync.py)** - Synchronous client basics
- **[basic_async.py](./examples/basic_async.py)** - Asynchronous operations
- **[instance_lifecycle.py](./examples/instance_lifecycle.py)** - Complete lifecycle management
- **[error_handling.py](./examples/error_handling.py)** - Error handling patterns
- **[pricing_and_types.py](./examples/pricing_and_types.py)** - Pricing and instance types
- **[context_managers.py](./examples/context_managers.py)** - Context manager patterns

See the [examples README](./examples/README.md) for detailed instructions.

## Advanced Usage

### Context Managers

Both clients support context managers for automatic cleanup:

```python
# Synchronous
with NovitaClient() as client:
    instances = client.gpu.list_instances()
    # Client automatically closed

# Asynchronous
async with AsyncNovitaClient() as client:
    instances = await client.gpu.list_instances()
    # Client automatically closed
```

### Custom Configuration

```python
client = NovitaClient(
    api_key="your-key",
    base_url="https://custom-api.novita.ai",  # Custom base URL
    timeout=120.0  # Custom timeout in seconds
)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/novita-ai/novita-sdk-python.git
cd novita-sdk-python

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=novita --cov-report=term-missing

# Run specific test file
pytest tests/test_gpu_api.py -v
```

### Code Quality

```bash
# Linting
ruff check src/ tests/

# Formatting
ruff format src/ tests/

# Type checking
mypy src/
```

## Requirements

- Python 3.11 or higher

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
