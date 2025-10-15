class ValidatorBase(BaseModel):
    @field_validator('value')
    @classmethod
    def check_positive(cls, v):
        if v <= 0:
            raise ValueError('must be positive')
        return v

DynamicModel = create_model(
    'DynamicModel',
    value=(int, ...),
    __base__=ValidatorBase
)
```

Sources:
- [pydantic/main.py:1083-1228]()
- [tests/test_create_model.py:20-124]()

## Customization Hooks

### Custom __init__

Override `__init__` to customize pre-validation behavior:

```python
class CustomModel(BaseModel):
    field1: str
    
    def __init__(self, special_arg: str = None, **data):
        if special_arg:
            data['field1'] = special_arg
        super().__init__(**data)

model = CustomModel(special_arg='value')
# field1 = 'value'
```

**Note**: `__pydantic_custom_init__` class attribute is set to `True` when `__init__` is overridden [pydantic/_internal/_model_construction.py:165]()

### model_post_init

Hook called after validation and instance creation:

```python
class CustomModel(BaseModel):
    field1: str
    _computed: int = PrivateAttr()
    
    def model_post_init(self, __context: Any) -> None:
        # Called after validation, before returning from __init__
        self._computed = len(self.field1)
```

**Signature**: [pydantic/main.py:587-590]()
```python
def model_post_init(self, __context: Any, /) -> None:
    ...
```

**Parameters**:
- `__context`: Context passed from validators or `None`

**When called**:
- After `__pydantic_validator__.validate_python()` completes
- Before `__init__` returns
- Also called from `model_construct()` with `context=None`

**Special behavior**:
- If private attributes exist, ModelMetaclass wraps `model_post_init` to initialize `__pydantic_private__` first [pydantic/_internal/_model_construction.py:133-147]()

### __pydantic_init_subclass__

Hook for subclass customization:

```python
class CustomBase(BaseModel):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        # Called when a subclass is created
        super().__pydantic_init_subclass__(**kwargs)
        # Custom logic for subclasses
```

**Called from**: [pydantic/_internal/_model_construction.py:266]()

Sources:
- [pydantic/main.py:587-590]()
- [pydantic/_internal/_model_construction.py:133-147]()
- [pydantic/_internal/_model_construction.py:165-168]()
- [pydantic/_internal/_model_construction.py:266]()

## Integration with Validators

BaseModel works closely with Pydantic validators to allow field-level and model-level validation:

```python
class Model(BaseModel):
    field1: str
    
    @field_validator('field1')
    def validate_field1(cls, v):
        if v.startswith('bad_'):
            raise ValueError('field1 cannot start with bad_')
        return v
```

This topic is covered in depth in the Validators documentation.

Sources:
- [tests/test_validators.py:192-215](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py:192-215)

## Usage Examples

### Basic Model Definition

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    is_active: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)
```

### Validation from Different Sources

```python
from pydantic import ValidationError

# From dict
user = User(id=1, name="John", email="john@example.com")

# From JSON string
user = User.model_validate_json('{"id": 1, "name": "John", "email": "john@example.com"}')

# From object attributes
class UserData:
    id = 1
    name = "John"
    email = "john@example.com"

user = User.model_validate(UserData(), from_attributes=True)

# Handle validation errors
try:
    User(id="invalid", name="John", email="bad-email")
except ValidationError as e:
    print(e.errors())
    # [{'type': 'int_parsing', 'loc': ('id',), ...}, ...]
```

### Serialization Patterns

```python
user = User(id=1, name="John", email="john@example.com")