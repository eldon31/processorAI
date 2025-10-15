```

### With cached_property

```python
from functools import cached_property

class Model(BaseModel):
    value: int

    @computed_field
    @cached_property
    def expensive_calc(self) -> int:
        # Computed once, then cached
        return self.value ** 2
```

**Note**: Cached values are stored in `__dict__`, not `__pydantic_private__`

Sources:
- [pydantic/main.py:208-209]()
- [pydantic/main.py:243-245]()
- [tests/test_computed_fields.py:27-66]()

## Model Rebuilding

The `model_rebuild()` class method regenerates a model's schema when forward references couldn't be resolved initially.

### When to Use

Forward references that can't be resolved during class definition:

```python
class Model(BaseModel):
    field: 'AnotherModel'  # Forward reference