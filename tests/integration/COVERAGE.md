# Integration Test Coverage

This document tracks which API endpoints have integration test coverage.

## Summary

- **Total Non-Invasive Endpoints**: 14
- **Covered**: 14 (100%)
- **Lifecycle Tests Planned**: 7

## Endpoint Coverage

### ✅ Clusters (2/2)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/clusters` | GET | `test_clusters.py` | ✅ Covered |
| Cluster validation | - | `test_clusters.py` | ✅ Covered |

### ✅ Products (4/4)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/products` | GET | `test_products.py` | ✅ Covered |
| `/products` (with filters) | GET | `test_products.py` | ✅ Covered |
| `/cpu/products` | GET | `test_products.py` | ✅ Covered |
| `/cpu/products` (with filters) | GET | `test_products.py` | ✅ Covered |

Filters tested:
- `clusterId`
- `gpuNum`
- `productName`
- `billingMethod`
- `minCpuPerGpu`
- `minMemoryPerGpu`
- `minRootFSSize`

### ✅ Instances (3/3)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/gpu/instances` | GET | `test_instances.py` | ✅ Covered |
| `/gpu/instances` (with filters) | GET | `test_instances.py` | ✅ Covered |
| `/gpu/instance` | GET | `test_instances.py` | ✅ Covered |

Filters tested:
- `pageSize` / `pageNum`
- `name`
- `productName`
- `status`

**Lifecycle Tests (Planned)**:
- ⏳ Create instance
- ⏳ Update instance
- ⏳ Start instance
- ⏳ Stop instance
- ⏳ Restart instance
- ⏳ Delete instance

### ✅ Serverless Endpoints (3/3)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/endpoints` | GET | `test_endpoints.py` | ✅ Covered |
| `/endpoint` | GET | `test_endpoints.py` | ✅ Covered |
| `/endpoint/limit` | GET | `test_endpoints.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create endpoint
- ⏳ Update endpoint
- ⏳ Delete endpoint

### ✅ Jobs (1/1)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/jobs` | GET | `test_jobs.py` | ✅ Covered |

### ✅ Image Registry (1/1)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/repository/auths` | GET | `test_image_registry.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create registry auth
- ⏳ Delete registry auth

### ✅ Networks (2/2)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/networks` | GET | `test_networks.py` | ✅ Covered |
| `/network` | GET | `test_networks.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create network
- ⏳ Update network
- ⏳ Delete network

### ✅ Network Storage (1/1)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/networkstorages/list` | GET | `test_network_storage.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create network storage
- ⏳ Update network storage (resize)
- ⏳ Delete network storage

### ✅ Templates (2/2)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/templates` | GET | `test_templates.py` | ✅ Covered |
| `/template` | GET | `test_templates.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create template from instance
- ⏳ Delete template

### ✅ Image Prewarm (2/2)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/image/prewarm` | GET | `test_image_prewarm.py` | ✅ Covered |
| `/image/prewarm/quota` | GET | `test_image_prewarm.py` | ✅ Covered |

**Lifecycle Tests (Planned)**:
- ⏳ Create prewarm task
- ⏳ Update prewarm task
- ⏳ Delete prewarm task

### ✅ Metrics (1/1)

| Endpoint | Method | Test File | Status |
|----------|--------|-----------|--------|
| `/metrics/gpu/instance` | GET | `test_metrics.py` | ✅ Covered |

## Invasive Endpoints (Not Tested for Safety)

The following endpoints modify resources and are intentionally not tested in the current integration test suite to avoid costs and unintended changes:

### Instance Management
- `POST /gpu/instance/create`
- `POST /gpu/instance/edit`
- `POST /gpu/instance/start`
- `POST /gpu/instance/stop`
- `POST /gpu/instance/delete`
- `POST /gpu/instance/restart`
- `POST /gpu/instance/upgrade`
- `POST /gpu/instance/migrate`
- `POST /gpu/instance/renewInstance`
- `POST /gpu/instance/transToMonthlyInstance`

### Endpoint Management
- `POST /endpoint/create`
- `POST /endpoint/update`
- `POST /endpoint/delete`

### Job Management
- `POST /job/break`
- `POST /job/save/image`

### Image Prewarm
- `POST /image/prewarm`
- `POST /image/prewarm/edit`
- `POST /image/prewarm/delete`

### Registry Auth
- `POST /repository/auth/save`
- `POST /repository/auth/delete`

### Network
- `POST /network/create`
- `POST /network/update`
- `POST /network/delete`

### Network Storage
- `POST /networkstorage/create`
- `POST /networkstorage/update`
- `POST /networkstorage/delete`

### Template
- `POST /template/create`
- `POST /template/delete`

## Lifecycle Test Implementation Plan

When lifecycle tests are implemented (by removing `@pytest.mark.skip`), they should:

1. **Instance Lifecycle**:
   - Create instance → wait for running → update → stop → delete
   - Verify state transitions
   - Test with different billing methods (onDemand, monthly, spot)

2. **Endpoint Lifecycle**:
   - Create endpoint → wait for running → update config → delete
   - Test scaling and configuration changes

3. **Network Lifecycle**:
   - Create network → update name → attach to instance → delete
   - Test network isolation

4. **Storage Lifecycle**:
   - Create storage → resize → attach to instance → detach → delete
   - Test data persistence

5. **Template Lifecycle**:
   - Create instance → create template from instance → create new instance from template → cleanup all

6. **Registry Auth Lifecycle**:
   - Create auth → use in instance creation → delete auth

7. **Image Prewarm Lifecycle**:
   - Create prewarm task → wait for completion → update → delete

## Test Utilities

The `utils.py` module provides helpers for lifecycle tests:

- ✅ `wait_for_condition()` - Generic condition waiter
- ✅ `wait_for_instance_status()` - Instance state transitions
- ✅ `wait_for_endpoint_status()` - Endpoint state transitions
- ✅ `cleanup_instance()` - Safe instance cleanup
- ✅ `cleanup_endpoint()` - Safe endpoint cleanup
- ✅ `cleanup_network()` - Safe network cleanup
- ✅ `cleanup_network_storage()` - Safe storage cleanup
- ✅ `cleanup_template()` - Safe template cleanup

## Running Tests

### Read-Only Tests (Safe, No Costs)
```bash
pytest tests/integration/ -v
```

### Future: Lifecycle Tests (Will Incur Costs)
```bash
# When implemented, run with caution
pytest tests/integration/ -v -m lifecycle
```

## Notes

- All current tests are **read-only** and safe to run repeatedly
- Lifecycle tests are marked with `@pytest.mark.skip`
- Tests automatically skip if required resources aren't available
- All tests require `NOVITA_API_KEY` environment variable
