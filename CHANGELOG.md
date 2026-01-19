# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-01-19

### Removed

- **SSH Key Management**: Removed SSH key API support (`client.gpu.ssh_keys`)
  - Removed `SSHKeys` and `AsyncSSHKeys` resource classes
  - Removed `SSHKey`, `CreateSSHKeyRequest`, `ListSSHKeysResponse` models
- **SSH Endpoint Extraction**: Removed SSH endpoint helper from instances
  - Removed `client.gpu.instances.get_ssh_endpoint()` method
  - Removed `SSHEndpoint` model

### Changed

- Simplified instance resource by removing SSH-related dependencies

---

## [0.2.0] - 2025-12-11

### Added

#### Automatic Price Conversion
- **Smart Price Handling**: Automatically converts Novita API's unusual price format (1/100000 USD units) to standard USD
- Applied to all pricing fields:
  - `GPUProduct.price` - On-demand pricing per hour
  - `GPUProduct.spot_price` - Spot instance pricing per hour
  - `SubscriptionPrice.price` - Monthly subscription pricing
  - `CPUProduct.price` - CPU instance pricing per hour
- Raw API values still accessible via `_raw` fields (e.g., `price_raw`, `spot_price_raw`)

#### Type Safety & Code Generation
- AST-based model transformation for price conversions
- `py.typed` marker for PEP 561 compliance

### Changed
- Improved OpenAPI spec accuracy based on real API behavior
- Enhanced test coverage and reliability

---

## [0.1.0] - 2025-10-19

### Added

#### Core Features
- Synchronous client (`NovitaClient`) for blocking operations
- Asynchronous client (`AsyncNovitaClient`) for async/await operations
- Context manager support for both sync and async clients
- Environment variable authentication via `NOVITA_API_KEY`
- Custom base URL and timeout configuration options

#### GPU Resources
- **Instances**: Create, list, get, update, start, stop, delete, upgrade, migrate, renew, convert, save image
- **Products**: List GPU products, list CPU products with filtering (cluster, GPU count, billing method, product name)
- **Endpoints**: List, get, create, update, delete endpoints; get endpoint limits
- **Networks**: List, get, create, update, delete VPC networks
- **Templates**: List, get, create, delete instance templates
- **Jobs**: List jobs, break job execution
- **Metrics**: Get instance metrics (CPU, GPU, memory, disk usage)
- **Storages**: List, create, update, delete network storages
- **Image Registry**: List, create, delete container registry authentications (accessible via `client.gpu.registries` or `client.gpu.image_registry`)
- **Images**: List, create, update, delete image prewarm tasks; get image prewarm quota
- **Clusters**: List available GPU clusters

#### Type Safety & Code Generation
- Full type hints with mypy strict mode compliance
- Pydantic v2 models auto-generated from OpenAPI specification

#### Error Handling
- `AuthenticationError` (401 Unauthorized)
- `BadRequestError` (400 Bad Request)
- `NotFoundError` (404 Not Found)
- `RateLimitError` (429 Too Many Requests)
- `APIError` (500+ Server Errors and other errors)
- Detailed error messages with request context

---
