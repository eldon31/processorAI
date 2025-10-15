model.dict()  # Deprecated method
```

In tests, the deprecation warnings are being handled explicitly:

```python
with pytest.warns(PydanticDeprecatedSince20):
    Model.parse_raw('{"x": 1, "y": 2}')
```

Sources: [tests/test_deprecated.py:27-50](tests/test_deprecated.py:27-50), [tests/test_deprecated.py:277-296](tests/test_deprecated.py:277-296)

## Migration Tool

To help automate the migration process, Pydantic provides a code transformation tool called `bump-pydantic`.

### Installation and Usage

```bash
pip install bump-pydantic
cd /path/to/repo_folder
bump-pydantic my_package
```

This tool attempts to automatically transform your code to use V2 patterns and APIs.

Sources: [docs/migration.md:25-47](docs/migration.md:25-47)

## Key Breaking Changes and Migration Paths

### Model API Changes

The following table shows the most important method/attribute name changes in `BaseModel`:

| Pydantic V1 | Pydantic V2  |
| ----------- | ------------ |
| `__fields__` | `model_fields` |
| `__private_attributes__` | `__pydantic_private__` |
| `__validators__` | `__pydantic_validator__` |
| `construct()` | `model_construct()` |
| `copy()` | `model_copy()` |
| `dict()` | `model_dump()` |
| `json_schema()` | `model_json_schema()` |
| `json()` | `model_dump_json()` |
| `parse_obj()` | `model_validate()` |
| `parse_raw()` | `model_validate_json()` |
| `update_forward_refs()` | `model_rebuild()` |

Many V1 methods are retained with deprecation warnings to ease migration.

Sources: [docs/migration.md:126-169](docs/migration.md:126-169), [tests/test_deprecated.py:319-346](tests/test_deprecated.py:319-346)

### Config Changes

Configuration in V2 uses a dictionary called `model_config` instead of a nested `Config` class:

```python
# V1 style
class Model(BaseModel):
    class Config:
        orm_mode = True

# V2 style
class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Note 'orm_mode' is now 'from_attributes'
```

Many config settings have been renamed or removed in V2.

Sources: [docs/migration.md:321-357](docs/migration.md:321-357), [docs/concepts/config.md:1-85](docs/concepts/config.md:1-85)

### Validator Changes

V2 replaces the decorators `@validator` and `@root_validator` with `@field_validator` and `@model_validator`, which provide new features and improvements:

```python