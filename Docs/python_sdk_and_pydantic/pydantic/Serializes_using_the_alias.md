print(user1.model_dump())  # {'fullName': 'John Doe'}
```

Sources: [pydantic/config.py:1038-1138]()

### Frozen Models

Create immutable models with `frozen=True`:

```python
class ImmutableUser(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str

user = ImmutableUser(name="John")
# This will raise an error:
# user.name = "Jane"
```

Sources: [pydantic/config.py:158-166]()

### Validation on Assignment

Enable validation when attributes are assigned after creation:

```python
class ValidatedUser(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    age: int

user = ValidatedUser(age=30)