The FastMCP Client System provides a programmatic interface for interacting with Model Context Protocol (MCP) servers through a well-typed, Pythonic API. This system handles protocol operations, connection management, and session lifecycle while abstracting away transport-specific implementation details.

For information about creating and configuring MCP servers, see [FastMCP Server Core](#2). For details about HTTP server deployment and authentication, see [HTTP Server and Deployment](#6).

## Core Architecture

The FastMCP Client System implements a separation of concerns between protocol handling and connection management through two primary components:

| Component | Responsibility | Key Classes |
|-----------|----------------|-------------|
| **Client** | MCP protocol operations, session management, callback handling | `Client` |
| **Transport** | Connection establishment, communication channel management | `ClientTransport`, `SSETransport`, `StreamableHttpTransport`, `StdioTransport`, `FastMCPTransport` |

### Client-Transport Relationship

```mermaid
graph TB
    subgraph "Client Layer"
        Client["Client<br/>• Protocol operations<br/>• Session lifecycle<br/>• Callback handling<br/>• Type conversion"]
    end
    
    subgraph "Transport Layer"
        Transport["ClientTransport (Abstract)"]
        
        StdioTransport["StdioTransport<br/>• Subprocess management<br/>• Environment isolation"]
        HttpTransports["HTTP Transports<br/>• StreamableHttpTransport<br/>• SSETransport"]
        FastMCPTransport["FastMCPTransport<br/>• In-memory communication"]
        MCPConfigTransport["MCPConfigTransport<br/>• Multi-server composition"]
        
        Transport --> StdioTransport
        Transport --> HttpTransports
        Transport --> FastMCPTransport
        Transport --> MCPConfigTransport
    end
    
    Client --> Transport
```

**Sources**: [src/fastmcp/client/client.py:90-149](), [src/fastmcp/client/transports.py:71-115]()

The `Client` class uses generic typing to preserve specific transport types, enabling transport-specific configuration while maintaining a consistent protocol interface.

### Transport Inference

The client automatically selects appropriate transports based on input type:

```mermaid
flowchart TD
    Input["Client Input"] --> FastMCPCheck{"FastMCP instance?"}
    FastMCPCheck -->|Yes| FastMCPTransport["FastMCPTransport<br/>In-memory communication"]
    
    FastMCPCheck -->|No| PathCheck{"File path?"}
    PathCheck -->|.py extension| PythonStdio["PythonStdioTransport<br/>Python subprocess"]
    PathCheck -->|.js extension| NodeStdio["NodeStdioTransport<br/>Node.js subprocess"]
    
    PathCheck -->|No| URLCheck{"HTTP URL?"}
    URLCheck -->|Yes| HTTPTransport["StreamableHttpTransport<br/>or SSETransport"]
    
    URLCheck -->|No| ConfigCheck{"MCPConfig dict?"}
    ConfigCheck -->|Yes| ConfigTransport["MCPConfigTransport<br/>Multi-server client"]
```

**Sources**: [src/fastmcp/client/transports.py:888-924](), [src/fastmcp/client/client.py:150-221]()

## Client Session Management

The `Client` implements a sophisticated session management system supporting reentrant context managers and concurrent usage patterns.

### Session State Architecture

```mermaid
graph LR
    subgraph "ClientSessionState"
        Session["session: ClientSession | None"]
        Counter["nesting_counter: int"]
        Lock["lock: anyio.Lock"]
        Task["session_task: asyncio.Task | None"]
        ReadyEvent["ready_event: anyio.Event"]
        StopEvent["stop_event: anyio.Event"]
        InitResult["initialize_result: InitializeResult | None"]
    end
    
    subgraph "Session Runner Task"
        Runner["_session_runner()<br/>• Background session management<br/>• Connection lifecycle<br/>• Event coordination"]
    end
    
    Task --> Runner
    ReadyEvent --> Runner
    StopEvent --> Runner
```

**Sources**: [src/fastmcp/client/client.py:73-88](), [src/fastmcp/client/client.py:451-474]()

### Connection Lifecycle

The client manages connection lifecycle through reference counting and background session management:

```mermaid
sequenceDiagram
    participant App as "Application Code"
    participant Client as "Client.__aenter__"
    participant State as "ClientSessionState"
    participant Runner as "Session Runner Task"
    participant Transport as "Transport"

    App->>Client: "async with client"
    Client->>State: "Acquire lock"
    
    alt "First connection"
        Client->>State: "Create events, start task"
        Client->>Runner: "Start _session_runner()"
        Runner->>Transport: "connect_session()"
        Runner->>State: "Set ready_event"
    else "Nested connection"
        Client->>State: "Wait for ready_event"
    end
    
    Client->>State: "Increment nesting_counter"
    Client-->>App: "Return self"
    
    Note over App: "Use client methods"
    
    App->>Client: "Exit context"
    Client->>State: "Acquire lock, decrement counter"
    
    alt "Last connection"
        Client->>State: "Set stop_event"
        Runner->>State: "Clean up session"
    end
```

**Sources**: [src/fastmcp/client/client.py:367-411](), [src/fastmcp/client/client.py:413-449]()

## Transport System

### Transport Interface

All transports implement the `ClientTransport` abstract base class:

```mermaid
classDiagram
    class ClientTransport {
        <<abstract>>
        +connect_session(**kwargs) AsyncIterator[ClientSession]
        +close() None
        +_set_auth(auth) None
    }
    
    class StdioTransport {
        +command: str
        +args: list[str]
        +env: dict | None
        +keep_alive: bool
        +connect() ClientSession
        +disconnect() None
    }
    
    class StreamableHttpTransport {
        +url: str
        +headers: dict
        +auth: httpx.Auth
        +sse_read_timeout: timedelta
    }
    
    class FastMCPTransport {
        +server: FastMCP
        +raise_exceptions: bool
    }
    
    class MCPConfigTransport {
        +config: MCPConfig
        +transport: ClientTransport
        +_composite_server: FastMCP
    }
    
    ClientTransport <|-- StdioTransport
    ClientTransport <|-- StreamableHttpTransport
    ClientTransport <|-- FastMCPTransport
    ClientTransport <|-- MCPConfigTransport
```

**Sources**: [src/fastmcp/client/transports.py:71-115](), [src/fastmcp/client/transports.py:301-417]()

### STDIO Transport Environment Management

STDIO transports implement environment isolation for security:

```mermaid
graph LR
    subgraph "Client Process"
        ClientEnv["Client Environment<br/>API_KEY=secret<br/>PATH=/usr/bin"]
    end
    
    subgraph "Server Subprocess"
        ServerEnv["Isolated Environment<br/>Only explicitly passed vars"]
        StdioServer["MCP Server Process"]
        ServerEnv --> StdioServer
    end
    
    ClientEnv -.->|"Explicit env parameter"| ServerEnv
    ClientEnv -->|"stdin/stdout pipes"| StdioServer
```

**Sources**: [src/fastmcp/client/transports.py:301-417](), [src/fastmcp/client/transports.py:465-508]()

## Client Protocol Operations

The `Client` class provides methods for all MCP protocol operations, with both raw protocol and convenience variants:

### Tool Operations

| Method | Return Type | Description |
|--------|-------------|-------------|
| `list_tools()` | `list[mcp.types.Tool]` | List available tools |
| `list_tools_mcp()` | `mcp.types.ListToolsResult` | Raw MCP protocol result |
| `call_tool()` | `CallToolResult` | Execute tool with type conversion |
| `call_tool_mcp()` | `mcp.types.CallToolResult` | Raw MCP tool execution |

**Sources**: [src/fastmcp/client/client.py:763-895]()

### Resource Operations

| Method | Return Type | Description |
|--------|-------------|-------------|
| `list_resources()` | `list[mcp.types.Resource]` | List available resources |
| `list_resource_templates()` | `list[mcp.types.ResourceTemplate]` | List URI templates |
| `read_resource()` | `list[mcp.types.TextResourceContents \| BlobResourceContents]` | Read resource contents |

**Sources**: [src/fastmcp/client/client.py:525-636]()

### Prompt Operations

| Method | Return Type | Description |
|--------|-------------|-------------|
| `list_prompts()` | `list[mcp.types.Prompt]` | List available prompts |
| `get_prompt()` | `mcp.types.GetPromptResult` | Render prompt with arguments |

**Sources**: [src/fastmcp/client/client.py:639-716]()

### Tool Result Processing

The client provides structured result handling through the `CallToolResult` dataclass:

```mermaid
graph TB
    subgraph "Tool Call Processing"
        CallTool["call_tool()"] --> ParseResult["Parse MCP Result"]
        ParseResult --> CheckError{"isError?"}
        
        CheckError -->|Yes| RaiseError["Raise ToolError"]
        CheckError -->|No| CheckStructured{"Has structured content?"}
        
        CheckStructured -->|Yes| ParseSchema["Parse with JSON schema"]
        CheckStructured -->|No| ReturnContent["Return text content"]
        
        ParseSchema --> TypeConvert["Convert to Python types"]
        
        ReturnContent --> Result["CallToolResult"]
        TypeConvert --> Result
    end
```

**Sources**: [src/fastmcp/client/client.py:826-894](), [src/fastmcp/client/client.py:897-903]()

## Client Configuration and Handlers

### Handler System

The client supports multiple callback handlers for server interactions:

| Handler Type | Purpose | Interface |
|--------------|---------|-----------|
| `LogHandler` | Process server log messages | `(LogMessage) -> Awaitable[None]` |
| `ProgressHandler` | Monitor operation progress | `(float, float?, str?) -> Awaitable[None]` |
| `SamplingHandler` | Respond to LLM sampling requests | Complex sampling interface |
| `RootsHandler` | Provide filesystem roots | `() -> RootsList` |

**Sources**: [src/fastmcp/client/client.py:210-267]()

### Client Factory Pattern

The client constructor uses overloaded signatures to support transport inference while maintaining type safety:

```mermaid
graph LR
    subgraph "Constructor Overloads"
        TransportT["Client[T](transport: T)"]
        URLOverload["Client[HttpTransport](url: AnyUrl)"]
        FastMCPOverload["Client[FastMCPTransport](server: FastMCP)"]
        PathOverload["Client[StdioTransport](path: Path)"]
        ConfigOverload["Client[MCPConfigTransport](config: MCPConfig)"]
    end
    
    subgraph "Transport Creation"
        InferTransport["infer_transport()"]
    end
    
    URLOverload --> InferTransport
    FastMCPOverload --> InferTransport
    PathOverload --> InferTransport
    ConfigOverload --> InferTransport
```

**Sources**: [src/fastmcp/client/client.py:150-221](), [src/fastmcp/client/transports.py:888-924]()

## Integration with Server Composition

The client system integrates with FastMCP's server composition patterns through several mechanisms:

### Proxy Client Usage

```mermaid
graph TB
    subgraph "Proxy Server Pattern"
        ProxyServer["FastMCPProxy"] --> ProxyClient["Client instance"]
        ProxyClient --> Transport["ClientTransport"]
        Transport --> BackendServer["Backend MCP Server"]
    end
    
    subgraph "Client Access"
        UserClient["User Client"] --> ProxyServer
    end
```

**Sources**: [docs/servers/proxy.mdx:278-329](), [examples/in_memory_proxy_example.py:40-50]()

### Multi-Server Configuration

The `MCPConfigTransport` enables single-client access to multiple servers through automatic composition:

```mermaid
graph LR
    subgraph "MCPConfig Client"
        Client["Client"] --> MCPConfigTransport["MCPConfigTransport"]
        MCPConfigTransport --> CompositeServer["FastMCP Composite"]
    end
    
    subgraph "Backend Servers"
        CompositeServer --> ServerA["Weather Server<br/>weather_* tools"]
        CompositeServer --> ServerB["Calendar Server<br/>calendar_* tools"]
    end
```

**Sources**: [src/fastmcp/client/transports.py:817-887](), [docs/clients/client.mdx:124-142]()