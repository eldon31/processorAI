```

Sources: [pydantic/config.py:246-296]()

## Working with Deferred Schema Building

For large model hierarchies, you can improve startup performance with `defer_build=True`:

```python
class LargeModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    # many fields...

# Schema validators won't be built until first use
```

Sources: [pydantic/config.py:775-784]()

## Advanced Configuration Use Cases

### Custom Alias Generation

Generate aliases automatically with a function:

```python
from pydantic.alias_generators import to_camel

class CamelCaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    
    user_name: str
    email_address: str
    
user = CamelCaseModel(userName="john", emailAddress="john@example.com")
print(user.model_dump(by_alias=True))  # {'userName': 'john', 'emailAddress': 'john@example.com'}
```

Sources: [pydantic/config.py:361-418]()

### Custom JSON Encoding

Control how special values are serialized:

```python
class TimeModel(BaseModel):
    model_config = ConfigDict(
        ser_json_timedelta='float',
        ser_json_inf_nan='strings'
    )
    
    # Fields that use these serialization formats
```

Sources: [pydantic/config.py:592-628]()

## Best Practices

1. **Be consistent with configuration** across related models to prevent surprising behavior
2. **Document your configuration choices** in your codebase
3. **Consider validation strictness** based on your application's requirements
4. **Use `defer_build=True`** for large model hierarchies that aren't immediately used
5. **Choose appropriate `extra` handling** based on your API contract requirements
6. **Prefer `model_config`** over the deprecated class-based `Config` approach

Sources: [pydantic/_internal/_config.py:31-32]()

## Configuration Defaults

All configuration options have sensible defaults that are used when not explicitly set:

```python