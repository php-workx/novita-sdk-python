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
pip install novita-sdk
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
from novita import NovitaClient, CreateInstanceRequest, Kind

client = NovitaClient()

request = CreateInstanceRequest(
    name="my-gpu-instance",
    product_id="prod-123",  # fetch via client.gpu.products.list()
    gpu_num=1,
    rootfs_size=50,
    image_url="ubuntu:22.04",
    kind=Kind.gpu,
)
response = client.gpu.instances.create(request)
print(f"Created instance: {response.id}")

instances = client.gpu.instances.list()
for instance in instances:
    print(f"{instance.name}: {instance.status.value}")

client.close()
```

### Asynchronous Client

```python
import asyncio
from novita import AsyncNovitaClient, CreateInstanceRequest, Kind

async def main():
    async with AsyncNovitaClient() as client:
        request = CreateInstanceRequest(
            name="my-async-instance",
            product_id="prod-123",
            gpu_num=1,
            rootfs_size=50,
            image_url="ubuntu:22.04",
            kind=Kind.gpu,
        )
        response = await client.gpu.instances.create(request)
        print(f"Created: {response.id}")

        instance = await client.gpu.instances.get(response.id)
        print(f"Status: {instance.status.value}")

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
    instances = client.gpu.instances.list()
    # Client automatically closed

# Asynchronous
async with AsyncNovitaClient() as client:
    instances = await client.gpu.instances.list()
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

### Price Conversion

**Important**: The Novita API returns prices in an unusual format (units of 1/100,000 USD). This SDK automatically converts all prices to standard USD for your convenience.

For example:
- API returns `67000` → SDK provides `$0.67/hour`
- API returns `35000` → SDK provides `$0.35/hour`

This conversion is applied to:
- `GPUProduct.price` - On-demand pricing
- `GPUProduct.spot_price` - Spot instance pricing
- `SubscriptionPrice.price` - Monthly subscription pricing
- `CPUProduct.price` - CPU instance pricing

The raw API values are still available if needed via `*_raw` fields (`price_raw`, `spot_price_raw`, etc.):
```python
products = client.gpu.products.list()
product = products[0]

print(f"Converted: ${product.price}/hour")  # e.g., $0.67/hour
print(f"Raw API value: {product.price_raw}")  # e.g., 67000
print(f"Spot (converted): ${product.spot_price}/hour")
print(f"Spot (raw): {product.spot_price_raw}")
```

## API Resources

The SDK provides complete coverage of the Novita GPU Cloud API:

- **Instances** - GPU instance lifecycle management
- **Products** - GPU and CPU product listings with filtering
- **Endpoints** - API endpoint management
- **Networks** - VPC network configuration
- **Templates** - Instance template management
- **Jobs** - Job execution and control
- **Metrics** - Instance performance metrics
- **Storages** - Network storage management
- **Image Registry** - Container registry authentication
- **Images** - Image prewarm task management
- **Clusters** - Available GPU cluster information

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks automatically run on every commit and check:

- **Linting** - Ruff checks for code issues
- **Formatting** - Ruff formats code consistently
- **Type checking** - MyPy validates type hints
- **Unit tests** - Fast test suite ensures no regressions
- **File checks** - Trailing whitespace, end-of-file, YAML/TOML validation

Install the hooks:

```bash
make pre-commit-install
```

Run manually on all files:

```bash
make pre-commit-run
```

Skip hooks for a specific commit (use sparingly):

```bash
git commit --no-verify
```

## Requirements

- Python 3.11 or higher

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
