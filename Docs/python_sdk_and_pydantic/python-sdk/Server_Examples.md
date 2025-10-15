This document provides comprehensive examples of MCP server implementations using both the low-level `Server` class and the high-level `FastMCP` framework. These examples demonstrate various MCP capabilities including tools, resources, prompts, progress reporting, and different transport mechanisms.

For client-side examples and integration patterns, see [Client Examples](#9.2). For detailed FastMCP framework documentation, see [FastMCP Server Framework](#2).

## Server Implementation Approaches

The MCP Python SDK provides two primary approaches for building servers, each suited for different use cases and complexity levels.

### Server Implementation Architecture

```mermaid
graph TB
    subgraph "High-Level Framework"
        FastMCP["FastMCP"]
        Decorators["@tool, @resource, @prompt"]
        AutoSchema["Automatic Schema Generation"]
    end
    
    subgraph "Low-Level Implementation"
        LowLevelServer["Server"]
        RequestHandlers["@app.call_tool(), @app.list_resources()"]
        ManualSchema["Manual Schema Definition"]
    end
    
    subgraph "Transport Layer"
        StdioTransport["stdio_server()"]
        SSETransport["SseServerTransport"]
        StreamableHTTP["StreamableHTTPSessionManager"]
    end
    
    subgraph "Core Protocol"
        MCPTypes["mcp.types"]
        SessionMessage["SessionMessage"]
        JSONRPCLayer["JSON-RPC Protocol"]
    end
    
    FastMCP --> LowLevelServer
    Decorators --> RequestHandlers
    AutoSchema --> ManualSchema
    
    LowLevelServer --> StdioTransport
    LowLevelServer --> SSETransport
    LowLevelServer --> StreamableHTTP
    
    StdioTransport --> JSONRPCLayer
    SSETransport --> JSONRPCLayer
    StreamableHTTP --> JSONRPCLayer
    
    JSONRPCLayer --> MCPTypes
    JSONRPCLayer --> SessionMessage
```

Sources: [examples/servers/simple-resource/mcp_simple_resource/server.py:1-94](), [examples/servers/simple-tool/mcp_simple_tool/server.py:1-94](), [examples/snippets/servers/structured_output.py:1-98]()

## Low-Level Server Examples

The low-level `Server` class provides direct control over MCP protocol handling and is suitable for complex server implementations requiring fine-grained control.

### Basic Resource Server

The simple resource server demonstrates fundamental resource serving capabilities using the low-level `Server` class.

```mermaid
graph LR
    subgraph "simple-resource Server"
        ServerInstance["Server('mcp-simple-resource')"]
        ListResourcesHandler["@app.list_resources()"]
        ReadResourceHandler["@app.read_resource()"]
        ResourceData["SAMPLE_RESOURCES dict"]
    end
    
    subgraph "Transport Support"
        StdioMode["stdio transport"]
        SSEMode["SSE transport + Starlette"]
    end
    
    subgraph "Resource Schema"
        FileUrlSchema["FileUrl('file:///name.txt')"]
        ResourceType["types.Resource"]
        ContentType["ReadResourceContents"]
    end
    
    ServerInstance --> ListResourcesHandler
    ServerInstance --> ReadResourceHandler
    ListResourcesHandler --> ResourceData
    ReadResourceHandler --> ResourceData
    
    ServerInstance --> StdioMode
    ServerInstance --> SSEMode
    
    ListResourcesHandler --> ResourceType
    ReadResourceHandler --> ContentType
    ResourceType --> FileUrlSchema
```

Sources: [examples/servers/simple-resource/mcp_simple_resource/server.py:34-58]()

### Basic Tool Server  

The simple tool server shows HTTP client functionality and tool execution patterns.

```mermaid
graph LR
    subgraph "simple-tool Server"
        ToolServer["Server('mcp-website-fetcher')"]
        CallToolHandler["@app.call_tool()"]
        ListToolsHandler["@app.list_tools()"]
        FetchFunction["fetch_website()"]
    end
    
    subgraph "HTTP Integration"
        HttpxClient["create_mcp_http_client()"]
        UserAgent["MCP Test Server headers"]
        ResponseProcessing["response.text -> TextContent"]
    end
    
    subgraph "Tool Schema"
        ToolDefinition["types.Tool"]
        InputSchema["JSON Schema validation"]
        ContentBlocks["list[types.ContentBlock]"]
    end
    
    CallToolHandler --> FetchFunction
    FetchFunction --> HttpxClient
    HttpxClient --> UserAgent
    FetchFunction --> ResponseProcessing
    
    ListToolsHandler --> ToolDefinition
    ToolDefinition --> InputSchema
    CallToolHandler --> ContentBlocks
```

Sources: [examples/servers/simple-tool/mcp_simple_tool/server.py:32-58]()

### Basic Prompt Server

The simple prompt server demonstrates template-based prompt generation.

```mermaid
graph LR
    subgraph "simple-prompt Server"
        PromptServer["Server('mcp-simple-prompt')"]
        ListPromptsHandler["@app.list_prompts()"]
        GetPromptHandler["@app.get_prompt()"]
        CreateMessages["create_messages()"]
    end
    
    subgraph "Prompt Schema"
        PromptType["types.Prompt"]
        PromptArgument["types.PromptArgument"]
        PromptMessage["types.PromptMessage"]
        TextContent["types.TextContent"]
    end
    
    subgraph "Dynamic Content"
        ContextParam["context argument"]
        TopicParam["topic argument"]
        MessageGeneration["Dynamic message building"]
    end
    
    ListPromptsHandler --> PromptType
    PromptType --> PromptArgument
    GetPromptHandler --> CreateMessages
    CreateMessages --> PromptMessage
    PromptMessage --> TextContent
    
    CreateMessages --> ContextParam
    CreateMessages --> TopicParam
    CreateMessages --> MessageGeneration
```

Sources: [examples/servers/simple-prompt/mcp_simple_prompt/server.py:44-77]()

## StreamableHTTP Transport Examples

StreamableHTTP transport enables bidirectional communication with session management and resumability features.

### StreamableHTTP with Event Store

```mermaid
graph TB
    subgraph "StreamableHTTP Server"
        StreamableServer["Server('mcp-streamable-http-demo')"]
        SessionManager["StreamableHTTPSessionManager"]
        EventStore["InMemoryEventStore"]
        StarletteApp["Starlette ASGI app"]
    end
    
    subgraph "Notification System"
        ToolWithNotifications["start-notification-stream tool"]
        LogMessages["ctx.session.send_log_message()"]
        ResourceUpdates["ctx.session.send_resource_updated()"]
        RequestContext["ctx.request_id"]
    end
    
    subgraph "Resumability Features"
        EventIds["Unique event IDs"]
        LastEventId["Last-Event-ID header"]
        EventReplay["Missed event replay"]
    end
    
    subgraph "CORS & Middleware"
        CORSMiddleware["CORS with Mcp-Session-Id"]
        SessionIdHeader["Session ID exposure"]
    end
    
    StreamableServer --> SessionManager
    SessionManager --> EventStore
    SessionManager --> StarletteApp
    
    ToolWithNotifications --> LogMessages
    ToolWithNotifications --> ResourceUpdates
    LogMessages --> RequestContext
    
    EventStore --> EventIds
    EventStore --> LastEventId
    EventStore --> EventReplay
    
    StarletteApp --> CORSMiddleware
    CORSMiddleware --> SessionIdHeader
```

Sources: [examples/servers/simple-streamablehttp/mcp_simple_streamablehttp/server.py:47-165]()

### Stateless StreamableHTTP

```mermaid
graph LR
    subgraph "Stateless Server"
        StatelessServer["Server('mcp-streamable-http-stateless-demo')"]
        StatelessManager["StreamableHTTPSessionManager(stateless=True)"]
        NoEventStore["event_store=None"]
    end
    
    subgraph "Simplified Architecture"
        NoResumability["No resumability support"]
        NoEventReplay["No event replay"]
        SimplerSetup["Simpler configuration"]
    end
    
    subgraph "Same Features"
        NotificationSupport["Notification streaming"]
        SessionManagement["Session management"]
        CORSSupport["CORS middleware"]
    end
    
    StatelessServer --> StatelessManager
    StatelessManager --> NoEventStore
    NoEventStore --> NoResumability
    NoEventStore --> NoEventReplay
    NoEventStore --> SimplerSetup
    
    StatelessManager --> NotificationSupport
    StatelessManager --> SessionManagement
    StatelessManager --> CORSSupport
```

Sources: [examples/servers/simple-streamablehttp-stateless/mcp_simple_streamablehttp_stateless/server.py:97-140]()

## FastMCP Framework Examples

FastMCP provides a decorator-based approach for rapid server development with automatic schema generation and simplified setup.

### Structured Output Example

```mermaid
graph TB
    subgraph "FastMCP Structured Output"
        FastMCPInstance["FastMCP('Structured Output Example')"]
        ToolDecorators["@mcp.tool() decorators"]
        AutomaticSchema["Automatic schema generation"]
    end
    
    subgraph "Data Structure Types"
        PydanticModel["WeatherData(BaseModel)"]
        TypedDict["LocationInfo(TypedDict)"]
        RegularDict["dict[str, float]"]
        RegularClass["UserProfile class"]
        UntypedClass["UntypedConfig (no schema)"]
    end
    
    subgraph "Schema Generation"
        PydanticSchema["Pydantic -> JSON Schema"]
        TypedDictSchema["TypedDict -> JSON Schema"]
        DictSchema["dict[K,V] -> JSON Schema"]
        ClassSchema["Typed class -> JSON Schema"]
        NoSchema["Untyped -> No schema"]
    end
    
    subgraph "Return Value Wrapping"
        StructuredReturn["Complex types as-is"]
        SimpleWrapping["Simple types wrapped in 'result'"]
        ListWrapping["Lists wrapped in 'result'"]
    end
    
    ToolDecorators --> AutomaticSchema
    
    PydanticModel --> PydanticSchema
    TypedDict --> TypedDictSchema
    RegularDict --> DictSchema
    RegularClass --> ClassSchema
    UntypedClass --> NoSchema
    
    AutomaticSchema --> StructuredReturn
    AutomaticSchema --> SimpleWrapping
    AutomaticSchema --> ListWrapping
```

Sources: [examples/snippets/servers/structured_output.py:9-98]()

### Direct Execution Example

```mermaid
graph LR
    subgraph "Direct Execution"
        FastMCPApp["FastMCP('My App')"]
        ToolFunction["hello() function"]
        ToolDecorator["@mcp.tool()"]
        RunMethod["mcp.run()"]
    end
    
    subgraph "Execution Flow"
        MainFunction["main() entry point"]
        DirectExecution["python servers/direct_execution.py"]
        UVRun["uv run direct-execution-server"]
    end
    
    subgraph "Auto-Configuration"
        DefaultTransport["Automatic transport selection"]
        SchemaGeneration["Automatic schema from type hints"]
        CLIHandling["Built-in CLI argument handling"]
    end
    
    ToolDecorator --> ToolFunction
    ToolFunction --> FastMCPApp
    FastMCPApp --> RunMethod
    
    MainFunction --> RunMethod
    MainFunction --> DirectExecution
    MainFunction --> UVRun
    
    RunMethod --> DefaultTransport
    ToolDecorator --> SchemaGeneration
    RunMethod --> CLIHandling
```

Sources: [examples/snippets/servers/direct_execution.py:10-27]()

## Feature-Specific Examples

The integration tests demonstrate various MCP features through focused example servers.

### Progress Reporting

```mermaid
graph LR
    subgraph "Progress Example"
        ProgressTool["long_running_task tool"]
        ProgressCallback["progress_callback parameter"]
        ProgressUpdates["Sequential progress reports"]
    end
    
    subgraph "Progress Implementation"
        StepIteration["for i in range(steps)"]
        ProgressCalculation["(i + 1) / steps"]
        MessageFormat["'Step {i+1}/{steps}'"]
    end
    
    subgraph "Client Integration"
        ClientCallback["progress_callback function"]
        ProgressCollection["progress_updates list"]
        Validation["Progress validation in tests"]
    end
    
    ProgressTool --> ProgressCallback
    ProgressCallback --> ProgressUpdates
    
    ProgressUpdates --> StepIteration
    StepIteration --> ProgressCalculation
    ProgressCalculation --> MessageFormat
    
    ProgressCallback --> ClientCallback
    ClientCallback --> ProgressCollection
    ProgressCollection --> Validation
```

Sources: [tests/server/fastmcp/test_integration.py:392-440]()

### Notification System

```mermaid
graph LR
    subgraph "Notification Example"
        NotificationTool["process_data tool"]
        LogLevels["debug, info, warning, error"]
        ResourceNotification["ResourceListChangedNotification"]
    end
    
    subgraph "Collection System"
        NotificationCollector["NotificationCollector class"]
        ProgressNotifications["progress_notifications list"]
        LogMessages["log_messages list"]
        ResourceNotifications["resource_notifications list"]
    end
    
    subgraph "Message Handling"
        GenericHandler["handle_generic_notification()"]
        MessageRouting["Route by notification type"]
        ClientHandler["message_handler parameter"]
    end
    
    NotificationTool --> LogLevels
    NotificationTool --> ResourceNotification
    
    LogLevels --> NotificationCollector
    ResourceNotification --> NotificationCollector
    NotificationCollector --> ProgressNotifications
    NotificationCollector --> LogMessages
    NotificationCollector --> ResourceNotifications
    
    NotificationCollector --> GenericHandler
    GenericHandler --> MessageRouting
    MessageRouting --> ClientHandler
```

Sources: [tests/server/fastmcp/test_integration.py:524-569]()

### Sampling and Elicitation

```mermaid
graph TB
    subgraph "Sampling Example"
        SamplingTool["generate_poem tool"]
        SamplingCallback["sampling_callback function"]
        CreateMessageRequest["CreateMessageRequestParams"]
        CreateMessageResult["CreateMessageResult"]
    end
    
    subgraph "Elicitation Example"
        ElicitationTool["book_table tool"]
        ElicitationCallback["elicitation_callback function"]
        ElicitRequest["ElicitRequestParams"]
        ElicitResult["ElicitResult"]
    end
    
    subgraph "Callback Integration"
        ClientSession["ClientSession parameters"]
        CallbackRegistration["sampling_callback/elicitation_callback"]
        TestSimulation["Simulated LLM/user responses"]
    end
    
    SamplingTool --> SamplingCallback
    SamplingCallback --> CreateMessageRequest
    SamplingCallback --> CreateMessageResult
    
    ElicitationTool --> ElicitationCallback
    ElicitationCallback --> ElicitRequest
    ElicitationCallback --> ElicitResult
    
    SamplingCallback --> ClientSession
    ElicitationCallback --> ClientSession
    ClientSession --> CallbackRegistration
    CallbackRegistration --> TestSimulation
```

Sources: [tests/server/fastmcp/test_integration.py:442-521]()

## Transport Configuration Patterns

All server examples support multiple transport configurations, allowing flexible deployment options.

### Universal Transport Pattern

```mermaid
graph TB
    subgraph "Transport Selection"
        ClickOption["@click.option('--transport')"]
        TransportChoice["Choice(['stdio', 'sse'])"]
        ConditionalSetup["if transport == 'sse'"]
    end
    
    subgraph "STDIO Setup"
        StdioImport["from mcp.server.stdio import stdio_server"]
        StdioContext["async with stdio_server() as streams"]
        AppRun["app.run(streams[0], streams[1], options)"]
    end
    
    subgraph "SSE Setup"
        SSEImport["from mcp.server.sse import SseServerTransport"]
        StarletteSetup["Starlette app configuration"]
        RouteSetup["Route('/sse') + Mount('/messages/')"]
        UvicornRun["uvicorn.run(starlette_app)"]
    end
    
    ClickOption --> TransportChoice
    TransportChoice --> ConditionalSetup
    
    ConditionalSetup --> StdioImport
    StdioImport --> StdioContext
    StdioContext --> AppRun
    
    ConditionalSetup --> SSEImport
    SSEImport --> StarletteSetup
    StarletteSetup --> RouteSetup
    RouteSetup --> UvicornRun
```

Sources: [examples/servers/simple-resource/mcp_simple_resource/server.py:60-93](), [examples/servers/simple-tool/mcp_simple_tool/server.py:60-93](), [examples/servers/simple-prompt/mcp_simple_prompt/server.py:79-112]()