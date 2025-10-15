```

**With validate_assignment=True**:
```python
class MyModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    field1: int

model = MyModel(field1=1)
model.field1 = '2'  # Validated: converts to 2
model.field1 = 'invalid'  # Raises ValidationError
```

Calls `__pydantic_validator__.validate_assignment(self, name, value)` [pydantic/main.py:111]()

### Frozen Fields

**Model-level frozen**:
```python
class MyModel(BaseModel):
    model_config = ConfigDict(frozen=True)
    field1: str

model = MyModel(field1='value')
model.field1 = 'new'  # ValidationError: frozen_instance
```

**Field-level frozen**:
```python
class MyModel(BaseModel):
    field1: str = Field(frozen=True)
    field2: str

model = MyModel(field1='value', field2='value')
model.field1 = 'new'  # ValidationError: frozen_field
model.field2 = 'new'  # OK
```

Frozen check: [pydantic/main.py:81-91]()

### Field Tracking with model_fields_set

The `model_fields_set` property returns fields explicitly set during initialization:

```python
model = MyModel(field1='value')  # field2 has default
assert model.model_fields_set == {'field1'}

model.field3 = 'assigned after init'
assert model.model_fields_set == {'field1', 'field3'}  # Updated by __setattr__
```

**Implementation**: [pydantic/main.py:293-301]()

Sources:
- [pydantic/main.py:81-115]()
- [pydantic/main.py:815-908]()
- [tests/test_main.py:535-610]()

## Extra Fields Handling

The `extra` config controls how fields not defined in the model are handled.

### Configuration Options

| Value | Behavior |
|-------|----------|
| `'ignore'` | Extra fields are silently ignored (default) |
| `'allow'` | Extra fields stored in `__pydantic_extra__` and accessible as attributes |
| `'forbid'` | Extra fields raise `ValidationError` with type `'extra_forbidden'` |

### extra='allow'

```python
class Model(BaseModel):
    model_config = ConfigDict(extra='allow')
    field1: str

model = Model(field1='value', extra_field='extra')
assert model.field1 == 'value'
assert model.extra_field == 'extra'
assert model.__dict__ == {'field1': 'value'}
assert model.__pydantic_extra__ == {'extra_field': 'extra'}
assert model.model_extra == {'extra_field': 'extra'}
```

**Attribute Access**: Extra fields are accessible via `__getattr__` [pydantic/main.py:910-924]()

**Serialization**: Extra fields are included in `model_dump()` output [pydantic/main.py:211-212]()

**Assignment After Init**:
```python
model.new_extra = 'value'  # Adds to __pydantic_extra__
```

### extra='forbid'

```python
class Model(BaseModel):
    model_config = ConfigDict(extra='forbid')
    field1: str

Model(field1='value', extra='x')
# ValidationError: [{'type': 'extra_forbidden', 'loc': ('extra',), ...}]
```

### extra='ignore'

```python
class Model(BaseModel):
    model_config = ConfigDict(extra='ignore')
    field1: str

model = Model(field1='value', extra='ignored')
assert not hasattr(model, 'extra')
assert model.model_extra is None
```

Sources:
- [pydantic/main.py:211-212]()
- [pydantic/main.py:910-924]()
- [tests/test_main.py:266-414]()

## validate_assignment Configuration

When `validate_assignment=True`, field assignments are validated after model initialization.

**Configuration**:
```python
class Model(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    field1: int
    field2: str
```

**Behavior**:
```python
model = Model(field1=1, field2='text')

model.field1 = 2        # OK: valid int
model.field1 = '3'      # OK: coerced to 3
model.field1 = 'invalid'  # ValidationError: int_parsing

model.field2 = 'new'    # OK: valid str
```

**Implementation**: [pydantic/main.py:111]()
- Calls `__pydantic_validator__.validate_assignment(model, name, value)`
- Runs full validation pipeline (field validators, type coercion, constraints)
- Updates `__dict__[name]` and adds `name` to `__pydantic_fields_set__`

**Performance Note**: Adds validation overhead to every field assignment. Only use when runtime data integrity is required.

Sources:
- [pydantic/main.py:111]()
- [tests/test_main.py:754-803]()

## Private Attributes

Private attributes (prefix `_`) are not validated or serialized. They are managed separately from regular fields.

### Defining Private Attributes

**With PrivateAttr**:
```python
from pydantic import BaseModel, PrivateAttr

class Model(BaseModel):
    public_field: str
    _private: int = PrivateAttr(default=0)
    _private_factory: list = PrivateAttr(default_factory=list)
```

**With annotation only**:
```python
class Model(BaseModel):
    public_field: str
    _private: int  # No default, must be set manually
```

**Implicit** (unannotated):
```python
class Model(BaseModel):
    public_field: str
    _private = 42  # Automatically becomes PrivateAttr(default=42)
```

### Storage and Access

Private attributes are stored in `__pydantic_private__` dict:

```python
model = Model(public_field='value')
model._private = 100
assert model.__pydantic_private__ == {'_private': 100}
```

**Initialization**: [pydantic/_internal/_model_construction.py:354-369]()
- `__pydantic_private__` is initialized in `init_private_attributes()`
- Called from wrapped `model_post_init()` if private attrs exist
- Default values are set from `__private_attributes__` metadata

### Characteristics

| Aspect | Behavior |
|--------|----------|
| **Validation** | None - not validated on init or assignment |
| **Serialization** | Excluded from `model_dump()` and `model_dump_json()` |
| **model_construct** | Can be set via `**values` after model_post_init [pydantic/main.py:371-375]() |
| **Naming** | Must start with single `_` (not `__` dunder) |
| **Access** | Normal Python attribute access |

Sources:
- [pydantic/main.py:217]()
- [pydantic/_internal/_model_construction.py:354-369]()
- [pydantic/_internal/_model_construction.py:418-517]()
- [tests/test_private_attributes.py]()

## Computed Fields

Computed fields are properties included in model serialization, defined with the `@computed_field` decorator.

### Definition

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: int
    height: int

    @computed_field
    @property
    def area(self) -> int:
        return self.width * self.height
```

### Characteristics

| Aspect | Behavior |
|--------|----------|
| **Validation** | Not validated on input; computed from other fields |
| **Serialization** | Included in `model_dump()` and `model_dump_json()` output |
| **Schema** | Included in JSON schema as read-only property |
| **Access** | Read-only property access (unless setter defined) |
| **Storage** | Stored in `__pydantic_computed_fields__` class attribute |

### Serialization

```python
model = Rectangle(width=10, height=5)
model.area  # 50

model.model_dump()