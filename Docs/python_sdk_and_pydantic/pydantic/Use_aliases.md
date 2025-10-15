class Model(BaseModel):
    internal_id: int = Field(alias='id')

model = Model(id=1)
model.model_dump(by_alias=True)  # {'id': 1}
model.model_dump(by_alias=False) # {'internal_id': 1}
```

### Model Construction and Copying

```python
# Bypass validation for trusted data
user = User.model_construct(
    _fields_set={'id', 'name'},
    id=1,
    name="John",
    email="john@example.com"
)

# Create modified copy
admin = user.model_copy(update={'is_active': True})

# Deep copy with nested models
user_copy = user.model_copy(deep=True)
```

### Working with Extra Fields

```python
class FlexibleModel(BaseModel):
    model_config = ConfigDict(extra='allow')
    required_field: str

model = FlexibleModel(required_field='value', extra1='a', extra2='b')
model.extra1  # 'a'
model.model_extra  # {'extra1': 'a', 'extra2': 'b'}
model.model_dump()  # Includes extra fields
```

Sources:
- [tests/test_main.py:56-115]()
- [tests/test_edge_cases.py:62-124]()

## Error Handling

When validation fails, BaseModel raises a `ValidationError` with detailed information:

```python
try:
    User(id="not an int", email="invalid")
except ValidationError as e:
    errors = e.errors()  # List of error dictionaries
    json_errors = e.json()  # JSON string representation
```

Error information includes:
- Error type
- Error location (field)
- Error message
- Invalid input value
- Context-specific details

Sources:
- [tests/test_main.py:87-103](https://github.com/pydantic/pydantic/blob/main/tests/test_main.py:87-103)

## Performance Considerations

- Use `model_construct` for trusted data to skip validation
- Consider `frozen=True` for immutable models (enables hashing)
- Use `exclude_unset=True` when serializing to minimize output
- Be mindful of deep validation in complex nested models

Sources:
- [tests/test_construction.py:15-35](https://github.com/pydantic/pydantic/blob/main/tests/test_construction.py:15-35)
- [tests/test_main.py:613-643](https://github.com/pydantic/pydantic/blob/main/tests/test_main.py:613-643)