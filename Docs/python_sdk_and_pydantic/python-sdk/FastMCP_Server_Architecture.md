This document explains the internal architecture of the FastMCP server framework, including its core components, managers, function introspection system, and transport integration. FastMCP provides a high-level, decorator-based interface for building MCP servers that automatically handles schema generation, validation, and protocol compliance.

For information about using FastMCP decorators and APIs, see [Tool Management](#2.2) and [Resource & Prompt Management](#2.3). For details about the underlying protocol implementation, see [Low-Level Server Architecture](#6.1).

## Core Architecture Overview

FastMCP implements a layered architecture that wraps the low-level MCP server with higher-level abstractions and automatic introspection capabilities.

```mermaid
graph TB
    subgraph "FastMCP Framework Layer"
        FastMCP["FastMCP<br/>Main Server Class"]
        ToolManager["ToolManager<br/>Tool Registration & Execution"]
        ResourceManager["ResourceManager<br/>Resource & Template Management"]
        PromptManager["PromptManager<br/>Prompt Management"]
        FuncMetadata["func_metadata<br/>Function Introspection"]
        Context["Context<br/>Request Context Injection"]
    end
    
    subgraph "Protocol Layer"
        MCPServer["MCPServer<br/>Low-level Protocol Handler"]
        ServerSession["ServerSession<br/>Client Session Management"]
    end
    
    subgraph "Transport Layer"
        StdioTransport["stdio_server<br/>Standard I/O"]
        SSETransport["SseServerTransport<br/>Server-Sent Events"]
        StreamableHTTP["StreamableHTTPSessionManager<br/>HTTP Sessions"]
    end
    
    subgraph "Function Processing"
        ArgModelBase["ArgModelBase<br/>Pydantic Input Models"]
        OutputValidation["Output Schema Validation<br/>Structured Output"]
        ContentConversion["_convert_to_content<br/>Result Conversion"]
    end
    
    %% Core relationships
    FastMCP --> ToolManager
    FastMCP --> ResourceManager
    FastMCP --> PromptManager
    FastMCP --> MCPServer
    
    ToolManager --> FuncMetadata
    ResourceManager --> FuncMetadata
    PromptManager --> FuncMetadata
    
    FuncMetadata --> ArgModelBase
    FuncMetadata --> OutputValidation
    FuncMetadata --> ContentConversion
    
    FastMCP --> Context
    Context -.-> ServerSession
    
    %% Protocol integration
    MCPServer --> ServerSession
    
    %% Transport integration
    FastMCP -.-> StdioTransport
    FastMCP -.-> SSETransport
    FastMCP -.-> StreamableHTTP
    
    MCPServer -.-> StdioTransport
    MCPServer -.-> SSETransport
    MCPServer -.-> StreamableHTTP
```

**Sources:** [src/mcp/server/fastmcp/server.py:122-206](), [src/mcp/server/fastmcp/utilities/func_metadata.py:62-67]()

## FastMCP Main Server Class

The `FastMCP` class serves as the primary entry point and orchestrator for the entire server framework. It manages settings, coordinates managers, and provides the decorator interface.

### Core Components

The `FastMCP` class initializes and coordinates several key subsystems:

- **Settings Management**: Uses `Settings` class with environment variable support (prefix `FASTMCP_`)
- **Manager Coordination**: Initializes `ToolManager`, `ResourceManager`, and `PromptManager`
- **Protocol Integration**: Wraps the low-level `MCPServer` with enhanced functionality
- **Transport Apps**: Generates transport-specific applications (stdio, SSE, StreamableHTTP)

```mermaid
graph LR
    subgraph "FastMCP.__init__"
        Settings["Settings<br/>Configuration Management"]
        MCPServerWrap["MCPServer Wrapper<br/>Low-level Protocol"]
        ManagerInit["Manager Initialization<br/>Tool/Resource/Prompt"]
        AuthConfig["Authentication Setup<br/>OAuth Integration"]
        HandlerSetup["Protocol Handler Setup<br/>MCP Method Bindings"]
    end
    
    Settings --> MCPServerWrap
    MCPServerWrap --> ManagerInit
    ManagerInit --> AuthConfig
    AuthConfig --> HandlerSetup
    
    HandlerSetup --> list_tools
    HandlerSetup --> call_tool
    HandlerSetup --> list_resources
    HandlerSetup --> read_resource
    HandlerSetup --> list_prompts
    HandlerSetup --> get_prompt
```

**Sources:** [src/mcp/server/fastmcp/server.py:152-209](), [src/mcp/server/fastmcp/server.py:268-280]()

### Decorator Interface

FastMCP provides three primary decorators that automatically handle function registration and introspection:

| Decorator | Manager | Purpose |
|-----------|---------|---------|
| `@tool()` | `ToolManager` | Register functions as callable tools |
| `@resource()` | `ResourceManager` | Register functions as resources or templates |
| `@prompt()` | `PromptManager` | Register functions as prompt generators |

Each decorator uses the same underlying pattern: function introspection → manager registration → protocol handler binding.

**Sources:** [src/mcp/server/fastmcp/server.py:393-451](), [src/mcp/server/fastmcp/server.py:479-578](), [src/mcp/server/fastmcp/server.py:588-641]()

## Manager Subsystem Architecture

The manager subsystem handles registration, validation, and execution of user-defined functions through a consistent interface pattern.

```mermaid
graph TB
    subgraph "Manager Pattern"
        Registration["Function Registration<br/>add_tool/add_resource/add_prompt"]
        Introspection["Function Introspection<br/>func_metadata()"]
        Storage["Internal Storage<br/>_tools/_resources/_prompts"]
        Execution["Function Execution<br/>call_tool/get_resource/get_prompt"]
    end
    
    subgraph "ToolManager"
        ToolStorage["_tools: dict[str, Tool]"]
        ToolValidation["Input/Output Validation"]
        ToolExecution["Tool Execution with Context"]
    end
    
    subgraph "ResourceManager"
        ResourceStorage["_resources: dict[str, Resource]"]
        TemplateStorage["_templates: dict[str, ResourceTemplate]"]
        ResourceResolution["URI to Resource Resolution"]
    end
    
    subgraph "PromptManager"
        PromptStorage["_prompts: dict[str, Prompt]"]
        PromptValidation["Argument Validation"]
        PromptExecution["Message Generation"]
    end
    
    Registration --> Introspection
    Introspection --> Storage
    Storage --> Execution
    
    Registration -.-> ToolStorage
    Registration -.-> ResourceStorage
    Registration -.-> PromptStorage
```

**Sources:** [src/mcp/server/fastmcp/tools.py](), [src/mcp/server/fastmcp/resources.py](), [src/mcp/server/fastmcp/prompts.py]()

### Function Registration Flow

All managers follow a consistent registration pattern:

1. **Function Analysis**: Extract signature, docstring, and type annotations
2. **Schema Generation**: Create Pydantic models for inputs and outputs
3. **Metadata Creation**: Build `Tool`, `Resource`, or `Prompt` objects
4. **Storage**: Register in manager's internal dictionary
5. **Validation**: Check for duplicates and conflicts

**Sources:** [src/mcp/server/fastmcp/utilities/func_metadata.py:166-284]()

## Function Introspection System

The function introspection system (`func_metadata`) is the core of FastMCP's automatic schema generation and validation capabilities.

### FuncMetadata Components

```mermaid
graph LR
    subgraph "FuncMetadata Structure"
        ArgModel["arg_model<br/>ArgModelBase subclass"]
        OutputSchema["output_schema<br/>JSON Schema dict"]
        OutputModel["output_model<br/>Pydantic Model"]
        WrapOutput["wrap_output<br/>Result Wrapping Flag"]
    end
    
    subgraph "Input Processing"
        PreParse["pre_parse_json<br/>JSON String Handling"]
        Validation["model_validate<br/>Pydantic Validation"]
        Injection["Context Injection<br/>arguments_to_pass_directly"]
    end
    
    subgraph "Output Processing"
        ResultConvert["convert_result<br/>Result Conversion"]
        ContentConvert["_convert_to_content<br/>ContentBlock Generation"]
        StructuredOut["Structured Output<br/>Schema Validation"]
    end
    
    ArgModel --> PreParse
    PreParse --> Validation
    Validation --> Injection
    
    OutputModel --> ResultConvert
    ResultConvert --> ContentConvert
    ResultConvert --> StructuredOut
```

**Sources:** [src/mcp/server/fastmcp/utilities/func_metadata.py:62-120]()

### Structured Output Detection

FastMCP automatically determines whether a function should have structured output based on its return type annotation:

| Return Type | Output Handling | Wrapping |
|-------------|-----------------|----------|
| `BaseModel` subclass | Direct schema generation | No wrapping |
| Primitive types (`str`, `int`, etc.) | Wrapped in `{"result": value}` | Yes |
| `dict[str, T]` | RootModel generation | No wrapping |
| Generic types (`list[T]`, `Union`) | Wrapped in `{"result": value}` | Yes |
| Unannotated classes | No structured output | N/A |

**Sources:** [src/mcp/server/fastmcp/utilities/func_metadata.py:287-371]()

## Context Injection System

FastMCP provides automatic context injection that gives functions access to request-specific information and MCP capabilities.

```mermaid
graph TB
    subgraph "Context Object"
        RequestContext["request_context<br/>RequestContext[ServerSession]"]
        FastMCPRef["fastmcp<br/>FastMCP Instance"]
        ContextMethods["info/debug/error<br/>Logging Methods"]
        ProgressMethods["report_progress<br/>Progress Reporting"]
        ResourceMethods["read_resource<br/>Resource Access"]
    end
    
    subgraph "Context Detection"
        ParamAnalysis["find_context_parameter<br/>Parameter Analysis"]
        TypeCheck["Context Type Annotation<br/>Detection"]
        Injection["Automatic Injection<br/>During Function Call"]
    end
    
    subgraph "Context Usage"
        UserFunction["@tool/@resource/@prompt<br/>User Functions"]
        ContextParam["ctx: Context<br/>Parameter"]
        MCPCapabilities["MCP Protocol Access<br/>via Context"]
    end
    
    ParamAnalysis --> TypeCheck
    TypeCheck --> Injection
    Injection --> RequestContext
    
    ContextParam --> UserFunction
    UserFunction --> MCPCapabilities
    MCPCapabilities -.-> ContextMethods
    MCPCapabilities -.-> ProgressMethods
    MCPCapabilities -.-> ResourceMethods
```

**Sources:** [src/mcp/server/fastmcp/utilities/context_injection.py](), [src/mcp/shared/context.py]()

## Transport Integration Architecture

FastMCP integrates with multiple transport protocols by generating transport-specific ASGI applications that wrap the core MCP server functionality.

```mermaid
graph TB
    subgraph "Transport Applications"
        StdioApp["run_stdio_async<br/>Direct Process Communication"]
        SSEApp["sse_app<br/>Starlette ASGI Application"]
        StreamableApp["streamable_http_app<br/>Session-based HTTP"]
    end
    
    subgraph "Transport Components"
        StdioServer["stdio_server<br/>Stream Handler"]
        SseTransport["SseServerTransport<br/>SSE Protocol Handler"]
        SessionManager["StreamableHTTPSessionManager<br/>Session Management"]
    end
    
    subgraph "Protocol Handlers"
        MCPServerCore["MCPServer.run<br/>Core Protocol Loop"]
        RequestHandling["MCP Request Processing<br/>JSON-RPC over Transport"]
        ResponseHandling["MCP Response Generation<br/>Protocol Compliance"]
    end
    
    StdioApp --> StdioServer
    SSEApp --> SseTransport
    StreamableApp --> SessionManager
    
    StdioServer --> MCPServerCore
    SseTransport --> MCPServerCore
    SessionManager --> MCPServerCore
    
    MCPServerCore --> RequestHandling
    RequestHandling --> ResponseHandling
```

**Sources:** [src/mcp/server/fastmcp/server.py:687-725](), [src/mcp/server/fastmcp/server.py:752-884](), [src/mcp/server/fastmcp/server.py:885-984]()

### Transport Application Generation

Each transport type requires different ASGI application structure:

1. **stdio**: Direct async function for process communication
2. **SSE**: Starlette app with GET/POST endpoints and optional authentication
3. **StreamableHTTP**: Session-managed app with resumable connections

The `FastMCP` class generates these applications on-demand, configuring middleware, authentication, and routing based on server settings.

**Sources:** [src/mcp/server/fastmcp/server.py:752-883]()

## Request Processing Flow

The following diagram shows how requests flow through the FastMCP architecture from transport to function execution:

```mermaid
sequenceDiagram
    participant Transport as "Transport Layer"
    participant MCPServer as "MCPServer"
    participant FastMCP as "FastMCP"
    participant Manager as "Manager"
    participant FuncMeta as "func_metadata"
    participant UserFunc as "User Function"
    
    Transport->>MCPServer: "JSON-RPC Request"
    MCPServer->>FastMCP: "call_tool/read_resource/get_prompt"
    FastMCP->>Manager: "call_tool/get_resource/get_prompt"
    Manager->>FuncMeta: "call_fn_with_arg_validation"
    
    FuncMeta->>FuncMeta: "pre_parse_json"
    FuncMeta->>FuncMeta: "model_validate (ArgModel)"
    FuncMeta->>UserFunc: "Function Call + Context Injection"
    UserFunc->>FuncMeta: "Return Value"
    
    FuncMeta->>FuncMeta: "convert_result"
    FuncMeta->>Manager: "ContentBlock[] + Structured Output"
    Manager->>FastMCP: "Tool/Resource/Prompt Result"
    FastMCP->>MCPServer: "MCP Response Object"
    MCPServer->>Transport: "JSON-RPC Response"
```

**Sources:** [src/mcp/server/fastmcp/server.py:308-312](), [src/mcp/server/fastmcp/utilities/func_metadata.py:68-89]()

This architecture enables FastMCP to provide a high-level, decorator-based interface while maintaining full compatibility with the MCP protocol and supporting multiple transport mechanisms.

# Tool Management




FastMCP's tool management system enables developers to register Python functions as MCP tools using the `@tool` decorator and execute them through the `ToolManager`. The system automatically handles argument validation, context injection, and structured output generation.

The tool management system consists of three main components: the `ToolManager` for centralized tool registration and execution, the `Tool` class for wrapping functions with metadata, and the `FuncMetadata` system for function introspection and validation.

## Tool Registration with @tool Decorator

Tools are registered using the `@tool` decorator, which automatically converts Python functions into MCP tools. The decorator analyzes function signatures, creates validation schemas, and registers the tool with the `ToolManager`.

### Tool Registration Flow

```mermaid
flowchart TD
    decorator["@app.tool"] --> add_tool["ToolManager.add_tool()"]
    add_tool --> Tool_from_function["Tool.from_function()"]
    
    Tool_from_function --> func_metadata_call["func_metadata()"]
    Tool_from_function --> context_detection["find_context_parameter()"]
    
    func_metadata_call --> FuncMetadata["FuncMetadata"]
    context_detection --> context_kwarg["context_kwarg"]
    
    FuncMetadata --> arg_model["ArgModelBase"]
    FuncMetadata --> output_schema["output_schema"]
    FuncMetadata --> parameters["JSON Schema"]
    
    arg_model --> Tool["Tool instance"]
    output_schema --> Tool
    parameters --> Tool
    context_kwarg --> Tool
    
    Tool --> registration["Store in ToolManager._tools"]
```

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:45-71](), [src/mcp/server/fastmcp/tools/base.py:42-84]()

### Function Metadata Extraction

The `func_metadata()` function performs deep introspection of Python functions to extract type information and create validation models.

```mermaid
flowchart TD
    PythonFunc["Python Function"] --> func_metadata["func_metadata()"]
    func_metadata --> FuncMetadata["FuncMetadata"]
    
    FuncMetadata --> arg_model["arg_model: ArgModelBase"]
    FuncMetadata --> output_schema["output_schema: dict | None"]
    FuncMetadata --> output_model["output_model: BaseModel | None"]
    FuncMetadata --> wrap_output["wrap_output: bool"]
    
    arg_model --> call_fn_with_arg_validation["call_fn_with_arg_validation()"]
    output_schema --> convert_result["convert_result()"]
```

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:166-207]()

The `func_metadata()` function performs deep introspection of Python functions to create a `FuncMetadata` object containing:

- **arg_model**: A Pydantic model representing function arguments with validation
- **output_schema**: JSON schema for structured output (if enabled)
- **output_model**: Pydantic model for return type validation
- **wrap_output**: Whether to wrap primitive returns in `{"result": value}`

### Argument Processing Pipeline

The `FuncMetadata.call_fn_with_arg_validation()` method processes raw arguments through validation and type conversion before function execution.

```mermaid
flowchart LR
    RawArgs["Raw Arguments\n{\"key\": \"value\"}"] --> pre_parse_json["pre_parse_json()"]
    pre_parse_json --> ParsedArgs["Parsed Arguments\n{\"key\": parsed_value}"]
    ParsedArgs --> model_validate["arg_model.model_validate()"]
    model_validate --> ValidatedModel["ArgModelBase instance"]
    ValidatedModel --> model_dump_one_level["model_dump_one_level()"]
    model_dump_one_level --> FunctionKwargs["Function kwargs\nready for execution"]
```

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:68-89](), [src/mcp/server/fastmcp/utilities/func_metadata.py:121-159](), [src/mcp/server/fastmcp/utilities/func_metadata.py:44-55]()

**Argument Processing Features:**

| Stage | Implementation | Purpose | Example |
|-------|---------------|---------|---------|
| JSON Pre-parsing | `pre_parse_json()` | Parse JSON strings to Python objects | `"[1,2,3]"` → `[1,2,3]` |
| Type Validation | `arg_model.model_validate()` | Validate against Pydantic model | `str` parameter rejects `int` |
| Alias Resolution | `model_dump_one_level()` | Map aliases to parameter names | Field aliases → function parameter names |
| Default Handling | Pydantic `Field()` | Apply default values | Optional parameters get defaults |
| Complex Types | Nested model support | Handle complex structures | `BaseModel`, `TypedDict`, dataclasses |

**JSON Pre-parsing Logic:**

The `pre_parse_json()` method handles cases where MCP clients send complex data as JSON strings instead of native types:

```mermaid
flowchart TD
    input_data["Input data"] --> check_value{"Value is string AND\nfield type is not str?"}
    check_value -->|No| keep_original["Keep original value"]
    check_value -->|Yes| try_json_parse["json.loads(value)"]
    try_json_parse --> parse_success{"Parse successful?"}
    parse_success -->|No| keep_original
    parse_success -->|Yes| check_primitive{"Result is primitive\n(str, int, float)?"}
    check_primitive -->|Yes| keep_original["Keep original string"]
    check_primitive -->|No| use_parsed["Use parsed object"]
```

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:121-159]()

## Tool Registration System

Tools are registered through the `Tool` class and the `@mcp.tool` decorator, which provides a high-level interface for function-to-tool conversion.

### Tool Class Structure

The `Tool` class encapsulates all information needed to execute a function as an MCP tool, including metadata, validation models, and execution logic.

```mermaid
classDiagram
    class ToolManager {
        +_tools: dict[str, Tool]
        +warn_on_duplicate_tools: bool
        +add_tool(fn) Tool
        +get_tool(name) Tool
        +list_tools() list[Tool]
        +call_tool(name, args) Any
    }
    
    class Tool {
        +fn: Callable
        +name: str
        +title: str | None
        +description: str
        +parameters: dict
        +fn_metadata: FuncMetadata
        +is_async: bool
        +context_kwarg: str | None
        +annotations: ToolAnnotations
        +from_function() Tool
        +run(arguments, context) Any
    }
    
    class FuncMetadata {
        +arg_model: type[ArgModelBase]
        +output_schema: dict | None
        +output_model: type[BaseModel] | None
        +wrap_output: bool
        +call_fn_with_arg_validation()
        +convert_result()
        +pre_parse_json()
    }
    
    class ArgModelBase {
        +model_dump_one_level() dict
        +model_config: ConfigDict
    }
    
    ToolManager --> Tool : manages
    Tool --> FuncMetadata : contains
    FuncMetadata --> ArgModelBase : creates
```

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:19-35](), [src/mcp/server/fastmcp/tools/base.py:22-39](), [src/mcp/server/fastmcp/utilities/func_metadata.py:62-66]()

### Tool Creation Process

The `Tool.from_function()` method creates a `Tool` instance from a Python function by extracting metadata and creating validation schemas.

```mermaid
flowchart TD
    fn["Python Function"] --> from_function["Tool.from_function()"]
    from_function --> extract_name["Extract function name"]
    from_function --> extract_doc["Extract docstring"]
    from_function --> is_async_check["_is_async_callable()"]
    from_function --> find_context["find_context_parameter()"]
    from_function --> func_metadata_call["func_metadata()"]
    
    extract_name --> func_name["name: str"]
    extract_doc --> func_doc["description: str"]
    is_async_check --> is_async["is_async: bool"]
    find_context --> context_kwarg["context_kwarg: str | None"]
    func_metadata_call --> func_arg_metadata["FuncMetadata"]
    
    func_arg_metadata --> parameters["parameters: dict"]
    
    func_name --> Tool_instance["Tool()"]
    func_doc --> Tool_instance
    is_async --> Tool_instance
    context_kwarg --> Tool_instance
    func_arg_metadata --> Tool_instance
    parameters --> Tool_instance
```

Sources: [src/mcp/server/fastmcp/tools/base.py:42-84]()

### Context Parameter Detection and Injection

The system automatically detects `Context` parameters in function signatures and excludes them from the tool schema while injecting them during execution.

**Context Detection in find_context_parameter():**

```mermaid
flowchart TD
    function_signature["Function Signature"] --> find_context_parameter["find_context_parameter()"]
    find_context_parameter --> scan_params["Scan parameters"]
    scan_params --> check_annotation["Check param.annotation"]
    check_annotation --> is_context_type{"Type is Context?"}
    is_context_type -->|Yes| return_param_name["return param.name"]
    is_context_type -->|No| continue_scan["Continue scanning"]
    continue_scan --> next_param["Next parameter"]
    next_param --> check_annotation
    return_param_name --> context_kwarg["context_kwarg: str"]
```

**Context Injection During Execution:**

```mermaid
flowchart TD
    tool_run["Tool.run()"] --> has_context_kwarg{"self.context_kwarg is not None?"}
    has_context_kwarg -->|Yes| create_context_dict["{self.context_kwarg: context}"]
    has_context_kwarg -->|No| no_context_args["arguments_to_pass_directly = None"]
    create_context_dict --> call_with_context["call_fn_with_arg_validation(..., arguments_to_pass_directly)"]
    no_context_args --> call_with_context
    call_with_context --> function_call["fn(**validated_args, **context_args)"]
```

The context parameter is excluded from the `func_metadata()` call via the `skip_names` parameter and injected separately during execution.

Sources: [src/mcp/server/fastmcp/tools/base.py:63-69](), [src/mcp/server/fastmcp/tools/base.py:94-99](), [src/mcp/server/fastmcp/utilities/context_injection.py]()

## Tool Execution System

Tool execution involves argument validation, context injection, and result conversion.

### Tool Execution Pipeline

```mermaid
sequenceDiagram
    participant Client as "MCP Client"
    participant ToolManager as "ToolManager"
    participant Tool as "Tool"
    participant FuncMetadata as "FuncMetadata"
    participant ArgModelBase as "ArgModelBase"
    participant Function as "Python Function"
    
    Client->>ToolManager: call_tool("sum", {"a": 1, "b": 2})
    ToolManager->>ToolManager: get_tool("sum")
    ToolManager->>Tool: run(arguments, context)
    Tool->>FuncMetadata: call_fn_with_arg_validation()
    
    FuncMetadata->>FuncMetadata: pre_parse_json(arguments)
    FuncMetadata->>ArgModelBase: model_validate(parsed_args)
    ArgModelBase-->>FuncMetadata: validated_model
    FuncMetadata->>ArgModelBase: model_dump_one_level()
    ArgModelBase-->>FuncMetadata: function_kwargs
    FuncMetadata->>Function: fn(**function_kwargs, **context_args)
    Function-->>FuncMetadata: result
    
    alt convert_result=True
        FuncMetadata->>FuncMetadata: convert_result(result)
        FuncMetadata-->>Tool: (unstructured_content, structured_content)
    else
        FuncMetadata-->>Tool: result
    end
    
    Tool-->>ToolManager: result
    ToolManager-->>Client: result
```

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:73-85](), [src/mcp/server/fastmcp/tools/base.py:86-106](), [src/mcp/server/fastmcp/utilities/func_metadata.py:68-89]()

### Error Handling

Tool execution wraps exceptions in `ToolError` for consistent error reporting:

```python
try:
    result = await self.fn_metadata.call_fn_with_arg_validation(
        self.fn,
        self.is_async,
        arguments,
        {self.context_kwarg: context} if self.context_kwarg is not None else None,
    )
    
    if convert_result:
        result = self.fn_metadata.convert_result(result)
    
    return result
except Exception as e:
    raise ToolError(f"Error executing tool {self.name}: {e}") from e
```

Sources: [src/mcp/server/fastmcp/tools/base.py:97-110]()

## ToolManager - Centralized Tool Management

The `ToolManager` class provides centralized registration, retrieval, and execution of tools. It maintains a registry of `Tool` instances and handles tool lifecycle management.

### ToolManager Architecture

```mermaid
flowchart TD
    ToolManager["ToolManager"] --> _tools["_tools: dict[str, Tool]"]
    ToolManager --> warn_on_duplicate_tools["warn_on_duplicate_tools: bool"]
    
    add_tool["add_tool()"] --> Tool_from_function["Tool.from_function()"]
    Tool_from_function --> check_existing["Check existing tool"]
    check_existing --> warn_duplicate["Warn if duplicate"]
    check_existing --> store_tool["_tools[tool.name] = tool"]
    
    get_tool["get_tool(name)"] --> lookup["_tools.get(name)"]
    list_tools["list_tools()"] --> values["list(_tools.values())"]
    call_tool["call_tool(name, args)"] --> get_tool
    get_tool --> tool_run["tool.run(args, context)"]
```

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:19-35](), [src/mcp/server/fastmcp/tools/tool_manager.py:45-85]()

### ToolManager API

| Method | Purpose | Parameters | Return Type |
|--------|---------|------------|-------------|
| `add_tool()` | Register function as tool | `fn`, `name`, `title`, `description`, `annotations`, `icons`, `structured_output` | `Tool` |
| `get_tool()` | Retrieve tool by name | `name: str` | `Tool \| None` |
| `list_tools()` | Get all registered tools | None | `list[Tool]` |
| `call_tool()` | Execute tool with arguments | `name`, `arguments`, `context`, `convert_result` | `Any` |

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:37-85]()

### Tool Registration Workflow

```mermaid
sequenceDiagram
    participant Dev as "Developer"
    participant Decorator as "@tool decorator"
    participant ToolManager as "ToolManager"
    participant Tool as "Tool"
    participant FuncMetadata as "FuncMetadata"
    
    Dev->>Decorator: @app.tool def my_tool(x: int)
    Decorator->>ToolManager: add_tool(my_tool)
    ToolManager->>Tool: Tool.from_function(my_tool)
    Tool->>FuncMetadata: func_metadata(my_tool)
    FuncMetadata-->>Tool: metadata with ArgModelBase
    Tool-->>ToolManager: Tool instance
    ToolManager->>ToolManager: _tools["my_tool"] = tool
    ToolManager-->>Decorator: Tool instance
```

Sources: [src/mcp/server/fastmcp/tools/tool_manager.py:45-71](), [src/mcp/server/fastmcp/tools/base.py:42-84]()

## Structured Output Support

Tools can return structured output with automatic schema generation and validation.

### Structured Output Types

```mermaid
flowchart TD
    ReturnType["Function Return Type"] --> BaseModel["BaseModel"]
    ReturnType --> Primitive["Primitive Types\n(str, int, float, bool)"]
    ReturnType --> Generic["Generic Types\n(list, dict, Union)"]
    ReturnType --> TypedDict["TypedDict"]
    ReturnType --> Dataclass["@dataclass"]
    ReturnType --> RegularClass["Regular Class\nwith annotations"]
    
    BaseModel --> DirectUse["Use directly as schema"]
    Primitive --> Wrapped["Wrap in {\"result\": value}"]
    Generic --> Wrapped
    TypedDict --> Convert["Convert to Pydantic model"]
    Dataclass --> Convert
    RegularClass --> Convert
    
    DirectUse --> Schema["JSON Schema"]
    Wrapped --> Schema
    Convert --> Schema
```

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:287-371](), [src/mcp/server/fastmcp/utilities/func_metadata.py:425-449]()

### Output Conversion Process

The `convert_result()` method handles both unstructured and structured output:

**Dual Output Generation:**

```mermaid
flowchart TD
    result["Function Result"] --> convert_to_content["_convert_to_content(result)"]
    convert_to_content --> unstructured["Unstructured Content\n(TextContent, etc.)"]
    
    result --> has_schema{"output_schema exists?"}
    has_schema -->|No| return_unstructured["Return unstructured only"]
    has_schema -->|Yes| check_wrap{"wrap_output?"}
    
    check_wrap -->|Yes| wrap_result["result = {'result': result}"]
    check_wrap -->|No| use_direct["Use result directly"]
    
    wrap_result --> validate["output_model.model_validate()"]
    use_direct --> validate
    validate --> dump["model_dump(mode='json', by_alias=True)"]
    dump --> structured["Structured Content\n(dict)"]
    
    unstructured --> tuple_result["(unstructured, structured)"]
    structured --> tuple_result
```

**Content Conversion Logic:**
- **Unstructured**: Converts results to `ContentBlock` sequences (text, image, audio)
- **Structured**: Validates against output schema and serializes to JSON-compatible dict
- **Return**: Tuple of both formats for backwards compatibility

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:91-119](), [src/mcp/server/fastmcp/utilities/func_metadata.py:489-524]()

## Advanced Features

### Reserved Parameter Names

The system handles conflicts with Pydantic `BaseModel` methods by using aliases:

```python
def tool(model_dump: str, validate: bool) -> str:
    # Parameters conflict with BaseModel methods
    # System automatically creates aliases
```

**Alias Resolution Process:**

```mermaid
flowchart TD
    param_name["Parameter Name"] --> check_conflict{"hasattr(BaseModel, name) &&\ncallable(getattr(BaseModel, name))?"}
    check_conflict -->|No| use_direct["Use parameter name directly"]
    check_conflict -->|Yes| create_alias["Create alias mapping"]
    
    create_alias --> set_aliases["field_info.alias = param_name\nfield_info.validation_alias = param_name\nfield_info.serialization_alias = param_name"]
    set_aliases --> internal_name["internal_name = f'field_{param_name}'"]
    internal_name --> store_internal["Store with internal name in model"]
    
    use_direct --> store_direct["Store with original name"]
```

This prevents Pydantic warnings about shadowing parent attributes while maintaining the original parameter names in the external API.

Sources: [src/mcp/server/fastmcp/utilities/func_metadata.py:240-252]()

### Async Function Support

Both sync and async functions are supported with automatic detection:

```python
def _is_async_callable(obj: Any) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func
    
    return inspect.iscoroutinefunction(obj) or (
        callable(obj) and inspect.iscoroutinefunction(getattr(obj, "__call__", None))
    )
```

Sources: [src/mcp/server/fastmcp/tools/base.py:113-119]()

### Tool Annotations

Tools support optional metadata through `ToolAnnotations`:

- `title`: Human-readable title
- `readOnlyHint`: Indicates read-only operations  
- `openWorldHint`: Indicates open-world assumptions

Sources: [src/mcp/server/fastmcp/tools/base.py:34]()