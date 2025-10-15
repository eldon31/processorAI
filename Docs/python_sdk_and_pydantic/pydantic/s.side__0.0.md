```

**Sources:** [tests/test_computed_fields.py:123-176]()

### Serialization Customization

Computed fields can be customized with `@field_serializer`:

```python
class Model(BaseModel):
    value: int
    
    @computed_field
    @property
    def doubled(self) -> int:
        return self.value * 2
    
    @field_serializer('doubled')
    def serialize_doubled(self, v):
        return f"Value: {v}"

m = Model(value=5)
# m.model_dump() == {'value': 5, 'doubled': 'Value: 10'}
```

**Sources:** [tests/test_computed_fields.py:123-150](), [pydantic/functional_serializers.py]()

### Cached Properties

Computed fields work with `functools.cached_property` for performance:

```python
from functools import cached_property
from pydantic import BaseModel, computed_field

class Model(BaseModel):
    minimum: int
    maximum: int
    
    @computed_field
    @cached_property
    def random_number(self) -> int:
        import random
        return random.randint(self.minimum, self.maximum)

m = Model(minimum=1, maximum=100)
first = m.random_number  # Calculated once
second = m.random_number  # Returns cached value