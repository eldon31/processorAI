def test_something(create_module):
    def my_module():
        from pydantic import BaseModel
        
        class MyModel(BaseModel):
            x: int
    
    module = create_module(my_module)
    assert module.MyModel(x=1).x == 1
```

The function:
1. Validates that the function has no arguments ([tests/conftest.py:31-32]())
2. Uses `inspect.getsource()` to get source code ([tests/conftest.py:36]())
3. Skips the `def` line ([tests/conftest.py:37-39]())
4. Dedents and returns the body ([tests/conftest.py:43]())

**Sources:** [tests/conftest.py:30-44]()

### Module File Creation

The `_create_module_file` function handles platform-specific file creation:

| Concern | Implementation |
|---------|---------------|
| Path length limits | Maximum 240 characters on Windows ([tests/conftest.py:48]()) |
| Invalid characters | Sanitizes `<>:"/\|?*` characters ([tests/conftest.py:50]()) |
| Name collisions | Appends 5-byte random hex token ([tests/conftest.py:51]()) |
| File extension | Always uses `.py` extension ([tests/conftest.py:52]()) |

**Sources:** [tests/conftest.py:46-54]()

### Assertion Rewriting

When `rewrite_assertions=True` (default), the fixture uses pytest's `AssertionRewritingHook` to enable detailed assertion failure messages. This hook rewrites Python assert statements at import time to provide better debugging information.

**Sources:** [tests/conftest.py:91-96]()

---

## Subprocess Code Execution

The `subprocess_run_code` fixture provides process-isolated code execution, essential for testing import-time side effects, environment isolation, and subprocess-specific behaviors.

```mermaid
graph LR
    subgraph "Input"
        func["FunctionType"]
        code_str["str source code"]
    end
    
    subgraph "File Creation"
        extract_func["_extract_source_code_from_function"]
        write_file["tmp_path / test.py<br/>Write source"]
    end
    
    subgraph "Subprocess Execution"
        check_output["subprocess.check_output<br/>sys.executable"]
        capture_stdout["Capture stdout<br/>encoding=utf8"]
    end
    
    func --> extract_func
    code_str --> write_file
    extract_func --> write_file
    write_file --> check_output
    check_output --> capture_stdout
    
    style write_file fill:#f9f9f9
    style check_output fill:#f9f9f9
```

**Sources:** [tests/conftest.py:105-119]()

The fixture creates a temporary `test.py` file and executes it with `subprocess.check_output`, returning the captured stdout as a UTF-8 string. This ensures complete process isolation between test execution and the code being tested.

---

## Schema Generation Monitoring

The `generate_schema_calls` fixture tracks how many times schema generation occurs, useful for testing caching behaviors and performance optimizations.

### Call Counter Implementation

```mermaid
graph TB
    subgraph "Fixture Setup"
        counter["CallCounter(count=0)<br/>Dataclass instance"]
        orig_func["orig_generate_schema<br/>Store original"]
        monkeypatch["monkeypatch.setattr<br/>Replace method"]
    end
    
    subgraph "Wrapper Logic"
        wrapper["generate_schema_call_counter<br/>Wrapper function"]
        depth_check["depth == 0?<br/>Handle recursion"]
        increment["counter.count += 1<br/>Increment if root call"]
        call_orig["orig_generate_schema<br/>Call original"]
    end
    
    subgraph "Test Usage"
        test_code["Test code<br/>Trigger schema generation"]
        assert_count["assert counter.count == N<br/>Verify caching"]
        counter_reset["counter.reset()<br/>Reset between checks"]
    end
    
    counter --> monkeypatch
    orig_func --> monkeypatch
    monkeypatch --> wrapper
    
    wrapper --> depth_check
    depth_check --> increment
    increment --> call_orig
    
    test_code --> assert_count
    assert_count --> counter_reset
    
    style counter fill:#f9f9f9
    style wrapper fill:#f9f9f9
```

**Sources:** [tests/conftest.py:144-161]()

The fixture uses a depth counter to handle recursive `GenerateSchema.generate_schema` calls - only root-level calls increment the counter. This prevents double-counting when schema generation triggers nested schema generation.

**Data Structures:**
- `CallCounter` dataclass with `count` field and `reset()` method ([tests/conftest.py:136-142]())
- `depth` variable tracks recursion level ([tests/conftest.py:148]())

**Sources:** [tests/conftest.py:136-161]()

---

## JSON Schema Validation

The `validate_json_schemas` fixture automatically validates all generated JSON schemas against the Draft 2020-12 specification. This runs for every test unless explicitly disabled.

### Validation Flow

```mermaid
graph TB
    subgraph "Fixture Installation"
        autouse["autouse=True<br/>Applies to all tests"]
        monkeypatch_gen["Monkeypatch GenerateJsonSchema.generate"]
        orig_generate["Store original generate method"]
    end
    
    subgraph "JSON Schema Generation"
        test_calls["Test calls<br/>model_json_schema()"]
        wrapper["Wrapped generate method"]
        orig_call["orig_generate(*args, **kwargs)<br/>Generate schema"]
    end
    
    subgraph "Validation Logic"
        check_marker["skip_json_schema_validation<br/>marker present?"]
        validate["Draft202012Validator.check_schema<br/>Validate against spec"]
        schema_error["SchemaError raised?"]
        pytest_fail["pytest.fail()<br/>Detailed error message"]
    end
    
    autouse --> monkeypatch_gen
    monkeypatch_gen --> orig_generate
    
    test_calls --> wrapper
    wrapper --> orig_call
    orig_call --> check_marker
    
    check_marker -->|No marker| validate
    check_marker -->|Has marker| return_schema["Return schema"]
    
    validate --> schema_error
    schema_error -->|Yes| pytest_fail
    schema_error -->|No| return_schema
    
    style validate fill:#f9f9f9
    style check_marker fill:#f9f9f9
```

**Sources:** [tests/conftest.py:163-182]()

### Opting Out of Validation

Tests can disable automatic JSON schema validation using the `skip_json_schema_validation` marker:

```python
@pytest.mark.skip_json_schema_validation
def test_invalid_json_schema():
    # This test intentionally generates invalid JSON Schema
    pass
```

The marker is checked via `request.node.get_closest_marker()` ([tests/conftest.py:169]()), and validation is skipped if found.

**Sources:** [tests/conftest.py:169-177]()

---

## Thread Safety Management

The test framework includes sophisticated thread safety detection to prevent race conditions when running tests in parallel with `pytest-run-parallel`.

### Thread-Unsafe Fixtures

```mermaid
graph TB
    subgraph "Unsafe Fixtures"
        gen_schema["generate_schema_calls<br/>Monkeypatches Pydantic"]
        benchmark["benchmark<br/>Cannot be reused"]
        tmp_path["tmp_path / tmpdir<br/>Duplicate paths"]
        copy_method["copy_method<br/>Uses pytest.warns()"]
        reset_plugins["reset_plugins<br/>Monkeypatching"]
    end
    
    subgraph "Detection Logic"
        pytest_itemcollected["pytest_itemcollected hook<br/>Per test item"]
        fixture_check["Check fixturenames<br/>tuple attribute"]
        match_check["fixture in _thread_unsafe_fixtures?"]
    end
    
    subgraph "Marker Application"
        add_marker["item.add_marker('thread_unsafe')<br/>Mark test"]
        serial_exec["pytest-run-parallel<br/>Serializes execution"]
    end
    
    gen_schema --> match_check
    benchmark --> match_check
    tmp_path --> match_check
    copy_method --> match_check
    reset_plugins --> match_check
    
    pytest_itemcollected --> fixture_check
    fixture_check --> match_check
    match_check -->|Match found| add_marker
    add_marker --> serial_exec
    
    style pytest_itemcollected fill:#f9f9f9
    style match_check fill:#f9f9f9
```

**Sources:** [tests/conftest.py:184-203]()

### Thread-Unsafe Fixture List

The following fixtures are marked as thread-unsafe:

| Fixture | Reason |
|---------|--------|
| `generate_schema_calls` | Monkeypatches global Pydantic code |
| `benchmark` | Fixture cannot be reused across threads |
| `tmp_path` / `tmpdir` | Risk of duplicate path creation |
| `copy_method` | Uses `pytest.warns()` which is not thread-safe |
| `reset_plugins` | Monkeypatches global state |

**Sources:** [tests/conftest.py:184-191]()

### Collection Hook Timing

The thread safety marker is added in `pytest_itemcollected`, which is critical because:
- `pytest-run-parallel` also implements this hook
- Pydantic's hook runs before the parallel plugin's hook
- Markers must be applied before the parallel plugin analyzes tests
- Using later hooks like `pytest_collection_modifyitems` would be too late

**Sources:** [tests/conftest.py:194-198]()

---

## Test Utility Classes

The testing framework provides utility dataclasses for common testing patterns.

### Err Dataclass

```mermaid
graph LR
    subgraph "Err Dataclass"
        message["message: str<br/>Error message"]
        errors["errors: Any | None<br/>Optional error details"]
    end
    
    subgraph "Methods"
        repr_method["__repr__()<br/>Custom representation"]
        message_escaped["message_escaped()<br/>re.escape() wrapper"]
    end
    
    message --> repr_method
    errors --> repr_method
    message --> message_escaped
    
    style message fill:#f9f9f9
    style repr_method fill:#f9f9f9
```

**Sources:** [tests/conftest.py:121-134]()

The `Err` dataclass represents expected validation errors in tests:

| Field | Type | Purpose |
|-------|------|---------|
| `message` | `str` | Expected error message text |
| `errors` | `Any \| None` | Optional detailed error information |

**Methods:**
- `__repr__()`: Custom string representation ([tests/conftest.py:126-130]())
- `message_escaped()`: Returns regex-escaped message for pattern matching ([tests/conftest.py:132-133]())

**Sources:** [tests/conftest.py:121-134]()

### CallCounter Dataclass

```mermaid
graph LR
    subgraph "CallCounter Dataclass"
        count["count: int = 0<br/>Counter value"]
    end
    
    subgraph "Methods"
        reset["reset() -> None<br/>Set count to 0"]
    end
    
    count --> reset
    
    style count fill:#f9f9f9
```

**Sources:** [tests/conftest.py:136-142]()

The `CallCounter` dataclass provides a simple mutable counter:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `count` | `int` | `0` | Number of calls recorded |

**Methods:**
- `reset()`: Resets count to zero ([tests/conftest.py:140-141]())

This is used by the `generate_schema_calls` fixture to track schema generation invocations.

**Sources:** [tests/conftest.py:136-142]()

---

## Summary

The Pydantic testing framework provides a comprehensive infrastructure for testing validation logic, schema generation, and type handling:

| Component | Purpose | Key Classes/Functions |
|-----------|---------|---------------------|
| pytest configuration | Command-line options and session setup | `pytest_addoption`, `disable_error_urls` |
| Module creation | Dynamic module import for testing | `create_module`, `_extract_source_code_from_function`, `_create_module_file` |
| Subprocess execution | Process-isolated code testing | `subprocess_run_code` |
| Schema monitoring | Track schema generation calls | `generate_schema_calls`, `CallCounter` |
| JSON validation | Automatic schema validation | `validate_json_schemas`, `Draft202012Validator` |
| Thread safety | Parallel test execution safety | `pytest_itemcollected`, `_thread_unsafe_fixtures` |
| Utilities | Common test patterns | `Err`, `CallCounter` |

**Sources:** [tests/conftest.py:1-203]()