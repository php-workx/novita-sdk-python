# Code Generation Workflow

This project uses **OpenAPI-based code generation** to maintain consistency between the API specification and the SDK implementation.

## 🎯 What Gets Generated
- ✅ **Pydantic v2 models** - Type-safe request/response models
- ✅ **Enums** - For fixed values (instance types, statuses, etc.)
- ✅ **Field validators** - Min/max constraints, required fields
- ❌ **HTTP client code** - We maintain this manually for better control

## 📦 Setup Complete

The following has been configured:

### Dependencies

**Dev Dependencies Only** (in `pyproject.toml`):
- `datamodel-code-generator` - Generates Pydantic models from OpenAPI spec
- `pytest-cov` - Test coverage

```bash
# Install dev dependencies (for SDK development)
pip install -e ".[dev]"

# Regular install (for SDK users - no code gen tools)
pip install novita-sdk-python
```

### Directory Structure
```
├── openapi/
│   ├── README.md              # Detailed workflow documentation
│   └── novita-api.yaml    # OpenAPI 3.0 specification
├── scripts/
│   └── generate_models.sh     # Generation script
├── src/novita/generated/
│   ├── __init__.py            # Generated package
│   └── models.py              # Generated Pydantic models
└── Makefile                   # Common tasks
```

## 🚀 Quick Reference

### Generate Models
```bash
# Using make (recommended)
make generate

# Or directly
./scripts/generate_models.sh
```

### Common Commands
```bash
make help        # Show all available commands
make install     # Install dependencies
make generate    # Generate models from spec
make test        # Run tests
make lint        # Run linting
make format      # Format code
make ci          # Run all CI checks
```

## 📝 Workflow

### Adding a New Endpoint

**1. Update OpenAPI Spec**
```yaml
# openapi/novita-api.yaml
paths:
  /gpu/instance/restart:
    post:
      operationId: restart_instance
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RestartRequest'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InstanceActionResponse'
```

**2. Generate Models**
```bash
make generate
```

**3. Use Generated Models**
```python
# src/novita/api/resources/gpu/instances.py
from novita.generated.models import (
    RestartRequest,
    InstanceActionResponse
)

class Instances(BaseResource):
    def restart(self, instance_id: str) -> InstanceActionResponse:
        request = RestartRequest(instance_id=instance_id)
        response = self._client.post(
            f"{BASE_PATH}/gpu/instance/restart",
            json=request.model_dump(exclude_none=True)
        )
        return InstanceActionResponse.model_validate(response.json())
```

**4. Add Tests**
```python
def test_restart_instance(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(...)
    response = client.gpu.instances.restart("inst-123")
    assert response.success is True
```

## 🔄 Keeping Spec Up to Date

### Sources for API Changes
1. **Novita Docs**: https://novita.ai/docs/api-reference/
2. **API Changelog**: Check for announcements

### Update Process
```bash
# 1. Edit OpenAPI spec
vim openapi/novita-api.yaml

# 2. Validate (optional)
make spec-validate

# 3. Regenerate models
make generate

# 4. Update resource classes
# Edit src/novita/api/resources/gpu/*.py

# 5. Run tests
make test

# 6. Commit together
git add openapi/ src/novita/generated/
git commit -m "feat: add restart endpoint"
```

## 🎨 Customization

### Generated Models
Located in `src/novita/generated/models.py`:
- **DO NOT** edit this file manually
- Changes will be overwritten on next generation
- If you need custom logic, extend in `src/novita/models/`

### Custom Wrapper Example
```python
# src/novita/models/custom.py
from novita.generated.models import InstanceInfo as GeneratedInstanceInfo

class InstanceInfo(GeneratedInstanceInfo):
    """Extended instance info with helper methods."""
    
    @property
    def is_ready(self) -> bool:
        return self.status in ["RUNNING", "READY"]
    
    def get_ssh_connection(self) -> str:
        return f"ssh -p {self.ssh_port} root@{self.ssh_host}"
```

## 🛠️ Advanced Usage

### Custom Generation Options

Edit `scripts/generate_models.sh` to customize:

```bash
datamodel-codegen \
    --input "$OPENAPI_SPEC" \
    --output "$OUTPUT_FILE" \
    --target-python-version "3.11" \
    --output-model-type pydantic_v2.BaseModel \
    --use-annotated \
    --use-standard-collections \
    --use-schema-description \
    --field-constraints \
    --snake-case-field \
    --enum-field-as-literal one \
    --collapse-root-models \
    --use-title-as-name \
    --use-default           # NEW: Use default values
    --use-subclass-enum     # NEW: Subclass string for enums
```

See [datamodel-code-generator docs](https://github.com/koxudaxi/datamodel-code-generator) for all options.

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Ensure generated models are up to date
if git diff --cached --name-only | grep "openapi/.*\.yaml"; then
    echo "OpenAPI spec changed, regenerating models..."
    make generate
    git add src/novita/generated/
fi
```

## 📚 Further Reading

- [OpenAPI README](openapi/README.md) - Detailed workflow guide
- [OpenAPI 3.0 Spec](https://swagger.io/specification/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/latest/)
- [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator)

## ✅ Checklist: Contributing a New Feature

- [ ] Update `openapi/novita-api.yaml` with new endpoint
- [ ] Run `make generate` to create models
- [ ] Implement resource method using generated models
- [ ] Add comprehensive tests
- [ ] Update documentation
- [ ] Run `make ci` to verify all checks pass
- [ ] Commit spec and generated code together
