# Integration Tests

This directory contains integration tests for the Novita SDK. These tests interact with the actual Novita API to verify end-to-end functionality.

## Prerequisites

1. **API Key**: You need a valid Novita API key to run integration tests
2. **Python Environment**: Python 3.8 or higher
3. **Dependencies**: Install the SDK and test dependencies

```bash
pip install -e .
pip install pytest pytest-asyncio
```

## Setup

### 1. Set Your API Key

Export your Novita API key as an environment variable:

```bash
export NOVITA_API_KEY="your-api-key-here"
```

Alternatively, create a `.env` file in the project root:

```
NOVITA_API_KEY=your-api-key-here
```

### 2. Verify Setup

Run a simple test to verify your setup:

```bash
pytest tests/integration/test_clusters.py::TestClusters::test_list_clusters -v
```

## Running Tests

### Run All Integration Tests

```bash
pytest tests/integration/ -v
```

### Run Tests for a Specific Resource Type

```bash
# Cluster tests
pytest tests/integration/test_clusters.py -v

# Product tests
pytest tests/integration/test_products.py -v

# Instance tests
pytest tests/integration/test_instances.py -v

# Endpoint tests
pytest tests/integration/test_endpoints.py -v

# Job tests
pytest tests/integration/test_jobs.py -v

# Image registry tests
pytest tests/integration/test_image_registry.py -v

# Network tests
pytest tests/integration/test_networks.py -v

# Network storage tests
pytest tests/integration/test_network_storage.py -v

# Template tests
pytest tests/integration/test_templates.py -v

# Image prewarm tests
pytest tests/integration/test_image_prewarm.py -v

# Metrics tests
pytest tests/integration/test_metrics.py -v
```

### Run a Specific Test

```bash
pytest tests/integration/test_clusters.py::TestClusters::test_list_clusters -v
```

### Run Tests with Different Verbosity

```bash
# Minimal output
pytest tests/integration/ -q

# Verbose output
pytest tests/integration/ -v

# Very verbose output (includes print statements)
pytest tests/integration/ -vv

# Show test output even for passing tests
pytest tests/integration/ -v -s
```

## Test Categories

### Read-Only Tests (Safe to Run Anytime)

These tests only query the API and don't create, modify, or delete resources. They are safe to run repeatedly without incurring costs:

- `test_clusters.py` - Cluster/region information
- `test_products.py` - GPU and CPU product listings
- `test_instances.py` - Instance listing and details (read-only tests)
- `test_endpoints.py` - Endpoint listing and limits (read-only tests)
- `test_jobs.py` - Job listing
- `test_image_registry.py` - Registry auth listing (read-only tests)
- `test_networks.py` - Network listing (read-only tests)
- `test_network_storage.py` - Storage listing (read-only tests)
- `test_templates.py` - Template listing (read-only tests)
- `test_image_prewarm.py` - Prewarm task listing (read-only tests)
- `test_metrics.py` - Metrics retrieval

### Lifecycle Tests (Currently Skipped)

These tests create, modify, and delete resources. They are currently marked with `@pytest.mark.skip` and will be implemented in the future:

- Instance lifecycle (create, update, start, stop, delete)
- Endpoint lifecycle (create, update, delete)
- Network lifecycle (create, update, delete)
- Network storage lifecycle (create, update, delete)
- Template lifecycle (create, delete)
- Image prewarm lifecycle (create, update, delete)
- Registry auth lifecycle (create, delete)

To see skipped tests:

```bash
pytest tests/integration/ -v --tb=no
```

## Test Structure

Each test file is organized by resource type:

```
tests/integration/
├── __init__.py
├── conftest.py              # Shared fixtures
├── utils.py                 # Utility functions for lifecycle tests
├── test_clusters.py         # Cluster tests
├── test_products.py         # Product tests (GPU & CPU)
├── test_instances.py        # Instance tests
├── test_endpoints.py        # Serverless endpoint tests
├── test_jobs.py             # Job tests
├── test_image_registry.py   # Image registry auth tests
├── test_networks.py         # VPC network tests
├── test_network_storage.py  # Network storage tests
├── test_templates.py        # Template tests
├── test_image_prewarm.py    # Image prewarm tests
└── test_metrics.py          # Metrics tests
```

## Shared Fixtures

The `conftest.py` file provides shared fixtures used across tests:

- `api_key` - API key from environment variable
- `client` - NovitaClient instance
- `cluster_id` - Valid cluster ID from the API
- `product_id` - Valid GPU product ID
- `cpu_product_id` - Valid CPU product ID

## Utility Functions

The `utils.py` file provides helper functions for lifecycle tests:

- `wait_for_condition()` - Generic wait function
- `wait_for_instance_status()` - Wait for instance to reach specific status
- `wait_for_endpoint_status()` - Wait for endpoint to reach specific status
- `cleanup_instance()` - Clean up test instances
- `cleanup_endpoint()` - Clean up test endpoints
- `cleanup_network()` - Clean up test networks
- `cleanup_network_storage()` - Clean up test storage
- `cleanup_template()` - Clean up test templates

## Future Lifecycle Tests

Lifecycle tests will test the full CRUD operations for each resource type. These will:

1. Create a resource
2. Verify it appears in listings
3. Update the resource (where applicable)
4. Delete the resource
5. Verify cleanup

Example workflow for instance lifecycle:
```python
# Create instance
instance = client.gpu.instances.create(...)
wait_for_instance_status(client, instance.id, "running")

# Update instance
client.gpu.instances.update(instance.id, ...)

# Stop instance
client.gpu.instances.stop(instance.id)
wait_for_instance_status(client, instance.id, "exited")

# Delete instance
cleanup_instance(client, instance.id)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest
      - name: Run integration tests
        env:
          NOVITA_API_KEY: ${{ secrets.NOVITA_API_KEY }}
        run: pytest tests/integration/ -v
```

## Troubleshooting

### API Key Issues

If you see `SKIPPED [1] ... NOVITA_API_KEY environment variable not set`:

```bash
# Check if API key is set
echo $NOVITA_API_KEY

# Set it if missing
export NOVITA_API_KEY="your-api-key-here"
```

### Authentication Errors

If you see 401 errors, verify your API key is valid:

```bash
curl -H "Authorization: Bearer $NOVITA_API_KEY" \
  https://api.novita.ai/gpu-instance/openapi/v1/clusters
```

### No Resources Found

Some tests are skipped if no resources are available (e.g., no instances exist). This is normal behavior.

### Rate Limiting

If you encounter rate limiting errors, add delays between test runs or reduce parallelization:

```bash
# Run tests sequentially
pytest tests/integration/ -v -n 1
```

## Best Practices

1. **Don't commit API keys** - Always use environment variables
2. **Clean up resources** - Use the cleanup utilities to avoid orphaned resources
3. **Monitor costs** - Be aware that lifecycle tests will create billable resources
4. **Use test markers** - Tag expensive tests with custom markers
5. **Test in stages** - Run read-only tests first, then lifecycle tests

## Contributing

When adding new integration tests:

1. Follow the existing test structure
2. Use shared fixtures from `conftest.py`
3. Add cleanup logic for lifecycle tests
4. Document any special requirements
5. Mark expensive/slow tests appropriately
