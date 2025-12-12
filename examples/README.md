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

## Tips

1. **Always use context managers** when possible for automatic cleanup
2. **Handle exceptions appropriately** for production code
3. **Use async operations** for better performance with multiple requests
4. **Check pricing** before creating expensive GPU instances
5. **Clean up resources** by deleting instances when done
