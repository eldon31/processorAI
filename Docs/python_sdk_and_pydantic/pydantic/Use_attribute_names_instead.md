schema = Model.model_json_schema(by_alias=False)  # {"properties": {"field_name": ...}}
```

Sources: [tests/test_json_schema.py:125-142](tests/test_json_schema.py), [tests/test_json_schema.py:253-259](tests/test_json_schema.py)

### Nested Models

When a model contains other models, those models are included in the `$defs` section and referenced:

```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address

# Generated schema will have Address in the $defs section
```

Sources: [tests/test_json_schema.py:195-223](tests/test_json_schema.py), [tests/test_json_schema.py:546-565](tests/test_json_schema.py)

### Enums

Enum classes are represented with their possible values:

```python
class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    status: Status