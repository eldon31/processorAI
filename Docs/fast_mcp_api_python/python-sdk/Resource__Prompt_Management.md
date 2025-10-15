The resource and prompt management system in FastMCP provides structured access to data sources and conversation templates for MCP servers. Resources represent data that can be read (files, HTTP endpoints, databases), while prompts are message templates that can be rendered with parameters for LLM interactions.

For tool execution functionality, see [Tool Management](#2.2). For low-level protocol handling, see [Protocol & Message System](#4).

## Resource Management Architecture

The resource system provides a unified interface for accessing various data sources through the `Resource` base class and supporting infrastructure.

### Resource Class Hierarchy

```mermaid
classDiagram
    class Resource {
        <<abstract>>
        +uri: AnyUrl
        +name: str
        +title: str
        +description: str  
        +mime_type: str
        +icons: list[Icon]
        +read()* str|bytes
    }
    
    class TextResource {
        +text: str
        +read() str
    }
    
    class BinaryResource {
        +data: bytes
        +read() bytes
    }
    
    class FunctionResource {
        +fn: Callable
        +read() str|bytes
        +from_function() FunctionResource
    }
    
    class FileResource {
        +path: Path
        +is_binary: bool
        +read() str|bytes
    }
    
    class HttpResource {
        +url: str
        +read() str|bytes
    }
    
    class DirectoryResource {
        +path: Path
        +recursive: bool
        +pattern: str
        +list_files() list[Path]
        +read() str
    }
    
    Resource <|-- TextResource
    Resource <|-- BinaryResource  
    Resource <|-- FunctionResource
    Resource <|-- FileResource
    Resource <|-- HttpResource
    Resource <|-- DirectoryResource
```

**Sources:** [src/mcp/server/fastmcp/resources/base.py:19-49](), [src/mcp/server/fastmcp/resources/types.py:20-200]()

### Resource Management Flow

```mermaid
sequenceDiagram
    participant Client
    participant "ResourceManager" as RM
    participant "ResourceTemplate" as RT
    participant "Resource" as R
    participant "Context" as CTX

    Note over RM: "Static resources and templates registered"
    
    Client->>RM: "get_resource(uri, context)"
    RM->>RM: "Check _resources dict"
    
    alt "Static resource exists"
        RM->>R: "Return cached resource"
        R->>Client: "Resource instance"
    else "No static resource"
        RM->>RT: "Check _templates for pattern match"
        RT->>RT: "matches(uri) -> params"
        RT->>CTX: "inject_context(fn, params, context)"
        RT->>RT: "fn(**params)"
        RT->>R: "create FunctionResource"
        R->>Client: "Dynamic resource instance"
    end
    
    Client->>R: "read()"
    R->>Client: "str | bytes"
```

**Sources:** [src/mcp/server/fastmcp/resources/resource_manager.py:77-98](), [src/mcp/server/fastmcp/resources/templates.py:84-110]()

## Resource Types and Implementation

### Static Resource Types

The system provides several concrete resource implementations for common data sources:

| Resource Type | Purpose | Key Methods | File Location |
|---------------|---------|-------------|---------------|
| `TextResource` | Static text content | `read() -> str` | [types.py:20-27]() |
| `BinaryResource` | Static binary data | `read() -> bytes` | [types.py:30-37]() |
| `FileResource` | File system access | `read() -> str\|bytes` | [types.py:105-145]() |
| `HttpResource` | HTTP endpoint data | `read() -> str\|bytes` | [types.py:148-159]() |
| `DirectoryResource` | Directory listings | `list_files() -> list[Path]` | [types.py:162-199]() |

**Sources:** [src/mcp/server/fastmcp/resources/types.py:1-200]()

### Function Resources and Templates

`FunctionResource` enables lazy loading by wrapping functions that return data only when accessed:

```mermaid
graph TB
    subgraph "FunctionResource Creation"
        F["Function Definition"] --> V["validate_call()"]
        V --> FR["FunctionResource Instance"]
    end
    
    subgraph "ResourceTemplate System"
        UT["uri_template: weather://{city}/current"] --> M["matches(uri)"]
        M --> P["Extract params: {city: 'london'}"]
        P --> CI["inject_context()"]
        CI --> FC["fn(**params)"]
        FC --> CR["create_resource()"]
    end
    
    subgraph "Runtime Execution"
        Client --> RM["ResourceManager.get_resource()"]
        RM --> RT["ResourceTemplate.create_resource()"]
        RT --> FR2["FunctionResource with closure"]
        FR2 --> Read["resource.read()"]
        Read --> Result["Data returned"]
    end
```

**Sources:** [src/mcp/server/fastmcp/resources/types.py:40-102](), [src/mcp/server/fastmcp/resources/templates.py:22-110]()

## Prompt Management System

The prompt system provides template-based message generation for LLM interactions with parameter validation and context injection.

### Prompt Architecture

```mermaid
classDiagram
    class Message {
        +role: "user"|"assistant"
        +content: ContentBlock
    }
    
    class UserMessage {
        +role: "user"
    }
    
    class AssistantMessage {
        +role: "assistant"
    }
    
    class PromptArgument {
        +name: str
        +description: str
        +required: bool
    }
    
    class Prompt {
        +name: str
        +title: str
        +description: str
        +arguments: list[PromptArgument]
        +fn: Callable
        +context_kwarg: str
        +from_function() Prompt
        +render() list[Message]
    }
    
    class PromptManager {
        +_prompts: dict[str, Prompt]
        +add_prompt() Prompt
        +get_prompt() Prompt
        +list_prompts() list[Prompt]
        +render_prompt() list[Message]
    }
    
    Message <|-- UserMessage
    Message <|-- AssistantMessage
    Prompt --> PromptArgument
    PromptManager --> Prompt
```

**Sources:** [src/mcp/server/fastmcp/prompts/base.py:22-184](), [src/mcp/server/fastmcp/prompts/manager.py:18-60]()

### Prompt Rendering Process

```mermaid
sequenceDiagram
    participant Client
    participant "PromptManager" as PM
    participant "Prompt" as P
    participant "func_metadata" as FM
    participant "Context" as CTX

    Note over PM: "Prompts registered via from_function()"
    
    Client->>PM: "render_prompt(name, arguments)"
    PM->>P: "get_prompt(name)"
    P->>P: "validate required arguments"
    P->>CTX: "inject_context(fn, arguments, context)"
    P->>P: "fn(**call_args)"
    
    alt "Function returns coroutine"
        P->>P: "await result"
    end
    
    P->>P: "Convert result to Message list"
    
    loop "For each result item"
        alt "isinstance(item, Message)"
            P->>P: "Add to messages"
        else "isinstance(item, dict)"
            P->>P: "message_validator.validate_python()"
        else "isinstance(item, str)"
            P->>P: "Create UserMessage with TextContent"
        else "Other types"
            P->>P: "JSON serialize and create Message"
        end
    end
    
    P->>Client: "list[Message]"
```

**Sources:** [src/mcp/server/fastmcp/prompts/base.py:137-183](), [src/mcp/server/fastmcp/prompts/manager.py:49-60]()

## Context Injection System

Both resources and prompts support context injection for accessing request-specific information during execution.

### Context Parameter Discovery

```mermaid
flowchart TD
    F["Function Definition"] --> TH["get_type_hints(fn)"]
    TH --> LP["Loop through parameters"]
    LP --> CT["Check if type is Context"]
    CT --> |"Yes"| RN["Return parameter name"]
    CT --> |"No"| GO["Check generic origin"]
    GO --> GA["Get type args"]
    GA --> CGA["Check if any arg is Context"]
    CGA --> |"Yes"| RN
    CGA --> |"No"| LP
    LP --> |"No more params"| RNone["Return None"]
```

**Sources:** [src/mcp/server/fastmcp/utilities/context_injection.py:11-46]()

### Integration Points

The context injection system integrates with both resource templates and prompts:

| Component | Context Usage | Implementation |
|-----------|---------------|----------------|
| `ResourceTemplate.create_resource()` | Access request context during resource creation | [templates.py:92-93]() |
| `Prompt.render()` | Access session/request context during rendering | [base.py:153]() |
| `inject_context()` | Generic context injection utility | [context_injection.py:49-68]() |

**Sources:** [src/mcp/server/fastmcp/resources/templates.py:84-110](), [src/mcp/server/fastmcp/prompts/base.py:137-183](), [src/mcp/server/fastmcp/utilities/context_injection.py:49-68]()

## Manager Registration and Lifecycle

Both `ResourceManager` and `PromptManager` provide registration APIs for adding resources and prompts to FastMCP servers:

### Resource Registration

```mermaid
graph LR
    subgraph "Resource Registration Methods"
        AR["add_resource(resource)"] --> R["_resources dict"]
        AT["add_template(fn, uri_template)"] --> T["_templates dict"]
    end
    
    subgraph "Resource Retrieval"
        GR["get_resource(uri, context)"] --> CR["Check _resources"]
        CR --> |"Found"| RET["Return resource"]
        CR --> |"Not found"| CT["Check _templates"]
        CT --> |"Match"| TR["template.create_resource()"]
        CT --> |"No match"| ERR["ValueError"]
    end
```

### Prompt Registration

The `PromptManager` maintains a simple dictionary mapping prompt names to `Prompt` instances, with optional duplicate warnings.

**Sources:** [src/mcp/server/fastmcp/resources/resource_manager.py:22-108](), [src/mcp/server/fastmcp/prompts/manager.py:18-60]()

# Function Introspection & Structured Output




This document explains how FastMCP automatically analyzes Python functions to generate JSON schemas for their arguments and return values, enabling automatic validation and structured output generation. This system allows FastMCP to seamlessly bridge between Python function signatures and the MCP protocol's JSON-based communication.

For information about how tools are registered and managed, see [Tool Management](#2.2). For details about the FastMCP server architecture, see [FastMCP Server Architecture](#2.1).

## Purpose and Scope

The function introspection system serves two primary purposes:

1. **Automatic Schema Generation**: Converts Python function signatures into JSON schemas that can be used by MCP clients to understand tool parameters
2. **Structured Output Support**: Enables tools to return structured data with schemas, allowing for richer client interactions

The system is built around the `func_metadata` function and `FuncMetadata` class, which analyze function signatures using Python's `inspect` module and Pydantic models to create validation and conversion pipelines.

## Function Introspection Architecture

The introspection system follows a pipeline from Python functions to validated execution:

```mermaid
graph TB
    subgraph "Function Analysis"
        Function["Python Function"]
        Signature["inspect.Signature"]
        TypeHints["Type Hints & Annotations"]
    end
    
    subgraph "Metadata Generation"
        FuncMetadata["FuncMetadata"]
        ArgModel["ArgModelBase (Pydantic)"]
        OutputModel["Output Model (Optional)"]
        JSONSchema["JSON Schema"]
    end
    
    subgraph "Runtime Processing"
        RawArgs["Raw Arguments (dict)"]
        PreParse["JSON Pre-parsing"]
        Validation["Pydantic Validation"]
        FunctionCall["Function Execution"]
        OutputConversion["Output Conversion"]
    end
    
    Function --> Signature
    Function --> TypeHints
    Signature --> FuncMetadata
    TypeHints --> FuncMetadata
    FuncMetadata --> ArgModel
    FuncMetadata --> OutputModel
    FuncMetadata --> JSONSchema
    
    RawArgs --> PreParse
    PreParse --> Validation
    ArgModel --> Validation
    Validation --> FunctionCall
    FunctionCall --> OutputConversion
    OutputModel --> OutputConversion
```

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:166-284](), [src/mcp/server/fastmcp/utilities/func_metadata.py:62-164]()

## Argument Model Generation

The `func_metadata` function creates Pydantic models from function signatures to enable automatic validation:

### Core Process

```mermaid
graph LR
    subgraph "Function Parameter Analysis"
        Params["Function Parameters"]
        TypeAnnotations["Type Annotations"]
        Defaults["Default Values"]
        FieldInfo["Pydantic FieldInfo"]
    end
    
    subgraph "Model Creation"
        ArgModelBase["ArgModelBase"]
        DynamicModel["create_model()"]
        ValidationModel["Validation Model"]
    end
    
    Params --> TypeAnnotations
    Params --> Defaults
    TypeAnnotations --> FieldInfo
    Defaults --> FieldInfo
    FieldInfo --> DynamicModel
    ArgModelBase --> DynamicModel
    DynamicModel --> ValidationModel
```

### Parameter Handling Rules

| Parameter Type | Treatment | Example |
|---------------|-----------|---------|
| Typed parameters | Direct mapping | `name: str` → `str` field |
| Untyped parameters | Mapped to `Any` with string schema | `value` → `Any` field |
| Parameters with `None` annotation | Mapped to null type | `x: None` → null field |
| Parameters starting with `_` | Rejected (raises `InvalidSignature`) | `_private: str` → Error |
| Parameters in `skip_names` | Excluded from model | Skipped entirely |
| BaseModel attribute conflicts | Uses aliases | `model_dump: str` → aliased field |

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:208-258](), [src/mcp/server/fastmcp/utilities/func_metadata.py:240-252]()

## Structured Output System

FastMCP supports structured output based on function return type annotations. The system automatically detects whether a function should return structured or unstructured output:

### Return Type Handling

```mermaid
graph TB
    subgraph "Return Type Analysis"
        ReturnAnnotation["Return Annotation"]
        StructuredOutputFlag["structured_output parameter"]
        TypeCheck["Type Analysis"]
    end
    
    subgraph "Model Creation Strategy"
        BaseModelDirect["BaseModel → Direct Use"]
        PrimitivesWrapped["Primitives → Wrapped in 'result'"]
        DictStrKeys["dict[str, T] → RootModel"]
        DictOtherKeys["dict[other, T] → Wrapped"]
        TypedDictConverted["TypedDict → Converted Model"]
        ClassWithHints["Annotated Class → Converted Model"]
        GenericTypesWrapped["Generic Types → Wrapped"]
        UnserializableNone["Unserializable → None"]
    end
    
    ReturnAnnotation --> TypeCheck
    StructuredOutputFlag --> TypeCheck
    TypeCheck --> BaseModelDirect
    TypeCheck --> PrimitivesWrapped
    TypeCheck --> DictStrKeys
    TypeCheck --> DictOtherKeys
    TypeCheck --> TypedDictConverted
    TypeCheck --> ClassWithHints
    TypeCheck --> GenericTypesWrapped
    TypeCheck --> UnserializableNone
```

### Structured Output Examples

| Return Type | Model Strategy | Schema Generation |
|-------------|---------------|-------------------|
| `str` | Wrapped as `{"result": str}` | Simple object schema |
| `BaseModel` | Used directly | Full model schema |
| `dict[str, int]` | RootModel for dict | Object with additionalProperties |
| `dict[int, str]` | Wrapped as `{"result": dict}` | Wrapped object schema |
| `TypedDict` | Converted to BaseModel | Object with typed properties |
| `list[str]` | Wrapped as `{"result": list}` | Array in wrapped object |
| Annotated class | Converted to BaseModel | Object with class fields |
| Unannotated class | No structured output | Returns None |

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:287-371](), [examples/snippets/servers/structured_output.py:1-98]()

## JSON Schema Generation

The system generates JSON schemas using Pydantic's schema generation with strict validation:

### Schema Generation Pipeline

```mermaid
graph LR
    subgraph "Schema Creation"
        OutputModel["Output Model"]
        StrictJsonSchema["StrictJsonSchema Generator"]
        SchemaDict["JSON Schema Dict"]
    end
    
    subgraph "Error Handling"
        ValidationErrors["Pydantic Errors"]
        SchemaErrors["Schema Generation Errors"] 
        FallbackToNone["Fallback to None"]
    end
    
    OutputModel --> StrictJsonSchema
    StrictJsonSchema --> SchemaDict
    StrictJsonSchema --> ValidationErrors
    ValidationErrors --> FallbackToNone
    SchemaErrors --> FallbackToNone
```

The `StrictJsonSchema` class raises exceptions instead of emitting warnings, allowing the system to detect non-serializable types and gracefully fall back to unstructured output.

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:30-38](), [src/mcp/server/fastmcp/utilities/func_metadata.py:355-371]()

## Input Validation & Pre-parsing

The validation system includes sophisticated JSON pre-parsing to handle common client behavior:

### Pre-parsing Logic

```mermaid
graph TB
    subgraph "Input Processing"
        RawInput["Raw Arguments Dict"]
        PreParseJSON["pre_parse_json()"]
        ModelValidation["Pydantic Validation"]
        ArgumentExtraction["model_dump_one_level()"]
    end
    
    subgraph "JSON Pre-parsing Rules"
        StringValue["String Value"]
        FieldAnnotation["Field Type Annotation"]
        JSONParseable["Valid JSON?"]
        ParsedValue["Parsed Value"]
        OriginalValue["Original String"]
    end
    
    RawInput --> PreParseJSON
    PreParseJSON --> ModelValidation
    ModelValidation --> ArgumentExtraction
    
    StringValue --> FieldAnnotation
    FieldAnnotation --> JSONParseable
    JSONParseable -->|Yes, Complex Type| ParsedValue
    JSONParseable -->|No or Simple Type| OriginalValue
```

### Pre-parsing Examples

| Input | Field Type | Pre-parsed Result | Reason |
|-------|-----------|-------------------|---------|
| `'["a", "b"]'` | `list[str]` | `["a", "b"]` | JSON array parsed |
| `'"hello"'` | `str` | `'"hello"'` | JSON string kept as string |
| `'{"x": 1}'` | `SomeModel` | `{"x": 1}` | JSON object parsed |
| `'123'` | `int` | `'123'` | Simple value kept as string |
| `'invalid'` | `list[str]` | `'invalid'` | Invalid JSON kept as string |

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:121-159](), [tests/server/fastmcp/test_func_metadata.py:463-552]()

## Output Conversion

The `convert_result` method handles converting function return values to the appropriate format for MCP responses:

### Conversion Flow

```mermaid
graph TB
    subgraph "Output Processing"
        FunctionResult["Function Return Value"]
        UnstructuredConversion["_convert_to_content()"]
        StructuredCheck["Has Output Schema?"]
        StructuredValidation["Output Model Validation"]
        BothFormats["(Unstructured, Structured)"]
        UnstructuredOnly["Unstructured Content Only"]
    end
    
    subgraph "Content Conversion"
        ContentBlock["ContentBlock → Direct"]
        ImageAudio["Image/Audio → Content"]
        ListTuple["List/Tuple → Flattened"]
        OtherTypes["Other → JSON + TextContent"]
    end
    
    FunctionResult --> UnstructuredConversion
    FunctionResult --> StructuredCheck
    UnstructuredConversion --> ContentBlock
    UnstructuredConversion --> ImageAudio
    UnstructuredConversion --> ListTuple
    UnstructuredConversion --> OtherTypes
    
    StructuredCheck -->|Yes| StructuredValidation
    StructuredCheck -->|No| UnstructuredOnly
    StructuredValidation --> BothFormats
```

### Content Conversion Rules

| Return Value Type | Conversion Result |
|------------------|-------------------|
| `None` | Empty list `[]` |
| `ContentBlock` | Single-item list `[ContentBlock]` |
| `Image` | `[ImageContent]` |
| `Audio` | `[AudioContent]` |
| `list/tuple` | Flattened list of converted items |
| Other types | JSON-serialized as `[TextContent]` |

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:91-119](), [src/mcp/server/fastmcp/utilities/func_metadata.py:489-523]()

## Integration with FastMCP

The function introspection system integrates seamlessly with FastMCP's tool registration:

```mermaid
graph LR
    subgraph "Tool Registration"
        ToolDecorator["@mcp.tool()"]
        FunctionAnalysis["func_metadata()"]
        ToolManager["ToolManager"]
    end
    
    subgraph "Runtime Execution"
        ClientCall["Client Tool Call"]
        ArgumentValidation["call_fn_with_arg_validation()"]
        FunctionExecution["Function Call"]
        ResultConversion["convert_result()"]
        MCPResponse["MCP Response"]
    end
    
    ToolDecorator --> FunctionAnalysis
    FunctionAnalysis --> ToolManager
    ClientCall --> ArgumentValidation
    ArgumentValidation --> FunctionExecution
    FunctionExecution --> ResultConversion
    ResultConversion --> MCPResponse
```

This system enables FastMCP to provide rich, type-safe tool interfaces while maintaining compatibility with the MCP protocol's JSON-based communication model.

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:68-89](), [tests/server/fastmcp/test_integration.py:666-700]()