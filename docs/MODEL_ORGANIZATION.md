# Model Organization Guide

## Current Approach: Single Generated File

Currently, all Pydantic models are generated into a single file: `src/novita/generated/models.py`

### Advantages
- ✅ **Simpler imports** - One place for all models
- ✅ **No circular dependencies** - Models can reference each other freely
- ✅ **Standard practice** - Most OpenAPI generators work this way
- ✅ **Fast imports** - Python efficiently handles single module imports
- ✅ **Easy regeneration** - Single command regenerates everything

### Current Usage
```python
from novita.generated.models import (
    InstanceInfo,
    ListInstancesResponse,
    CreateInstanceRequest,
)
```

## Alternative: Manually Split by Resource Type

If you prefer organized model files, you can create a secondary organization layer:

### Structure
```
src/novita/generated/
├── __init__.py          # Main exports (auto-generated)
├── models.py            # All models (auto-generated)
└── types/               # Manual organization (optional)
    ├── __init__.py      # Re-exports from models.py
    ├── instances.py     # Instance models
    ├── registries.py    # Registry models
    ├── templates.py     # Template models
    ├── networks.py      # Network models
    ├── storage.py       # Storage models
    ├── endpoints.py     # Endpoint models
    ├── products.py      # Product models
    ├── jobs.py          # Job models
    └── images.py        # Image models
```

### Example: types/instances.py
```python
"""Instance-related models organized for convenience.

These are re-exports from the generated models.py file.
"""

from novita.generated.models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    EditInstanceRequest,
    InstanceInfo,
    ListInstancesResponse,
    UpgradeInstanceRequest,
)

__all__ = [
    "CreateInstanceRequest",
    "CreateInstanceResponse",
    "EditInstanceRequest",
    "InstanceInfo",
    "ListInstancesResponse",
    "UpgradeInstanceRequest",
]
```

### Example: types/__init__.py
```python
"""Organized model exports by resource type."""

from . import (
    endpoints,
    images,
    instances,
    jobs,
    networks,
    products,
    registries,
    storage,
    templates,
)

__all__ = [
    "endpoints",
    "images",
    "instances",
    "jobs",
    "networks",
    "products",
    "registries",
    "storage",
    "templates",
]
```

### Usage
```python
# Option 1: Import from organized types
from novita.generated.types import instances
user_instances = instances.ListInstancesResponse(...)

# Option 2: Direct import from types module
from novita.generated.types.instances import InstanceInfo, ListInstancesResponse

# Option 3: Still use the generated models directly
from novita.generated.models import InstanceInfo, ListInstancesResponse
```

## Automatic Splitting (Not Recommended)

While it's technically possible to automatically split the generated file, it has several drawbacks:

### Why Not Recommended
- ❌ **Circular dependencies** - Models reference each other across resources
- ❌ **Complex tooling** - Requires custom post-processing scripts
- ❌ **Maintenance burden** - Breaks on model relationships changes
- ❌ **Import complexity** - Harder to find models
- ❌ **Regeneration issues** - Each regeneration needs post-processing

### If You Really Want It
You would need to:
1. Parse the generated `models.py` file
2. Analyze model dependencies
3. Group models by OpenAPI tags or naming patterns
4. Generate separate files with proper imports
5. Handle cross-file model references
6. Re-run this after every generation

## Recommendation

**Stick with the single file approach** unless you have a specific need for organization.

If organization is important:
1. Keep the generated `models.py` as-is
2. Create the `types/` subdirectory manually
3. Add organized re-export files as needed
4. Update them when adding new models

This gives you organization without breaking the generation workflow.

## Future Improvements

If the SDK grows significantly (100+ models), consider:
1. **Splitting the OpenAPI spec** - Separate specs for each resource group
2. **Multiple generation runs** - Generate each resource separately
3. **Custom generator** - Write a custom script that understands Novita's structure

For now, the single file (~50 models) is manageable and follows best practices.
