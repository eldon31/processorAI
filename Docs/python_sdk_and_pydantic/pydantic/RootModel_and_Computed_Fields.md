This page documents two distinct but complementary features: **RootModel** for validating root-level values, and **Computed Fields** for adding dynamic, read-only properties to models that appear during serialization.

For basic model functionality, see [BaseModel](#2.1). For field configuration and metadata, see [Field System](#2.2). For serialization customization, see [Serializers](#4.2).

---

## Overview

**RootModel** enables validation of types that don't naturally fit into Pydantic's field-based structure. Instead of defining multiple fields, a RootModel wraps a single root value of any type (primitives, collections, custom types, etc.).

**Computed Fields** are dynamic properties decorated with `@computed_field` that are calculated on-access and automatically included in serialization output. Unlike regular properties, computed fields appear in `model_dump()`, `model_dump_json()`, and JSON schema generation.

---

## RootModel

### Purpose and Design

RootModel provides a way to validate and serialize root-level values that are not traditional models with named fields. This is useful for:
- Wrapping primitive types with validation logic
- Validating collection types (lists, dicts) at the root level
- Creating type aliases with custom validation
- Building discriminated union handlers
- Parsing configuration formats where the entire structure is a single type

**Sources:** [pydantic/root_model.py:1-155]()

### Core Architecture

```mermaid
graph TB
    subgraph "Class Hierarchy"
        BaseModel["BaseModel"]
        RootModel["RootModel[RootModelRootType]<br/>Generic class"]
        BaseModel --> RootModel
    end
    
    subgraph "Key Attributes"
        root["root: RootModelRootType<br/>The validated value"]
        pydantic_root_model["__pydantic_root_model__ = True<br/>Marker flag"]
        pydantic_private["__pydantic_private__ = None<br/>No private attributes"]
        pydantic_extra["__pydantic_extra__ = None<br/>No extra fields"]
    end
    
    subgraph "Special Methods"
        init["__init__(root, **data)<br/>Single positional or kwargs"]
        model_construct["model_construct(root, _fields_set)<br/>Bypass validation"]
        copy_methods["__copy__, __deepcopy__<br/>Copy support"]
        state_methods["__getstate__, __setstate__<br/>Pickle support"]
    end
    
    RootModel --> root
    RootModel --> pydantic_root_model
    RootModel --> pydantic_private
    RootModel --> pydantic_extra
    
    RootModel --> init
    RootModel --> model_construct
    RootModel --> copy_methods
    RootModel --> state_methods
```

**Sources:** [pydantic/root_model.py:32-155](), [pydantic/_internal/_model_construction.py]()

### Basic Usage

The `root` field contains the validated value. RootModel can be instantiated with either a positional argument or keyword arguments:

```python
from pydantic import RootModel

# Wrapping a list
class IntList(RootModel[list[int]]):
    pass

# Usage
model = IntList([1, 2, 3])  # positional
model = IntList(root=[1, 2, 3])  # keyword
model = IntList(**{'root': [1, 2, 3]})  # dict unpacking
```

**Sources:** [pydantic/root_model.py:60-69](), [tests/test_root_model.py]()

### Key Characteristics

| Characteristic | Behavior | Rationale |
|---------------|----------|-----------|
| Single field | Only `root` field exists | RootModel represents a single value |
| Extra fields | Not supported (`model_config['extra']` raises error) | Would conflict with root-level validation |
| Private attributes | Set to `None` | Root models don't support `_private` attrs |
| Initialization | Accepts positional or keyword args | Flexible instantiation patterns |
| Validation | Applied to `root` value | Standard validation pipeline |
| Serialization | Returns root value directly in `model_dump()` | Not wrapped in a dict |

**Sources:** [pydantic/root_model.py:52-58](), [pydantic/root_model.py:60-69]()

### Initialization Flow

```mermaid
sequenceDiagram
    participant User
    participant RootModel__init__
    participant __pydantic_validator__
    participant ValidationPipeline
    
    User->>RootModel__init__: __init__(root=value) or __init__(**data)
    
    alt Has data dict
        RootModel__init__->>RootModel__init__: Check root is undefined
        RootModel__init__->>RootModel__init__: Set root = data
    end
    
    RootModel__init__->>__pydantic_validator__: validate_python(root, self_instance=self)
    __pydantic_validator__->>ValidationPipeline: Execute validation
    ValidationPipeline-->>__pydantic_validator__: Validated value
    __pydantic_validator__-->>RootModel__init__: Set self.root
    RootModel__init__-->>User: Initialized RootModel instance
```

**Sources:** [pydantic/root_model.py:60-69](), [pydantic/main.py]()

### Construction and Copying

RootModel provides special methods for construction and copying:

**model_construct**: Creates instances without validation
```python
# Bypass validation
model = IntList.model_construct(root=[1, 2, 3], _fields_set={'root'})
```

**Copy operations**: Shallow and deep copy support via `__copy__` and `__deepcopy__`

**Pickle support**: Via `__getstate__` and `__setstate__` for serialization

**Sources:** [pydantic/root_model.py:72-114](), [tests/test_construction.py]()

### Serialization Behavior

Unlike regular models, RootModel's `model_dump()` returns the root value directly, not a dictionary:

```python
model = IntList([1, 2, 3])