adapter.rebuild()
```

When `defer_build` is `True`, TypeAdapter sets mock objects for the core schema, validator, and serializer. These mocks will attempt to rebuild the schema when accessed.

Sources: [pydantic/type_adapter.py:317-331](, [pydantic/_internal/_mock_val_ser.py:112-148](

## Working with Different Types

TypeAdapter works with various Python types:

### Primitive Types

```python
int_adapter = TypeAdapter(int)
float_adapter = TypeAdapter(float)
str_adapter = TypeAdapter(str)
bool_adapter = TypeAdapter(bool)
```

### Container Types

```python
list_adapter = TypeAdapter(list[int])
dict_adapter = TypeAdapter(dict[str, int])
tuple_adapter = TypeAdapter(tuple[str, int])
set_adapter = TypeAdapter(set[int])
```

### Pydantic Models

```python
from pydantic import BaseModel, TypeAdapter

class User(BaseModel):
    id: int
    name: str

user_adapter = TypeAdapter(User)
```

### Dataclasses

```python
from dataclasses import dataclass
from pydantic import TypeAdapter

@dataclass
class Point:
    x: int
    y: int

point_adapter = TypeAdapter(Point)
```

### TypedDict

```python
from typing import TypedDict
from pydantic import TypeAdapter

class UserDict(TypedDict):
    id: int
    name: str

user_dict_adapter = TypeAdapter(UserDict)
```

### Union Types

```python
from typing import Union
from pydantic import TypeAdapter

union_adapter = TypeAdapter(Union[int, str])
```

### Generic Types

```python
from typing import Generic, TypeVar
from pydantic import BaseModel, TypeAdapter

T = TypeVar('T')

class Container(BaseModel, Generic[T]):
    value: T

int_container_adapter = TypeAdapter(Container[int])
```

Sources: [tests/test_type_adapter.py:42-65](, [tests/test_type_adapter.py:185-193](, [tests/test_type_adapter.py:364-383](

## Error Handling

When validation fails, TypeAdapter raises a `ValidationError` with details about the validation failures:

```python
from pydantic import TypeAdapter, ValidationError
from typing import List

int_list_adapter = TypeAdapter(List[int])

try:
    int_list_adapter.validate_python(["1", "not_an_int"])
except ValidationError as e:
    print(f"Validation errors: {e.errors()}")
```

ValidationError provides detailed information about what failed, where the error occurred, and why.

Sources: [tests/test_type_adapter.py:194-254](

## Type Detection

TypeAdapter has logic to detect if a type has its own configuration. This is important because you cannot override the configuration of certain types:

```python
def _type_has_config(type_: Any) -> bool:
    """Returns whether the type has config."""
    type_ = _typing_extra.annotated_type(type_) or type_
    try:
        return issubclass(type_, BaseModel) or is_dataclass(type_) or is_typeddict(type_)
    except TypeError:
        # type is not a class
        return False
```

Sources: [pydantic/type_adapter.py:58-66](

## Technical Implementation Details

TypeAdapter uses a combination of:

1. Core schema generation via `GenerateSchema`
2. Validation via `SchemaValidator` or `PluggableSchemaValidator`
3. Serialization via `SchemaSerializer`
4. Namespace resolution for type resolution
5. Mock objects for deferred building

It also has special handling for generic types, forward references, and namespace management to ensure types are correctly resolved.

Sources: [pydantic/type_adapter.py:246-316](, [pydantic/_internal/_namespace_utils.py:143-293](, [pydantic/_internal/_mock_val_ser.py:21-149](

## Summary

TypeAdapter is a powerful component that brings Pydantic's validation and serialization capabilities to any Python type. It's particularly useful for:

1. Validating simple types like integers and strings with Pydantic's conversion logic
2. Validating complex types like lists and dictionaries with nested validation
3. Working with non-model types like dataclasses and TypedDict
4. Applying validation to arbitrary types in a consistent way
5. Generating JSON schemas for arbitrary types
6. Serializing instances of arbitrary types consistently

By wrapping a type in a TypeAdapter, you can leverage Pydantic's robust validation and serialization features without having to create a full model class.