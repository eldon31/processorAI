```

This behavior is controlled by the model's serialization schema and differs from BaseModel to match the semantic meaning of a "root" value.

**Sources:** [pydantic/root_model.py:116-144](), [tests/test_root_model.py]()

---

## Computed Fields

### Purpose and Design

Computed fields are dynamic properties that:
1. Are calculated on-access (not stored in `__dict__`)
2. Automatically appear in serialization (`model_dump()`, `model_dump_json()`)
3. Generate JSON schema with `readOnly: true`
4. Can have custom serializers applied
5. Support property setters and deleters

They bridge the gap between regular properties (not serialized) and model fields (stored and validated).

**Sources:** [pydantic/fields.py](), [tests/test_computed_fields.py:27-66]()

### Core Components

```mermaid
graph TB
    subgraph "Decorator and Metadata"
        computed_field_decorator["@computed_field decorator<br/>pydantic.computed_field()"]
        ComputedFieldInfo["ComputedFieldInfo<br/>Metadata container"]
        DecoratorInfos["DecoratorInfos.computed_fields<br/>Dict storage"]
    end
    
    subgraph "Property Integration"
        property_obj["property object<br/>Standard Python property"]
        wrapped_property["wrapped_property<br/>Stored in ComputedFieldInfo"]
        getter["@property getter<br/>Computes value"]
        setter["@property.setter<br/>Optional setter"]
        deleter["@property.deleter<br/>Optional deleter"]
    end
    
    subgraph "Schema Generation"
        model_computed_fields["model_computed_fields<br/>ClassVar[dict]"]
        json_schema["JSON Schema<br/>readOnly: true"]
        serialization_schema["Serialization Schema<br/>Include in output"]
    end
    
    computed_field_decorator --> ComputedFieldInfo
    ComputedFieldInfo --> DecoratorInfos
    ComputedFieldInfo --> wrapped_property
    
    property_obj --> getter
    property_obj --> setter
    property_obj --> deleter
    wrapped_property --> property_obj
    
    ComputedFieldInfo --> model_computed_fields
    ComputedFieldInfo --> json_schema
    ComputedFieldInfo --> serialization_schema
```

**Sources:** [pydantic/fields.py](), [pydantic/_internal/_decorators.py:427](), [tests/test_computed_fields.py]()

### Basic Usage

The `@computed_field` decorator can be used directly or with the `@property` decorator:

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: int
    length: int
    
    @computed_field
    @property
    def area(self) -> int:
        """Calculate area"""
        return self.width * self.length
    
    # Shorthand (property is implied)
    @computed_field
    def perimeter(self) -> int:
        return 2 * (self.width + self.length)

rect = Rectangle(width=10, length=5)