from typing import Annotated
from pydantic import BaseModel, Field

class Model(BaseModel):
    value: Annotated[int, Field(gt=0, lt=100)]
```

The latter approach using `Annotated` is recommended for better support with static analysis tools.

### Strict Mode

Pydantic allows enforcing strict type checking using the `Strict` class:

```mermaid
graph TD
    subgraph "Strict Mode Options"
        S1["Strict Class (Annotated[type, Strict()])"]
        S2["StrictXXX Types (StrictInt, StrictStr, etc.)"]
        S3["strict=True parameter in constrained types"]
    end
    
    Input["Input Data"] --> IsStrict{"Strict Mode?"}
    IsStrict -->|Yes| Exact["Exact Type Check\n(isinstance check)"]
    IsStrict -->|No| Coercion["Allow Type Coercion"]
    
    Exact --> Valid["Valid Data or Error"]
    Coercion --> Valid
```

Sources: [pydantic/types.py:113-146]()

## Constrained Types

### Numeric Types

Pydantic provides constrained versions of numeric types with validation rules:

| Type | Description | Constraints |
|------|-------------|-------------|
| `conint()` | Constrained integer | `gt`, `ge`, `lt`, `le`, `multiple_of` |
| `PositiveInt` | Integer > 0 | Equivalent to `Annotated[int, Gt(0)]` |
| `NegativeInt` | Integer < 0 | Equivalent to `Annotated[int, Lt(0)]` |
| `NonNegativeInt` | Integer >= 0 | Equivalent to `Annotated[int, Ge(0)]` |
| `NonPositiveInt` | Integer <= 0 | Equivalent to `Annotated[int, Le(0)]` |
| `confloat()` | Constrained float | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan` |
| `PositiveFloat` | Float > 0 | Equivalent to `Annotated[float, Gt(0)]` |
| `NegativeFloat` | Float < 0 | Equivalent to `Annotated[float, Lt(0)]` |
| `NonNegativeFloat` | Float >= 0 | Equivalent to `Annotated[float, Ge(0)]` |
| `NonPositiveFloat` | Float <= 0 | Equivalent to `Annotated[float, Le(0)]` |
| `FiniteFloat` | Float that is not `inf` or `nan` | Equivalent to `Annotated[float, AllowInfNan(False)]` |
| `condecimal()` | Constrained decimal | Similar to `confloat()` + `max_digits`, `decimal_places` |

Sources: [pydantic/types.py:147-362](), [pydantic/types.py:386-645]()

### String Types

Pydantic offers string constraints through `constr()` and `StringConstraints`:

```mermaid
graph TD
    subgraph "String Constraints"
        S1["min_length: Minimum length"]
        S2["max_length: Maximum length"]
        S3["pattern: Regex pattern"]
        S4["strip_whitespace: Remove whitespace"]
        S5["to_lower: Convert to lowercase"]
        S6["to_upper: Convert to uppercase"]
        S7["strict: Strict type checking"]
    end
    
    ConStr["constr() function"] --> S1
    ConStr --> S2
    ConStr --> S3
    ConStr --> S4
    ConStr --> S5
    ConStr --> S6
    ConStr --> S7
    
    StringConstraints["StringConstraints class"] --> S1
    StringConstraints --> S2
    StringConstraints --> S3
    StringConstraints --> S4
    StringConstraints --> S5
    StringConstraints --> S6
    StringConstraints --> S7
```

Sources: [pydantic/types.py:690-828]()

Similar constraints exist for bytes with `conbytes()`.

### Collection Types

Pydantic provides constrained collection types:

| Type | Description | Constraints |
|------|-------------|-------------|
| `conlist()` | Constrained list | `item_type`, `min_length`, `max_length` |
| `conset()` | Constrained set | `item_type`, `min_length`, `max_length` |
| `confrozenset()` | Constrained frozenset | `item_type`, `min_length`, `max_length` |

Sources: [pydantic/types.py:836-903]()

## Network Types

Pydantic includes a rich set of network-related types defined in `networks.py`:

```mermaid
graph TD
    subgraph "URL Types"
        BaseUrl["_BaseUrl (Abstract Base)"]
        AnyUrl["AnyUrl"] --> BaseUrl
        HttpUrl["HttpUrl"] --> AnyUrl
        AnyHttpUrl["AnyHttpUrl"] --> AnyUrl
        FileUrl["FileUrl"] --> AnyUrl
        FtpUrl["FtpUrl"] --> AnyUrl
        WebsocketUrl["WebsocketUrl"] --> AnyUrl

        BaseMultiHostUrl["_BaseMultiHostUrl (Abstract Base)"]
        PostgresDsn["PostgresDsn"] --> BaseMultiHostUrl
        RedisDsn["RedisDsn"] --> BaseMultiHostUrl
        MongoDsn["MongoDsn"] --> BaseMultiHostUrl
        KafkaDsn["KafkaDsn"] --> BaseMultiHostUrl
    end

    subgraph "Email Types"
        EmailStr["EmailStr"]
        NameEmail["NameEmail"]
    end

    subgraph "IP Types"
        IPvAnyAddress["IPvAnyAddress"]
        IPvAnyInterface["IPvAnyInterface"]
        IPvAnyNetwork["IPvAnyNetwork"]
    end
```

Sources: [pydantic/networks.py:70-526](), [pydantic/networks.py:534-669]()

Network types provide specialized validation:
- URL types validate and normalize URLs with various schemes
- Email types validate email addresses
- IP types validate IPv4 and IPv6 addresses, networks, and interfaces

These network types can be directly used in models:

```python
from pydantic import BaseModel, HttpUrl, EmailStr

class User(BaseModel):
    website: HttpUrl
    email: EmailStr
```

## Special Types

### Path Types

Path-related types provide validation for file system paths:

| Type | Description |
|------|-------------|
| `FilePath` | Path that points to an existing file |
| `DirectoryPath` | Path that points to an existing directory |
| `NewPath` | Path that does not currently exist |
| `SocketPath` | Path pointing to a Unix socket |

Sources: [pydantic/__init__.py:73-77](), [pydantic/__init__.py:357-359]()

### Secret Types

Secret types provide special handling for sensitive data:

| Type | Description |
|------|-------------|
| `SecretStr` | String that hides its contents in repr |  
| `SecretBytes` | Bytes that hides its contents in repr |
| `Secret` | Generic version of secret types |

Sources: [pydantic/__init__.py:78-80](), [pydantic/__init__.py:348-350]()

### ImportString Type

`ImportString` provides a way to import Python objects from strings:

```mermaid
graph TD
    Input["String Input\n(e.g., 'math.cos')"] --> Processing["ImportString Processing"] 
    Processing --> Output["Imported Python Object\n(e.g., math.cos function)"]
    
    subgraph "ImportString Features"
        F1["Module path parsing"]
        F2["Attribute separation"]
        F3["Import error handling"]
        F4["Serialization to string"]
    end
```

Sources: [pydantic/types.py:906-1028]()

## Type Adapter

The `TypeAdapter` class provides a way to use Pydantic's validation system outside of models:

```mermaid
graph TD
    subgraph "TypeAdapter Functionality"
        TA["TypeAdapter(Type)"]
        
        TA --> V1["validate_python(data)"]
        TA --> V2["validate_json(json_data)"]
        TA --> S1["dump_python(obj)"]
        TA --> S2["json_schema()"]
    end
    
    Type["Any Python Type"] --> TA
    Data["Input Data"] --> V1
    JsonData["JSON String"] --> V2
    
    V1 --> ValidatedObj["Validated Object"]
    V2 --> ValidatedObj
```

Sources: [pydantic/__init__.py:380]()

The TypeAdapter makes it easy to apply Pydantic validation to standalone types:

```python
from pydantic import TypeAdapter

int_list_validator = TypeAdapter(list[int])
validated = int_list_validator.validate_python(['1', '2', '3'])
# Result: [1, 2, 3]
```

## Working with Annotated Types

Pydantic provides special handling for Python's `Annotated` type:

```mermaid
graph TD
    subgraph "Annotated Type Uses"
        A1["Type constraints\nAnnotated[int, Gt(5)]"]
        A2["Validation\nAnnotated[str, BeforeValidator(func)]"]
        A3["Field metadata\nAnnotated[str, Field(description='...')]"]
        A4["Type-specific behavior\nAnnotated[float, AllowInfNan(True)]"]
    end
    
    A1 --> Validation["Pydantic Validation"]
    A2 --> Validation
    A3 --> Schema["Schema Generation"]
    A4 --> Validation
```

Sources: [pydantic/_internal/_known_annotated_metadata.py:1-42]()

`Annotated` provides a clean way to combine type information with metadata:

```python
from typing import Annotated
from annotated_types import Gt, Lt
from pydantic import BaseModel

class Model(BaseModel):
    # Integer between 1 and 100
    value: Annotated[int, Gt(0), Lt(101)]
```

## Creating Custom Types

Pydantic allows for creation of custom types by implementing `__get_pydantic_core_schema__` method:

```mermaid
graph TD
    subgraph "Custom Type Components"
        C1["__get_pydantic_core_schema__() method"]
        C2["Optional __get_pydantic_json_schema__() method"]
        C3["Optional serializer"]
    end
    
    CustomType["Custom Type Class"] --> C1
    CustomType --> C2
    CustomType --> C3
    
    C1 --> CoreSchema["CoreSchema Generation"]
    C2 --> JsonSchema["JSON Schema Generation"]
    C3 --> Serialization["Custom Serialization"]
```

Sources: [pydantic/_internal/_validators.py:66-127]()

## Internal Validation Process

The type system works with Pydantic's validation engine:

```mermaid
graph LR
    Type["Python Type"] --> GenerateSchema["GenerateSchema"] --> CoreSchema["CoreSchema"]
    
    subgraph "Validation"
        Input["Input Data"] --> Validator["SchemaValidator"] --> ValidData["Validated Data"]
    end
    
    CoreSchema --> Validator
```

Sources: [pydantic/_internal/_core_utils.py:43-66](), [pydantic/_internal/_validators.py:66-127]()

## Constraints Reference

| Type Category | Available Constraints |
|---------------|------------------------|
| String        | `min_length`, `max_length`, `pattern`, `strip_whitespace`, `to_lower`, `to_upper`, `strict` |
| Bytes         | `min_length`, `max_length`, `strict` |
| List          | `min_length`, `max_length`, `strict`, `fail_fast` |
| Set           | `min_length`, `max_length`, `strict`, `fail_fast` |
| Dict          | `min_length`, `max_length`, `strict` |
| Float         | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`, `strict` |
| Integer       | `gt`, `ge`, `lt`, `le`, `multiple_of`, `strict` |
| Decimal       | `gt`, `ge`, `lt`, `le`, `multiple_of`, `max_digits`, `decimal_places`, `strict` |

Sources: [pydantic/_internal/_known_annotated_metadata.py:18-64]()