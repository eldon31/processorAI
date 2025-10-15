```

**Sources:** [tests/test_computed_fields.py:178-214]()

### JSON Schema Generation

Computed fields appear in JSON schema with `readOnly: true`:

```python
class Rectangle(BaseModel):
    width: int
    length: int
    
    @computed_field
    def area(self) -> int:
        """Calculated area"""
        return self.width * self.length

schema = Rectangle.model_json_schema(mode='serialization')
# schema['properties']['area'] == {
#     'title': 'Area',
#     'description': 'Calculated area',
#     'type': 'integer',
#     'readOnly': True
# }
```

The `readOnly` flag indicates that the field is computed during serialization and cannot be provided during validation.

**Sources:** [tests/test_computed_fields.py:68-121](), [pydantic/json_schema.py]()

### Include/Exclude Behavior

Computed fields respect include/exclude parameters in serialization:

```python
class Model(BaseModel):
    x: int
    
    @computed_field
    @property
    def x_doubled(self) -> int:
        return self.x * 2

m = Model(x=5)