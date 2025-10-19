# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-19

### Added

#### Core Features
- Initial release of the Novita AI Python SDK
- Synchronous client (`NovitaClient`) for blocking operations
- Asynchronous client (`AsyncNovitaClient`) for async/await operations
- Context manager support for both sync and async clients
- Environment variable authentication via `NOVITA_API_KEY`
- Custom base URL and timeout configuration options

#### GPU Instance Management API
- `create_instance()` - Create new GPU instances with configurable options
- `list_instances()` - List all GPU instances in the account
- `get_instance()` - Get detailed information about a specific instance
- `update_instance()` - Update instance name and disk size
- `start_instance()` - Start a stopped GPU instance
- `stop_instance()` - Stop a running GPU instance
- `delete_instance()` - Permanently delete a GPU instance
- `get_pricing()` - Get pricing information for all instance types

---

[0.1.0]: https://github.com/novita-ai/novita-sdk-python/releases/tag/v0.1.0
