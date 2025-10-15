int_container = Container[int](value=1)
str_container = Container[str](value="hello")
```

When you parameterize a generic model with a specific type (e.g., `Container[int]`), Pydantic creates a specialized model class with validation specifically for that type.

```mermaid
flowchart TD
    Generic["Generic Model Creation"] --> Parameterize["Model Parameterization"]
    Parameterize --> Validation["Type-specific Validation"]
    
    subgraph "Generic Model Creation"
        TypeVar["TypeVar('T')"] --> BaseGeneric["class Container(BaseModel, Generic[T])"]
        BaseGeneric --> FieldDef["value: T"]
    end
    
    subgraph "Model Parameterization"
        BaseGeneric --> ConcreteInt["Container[int]"]
        BaseGeneric --> ConcreteStr["Container[str]"]
    end
    
    subgraph "Type-specific Validation"
        ConcreteInt --> ValidateInt["Validates integers"]
        ConcreteStr --> ValidateStr["Validates strings"]
    end
```

Sources: 
- `tests/test_generics.py:83-92`
- `tests/test_generics.py:580-648`

### Implementation Mechanics

When you parameterize a generic model like `Container[int]`, several key processes occur:

1. **Type Substitution**: All occurrences of the type variable `T` in the model are replaced with the concrete type `int`
2. **Class Creation**: A new subclass of the original model is created with the concrete types
3. **Caching**: The created class is cached to ensure the same parameterization returns the same class

```mermaid
sequenceDiagram
    participant ModelClass as "Generic Model"
    participant ClassGetItem as "__class_getitem__"
    participant GenericCache as "_GENERIC_TYPES_CACHE"
    participant CreateSubmodel as "create_generic_submodel"
    participant ReplaceTypes as "replace_types"
    
    ModelClass->>ClassGetItem: Model[int]
    ClassGetItem->>GenericCache: Check cache for Model[int]
    
    alt Already in cache
        GenericCache-->>ClassGetItem: Return cached class
    else Not in cache
        ClassGetItem->>CreateSubmodel: Create new class
        CreateSubmodel->>ReplaceTypes: Replace T with int in fields
        ReplaceTypes-->>CreateSubmodel: Fields with concrete types
        CreateSubmodel-->>ClassGetItem: New model class
        ClassGetItem->>GenericCache: Store in cache
    end
    
    ClassGetItem-->>ModelClass: Return parameterized model
```

Sources:
- `pydantic/_internal/_generics.py:106-150`
- `pydantic/_internal/_generics.py:246-340`
- `pydantic/_internal/_generics.py:439-547`

### Type Substitution in Depth

The `replace_types` function recursively traverses type annotations and substitutes type variables with concrete types:

```mermaid
graph TD
    subgraph "Type Substitution"
        TypeAnnotation["Type Annotation"] --> CheckType{"Is TypeVar?"}
        CheckType -->|Yes| Substitute["Substitute with concrete type"]
        CheckType -->|No| CheckContainer{"Is container type?"}
        CheckContainer -->|Yes| RecurseIntoArgs["Recurse into type args"]
        CheckContainer -->|No| ReturnUnchanged["Return unchanged"]
        
        RecurseIntoArgs --> ProcessArgs["Process each argument"]
        ProcessArgs --> ReassembleType["Reassemble container type"]
    end
```

This handles complex nested types like `List[Dict[str, T]]` → `List[Dict[str, int]]` when substituting `T` with `int`.

Sources:
- `pydantic/_internal/_generics.py:178-195`
- `pydantic/_internal/_generics.py:246-340`

### Caching System

Pydantic employs a sophisticated caching mechanism to ensure that:
1. The same parameterization of a generic model returns the same class
2. Memory usage is optimized by using weak references
3. The system can handle recursive generic types

```mermaid
classDiagram
    class GenericTypesCache {
        <<WeakValueDictionary>>
        Cache of parametrized models
    }
    
    class ContextVar_GENERIC_TYPES_CACHE {
        <<ContextVar>>
        Thread-local cache access
    }
    
    class LimitedDict {
        size_limit: int
        Maximum cache size
    }
    
    ContextVar_GENERIC_TYPES_CACHE --> GenericTypesCache : references
    GenericTypesCache --> LimitedDict : uses for overflow
```

The caching system uses a two-stage lookup to optimize performance:
1. An "early" cache key for quick lookups
2. A "late" cache key that handles more complex equivalence relationships

Sources:
- `pydantic/_internal/_generics.py:42-57`
- `pydantic/_internal/_generics.py:97-97`
- `pydantic/_internal/_generics.py:439-547`
- `tests/test_generics.py:352-456`

## Forward References

Forward references allow referencing types that haven't been fully defined yet, which is essential for recursive models and handling circular dependencies.

### Basic Usage

In Python, forward references are typically written as string literals:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    friends: list["Person"] = []  # Forward reference to Person itself
```

This creates a recursive data structure where a `Person` can have a list of `Person` objects as friends.

```mermaid
graph TD
    subgraph "Person Model"
        PersonClass["Person"] -->|has field| FriendsField["friends: list['Person']"]
        FriendsField -->|references| PersonClass
    end
```

Sources:
- `tests/test_forward_ref.py:128-166`
- `tests/test_forward_ref.py:261-289`

### Forward Reference Resolution

When Pydantic encounters a string annotation, it:
1. Records the original string annotation
2. Marks the field as incomplete (`_complete = False`)
3. Attempts to resolve the reference when needed

The resolution process happens:
- **Automatically** during validation if a model has unresolved references
- **Explicitly** when calling `Model.model_rebuild()`

```mermaid
flowchart TD
    ModelDefinition["Model definition with\nforward references"] --> ModelCreation["Model class creation"]
    ModelCreation --> StoreOriginalAnnotation["Store original string annotation"]
    ModelCreation --> MarkIncomplete["Mark model as\n__pydantic_complete__ = False"]
    
    MarkIncomplete --> TriggerA["Validation triggers\nresolution"]
    MarkIncomplete --> TriggerB["Explicit model_rebuild()\ntriggers resolution"]
    
    TriggerA --> Resolve["rebuild_model_fields()"]
    TriggerB --> Resolve
    Resolve --> EvaluateAnnotations["Evaluate string annotations\ninto actual types"]
    EvaluateAnnotations --> CompleteModel["Mark model as\n__pydantic_complete__ = True"]
```

Sources:
- `pydantic/_internal/_fields.py:78-282`
- `pydantic/_internal/_fields.py:300-337`
- `tests/test_forward_ref.py:42-75`

### Type Evaluation

Pydantic evaluates string annotations by:
1. Using the `eval_type` function to convert the string to a type object
2. Searching for the referenced type in appropriate namespaces
3. Handling failure gracefully if a type can't be resolved immediately

```mermaid
flowchart TD
    StringAnnotation["String annotation\n'TypeName'"] --> TryEval["try_eval_type()"]
    TryEval -->|Success| ResolvedType["Resolved type"]
    TryEval -->|Failure| StoreOriginal["Store original for\nlater resolution"]
    
    subgraph "Namespace Resolution"
        GlobalNamespace["Module globals"]
        LocalNamespace["Local variables"]
        ImportedModules["Imported modules"]
    end
    
    TryEval --> GlobalNamespace
    TryEval --> LocalNamespace
    TryEval --> ImportedModules
```

Sources:
- `pydantic/_internal/_typing_extra.py:290-457`
- `pydantic/_internal/_typing_extra.py:209-271`

### Recursive Models and Circular Dependencies

Pydantic efficiently handles recursive models (like trees or graphs) and circular dependencies between models by:
1. Detecting recursion during schema generation
2. Using special schema references to avoid infinite recursion
3. Auto-rebuilding models as necessary to resolve circular dependencies

```mermaid
flowchart TD
    subgraph "Recursive Model Example"
        ModelA["TreeNode"] -->|has field| Children["children: list['TreeNode']"]
        Children -->|references| ModelA
    end
    
    subgraph "Circular Dependency Example"
        ModelB["Person"] -->|has field| Friends["friends: list['Person']"]
        Friends -->|references| ModelB
        
        ModelC["Department"] -->|has field| Employees["employees: list['Employee']"]
        ModelD["Employee"] -->|has field| Department["department: 'Department'"]
        Employees -->|references| ModelD
        Department -->|references| ModelC
    end
```

Sources:
- `tests/test_forward_ref.py:111-166`
- `tests/test_forward_ref.py:205-260`
- `tests/test_forward_ref.py:261-411`
- `tests/test_forward_ref.py:697-714`

## Combining Generics and Forward References

### Generic Models with Forward References

Combining generics and forward references enables powerful type patterns:

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class TreeNode(BaseModel, Generic[T]):
    value: T
    children: list["TreeNode[T]"] = []  # Forward reference to the generic model itself
```

When this forward reference is resolved, the type variable `T` is correctly substituted with the concrete type.

```mermaid
flowchart TD
    GenericTree["TreeNode[T]"] --> Parameterize["TreeNode[int]"]
    Parameterize --> ResolveForward["Resolve forward reference"]
    ResolveForward --> SubstituteT["Substitute T with int"]
    SubstituteT --> Result["children: list[TreeNode[int]]"]
    
    subgraph "Model Instantiation"
        Result --> Instance["TreeNode[int](value=1, children=[...])"]
    end
```

Sources:
- `tests/test_generics.py:664-794`
- `pydantic/_internal/_fields.py:327-328`
- `pydantic/_internal/_generics.py:396-437`

### Handling Recursive Generic Types

For recursive generic types, Pydantic implements special handling to prevent infinite recursion:

```mermaid
flowchart TD
    RecursiveGenericType["Recursive Generic Type"] --> DetectRecursion["generic_recursion_self_type()"]
    DetectRecursion -->|First occurrence| ContinueProcessing["Continue processing"]
    DetectRecursion -->|Repeated occurrence| CreatePlaceholder["Create PydanticRecursiveRef"]
    CreatePlaceholder --> UseInSchema["Use as placeholder in schema"]
```

This allows for properly handling complex structures like trees where nodes can contain other nodes of the same type.

Sources:
- `pydantic/_internal/_generics.py:396-437`
- `tests/test_generics.py:458-486`

## Advanced Usage Patterns

### Bounded Type Variables

You can restrict the allowed types by using bounded type variables:

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=int)  # T must be int or a subclass of int

class NumberModel(BaseModel, Generic[T]):
    value: T
```

This ensures that only types compatible with the bound can be used as parameters.

Sources:
- `tests/test_generics.py:881-912`

### Default Type Arguments

Generic models can have default type arguments using Python 3.12+ syntax:

```python
from typing import Generic, TypeVar
from typing_extensions import TypeVar

T = TypeVar('T')
S = TypeVar('S', default=int)  # Default type is int

class Model(BaseModel, Generic[T, S]):
    t: T
    s: S
```

This allows users to only specify some type arguments while others default to predefined types.

Sources:
- `tests/test_generics.py:297-349`

### Partial Specialization

You can partially specialize a generic model with multiple type variables:

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')
S = TypeVar('S')

class Model(BaseModel, Generic[T, S]):
    t: T
    s: S

IntModel = Model[int, S]  # Partially specialized
IntStrModel = IntModel[str]  # Fully specialized
```

Partial specialization allows for creating intermediate template models.

Sources:
- `tests/test_generics.py:797-878`

## Implementation Details

### Generic Model Creation Internals

When a generic model is parameterized, the `create_generic_submodel` function creates a new subclass:

```mermaid
flowchart TD
    ClassGetItem["__class_getitem__"] --> CheckCache["Check cache for existing model"]
    CheckCache -->|Not found| CreateSub["create_generic_submodel()"]
    CreateSub --> PrepareClass["prepare_class()"]
    PrepareClass --> SetMetadata["Set __pydantic_generic_metadata__"]
    SetMetadata --> RegisterGlobally["Register in module globals\nif called globally"]
    RegisterGlobally --> ReturnModel["Return new model class"]
```

The created model contains metadata about its generic origin, arguments, and parameters to support further operations.

Sources:
- `pydantic/_internal/_generics.py:100-150`
- `pydantic/_internal/_generics.py:343-393`

### Forward Reference Handling Internals

The handling of forward references is primarily implemented in the `_fields.py` and `_typing_extra.py` modules:

```mermaid
flowchart TD
    CollectFields["collect_model_fields()"] --> DetectForwardRef["Detect string annotations"]
    DetectForwardRef --> StoreAnnotation["Store in field._original_annotation"]
    StoreAnnotation --> MarkIncomplete["Mark field._complete = False"]
    
    RebuildFields["rebuild_model_fields()"] --> FindIncomplete["Find incomplete fields"]
    FindIncomplete --> EvalType["_typing_extra.eval_type()"]
    EvalType --> ApplyTypes["Apply types with typevars_map"]
    ApplyTypes --> CreateNewField["Create new field with resolved type"]
```

The resolution process uses Python's introspection capabilities to find the right namespace context for evaluating the string annotations.

Sources:
- `pydantic/_internal/_fields.py:78-167`
- `pydantic/_internal/_fields.py:300-337`
- `pydantic/_internal/_typing_extra.py:290-464`

## Conclusion

Generics and forward references are powerful features in Pydantic that enable complex type patterns while maintaining type safety. They allow for:

1. Creating reusable model templates with generics
2. Building recursive data structures with forward references
3. Combining both to create sophisticated type systems

Understanding these features is essential for advanced Pydantic usage, especially when building models with complex relationships or when creating reusable model libraries.