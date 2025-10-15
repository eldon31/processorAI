The Client Framework provides the core client-side components for connecting to and interacting with MCP servers. This framework handles session management, protocol communication, request/response patterns, and server capability discovery. It abstracts the underlying transport mechanisms while providing a high-level API for MCP operations.

For information about server-side implementations, see [FastMCP Server Framework](#2) and [Low-Level Server Implementation](#6). For transport-specific client implementations, see [Client Transports](#3.2). For authentication details, see [Client Authentication](#3.3).

## ClientSession Architecture

The `ClientSession` class serves as the primary interface for MCP client applications, built on top of the `BaseSession` foundation for session management and message handling.

```mermaid
graph TB
    subgraph "Client Framework Architecture"
        ClientSession["ClientSession<br/>High-level Client API"]
        BaseSession["BaseSession<br/>Generic Session Management"]
        
        subgraph "Core Components"
            RequestResponder["RequestResponder<br/>Request Lifecycle Management"]
            MessageMetadata["MessageMetadata<br/>Message Context"]
            SessionMessage["SessionMessage<br/>Transport Abstraction"]
        end
        
        subgraph "Protocol Types"
            ClientRequest["ClientRequest<br/>Outbound Requests"]
            ClientResult["ClientResult<br/>Response Types"]
            ServerRequest["ServerRequest<br/>Inbound Requests"]
            ServerNotification["ServerNotification<br/>Server Messages"]
        end
        
        subgraph "Callback System"
            SamplingFnT["SamplingFnT<br/>LLM Sampling Handler"]
            ElicitationFnT["ElicitationFnT<br/>Content Elicitation"]
            ListRootsFnT["ListRootsFnT<br/>Root Directory Listing"]
            LoggingFnT["LoggingFnT<br/>Server Log Handler"]
            MessageHandlerFnT["MessageHandlerFnT<br/>Generic Message Handler"]
        end
        
        subgraph "Stream Infrastructure"
            MemoryObjectReceiveStream["MemoryObjectReceiveStream<br/>Inbound Messages"]
            MemoryObjectSendStream["MemoryObjectSendStream<br/>Outbound Messages"]
        end
    end
    
    ClientSession --> BaseSession
    BaseSession --> RequestResponder
    BaseSession --> SessionMessage
    ClientSession --> SamplingFnT
    ClientSession --> ElicitationFnT
    ClientSession --> ListRootsFnT
    ClientSession --> LoggingFnT
    ClientSession --> MessageHandlerFnT
    
    BaseSession --> MemoryObjectReceiveStream
    BaseSession --> MemoryObjectSendStream
    
    ClientSession --> ClientRequest
    ClientSession --> ServerRequest
    BaseSession --> MessageMetadata
```

**Sources:** [src/mcp/client/session.py:101-136](), [src/mcp/shared/session.py:159-200]()

## Session Lifecycle and Initialization

The client session follows a structured initialization process to establish protocol compatibility and exchange capability information with the server.

```mermaid
sequenceDiagram
    participant Client as "ClientSession"
    participant BaseSession as "BaseSession"
    participant Server as "MCP Server"
    participant Transport as "Transport Layer"
    
    Note over Client,Transport: Session Setup
    Client->>BaseSession: "__aenter__()"
    BaseSession->>BaseSession: "start _receive_loop()"
    
    Note over Client,Server: Protocol Negotiation
    Client->>Server: "InitializeRequest"
    Note right of Client: "protocolVersion: LATEST_PROTOCOL_VERSION<br/>capabilities: ClientCapabilities<br/>clientInfo: Implementation"
    Server->>Client: "InitializeResult"
    Note left of Server: "protocolVersion: negotiated_version<br/>capabilities: ServerCapabilities<br/>serverInfo: Implementation"
    
    Client->>Client: "validate protocol version"
    Client->>Server: "InitializedNotification"
    
    Note over Client,Server: Ready for Operations
    Client->>Server: "ListToolsRequest"
    Client->>Server: "CallToolRequest"
    Client->>Server: "ListResourcesRequest"
```

**Sources:** [src/mcp/client/session.py:137-174](), [tests/client/test_session.py:30-114]()

## Request and Response Handling

The framework implements a sophisticated request/response system with progress tracking, timeout management, and structured validation.

### Core Request Methods

| Method | Purpose | Request Type | Response Type |
|--------|---------|--------------|---------------|
| `call_tool()` | Execute server tools | `CallToolRequest` | `CallToolResult` |
| `list_tools()` | Discover available tools | `ListToolsRequest` | `ListToolsResult` |
| `read_resource()` | Access server resources | `ReadResourceRequest` | `ReadResourceResult` |
| `list_resources()` | Discover available resources | `ListResourcesRequest` | `ListResourcesResult` |
| `get_prompt()` | Retrieve prompt templates | `GetPromptRequest` | `GetPromptResult` |
| `complete()` | Get completion suggestions | `CompleteRequest` | `CompleteResult` |

**Sources:** [src/mcp/client/session.py:270-297](), [src/mcp/client/session.py:366-383]()

### Tool Output Validation

The client automatically validates structured tool outputs against server-provided schemas:

```mermaid
graph LR
    subgraph "Tool Validation Process"
        CallTool["call_tool(name, args)"]
        ListTools["list_tools()"]
        SchemaCache["_tool_output_schemas<br/>dict[str, dict]"]
        ValidateResult["_validate_tool_result()"]
        JSONSchema["JSON Schema Validation"]
        
        CallTool --> ValidateResult
        ValidateResult --> SchemaCache
        SchemaCache --> ListTools
        ValidateResult --> JSONSchema
        
        ValidationError["ValidationError<br/>Invalid structured content"]
        SchemaError["SchemaError<br/>Invalid schema definition"]
        
        JSONSchema --> ValidationError
        JSONSchema --> SchemaError
    end
```

**Sources:** [src/mcp/client/session.py:298-319](), [src/mcp/client/session.py:377-381]()

## Progress and Notification System

The client framework supports bidirectional progress reporting and server-initiated notifications through callback functions and progress tokens.

### Progress Callback Integration

```mermaid
graph TB
    subgraph "Progress System"
        SendRequest["send_request()<br/>with progress_callback"]
        ProgressToken["Progress Token<br/>request_id as token"]
        CallbackStore["_progress_callbacks<br/>dict[RequestId, ProgressFnT]"]
        
        subgraph "Server Side"
            ServerProgress["Server sends<br/>ProgressNotification"]
        end
        
        subgraph "Client Processing"
            ReceiveLoop["_receive_loop()"]
            HandleProgress["Handle ProgressNotification"]
            InvokeCallback["Invoke progress_callback()"]
        end
        
        SendRequest --> ProgressToken
        ProgressToken --> CallbackStore
        ServerProgress --> ReceiveLoop
        ReceiveLoop --> HandleProgress
        HandleProgress --> CallbackStore
        CallbackStore --> InvokeCallback
    end
```

**Sources:** [src/mcp/shared/session.py:242-253](), [src/mcp/shared/session.py:389-399]()

### Server Request Handling

The client can handle server-initiated requests through configurable callback functions:

| Callback Type | Purpose | Default Behavior |
|---------------|---------|------------------|
| `SamplingFnT` | Handle LLM sampling requests | Returns "not supported" error |
| `ElicitationFnT` | Handle content elicitation | Returns "not supported" error |
| `ListRootsFnT` | Handle root directory listing | Returns "not supported" error |
| `LoggingFnT` | Handle server log messages | No-op (silent) |
| `MessageHandlerFnT` | Handle all incoming messages | No-op checkpoint |

**Sources:** [src/mcp/client/session.py:21-96](), [src/mcp/client/session.py:388-434]()

## Transport Integration

The client framework abstracts transport details through stream-based interfaces, allowing it to work with various transport mechanisms.

```mermaid
graph TB
    subgraph "Transport Abstraction Layer"
        subgraph "Client Session"
            ClientSession_transport["ClientSession"]
            StreamInterfaces["Stream Interfaces<br/>MemoryObjectReceiveStream<br/>MemoryObjectSendStream"]
        end
        
        subgraph "Transport Implementations"
            StdioClient["stdio_client<br/>Process Communication"]
            SSEClient["sse_client<br/>HTTP Server-Sent Events"]
            StreamableHTTPClient["streamablehttp_client<br/>Bidirectional HTTP"]
        end
        
        subgraph "Message Layer"
            SessionMessage_transport["SessionMessage<br/>Transport Envelope"]
            JSONRPCMessage["JSONRPCMessage<br/>Protocol Content"]
            MessageMetadata_transport["MessageMetadata<br/>Transport Context"]
        end
        
        ClientSession_transport --> StreamInterfaces
        StdioClient --> StreamInterfaces
        SSEClient --> StreamInterfaces
        StreamableHTTPClient --> StreamInterfaces
        
        StreamInterfaces --> SessionMessage_transport
        SessionMessage_transport --> JSONRPCMessage
        SessionMessage_transport --> MessageMetadata_transport
    end
```

**Sources:** [src/mcp/client/session.py:110-128](), [src/mcp/client/__main__.py:36-64]()

## Testing and Development Utilities

The framework includes memory-based transport utilities for testing and development scenarios.

### Memory Transport Factory

The `create_connected_server_and_client_session()` function provides a complete testing environment with in-memory communication:

```mermaid
graph LR
    subgraph "Memory Transport Setup"
        CreateStreams["create_client_server_memory_streams()"]
        ClientStreams["Client Streams<br/>read: server_to_client_receive<br/>write: client_to_server_send"]
        ServerStreams["Server Streams<br/>read: client_to_server_receive<br/>write: server_to_client_send"]
        
        ClientSession_memory["ClientSession<br/>connected to memory streams"]
        ServerInstance["Server Instance<br/>running in task group"]
        
        CreateStreams --> ClientStreams
        CreateStreams --> ServerStreams
        ClientStreams --> ClientSession_memory
        ServerStreams --> ServerInstance
    end
```

**Sources:** [src/mcp/shared/memory.py:28-50](), [src/mcp/shared/memory.py:53-99]()

### Error Handling and Exception Management

The client framework provides comprehensive error handling for various failure scenarios:

| Error Type | Source | Handling |
|------------|--------|----------|
| `TimeoutError` | Request timeout | Converted to `McpError` with timeout details |
| `JSONRPCError` | Server error response | Converted to `McpError` with server error |
| `ValidationError` | Tool output validation | Runtime error with validation details |
| `anyio.ClosedResourceError` | Transport closure | Graceful session termination |
| `RuntimeError` | Protocol version mismatch | Immediate session failure |

**Sources:** [src/mcp/shared/session.py:273-283](), [src/mcp/shared/session.py:416-436](), [src/mcp/client/session.py:314-318]()