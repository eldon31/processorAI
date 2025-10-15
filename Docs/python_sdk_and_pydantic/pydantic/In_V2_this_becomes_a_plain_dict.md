from pydantic import TypeAdapter
class MyDict(dict): pass
ta = TypeAdapter(Mapping[str, int])
v = ta.validate_python(MyDict())  # v will be dict, not MyDict
```

Sources: [docs/migration.md:498-615](docs/migration.md:498-615)

### Default Value Validation

In V2, validators marked with `always=True` will cause standard type validation to be applied to default values:

```python
class Model(BaseModel):
    x: str = 1  # Will raise ValidationError in V2 with always=True validators
    
    @validator('x', always=True)
    @classmethod
    def validate_x(cls, v):
        return v
```

Sources: [docs/migration.md:372-396](docs/migration.md:372-396)

## Best Practices

1. **Update incrementally**: Start by installing V2 and using the `pydantic.v1` namespace for incompatible code.
2. **Address deprecation warnings**: Run your tests with deprecation warnings enabled to catch and fix deprecated usage.
3. **Use type annotations**: Proper type annotations will help tools and error messages guide you during migration.
4. **Test thoroughly**: Ensure your tests cover edge cases as V2's validation behavior differs in some subtle ways.
5. **Use modern Python features**: Prefer modern Python typing features like `list[int]` over `List[int]`.

## Conclusion

Migrating from Pydantic V1 to V2 involves several significant changes, but the provided compatibility mechanisms, migration tools, and incremental migration paths make the transition manageable. By understanding the key changes and following the recommended migration patterns, you can successfully update your code to take advantage of the improvements in Pydantic V2.

Sources: [docs/migration.md:1-10](docs/migration.md:1-10)