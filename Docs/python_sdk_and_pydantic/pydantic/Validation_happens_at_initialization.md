user = User(name='John', age='30')  # age is automatically converted to int
```

Sources: [pydantic/dataclasses.py:98-282](pydantic/dataclasses.py:98-282), [pydantic/_internal/_dataclasses.py:64-112](pydantic/_internal/_dataclasses.py:64-112), [tests/test_dataclasses.py:62-147](tests/test_dataclasses.py:62-147)

## Common Validation and Serialization Scenarios

### Field-Level Validation

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @field_validator('age')
    def age_must_be_reasonable(cls, v):
        if v < 0 or v > 120:
            raise ValueError('must be between 0 and 120')
        return v
```

### Model-Level Validation

```python
from pydantic import BaseModel, model_validator

class UserRegistration(BaseModel):
    username: str
    password: str
    password_confirmation: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError('passwords do not match')
        return self
```

### Custom Serialization

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
```

Sources: [tests/test_validators.py:192-216](tests/test_validators.py:192-216), [tests/test_serialize.py:148-170](tests/test_serialize.py:148-170)

## Using Annotated for Validation and Serialization

Pydantic supports using the `Annotated` type to attach validators and serializers directly to type annotations:

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator, PlainSerializer

def validate_positive(v: int) -> int:
    if v <= 0:
        raise ValueError('must be positive')
    return v

def serialize_as_string(v: int) -> str:
    return f"{v:,}"

PositiveInt = Annotated[
    int,
    AfterValidator(validate_positive),
    PlainSerializer(serialize_as_string, when_used='json')
]

class Product(BaseModel):
    id: int
    quantity: PositiveInt
```

This approach allows for reusable validation and serialization logic that can be applied to multiple fields across different models.

Sources: [tests/test_validators.py:51-87](tests/test_validators.py:51-87), [tests/test_serialize.py:82-96](tests/test_serialize.py:82-96)

## Validation and Serialization Modes

Both validation and serialization offer different modes:

### Validation Modes:
- **Standard**: Regular field-by-field validation
- **Strict**: Enforces exact type matches without coercion

### Serialization Modes:
- **python**: Serializes to Python native types (dict, list, etc.)
- **json**: Serializes to JSON-compatible Python types
- **json string**: Directly serializes to a JSON string

```python
# Example of different serialization modes
model.model_dump()  # Python mode
model.model_dump(mode='json')  # JSON-compatible mode
model.model_dump_json()  # JSON string
```

Sources: [tests/test_serialize.py:82-109](tests/test_serialize.py:82-109), [tests/test_serialize.py:171-197](tests/test_serialize.py:171-197)

## Conclusion

Pydantic's validation and serialization systems provide a robust foundation for ensuring data quality and consistency. The architecture allows for customization at various levels, from field-specific validators to model-wide serializers. These systems work together to provide a seamless flow from raw input data to validated models and then to serialized output.