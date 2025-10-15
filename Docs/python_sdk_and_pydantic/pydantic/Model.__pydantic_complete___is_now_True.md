```

### Implementation

**Method signature**: [pydantic/main.py:593-650]()

```python
@classmethod
def model_rebuild(
    cls,
    *,
    force: bool = False,
    raise_errors: bool = True,
    _parent_namespace_depth: int = 2,
    _types_namespace: MappingNamespace | None = None,
) -> bool | None
```

**Parameters**:
- `force`: Rebuild even if `__pydantic_complete__=True`
- `raise_errors`: Raise exceptions on schema generation errors
- `_parent_namespace_depth`: Frame depth for namespace resolution
- `_types_namespace`: Explicit namespace for type resolution

**Returns**:
- `None`: Schema was already complete and rebuild skipped
- `True`: Rebuild succeeded
- `False`: Rebuild failed (only when `raise_errors=False`)

### Rebuild Process

1. **Check Completion**: If `__pydantic_complete__=True` and `force=False`, returns `None`
2. **Clear Schema Artifacts**: Deletes `__pydantic_core_schema__`, `__pydantic_validator__`, `__pydantic_serializer__`
3. **Resolve Namespace**: Gets parent frame namespace for type resolution
4. **Complete Model**: Calls `complete_model_class()` to regenerate schema

**Note**: Not thread-safe. Concurrent rebuilds can cause issues with shared validator/serializer instances.

Sources:
- [pydantic/main.py:593-650]()
- [pydantic/_internal/_model_construction.py:619-650]()

## Dynamic Model Creation

The `create_model()` function creates BaseModel subclasses at runtime.

**Function signature**: [pydantic/main.py:1083-1228]()

```python
from pydantic import create_model, Field

DynamicModel = create_model(
    'DynamicModel',
    field1=(str, ...),            # Required, no default (... = Ellipsis)
    field2=(int, 42),             # Required with default
    field3=str,                   # Required annotation shorthand
    field4=(int, Field(gt=0)),    # With Field constraints
    __config__=ConfigDict(...),   # Optional config
    __base__=BaseModel,           # Optional base class(es)
    __module__='my.module',       # Optional module name
    __validators__={...},         # Optional validators dict
    __cls_kwargs__={...},         # Optional metaclass kwargs
)
```

### Field Definition Formats

| Format | Description | Example |
|--------|-------------|---------|
| `(type, default)` | Type with default value | `field1=(str, 'default')` |
| `(type, ...)` | Required field | `field2=(int, ...)` |
| `type` | Required, annotation-only | `field3=str` |
| `FieldInfo` | From Field() function | `field4=Field(default=0, gt=0)` |

### Special Parameters

| Parameter | Description |
|-----------|-------------|
| `__config__` | ConfigDict for model configuration |
| `__base__` | Base class or tuple of base classes |
| `__module__` | Set `__module__` attribute (affects pickling, repr) |
| `__validators__` | Validators dict (V1-style, deprecated) |
| `__cls_kwargs__` | Kwargs passed to ModelMetaclass |
| `__doc__` | Docstring for the model class |

### Usage Examples

**With inheritance**:
```python
class BaseModel(BaseModel):
    base_field: str

DynamicModel = create_model(
    'DynamicModel',
    dynamic_field=(int, ...),
    __base__=BaseModel
)
# Has both base_field and dynamic_field
```

**With validators** (V2 style):
```python
from pydantic import field_validator

def validate_positive(cls, v):
    if v <= 0:
        raise ValueError('must be positive')
    return v