async with httpx.AsyncClient(auth=auth_provider) as client:
    response = await client.get("https://api.example.com/v1/mcp/tools/list")
```

### Transport Integration

The authentication provider integrates seamlessly with all MCP transports:

- **StreamableHTTP**: Built-in OAuth support via `httpx.AsyncClient`
- **SSE**: Authentication headers added to SSE connections  
- **WebSocket**: OAuth tokens passed in connection headers
- **stdio**: Not applicable (local process communication)

Sources: [examples/clients/simple-auth-client/](), [src/mcp/client/auth.py:485-552]()

# Protocol & Message System




This page documents the core Model Context Protocol (MCP) message system, JSON-RPC foundation, and type system that enables communication between MCP clients and servers. This covers the fundamental protocol layer that underlies all MCP interactions.

For high-level server development using decorators and simplified APIs, see [FastMCP Server Framework](#2). For transport-specific implementations like stdio, SSE, and StreamableHTTP, see [Transport Layer](#5). For client-side message handling, see [Client Framework](#3).

## JSON-RPC Foundation

MCP is built on JSON-RPC 2.0, providing a standardized request-response and notification messaging pattern. The protocol defines four core message types that form the foundation of all MCP communication.

```mermaid
graph TB
    subgraph "JSON-RPC Message Types"
        JSONRPCRequest["JSONRPCRequest<br/>id + method + params"]
        JSONRPCResponse["JSONRPCResponse<br/>id + result"]
        JSONRPCError["JSONRPCError<br/>id + error"]
        JSONRPCNotification["JSONRPCNotification<br/>method + params"]
    end
    
    subgraph "MCP Protocol Layer"
        ClientRequest["ClientRequest<br/>Union of all client requests"]
        ServerRequest["ServerRequest<br/>Union of all server requests"]
        ClientNotification["ClientNotification<br/>Union of all client notifications"]
        ServerNotification["ServerNotification<br/>Union of all server notifications"]
    end
    
    subgraph "Message Processing"
        RequestResponder["RequestResponder<br/>Handles request-response lifecycle"]
        SessionMessage["SessionMessage<br/>Transport-agnostic message wrapper"]
    end
    
    JSONRPCRequest --> ClientRequest
    JSONRPCRequest --> ServerRequest
    JSONRPCNotification --> ClientNotification
    JSONRPCNotification --> ServerNotification
    
    ClientRequest --> RequestResponder
    ServerRequest --> RequestResponder
    RequestResponder --> SessionMessage
```

**Sources:** [src/mcp/types.py:124-193](), [src/mcp/shared/message.py]()

The base JSON-RPC types define the message structure:

- `JSONRPCRequest`: Request expecting a response, includes `id`, `method`, and `params`
- `JSONRPCResponse`: Successful response with `id` and `result`
- `JSONRPCError`: Error response with `id` and `error` containing code, message, and optional data
- `JSONRPCNotification`: One-way message with `method` and `params`, no response expected

## Protocol Message Hierarchy

MCP defines a structured hierarchy of message types that inherit from the JSON-RPC foundation, creating type-safe request and response patterns.

```mermaid
graph TB
    subgraph "Base Protocol Types"
        Request["Request[ParamsT, MethodT]<br/>Generic request base"]
        Notification["Notification[ParamsT, MethodT]<br/>Generic notification base"]
        Result["Result<br/>Generic result base"]
        RequestParams["RequestParams<br/>Base for all request parameters"]
        NotificationParams["NotificationParams<br/>Base for all notification parameters"]
    end
    
    subgraph "Specialized Request Types"
        PaginatedRequest["PaginatedRequest<br/>cursor-based pagination"]
        InitializeRequest["InitializeRequest<br/>initialize method"]
        ListToolsRequest["ListToolsRequest<br/>tools/list method"]
        CallToolRequest["CallToolRequest<br/>tools/call method"]
        ReadResourceRequest["ReadResourceRequest<br/>resources/read method"]
    end
    
    subgraph "Specialized Result Types"
        PaginatedResult["PaginatedResult<br/>nextCursor support"]
        InitializeResult["InitializeResult<br/>capabilities exchange"]
        ListToolsResult["ListToolsResult<br/>tools array"]
        CallToolResult["CallToolResult<br/>content + structuredContent"]
        ReadResourceResult["ReadResourceResult<br/>resource contents"]
    end
    
    Request --> InitializeRequest
    Request --> ListToolsRequest
    Request --> CallToolRequest
    Request --> ReadResourceRequest
    
    PaginatedRequest --> ListToolsRequest
    
    Result --> InitializeResult
    Result --> ListToolsResult
    Result --> CallToolResult
    Result --> ReadResourceResult
    
    PaginatedResult --> ListToolsResult
```

**Sources:** [src/mcp/types.py:82-122](), [src/mcp/types.py:335-365](), [src/mcp/types.py:815-922]()

Each protocol operation follows this pattern:
1. **Request class**: Defines the method name and parameter structure
2. **Parameter class**: Strongly-typed parameters extending `RequestParams`
3. **Result class**: Response structure extending `Result`
4. **Specialized handling**: Pagination, metadata, and protocol-specific features

## Core Protocol Operations

MCP defines several categories of protocol operations, each with specific request-response patterns and capabilities.

```mermaid
graph LR
    subgraph "Initialization"
        initialize["initialize<br/>InitializeRequest → InitializeResult"]
        initialized["initialized<br/>InitializedNotification"]
        ping["ping<br/>PingRequest → EmptyResult"]
    end
    
    subgraph "Resource Operations"
        list_resources["resources/list<br/>ListResourcesRequest → ListResourcesResult"]
        read_resource["resources/read<br/>ReadResourceRequest → ReadResourceResult"]
        list_templates["resources/templates/list<br/>ListResourceTemplatesRequest → ListResourceTemplatesResult"]
        subscribe["resources/subscribe<br/>SubscribeRequest → EmptyResult"]
    end
    
    subgraph "Tool Operations"
        list_tools["tools/list<br/>ListToolsRequest → ListToolsResult"]
        call_tool["tools/call<br/>CallToolRequest → CallToolResult"]
    end
    
    subgraph "Prompt Operations"
        list_prompts["prompts/list<br/>ListPromptsRequest → ListPromptsResult"]
        get_prompt["prompts/get<br/>GetPromptRequest → GetPromptResult"]
    end
    
    subgraph "Server-Initiated"
        create_message["sampling/createMessage<br/>CreateMessageRequest → CreateMessageResult"]
        elicit["elicitation/create<br/>ElicitRequest → ElicitResult"]
        list_roots["roots/list<br/>ListRootsRequest → ListRootsResult"]
    end
```

**Sources:** [src/mcp/types.py:345-365](), [src/mcp/types.py:419-554](), [src/mcp/types.py:815-922](), [src/mcp/types.py:630-802](), [src/mcp/types.py:1061-1081]()

## Message Processing Architecture

The server processes incoming messages through a structured handler system that maps message types to handler functions and manages the request lifecycle.

```mermaid
graph TB
    subgraph "Message Reception"
        SessionMessage["SessionMessage<br/>from transport"]
        RequestResponder_msg["RequestResponder<br/>wraps client requests"]
        ClientNotification_msg["ClientNotification<br/>one-way messages"]
    end
    
    subgraph "Server Message Handling"
        Server["Server<br/>lowlevel server instance"]
        request_handlers["request_handlers<br/>dict[type, handler]"]
        notification_handlers["notification_handlers<br/>dict[type, handler]"]
        _handle_message["_handle_message<br/>message dispatcher"]
        _handle_request["_handle_request<br/>request processor"]
        _handle_notification["_handle_notification<br/>notification processor"]
    end
    
    subgraph "Handler Registration"
        list_tools_decorator["@server.list_tools()<br/>decorator registration"]
        call_tool_decorator["@server.call_tool()<br/>decorator registration"]
        list_resources_decorator["@server.list_resources()<br/>decorator registration"]
    end
    
    subgraph "Response Generation"
        ServerResult["ServerResult<br/>union of all server results"]
        ErrorData["ErrorData<br/>JSON-RPC error response"]
    end
    
    SessionMessage --> RequestResponder_msg
    SessionMessage --> ClientNotification_msg
    
    RequestResponder_msg --> _handle_message
    ClientNotification_msg --> _handle_message
    
    _handle_message --> _handle_request
    _handle_message --> _handle_notification
    
    _handle_request --> request_handlers
    _handle_notification --> notification_handlers
    
    list_tools_decorator --> request_handlers
    call_tool_decorator --> request_handlers
    list_resources_decorator --> request_handlers
    
    _handle_request --> ServerResult
    _handle_request --> ErrorData
```

**Sources:** [src/mcp/server/lowlevel/server.py:625-723](), [src/mcp/server/lowlevel/server.py:152-155](), [src/mcp/server/lowlevel/server.py:238-259]()

The `Server` class maintains handler registries that map message types to handler functions:
- `request_handlers`: Maps request types to async handler functions
- `notification_handlers`: Maps notification types to async handler functions
- Decorator pattern for handler registration (e.g., `@server.list_tools()`)

## Content and Structured Output System

MCP supports both unstructured content and structured data in responses, enabling rich tool outputs and backward compatibility.

```mermaid
graph TB
    subgraph "Content Types"
        TextContent["TextContent<br/>type: 'text', text: str"]
        ImageContent["ImageContent<br/>type: 'image', data: str, mimeType: str"]
        AudioContent["AudioContent<br/>type: 'audio', data: str, mimeType: str"]
        EmbeddedResource["EmbeddedResource<br/>type: 'resource', resource: ResourceContents"]
        ResourceLink["ResourceLink<br/>type: 'resource_link', uri: AnyUrl"]
    end
    
    subgraph "ContentBlock Union"
        ContentBlock["ContentBlock<br/>Union of all content types"]
    end
    
    subgraph "Tool Output Structure"
        CallToolResult_content["CallToolResult<br/>content: list[ContentBlock]<br/>structuredContent: dict | None<br/>isError: bool"]
    end
    
    subgraph "Structured Output Processing"
        StructuredContent_type["StructuredContent<br/>dict[str, Any]"]
        UnstructuredContent_type["UnstructuredContent<br/>Iterable[ContentBlock]"]
        CombinationContent_type["CombinationContent<br/>tuple[Unstructured, Structured]"]
    end
    
    TextContent --> ContentBlock
    ImageContent --> ContentBlock
    AudioContent --> ContentBlock
    EmbeddedResource --> ContentBlock
    ResourceLink --> ContentBlock
    
    ContentBlock --> CallToolResult_content
    StructuredContent_type --> CallToolResult_content
    
    UnstructuredContent_type --> CombinationContent_type
    StructuredContent_type --> CombinationContent_type
```

**Sources:** [src/mcp/types.py:688-782](), [src/mcp/types.py:914-922](), [src/mcp/server/lowlevel/server.py:100-102]()

The content system supports:
- **Unstructured content**: Human-readable content blocks (text, images, audio, resources)
- **Structured content**: Machine-readable JSON data with optional schema validation
- **Combination output**: Both structured and unstructured content in the same response
- **Schema validation**: Optional `outputSchema` validation for structured content

## Protocol Versioning and Capabilities

MCP uses semantic versioning and capability negotiation to ensure compatibility between clients and servers with different feature sets.

```mermaid
graph TB
    subgraph "Version Constants"
        LATEST_PROTOCOL_VERSION["LATEST_PROTOCOL_VERSION<br/>'2025-06-18'"]
        DEFAULT_NEGOTIATED_VERSION["DEFAULT_NEGOTIATED_VERSION<br/>'2025-03-26'"]
    end
    
    subgraph "Capability Exchange"
        ClientCapabilities["ClientCapabilities<br/>sampling, elicitation, roots"]
        ServerCapabilities["ServerCapabilities<br/>prompts, resources, tools, logging, completions"]
        InitializeRequest_caps["InitializeRequest<br/>protocolVersion + clientInfo + capabilities"]
        InitializeResult_caps["InitializeResult<br/>protocolVersion + serverInfo + capabilities"]
    end
    
    subgraph "Individual Capabilities"
        PromptsCapability["PromptsCapability<br/>listChanged: bool"]
        ResourcesCapability["ResourcesCapability<br/>subscribe: bool, listChanged: bool"]
        ToolsCapability["ToolsCapability<br/>listChanged: bool"]
        SamplingCapability["SamplingCapability<br/>create message support"]
        LoggingCapability["LoggingCapability<br/>log message support"]
    end
    
    LATEST_PROTOCOL_VERSION --> InitializeRequest_caps
    DEFAULT_NEGOTIATED_VERSION --> InitializeRequest_caps
    
    ClientCapabilities --> InitializeRequest_caps
    ServerCapabilities --> InitializeResult_caps
    
    PromptsCapability --> ServerCapabilities
    ResourcesCapability --> ServerCapabilities
    ToolsCapability --> ServerCapabilities
    LoggingCapability --> ServerCapabilities
    
    SamplingCapability --> ClientCapabilities
```

**Sources:** [src/mcp/types.py:26-34](), [src/mcp/types.py:265-332](), [src/mcp/types.py:335-365]()

Capability negotiation enables:
- **Protocol versioning**: Semantic version strings for compatibility checking
- **Feature detection**: Clients and servers declare supported capabilities
- **Graceful degradation**: Optional features can be disabled if not supported
- **Extension points**: Experimental capabilities for new features

## Error Handling and Status Codes

MCP defines standardized error codes and error handling patterns based on JSON-RPC 2.0 specifications.

```mermaid
graph TB
    subgraph "Error Code Constants"
        CONNECTION_CLOSED["-32000: CONNECTION_CLOSED"]
        PARSE_ERROR["-32700: PARSE_ERROR"]
        INVALID_REQUEST["-32600: INVALID_REQUEST"]
        METHOD_NOT_FOUND["-32601: METHOD_NOT_FOUND"]
        INVALID_PARAMS["-32602: INVALID_PARAMS"]
        INTERNAL_ERROR["-32603: INTERNAL_ERROR"]
    end
    
    subgraph "Error Structure"
        ErrorData_struct["ErrorData<br/>code: int<br/>message: str<br/>data: Any | None"]
        JSONRPCError_struct["JSONRPCError<br/>jsonrpc: '2.0'<br/>id: RequestId<br/>error: ErrorData"]
    end
    
    subgraph "Error Response Generation"
        McpError["McpError<br/>exception with error data"]
        _make_error_result["Server._make_error_result<br/>creates error CallToolResult"]
    end
    
    CONNECTION_CLOSED --> ErrorData_struct
    PARSE_ERROR --> ErrorData_struct
    METHOD_NOT_FOUND --> ErrorData_struct
    
    ErrorData_struct --> JSONRPCError_struct
    ErrorData_struct --> McpError
    
    McpError --> _make_error_result
```

**Sources:** [src/mcp/types.py:149-179](), [src/mcp/server/lowlevel/server.py:440-447](), [src/mcp/shared/exceptions.py]()

Error handling includes:
- **Standard JSON-RPC codes**: Parse, request, method, and parameter errors
- **MCP-specific codes**: Connection and transport-related errors  
- **Structured error data**: Code, message, and optional additional data
- **Exception mapping**: Python exceptions converted to MCP error responses