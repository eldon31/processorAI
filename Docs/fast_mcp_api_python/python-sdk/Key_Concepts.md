This document explains the fundamental concepts of the Model Context Protocol (MCP) Python SDK. It covers the core entities, protocol mechanics, and architectural patterns that developers need to understand when building MCP servers and clients. For specific implementation guidance on building servers, see [FastMCP Server Framework](#2). For client-side development, see [Client Framework](#3).

## MCP Protocol Overview

The Model Context Protocol enables standardized communication between Large Language Models and external systems. The protocol defines how clients (typically LLM applications) can discover and interact with servers that expose tools, data, and interaction patterns.

```mermaid
graph TB
    subgraph "MCP Ecosystem"
        Client["MCP Client<br/>(ClientSession)"]
        Server["MCP Server<br/>(FastMCP/Server)"]
        LLM["Large Language Model"]
    end
    
    subgraph "Core Entities"
        Tools["Tools<br/>@tool decorator"]
        Resources["Resources<br/>@resource decorator"] 
        Prompts["Prompts<br/>@prompt decorator"]
    end
    
    subgraph "Protocol Messages"
        Initialize["InitializeRequest<br/>InitializeResult"]
        List["ListToolsRequest<br/>ListResourcesRequest<br/>ListPromptsRequest"]
        Execute["CallToolRequest<br/>ReadResourceRequest<br/>GetPromptRequest"]
    end
    
    Client <--> Server
    Client <--> LLM
    Server --> Tools
    Server --> Resources
    Server --> Prompts
    Client --> Initialize
    Client --> List
    Client --> Execute
```

**MCP Core Architecture**

Sources: [README.md:84-194](), [src/mcp/types.py:8-34]()

## Servers and Clients

### MCP Servers

Servers expose functionality and data to LLM applications. The MCP Python SDK provides two server implementation approaches:

- **FastMCP**: High-level decorator-based framework using `FastMCP` class
- **Low-level Server**: Direct protocol implementation using `Server` class

```mermaid
graph TB
    subgraph "Server Implementation Layers"
        FastMCP["FastMCP<br/>High-level Framework"]
        LowLevel["Server<br/>Low-level Implementation"]
        Session["ServerSession<br/>Connection Management"]
        Protocol["Protocol Types<br/>types.py"]
    end
    
    subgraph "Developer Interface"
        ToolDecorator["@mcp.tool()"]
        ResourceDecorator["@mcp.resource()"]
        PromptDecorator["@mcp.prompt()"]
    end
    
    subgraph "Protocol Handlers"
        CallTool["call_tool()"]
        ReadResource["read_resource()"]
        GetPrompt["get_prompt()"]
    end
    
    ToolDecorator --> FastMCP
    ResourceDecorator --> FastMCP
    PromptDecorator --> FastMCP
    
    FastMCP --> LowLevel
    CallTool --> LowLevel
    ReadResource --> LowLevel
    GetPrompt --> LowLevel
    
    LowLevel --> Session
    Session --> Protocol
```

**Server Implementation Architecture**

Sources: [src/mcp/server/lowlevel/server.py:1-66](), [README.md:198-265]()

### MCP Clients

Clients connect to servers and facilitate communication with LLMs. The primary client implementation is `ClientSession`, which handles protocol negotiation, message routing, and connection management.

Sources: [README.md:84-92]()

## Core MCP Entities

### Tools

Tools are executable functions that LLMs can call to perform actions or computations. They are defined using the `@tool` decorator in FastMCP or the `call_tool()` handler in low-level servers.

```mermaid
graph LR
    subgraph "Tool Definition"
        Decorator["@mcp.tool()"]
        Function["Python Function"]
        Schema["Input Schema<br/>JSON Schema"]
        Output["Output Schema<br/>Optional"]
    end
    
    subgraph "Protocol Messages"
        ListTools["ListToolsRequest<br/>ListToolsResult"]
        CallTool["CallToolRequest<br/>CallToolResult"]
    end
    
    subgraph "Tool Execution"
        Validation["Input Validation<br/>jsonschema.validate()"]
        Handler["Tool Function Call"]
        Result["Structured/Unstructured Output"]
    end
    
    Decorator --> Function
    Function --> Schema
    Schema --> ListTools
    ListTools --> CallTool
    CallTool --> Validation
    Validation --> Handler
    Handler --> Result
```

**Tool Lifecycle and Processing**

Tools support both structured and unstructured output. The `CallToolResult` type includes both `content` (unstructured) and `structuredContent` (structured) fields for maximum compatibility.

Sources: [README.md:297-384](), [src/mcp/server/lowlevel/server.py:465-547](), [src/mcp/types.py:869-922]()

### Resources

Resources provide read-only access to data that LLMs can consume. They are identified by URIs and can return text, binary data, or multiple content blocks.

```mermaid
graph TB
    subgraph "Resource Types"
        Static["Static Resources<br/>@resource(uri)"]
        Template["Resource Templates<br/>@resource(uri_template)"]
        Dynamic["Dynamic Resources<br/>URI Parameters"]
    end
    
    subgraph "Resource Content"
        Text["TextResourceContents"]
        Blob["BlobResourceContents"]
        Multiple["Multiple Contents"]
    end
    
    subgraph "Protocol Flow"
        List["ListResourcesRequest<br/>ListResourceTemplatesRequest"]
        Read["ReadResourceRequest<br/>ReadResourceResult"]
        Subscribe["SubscribeRequest<br/>ResourceUpdatedNotification"]
    end
    
    Static --> Text
    Template --> Text
    Dynamic --> Multiple
    Text --> Read
    Blob --> Read
    Multiple --> Read
    List --> Read
    Read --> Subscribe
```

**Resource Architecture and Content Types**

Sources: [README.md:266-296](), [src/mcp/types.py:431-554](), [src/mcp/server/lowlevel/server.py:311-367]()

### Prompts

Prompts are reusable templates that help structure LLM interactions. They can include parameters and return formatted message sequences.

```mermaid
graph LR
    subgraph "Prompt Definition"
        PromptDecorator["@mcp.prompt()"]
        Template["Template Function"]
        Args["PromptArgument[]"]
    end
    
    subgraph "Prompt Content"
        Messages["PromptMessage[]"]
        UserMsg["UserMessage"]
        AssistantMsg["AssistantMessage"]
    end
    
    subgraph "Protocol Messages"
        ListPrompts["ListPromptsRequest"]
        GetPrompt["GetPromptRequest<br/>GetPromptResult"]
    end
    
    PromptDecorator --> Template
    Template --> Args
    Args --> Messages
    Messages --> UserMsg
    Messages --> AssistantMsg
    ListPrompts --> GetPrompt
    GetPrompt --> Messages
```

**Prompt Template System**

Sources: [README.md:490-517](), [src/mcp/types.py:630-812]()

## Protocol and Message Flow

The MCP protocol uses JSON-RPC 2.0 for message exchange. Communication follows a request-response pattern with support for notifications.

```mermaid
sequenceDiagram
    participant Client as "ClientSession"
    participant Server as "ServerSession"
    participant Handler as "Request Handler"
    
    Note over Client,Server: "Initialization Phase"
    Client->>Server: "InitializeRequest"
    Server->>Client: "InitializeResult"
    Client->>Server: "InitializedNotification"
    
    Note over Client,Server: "Discovery Phase"
    Client->>Server: "ListToolsRequest"
    Server->>Handler: "list_tools()"
    Handler->>Server: "list[Tool]"
    Server->>Client: "ListToolsResult"
    
    Note over Client,Server: "Execution Phase"
    Client->>Server: "CallToolRequest"
    Server->>Handler: "call_tool(name, args)"
    Handler->>Server: "CallToolResult"
    Server->>Client: "CallToolResult"
    
    Note over Client,Server: "Notifications"
    Server->>Client: "ProgressNotification"
    Server->>Client: "LoggingMessageNotification"
```

**MCP Protocol Message Flow**

The protocol supports several core message types defined in `types.py`:

- **Requests**: `ClientRequest`, `ServerRequest` - expect responses
- **Notifications**: `ClientNotification`, `ServerNotification` - no response expected  
- **Results**: `ClientResult`, `ServerResult` - responses to requests

Sources: [src/mcp/types.py:82-348](), [README.md:25-194]()

## Transport Layer

MCP supports multiple transport mechanisms for client-server communication:

```mermaid
graph TB
    subgraph "Transport Types"
        Stdio["Standard I/O<br/>stdio_client/stdio_server"]
        SSE["Server-Sent Events<br/>SseServerTransport"]
        StreamableHTTP["StreamableHTTP<br/>StreamableHTTPServerTransport"]
    end
    
    subgraph "Connection Management"
        ClientSession["ClientSession"]
        ServerSession["ServerSession"]
        MessageStream["SessionMessage Stream"]
    end
    
    subgraph "Message Processing"
        JSONRPCRequest["JSONRPCRequest"]
        JSONRPCResponse["JSONRPCResponse"]
        JSONRPCNotification["JSONRPCNotification"]
    end
    
    Stdio --> ClientSession
    SSE --> ClientSession
    StreamableHTTP --> ClientSession
    ClientSession --> MessageStream
    ServerSession --> MessageStream
    MessageStream --> JSONRPCRequest
    MessageStream --> JSONRPCResponse
    MessageStream --> JSONRPCNotification
```

**Transport Layer Architecture**

Each transport provides bidirectional communication with different characteristics:

- **stdio**: Process-based communication via stdin/stdout
- **SSE**: HTTP-based with server-sent events for real-time updates
- **StreamableHTTP**: Advanced HTTP transport with session management and resumability

Sources: [src/mcp/types.py:124-193](), Transport architecture from overview diagrams

## Server Implementations

### FastMCP Framework

`FastMCP` provides a decorator-based approach for rapid server development. It automatically handles protocol compliance, schema generation, and message routing.

```mermaid
graph TB
    subgraph "FastMCP Components"
        FastMCPClass["FastMCP"]
        ToolManager["ToolManager"]
        ResourceManager["ResourceManager"]
        PromptManager["PromptManager"]
    end
    
    subgraph "Function Processing"
        FuncMetadata["func_metadata<br/>Introspection"]
        Validation["Argument Validation"]
        ContextInjection["Context Injection"]
    end
    
    subgraph "Generated Components"
        JSONSchema["JSON Schema Generation"]
        RequestHandlers["Request Handlers"]
        TransportApps["Transport Applications"]
    end
    
    FastMCPClass --> ToolManager
    FastMCPClass --> ResourceManager
    FastMCPClass --> PromptManager
    ToolManager --> FuncMetadata
    ResourceManager --> FuncMetadata
    PromptManager --> FuncMetadata
    FuncMetadata --> Validation
    FuncMetadata --> ContextInjection
    FuncMetadata --> JSONSchema
    JSONSchema --> RequestHandlers
    RequestHandlers --> TransportApps
```

**FastMCP Internal Architecture**

### Low-level Server

The `Server` class provides direct access to the MCP protocol with explicit handler registration using decorators like `list_tools()`, `call_tool()`, etc.

Sources: [src/mcp/server/lowlevel/server.py:133-158](), FastMCP concepts from overview diagrams

## Context and Session Management

### Request Context

The `Context` object provides access to MCP capabilities and request metadata within tool and resource functions.

```mermaid
graph LR
    subgraph "Context Components"
        Context["Context[SessionT, LifespanT]"]
        RequestContext["RequestContext"]
        Session["ServerSession"]
        Lifespan["LifespanContext"]
    end
    
    subgraph "Context Capabilities"
        Logging["debug(), info(), warning(), error()"]
        Progress["report_progress()"]
        Resources["read_resource()"]
        Elicitation["elicit()"]
    end
    
    subgraph "Session Access"
        ClientParams["client_params"]
        Notifications["send_*_notification()"]
        Sampling["create_message()"]
    end
    
    Context --> RequestContext
    Context --> Session
    Context --> Lifespan
    Context --> Logging
    Context --> Progress
    Context --> Resources
    Context --> Elicitation
    Session --> ClientParams
    Session --> Notifications
    Session --> Sampling
```

**Context and Session Architecture**

The context system enables:

- **Logging**: Send log messages to clients via `LoggingMessageNotification`
- **Progress**: Report operation progress via `ProgressNotification`  
- **Resource Access**: Read other resources via `ReadResourceRequest`
- **User Interaction**: Request additional information via `ElicitRequest`
- **LLM Sampling**: Generate text via `CreateMessageRequest`

### Session Lifecycle

Both `ClientSession` and `ServerSession` manage connection state, protocol version negotiation, and message routing throughout the connection lifetime.

Sources: [README.md:580-646](), [src/mcp/shared/context.py]() (referenced), [src/mcp/server/session.py]() (referenced)

# FastMCP Server Framework




FastMCP is a high-level, decorator-based framework for building Model Context Protocol (MCP) servers in Python. It provides an ergonomic interface that simplifies server development through automatic function introspection, context injection, and seamless integration with multiple transport protocols.

For low-level server implementation details, see [Low-Level Server Implementation](#6). For client-side components, see [Client Framework](#3). For transport layer specifics, see [Transport Layer](#5).

## Overview

FastMCP abstracts away the complexities of the MCP protocol by providing a decorator-based API that automatically converts Python functions into MCP tools, resources, and prompts. The framework handles JSON schema generation, input validation, output conversion, and protocol message handling.

### FastMCP Core Architecture

```mermaid
graph TB
    subgraph "FastMCP Server Framework"
        FastMCPClass[FastMCP]
        Settings[Settings]
        Context[Context]
        
        subgraph "Managers"
            ToolManager[ToolManager]
            ResourceManager[ResourceManager] 
            PromptManager[PromptManager]
        end
        
        subgraph "Decorators"
            ToolDecorator["@tool()"]
            ResourceDecorator["@resource()"]
            PromptDecorator["@prompt()"]
        end
        
        subgraph "Low-Level Integration"
            MCPServer[MCPServer]
            ServerSession[ServerSession]
        end
        
        subgraph "Transport Apps"
            StdioTransport["stdio_server()"]
            SSEApp["sse_app()"]
            StreamableApp["streamable_http_app()"]
        end
    end
    
    subgraph "User Code"
        UserFunctions["Python Functions"]
    end
    
    %% User interactions
    UserFunctions --> ToolDecorator
    UserFunctions --> ResourceDecorator
    UserFunctions --> PromptDecorator
    
    %% Decorator to manager connections
    ToolDecorator --> ToolManager
    ResourceDecorator --> ResourceManager
    PromptDecorator --> PromptManager
    
    %% FastMCP orchestration
    FastMCPClass --> Settings
    FastMCPClass --> ToolManager
    FastMCPClass --> ResourceManager
    FastMCPClass --> PromptManager
    FastMCPClass --> MCPServer
    
    %% Context injection
    Context -.-> UserFunctions
    FastMCPClass --> Context
    
    %% Transport integration
    FastMCPClass --> StdioTransport
    FastMCPClass --> SSEApp
    FastMCPClass --> StreamableApp
    
    %% Low-level connection
    MCPServer --> ServerSession
```

Sources: [src/mcp/server/fastmcp/server.py:122-209](), [src/mcp/server/fastmcp/server.py:268-280]()

## Core Components

### FastMCP Class

The `FastMCP` class serves as the central orchestrator, managing all server components and providing the decorator-based API. It wraps a low-level `MCPServer` instance while providing higher-level abstractions.

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| `FastMCP` | Main server class | `tool()`, `resource()`, `prompt()`, `run()` |
| `Settings` | Configuration management | Environment variable integration |
| `Context` | Request context access | `log()`, `report_progress()`, `read_resource()` |

### Manager Classes

FastMCP uses specialized manager classes to handle different types of MCP entities:

```mermaid
graph LR
    subgraph "Entity Managers"
        ToolManager["ToolManager<br/>_tool_manager"]
        ResourceManager["ResourceManager<br/>_resource_manager"]
        PromptManager["PromptManager<br/>_prompt_manager"]
    end
    
    subgraph "MCP Protocol Handlers"
        ListTools["list_tools()"]
        CallTool["call_tool()"]
        ListResources["list_resources()"]
        ReadResource["read_resource()"]
        ListPrompts["list_prompts()"]
        GetPrompt["get_prompt()"]
    end
    
    ToolManager --> ListTools
    ToolManager --> CallTool
    ResourceManager --> ListResources
    ResourceManager --> ReadResource
    PromptManager --> ListPrompts
    PromptManager --> GetPrompt
```

Sources: [src/mcp/server/fastmcp/server.py:181-183](), [src/mcp/server/fastmcp/server.py:270-279]()

## Decorator-Based API

### Tool Registration

The `@tool()` decorator converts Python functions into MCP tools with automatic schema generation:

```python
@server.tool()
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@server.tool()
async def async_tool(x: int, ctx: Context) -> str:
    await ctx.report_progress(50, 100)
    return f"Processed {x}"
```

The decorator supports several parameters for customization:

| Parameter | Type | Purpose |
|-----------|------|---------|
| `name` | `str \| None` | Custom tool name (defaults to function name) |
| `title` | `str \| None` | Human-readable title |
| `description` | `str \| None` | Tool description |
| `structured_output` | `bool \| None` | Controls output schema generation |

Sources: [src/mcp/server/fastmcp/server.py:393-451](), [tests/server/fastmcp/test_server.py:146-153]()

### Resource Registration

Resources can be registered as static resources or parameterized templates:

```python