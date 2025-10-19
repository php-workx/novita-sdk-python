# Novita SDK Examples

This directory contains practical examples demonstrating various features and usage patterns of the Novita AI Python SDK.

## Prerequisites

Before running the examples, make sure you have:

1. **Installed the SDK:**
   ```bash
   pip install novita-sdk-python
   ```

2. **Set your API key:**
   ```bash
   export NOVITA_API_KEY="your-api-key-here"
   ```

## Available Examples

### 1. Basic Synchronous Usage
**File:** [`basic_sync.py`](./basic_sync.py)

Learn the fundamentals of using the synchronous client:
- Client initialization
- Creating GPU instances
- Listing instances
- Getting instance details
- Proper resource cleanup

```bash
python examples/basic_sync.py
```

### 2. Asynchronous Operations
**File:** [`basic_async.py`](./basic_async.py)

Explore async/await patterns:
- Async client usage
- Async context managers
- Concurrent operations with `asyncio.gather`
- Non-blocking API calls

```bash
python examples/basic_async.py
```

### 3. Instance Lifecycle Management
**File:** [`instance_lifecycle.py`](./instance_lifecycle.py)

Complete guide to managing GPU instances through their entire lifecycle:
- Creating instances
- Updating configuration
- Starting and stopping instances
- Deleting instances
- Step-by-step lifecycle demonstration

```bash
python examples/instance_lifecycle.py
```

### 4. Error Handling Patterns
**File:** [`error_handling.py`](./error_handling.py)

Master error handling and recovery strategies:
- Handling specific exception types
- Retry logic for transient failures
- Best practices for error recovery
- Graceful degradation

```bash
python examples/error_handling.py
```

### 5. Pricing and Instance Types
**File:** [`pricing_and_types.py`](./pricing_and_types.py)

Understand GPU pricing and make informed decisions:
- Fetching pricing information
- Comparing instance types
- Cost estimation
- Finding best value options

```bash
python examples/pricing_and_types.py
```

### 6. Context Managers
**File:** [`context_managers.py`](./context_managers.py)

Learn proper resource management patterns:
- Sync and async context managers
- Automatic cleanup
- Error handling within context managers
- Best practices

```bash
python examples/context_managers.py
```

## Running Examples

### Run a Specific Example
```bash
python examples/<example_name>.py
```

### Run All Examples
```bash
for file in examples/*.py; do
    [ -f "$file" ] && echo "Running $file..." && python "$file" && echo ""
done
```

## Example Structure

Each example follows this structure:

```python
"""Example description.

This example demonstrates:
- Feature 1
- Feature 2
- Feature 3
"""

from novita import NovitaClient

def main() -> None:
    """Main example function."""
    # Example code here
    pass

if __name__ == "__main__":
    main()
```

## Common Patterns

### Pattern 1: Using Context Managers (Recommended)
```python
with NovitaClient() as client:
    # Your operations here
    instances = client.gpu.list_instances()
# Client automatically closed
```

### Pattern 2: Manual Cleanup
```python
client = NovitaClient()
try:
    instances = client.gpu.list_instances()
finally:
    client.close()
```

### Pattern 3: Async Operations
```python
async with AsyncNovitaClient() as client:
    instances = await client.gpu.list_instances()
```

## Error Handling

All examples include proper error handling:

```python
from novita import AuthenticationError, BadRequestError, NovitaClient

try:
    client = NovitaClient()
    # Operations...
except AuthenticationError:
    print("Invalid API key")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
finally:
    client.close()
```

## Tips

1. **Always use context managers** when possible for automatic cleanup
2. **Handle exceptions appropriately** for production code
3. **Use async operations** for better performance with multiple requests
4. **Check pricing** before creating expensive GPU instances
5. **Clean up resources** by deleting instances when done

## Need Help?

- **Documentation:** [Novita API Docs](https://novita.ai/docs/api-reference/)
- **SDK README:** [../README.md](../README.md)
- **Issues:** [GitHub Issues](https://github.com/novita-ai/novita-sdk-python/issues)

## Contributing

Have a useful example to share? Contributions are welcome!

1. Create your example file following the existing pattern
2. Add it to this README
3. Submit a pull request

---

**Note:** These examples use the Novita API and will consume credits. Always clean up instances when you're done to avoid unnecessary charges.
