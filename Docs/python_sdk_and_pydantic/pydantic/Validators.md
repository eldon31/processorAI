Validators in Pydantic are powerful tools for customizing validation logic beyond simple type checking. They allow you to validate and transform data during model creation or when field values change, ensuring data meets specific requirements, enforcing business rules, and modifying values as needed.

For information about serializers, which handle converting data out of Pydantic models, see [Serializers](#4.2).

## Validation Pipeline

The Pydantic validation process follows a structured pipeline to transform raw input data into validated model instances:

```mermaid
flowchart TD
    InputData["Input Data"] --> ModelInit["Model.__init__"]
    ModelInit --> Validator["Validation Pipeline"]
    
    subgraph "Validation Pipeline"
        BeforeVal["Before Validators"] --> FieldVal["Field Validators"]
        FieldVal --> AfterVal["After Validators"]
        AfterVal --> ModelVal["Model Validators"]
    end
    
    Validator -->|"Success"| ModelInstance["Model Instance"]
    Validator -->|"Failure"| ValidationError["ValidationError"]
    
    classDef pipeline fill:#f9f9f9,stroke:#333,stroke-width:1px;
    class "Validation Pipeline" pipeline;
```

Sources: 
- [tests/test_validators.py:312-384](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L312-L384)
- [tests/test_validators.py:192-215](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L192-L215)

## Field Validators

Field validators work on individual fields and are defined with the `@field_validator` decorator. They can validate or transform field values before or after standard validation.

### Basic Usage

```python
class Model(BaseModel):
    a: str
    
    @field_validator('a')
    @classmethod
    def check_a(cls, v: Any):
        if 'foobar' not in v:
            raise ValueError('"foobar" not found in a')
        return v
```

When validators raise an error, Pydantic will include this in the `ValidationError` with contextual information about which field failed and why.

Sources: 
- [tests/test_validators.py:192-215](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L192-L215)

### Validator Modes

Field validators can operate in different modes that determine when they run in the validation pipeline:

- `mode='before'`: Runs before type coercion, useful for custom parsing or transforming raw input data
- `mode='after'`: Runs after type coercion (default), for validating properly typed values 
- `mode='plain'`: Similar to 'after' but with a simpler function signature
- `mode='wrap'`: Advanced mode that wraps around standard validation, giving access to both pre- and post-validation values

```python
class Model(BaseModel):
    a: list[int]
    
    @field_validator('a', mode='before')
    @classmethod
    def check_a1(cls, v: Any) -> list[Any]:
        # Transform input before standard validation
        v.append('123')  # This will be coerced to int by standard validation
        return v
    
    @field_validator('a')  # mode='after' is the default
    @classmethod
    def check_a2(cls, v: list[int]) -> list[Any]:
        # Add to already-validated list
        v.append(456)
        return v
```

Sources: 
- [tests/test_validators.py:313-329](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L313-L329)
- [pydantic/_internal/_decorators.py:518-552](https://github.com/pydantic/pydantic/blob/main/pydantic/_internal/_decorators.py#L518-L552)

### Multi-field Validators

Validators can be applied to multiple fields at once:

```python
class Model(BaseModel):
    a: str
    b: str
    
    @field_validator('a', 'b')
    @classmethod
    def check_a_and_b(cls, v: Any, info: ValidationInfo) -> Any:
        if len(v) < 4:
            field = cls.model_fields[info.field_name]
            raise AssertionError(f'{field.alias or info.field_name} is too short')
        return v + 'x'
```

The `info` parameter provides context about the current validation, including the field being validated and model data.

Sources: 
- [tests/test_validators.py:486-518](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L486-L518)

### Wildcard Validators

Use `'*'` to apply a validator to all fields:

```python
class MyModel(BaseModel):
    x: int
    
    @field_validator('*')
    @classmethod
    def validate_all(cls, v: Any):
        return v * 2
```

Sources: 
- [tests/test_validators.py:860-869](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L860-L869)
- [tests/test_validators.py:728-759](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L728-L759)

### Validator Information

Validators can accept a `ValidationInfo` parameter to access additional context:

```python
class ModelTwo(BaseModel):
    m: ModelOne
    b: int
    
    @field_validator('b')
    @classmethod
    def validate_b(cls, b, info: ValidationInfo):
        if 'm' in info.data:
            return b + info.data['m'].a
        else:
            return b
```

Sources: 
- [tests/test_validators.py:462-483](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L462-L483)
- [tests/test_validators.py:394-406](https://github.com/pydantic/pydantic/blob/main/tests/test_validators.py#L394-L406)

## Model Validators

Model validators validate entire models, enabling validation logic that depends on multiple fields:

```python
class User(BaseModel):
    username: str
    password1: str
    password2: str
    
    @model_validator
    def check_passwords_match(cls, values):
        if values.password1 != values.password2:
            raise ValueError('passwords do not match')
        return values
```

Model validators can run in three modes:

- `mode='before'`: Runs before field validation, useful for pre-processing raw input data
- `mode='after'`: Runs after field validation (default), for validating the model as a whole
- `mode='wrap'`: Wraps the validation process, giving full control over the validation pipeline

Sources:
- [pydantic/_internal/_decorators.py:141-143](https://github.com/pydantic/pydantic/blob/main/pydantic/_internal/_decorators.py#L141-L143)

## Functional Validators

Functional validators are used with `Annotated` types and provide a reusable way to apply validation logic:

```mermaid
flowchart LR
    subgraph "Functional Validators"
        BeforeValidator["BeforeValidator"] --> Raw["Raw Value"]
        Raw --> StandardVal["Standard Validation"]
        StandardVal --> ValidatedValue["Validated Value"]
        ValidatedValue --> AfterValidator["AfterValidator"]
        
        PlainValidator["PlainValidator"] -->|"Direct\nValidation"| ValidatedValue
        
        WrapValidator["WrapValidator"] -->|"Controls\nEntire Process"| ValidationProcess["Validation Process"]
    end
    
    classDef validator fill:#f9f9f9,stroke:#333,stroke-width:1px;
    class "Functional Validators" validator;
```

### Types of Functional Validators

- **BeforeValidator**: Runs before standard validation, useful for pre-processing input
- **AfterValidator**: Runs after standard validation, for additional checks on typed data
- **PlainValidator**: Direct validator without standard validation
- **WrapValidator**: Gives full control over the validation process

### Examples

```python