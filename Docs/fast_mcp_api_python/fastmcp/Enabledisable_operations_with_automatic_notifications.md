def enable(self) -> None:
    super().enable()
    try:
        context = get_context()
        context._queue_tool_list_changed()  # Notify protocol
    except RuntimeError:
        pass  # No context available

def disable(self) -> None:
    super().disable()
    # Similar notification logic
```

This ensures that MCP clients receive updated component lists when components are dynamically enabled or disabled.

**Sources**: [src/fastmcp/tools/tool.py:123-137](), [src/fastmcp/resources/resource.py:53-67](), [src/fastmcp/prompts/prompt.py:72-86](), [src/fastmcp/resources/template.py:72-86]()

# Context System and Dependencies




This section covers the Context object system and dependency injection mechanisms in FastMCP. The `Context` class provides tools and resources with access to MCP protocol capabilities like logging, sampling, and resource reading, while the dependency injection system automatically provides these capabilities to user functions based on type annotations.

For information about how components (tools, resources, prompts) are created and managed, see [Component System Architecture](#2.1). For details about server composition and mounting, see [Server Composition and Proxying](#2.3).

## Context Object Architecture

The `Context` class serves as the primary interface between user-defined tools/resources and the underlying MCP protocol capabilities. It provides a clean, Pythonic API for accessing server session functionality.

```mermaid
graph TB
    subgraph "Context Object Structure"
        Context["Context<br/>- fastmcp: weakref[FastMCP]<br/>- _tokens: list[Token]<br/>- _notification_queue: set[str]<br/>- _state: dict[str, Any]"]
        
        subgraph "MCP Protocol Access"
            RequestContext["RequestContext<br/>- request_id<br/>- session<br/>- meta<br/>- request"]
            ServerSession["ServerSession<br/>- send_log_message()<br/>- send_progress_notification()<br/>- create_message()<br/>- elicit()"]
        end
        
        subgraph "Context Capabilities"
            Logging["Logging Methods<br/>- log()<br/>- debug()<br/>- info()<br/>- warning()<br/>- error()"]
            Progress["Progress Reporting<br/>- report_progress()"]
            Sampling["AI Sampling<br/>- sample()<br/>- elicit()"]
            Resources["Resource Access<br/>- read_resource()<br/>- list_roots()"]
            State["State Management<br/>- set_state()<br/>- get_state()"]
            Notifications["Notifications<br/>- send_tool_list_changed()<br/>- send_resource_list_changed()<br/>- send_prompt_list_changed()"]
        end
    end
    
    Context --> RequestContext
    RequestContext --> ServerSession
    Context --> Logging
    Context --> Progress
    Context --> Sampling
    Context --> Resources
    Context --> State
    Context --> Notifications
```

**Sources:** [src/fastmcp/server/context.py:79-123](), [src/fastmcp/server/context.py:159-169]()

### Context Lifecycle Management

The `Context` object implements async context manager semantics with inheritance-based state management:

```mermaid
graph TD
    subgraph "Context Lifecycle"
        ContextVar["_current_context: ContextVar[Context | None]"]
        ParentContext["Parent Context<br/>with state"]
        ChildContext["Child Context<br/>inherits parent state"]
        TokenManagement["Token Management<br/>_tokens: list[Token]"]
    end
    
    subgraph "State Inheritance"
        ParentState["Parent State<br/>{key1: value1, key2: value2}"]
        CopiedState["Copied State<br/>copy.deepcopy(parent._state)"]
        ChildState["Child State<br/>{key1: value1, key2: value2, key3: value3}"]
    end
    
    ContextVar --> ParentContext
    ParentContext --> ChildContext
    ParentState --> CopiedState
    CopiedState --> ChildState
    ChildContext --> TokenManagement
```

**Sources:** [src/fastmcp/server/context.py:53](), [src/fastmcp/server/context.py:138-157](), [src/fastmcp/server/context.py:584-590]()

## Dependency Injection System

FastMCP uses type annotation-based dependency injection to automatically provide `Context` objects and other dependencies to user functions.

```mermaid
graph LR
    subgraph "User Function"
        UserFunction["@server.tool<br/>async def my_tool(x: int, ctx: Context) -> str"]
        TypeHints["Function Annotations<br/>x: int<br/>ctx: Context"]
    end
    
    subgraph "Type Analysis"
        FindKwargByType["find_kwarg_by_type()<br/>Inspect function signature<br/>Match Context type"]
        TypeHints2["get_type_hints()<br/>include_extras=True<br/>Handle forward refs"]
        IsClassMember["is_class_member_of_type()<br/>Handle Union, Annotated"]
    end
    
    subgraph "Injection Process"
        ContextInjection["Context Injection<br/>Provide current context<br/>as 'ctx' parameter"]
        FunctionCall["Function Execution<br/>my_tool(x=5, ctx=context)"]
    end
    
    UserFunction --> TypeHints
    TypeHints --> FindKwargByType
    FindKwargByType --> TypeHints2
    TypeHints2 --> IsClassMember
    IsClassMember --> ContextInjection
    ContextInjection --> FunctionCall
```

**Sources:** [src/fastmcp/utilities/types.py:152-176](), [src/fastmcp/utilities/types.py:130-149]()

### Type Annotation Processing

The system handles complex type annotations including unions, forward references, and `Annotated` types:

| Type Pattern | Example | Processing |
|--------------|---------|------------|
| Direct Type | `ctx: Context` | Direct match via `issubclass_safe()` |
| Union Type | `ctx: Context \| None` | Check each union member |
| Annotated Type | `ctx: Annotated[Context, "description"]` | Extract base type from first argument |
| Forward Reference | `ctx: "Context"` | Resolve via `get_type_hints()` |

**Sources:** [src/fastmcp/utilities/types.py:120-128](), [src/fastmcp/utilities/types.py:54-117]()

## MCP Capabilities Access

The `Context` object provides access to core MCP protocol capabilities through a clean interface:

### Logging and Progress

```mermaid
graph TB
    subgraph "Logging System"
        LogMethods["Context Log Methods<br/>- debug(), info(), warning(), error()<br/>- log(message, level, logger_name, extra)"]
        LogData["LogData<br/>- msg: str<br/>- extra: Mapping[str, Any] | None"]
        SessionLog["session.send_log_message()<br/>- level: LoggingLevel<br/>- data: LogData<br/>- related_request_id"]
    end
    
    subgraph "Progress Reporting"
        ReportProgress["report_progress()<br/>- progress: float<br/>- total: float | None<br/>- message: str | None"]
        ProgressToken["request_context.meta.progressToken"]
        SessionProgress["session.send_progress_notification()"]
    end
    
    LogMethods --> LogData
    LogData --> SessionLog
    ReportProgress --> ProgressToken
    ProgressToken --> SessionProgress
```

**Sources:** [src/fastmcp/server/context.py:57-67](), [src/fastmcp/server/context.py:210-234](), [src/fastmcp/server/context.py:170-195]()

### AI Sampling and Elicitation

```mermaid
graph TB
    subgraph "Sampling System"
        SampleMethod["sample()<br/>- messages: str | Sequence[SamplingMessage]<br/>- system_prompt, temperature, max_tokens<br/>- model_preferences"]
        SamplingFallback["Sampling Handler Fallback<br/>- fastmcp.sampling_handler<br/>- behavior: 'always' | 'fallback'"]
        CreateMessage["session.create_message()<br/>Returns: CreateMessageResult"]
    end
    
    subgraph "Elicitation System"
        ElicitMethod["elicit()<br/>- message: str<br/>- response_type: type[T] | list[str] | None"]
        SchemaGeneration["get_elicitation_schema()<br/>Handle primitives, dataclasses, enums"]
        ElicitResult["AcceptedElicitation[T]<br/>DeclinedElicitation<br/>CancelledElicitation"]
    end
    
    SampleMethod --> SamplingFallback
    SamplingFallback --> CreateMessage
    ElicitMethod --> SchemaGeneration
    SchemaGeneration --> ElicitResult
```

**Sources:** [src/fastmcp/server/context.py:361-442](), [src/fastmcp/server/context.py:444-567]()

### Session and Resource Management

```mermaid
graph TB
    subgraph "Session Management"
        SessionId["session_id Property<br/>- HTTP headers: mcp-session-id<br/>- Generated UUID fallback<br/>- Cached on session._fastmcp_id"]
        ClientId["client_id Property<br/>request_context.meta.client_id"]
        RequestId["request_id Property<br/>str(request_context.request_id)"]
    end
    
    subgraph "Resource Access"
        ReadResource["read_resource(uri)<br/>- str | AnyUrl parameter<br/>- Returns: list[ReadResourceContents]"]
        ListRoots["list_roots()<br/>- Returns: list[Root]<br/>- Client-provided root directories"]
        FastMCPRead["fastmcp._mcp_read_resource()<br/>Delegate to server implementation"]
    end
    
    SessionId --> ClientId
    ClientId --> RequestId
    ReadResource --> FastMCPRead
    ListRoots --> FastMCPRead
```

**Sources:** [src/fastmcp/server/context.py:250-292](), [src/fastmcp/server/context.py:197-208](), [src/fastmcp/server/context.py:344-347]()

## State Management

The Context system provides request-scoped state management with inheritance semantics:

```mermaid
graph TD
    subgraph "State Architecture"
        ContextState["Context._state: dict[str, Any]<br/>Per-context state storage"]
        SetState["set_state(key: str, value: Any)<br/>Store value in current context"]
        GetState["get_state(key: str) -> Any<br/>Retrieve value or None"]
    end
    
    subgraph "Inheritance Flow"
        ParentCtx["Parent Context<br/>state = {a: 1, b: 2}"]
        ChildCtx["Child Context<br/>state = copy.deepcopy(parent._state)"]
        ChildMod["Child Modifications<br/>state = {a: 1, b: 2, c: 3}"]
        ParentUnchanged["Parent Unchanged<br/>state = {a: 1, b: 2}"]
    end
    
    ContextState --> SetState
    ContextState --> GetState
    ParentCtx --> ChildCtx
    ChildCtx --> ChildMod
    ChildMod --> ParentUnchanged
```

**Sources:** [src/fastmcp/server/context.py:113-117](), [src/fastmcp/server/context.py:140-144](), [tests/server/test_context.py:134-180]()

## Type System Integration

FastMCP's type system supports the Context dependency injection through several utility functions:

### Type Adapter Caching

```mermaid
graph LR
    subgraph "TypeAdapter Creation"
        GetCachedAdapter["get_cached_typeadapter(cls)<br/>@lru_cache(maxsize=5000)"]
        AnnotationProcess["Process Annotations<br/>Annotated[Type, 'string'] →<br/>Annotated[Type, Field(description='string')]"]
        TypeAdapterCreate["TypeAdapter(processed_function)<br/>Heavy object creation<br/>Cached for reuse"]
    end
    
    subgraph "Function Processing"
        GetTypeHints["get_type_hints(include_extras=True)<br/>Resolve forward references"]
        ProcessHints["Process Annotations<br/>Handle string descriptions"]
        NewFunction["Create New Function<br/>With processed annotations"]
    end
    
    GetCachedAdapter --> AnnotationProcess
    AnnotationProcess --> GetTypeHints
    GetTypeHints --> ProcessHints
    ProcessHints --> NewFunction
    NewFunction --> TypeAdapterCreate
```

**Sources:** [src/fastmcp/utilities/types.py:44-117](), [tests/utilities/test_types.py:624-695]()

### Helper Type Classes

FastMCP provides helper classes for common content types that integrate with the Context system:

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `Image` | Image content handling | `to_image_content()` → `ImageContent` |
| `Audio` | Audio content handling | `to_audio_content()` → `AudioContent` |
| `File` | File resource handling | `to_resource_content()` → `EmbeddedResource` |

**Sources:** [src/fastmcp/utilities/types.py:178-379](), [examples/get_file.py:4](), [examples/get_file.py:15](), [examples/get_file.py:27]()

### Type Replacement System

```mermaid
graph TB
    subgraph "Type Transformation"
        ReplaceType["replace_type(type_, type_map)<br/>Transform complex types"]
        GetOrigin["get_origin(type_)<br/>Extract generic origin"]
        GetArgs["get_args(type_)<br/>Extract type arguments"]
        Recursive["Recursive Processing<br/>Handle nested generics"]
    end
    
    subgraph "Supported Patterns"
        UnionType["UnionType | typing.Union<br/>Handle both syntaxes"]
        AnnotatedType["Annotated[T, ...]<br/>Process first argument"]
        GenericType["list[T], dict[K, V]<br/>Process all arguments"]
    end
    
    ReplaceType --> GetOrigin
    GetOrigin --> GetArgs
    GetArgs --> Recursive
    UnionType --> ReplaceType
    AnnotatedType --> ReplaceType
    GenericType --> ReplaceType
```

**Sources:** [src/fastmcp/utilities/types.py:381-415](), [tests/utilities/test_types.py:598-622]()