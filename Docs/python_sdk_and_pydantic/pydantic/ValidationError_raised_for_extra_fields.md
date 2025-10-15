```

Sources: [pydantic/config.py:63-156]()

### Strict Validation

The `strict` option enforces strict type checking:

```python
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    age: int
    
# This will raise ValidationError because "42" is not an int
model = StrictModel(age="42")
```

Sources: [pydantic/config.py:444-469]()

### Alias Handling

Control how aliases are used for validation and serialization:

```python
class UserModel(BaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True
    )
    
    full_name: str = Field(alias='fullName')