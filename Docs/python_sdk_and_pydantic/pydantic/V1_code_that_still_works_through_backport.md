from pydantic.utils import import_string
```

**Note:** Test utilities like `import_string` are now located in `pydantic._internal._validators`.

**Sources:** [pydantic/utils.py:1-5](), [tests/test_utils.py:35-47]()

---

### pydantic.typing

The `typing` module in V1 contained type-related utilities. In V2, typing utilities have been reorganized into `pydantic._internal._typing_extra`.

**File Location:** [pydantic/typing.py]()

**V1 Usage Example:**
```python
# V1 code that still works through backport
from pydantic.typing import get_origin
```

**Sources:** [pydantic/typing.py:1-5]()

---

### pydantic.env_settings

The `env_settings` module provided the `BaseSettings` class for environment-based configuration in V1. In V2, this functionality has been moved to a separate package: `pydantic-settings`.

**File Location:** [pydantic/env_settings.py]()

**Migration Path:**
```python