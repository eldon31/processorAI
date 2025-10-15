The Model Context Protocol (MCP) Python SDK is a comprehensive framework for building servers and clients that enable Large Language Models to access external tools, data, and services in a standardized way. This SDK implements the complete MCP specification, providing both high-level developer-friendly APIs and low-level protocol implementations.

The SDK enables developers to create MCP servers that expose resources (data), tools (functions), and prompts (templates) to LLM applications, as well as MCP clients that can discover and interact with these servers. For detailed implementation guidance on building servers, see [FastMCP Server Framework](#2). For client development, see [Client Framework](#3). For protocol-level details, see [Protocol & Message System](#4).

## System Architecture

The MCP Python SDK is organized into several distinct layers, each serving specific roles in the protocol implementation:

```mermaid
graph TB
    subgraph "Application Layer"
        UserServers["User MCP Servers<br/>(@tool, @resource, @prompt decorators)"]
        UserClients["User MCP Clients<br/>(ClientSession usage)"]
        CLI["mcp CLI<br/>(dev, run, install commands)"]
    end
    
    subgraph "High-Level Frameworks"
        FastMCP["FastMCP<br/>(mcp.server.fastmcp.FastMCP)"]
        ClientSession["ClientSession<br/>(mcp.ClientSession)"]
    end
    
    subgraph "Core Protocol Layer"
        LowLevelServer["Server<br/>(mcp.server.lowlevel.Server)"]
        BaseSession["BaseSession<br/>(mcp.shared.session.BaseSession)"]
        Types["mcp.types<br/>(Protocol Message Definitions)"]
    end
    
    subgraph "Transport Layer"
        StdioTransport["stdio<br/>(mcp.server.stdio, mcp.client.stdio)"]
        SSETransport["sse<br/>(mcp.server.sse, mcp.client.sse)"] 
        StreamableHTTP["streamable-http<br/>(mcp.server.streamablehttp)"]
    end
    
    subgraph "Authentication Layer"
        TokenVerifier["TokenVerifier<br/>(mcp.server.auth.provider)"]
        OAuthClient["OAuthClientProvider<br/>(mcp.client.auth.provider)"]
    end
    
    %% User layer connections
    UserServers --> FastMCP
    UserClients --> ClientSession
    CLI --> FastMCP
    
    %% Framework connections
    FastMCP --> LowLevelServer
    ClientSession --> BaseSession
    
    %% Core connections
    LowLevelServer --> Types
    BaseSession --> Types
    
    %% Transport connections
    LowLevelServer -.-> StdioTransport
    LowLevelServer -.-> SSETransport
    LowLevelServer -.-> StreamableHTTP
    ClientSession -.-> StdioTransport
    ClientSession -.-> SSETransport
    ClientSession -.-> StreamableHTTP
    
    %% Auth connections
    FastMCP --> TokenVerifier
    ClientSession --> OAuthClient
```

**Sources:** [README.md:1-1770](), [src/mcp/server/lowlevel/server.py:1-727](), [src/mcp/types.py:1-1349]()

## Core Components

### Protocol Foundation

The MCP SDK is built on JSON-RPC 2.0 messaging with well-defined protocol types. The `mcp.types` module contains all protocol message definitions, including requests, responses, and notifications that flow between clients and servers.

```mermaid
graph LR
    subgraph "Protocol Types (mcp.types)"
        ClientRequest["ClientRequest<br/>(InitializeRequest, CallToolRequest, etc.)"]
        ServerResult["ServerResult<br/>(CallToolResult, ListToolsResult, etc.)"]
        Notifications["Notifications<br/>(ProgressNotification, LoggingMessageNotification)"]
    end
    
    subgraph "Core Protocol Classes"
        JSONRPCRequest["JSONRPCRequest<br/>(id, method, params)"]
        JSONRPCResponse["JSONRPCResponse<br/>(id, result)"]
        JSONRPCError["JSONRPCError<br/>(id, error)"]
    end
    
    subgraph "Session Management"
        BaseSession["BaseSession<br/>(mcp.shared.session)"]
        ServerSession["ServerSession<br/>(mcp.server.session)"]
        RequestResponder["RequestResponder<br/>(mcp.shared.session)"]
    end
    
    ClientRequest --> JSONRPCRequest
    ServerResult --> JSONRPCResponse
    JSONRPCError --> ServerResult
    
    BaseSession --> RequestResponder
    ServerSession --> BaseSession
```

**Sources:** [src/mcp/types.py:124-192](), [src/mcp/types.py:1248-1349]()

### Server Implementations

The SDK provides two primary approaches for building MCP servers:

**FastMCP Framework** - A decorator-based high-level framework that automatically handles protocol compliance, schema generation, and transport integration. Users define tools, resources, and prompts using Python decorators.

**Low-Level Server** - Direct protocol implementation providing full control over message handling, lifecycle management, and custom protocol extensions.

```mermaid
graph TB
    subgraph "FastMCP Framework (mcp.server.fastmcp)"
        FastMCPClass["FastMCP"]
        ToolDecorator["@mcp.tool()"]
        ResourceDecorator["@mcp.resource()"]
        PromptDecorator["@mcp.prompt()"]
        Context["Context[ServerSession, LifespanContext]"]
    end
    
    subgraph "Low-Level Server (mcp.server.lowlevel)"
        ServerClass["Server[LifespanResultT, RequestT]"]
        ListToolsHandler["@server.list_tools()"]
        CallToolHandler["@server.call_tool()"]
        RequestContext["request_ctx: ContextVar"]
    end
    
    subgraph "Common Infrastructure"
        ServerSession["ServerSession"]
        ToolManager["ToolManager"]
        FuncMetadata["func_metadata"]
    end
    
    ToolDecorator --> ToolManager
    ResourceDecorator --> ToolManager
    PromptDecorator --> ToolManager
    FastMCPClass --> ServerClass
    
    ListToolsHandler --> ServerClass
    CallToolHandler --> ServerClass
    
    ServerClass --> ServerSession
    ToolManager --> FuncMetadata
    Context --> ServerSession
    RequestContext --> ServerSession
```

**Sources:** [README.md:138-170](), [src/mcp/server/lowlevel/server.py:133-158]()

### Client Framework

The client framework centers around `ClientSession` which provides high-level methods for discovering and interacting with MCP servers. It handles transport abstraction, authentication, and protocol message management.

```mermaid
graph LR
    subgraph "Client API (mcp.client)"
        ClientSession["ClientSession"]
        StdioClient["stdio_client"]
        SSEClient["sse_client"] 
        StreamableClient["streamablehttp_client"]
    end
    
    subgraph "Client Operations"
        Initialize["session.initialize()"]
        ListTools["session.list_tools()"]
        CallTool["session.call_tool()"]
        ReadResource["session.read_resource()"]
    end
    
    subgraph "Authentication (mcp.client.auth)"
        OAuthProvider["OAuthClientProvider"]
        TokenStorage["TokenStorage"]
    end
    
    ClientSession --> StdioClient
    ClientSession --> SSEClient
    ClientSession --> StreamableClient
    
    ClientSession --> Initialize
    ClientSession --> ListTools
    ClientSession --> CallTool
    ClientSession --> ReadResource
    
    ClientSession --> OAuthProvider
    OAuthProvider --> TokenStorage
```

**Sources:** [README.md:660-733]()

### Transport Layer

The SDK supports three transport mechanisms for MCP communication, each suited for different deployment scenarios:

| Transport | Use Case | Implementation |
|-----------|----------|----------------|
| `stdio` | Process-based servers, development | `mcp.server.stdio`, `mcp.client.stdio` |
| `sse` | Real-time web applications | `mcp.server.sse`, `mcp.client.sse` |
| `streamable-http` | Production HTTP deployments | `mcp.server.streamablehttp` |

**Sources:** [README.md:1104-1217]()

## Development Workflow

The SDK includes comprehensive development tools accessible through the `mcp` CLI:

```mermaid
graph TB
    subgraph "Development Commands"
        McpDev["mcp dev server.py<br/>(MCP Inspector)"]
        McpRun["mcp run server.py<br/>(Direct execution)"]
        McpInstall["mcp install server.py<br/>(Claude Desktop integration)"]
    end
    
    subgraph "Server Types"
        FastMCPServer["FastMCP Server<br/>(Decorator-based)"]
        LowLevelServer["Low-Level Server<br/>(Protocol handlers)"]
    end
    
    subgraph "Target Environments"
        Inspector["MCP Inspector<br/>(Development)"]
        ClaudeDesktop["Claude Desktop<br/>(Production)"]
        DirectExecution["Direct Process<br/>(Custom deployment)"]
    end
    
    McpDev --> FastMCPServer
    McpRun --> FastMCPServer
    McpInstall --> FastMCPServer
    
    McpDev --> Inspector
    McpInstall --> ClaudeDesktop
    McpRun --> DirectExecution
    
    FastMCPServer -.-> LowLevelServer
```

**Sources:** [README.md:1027-1102]()

For specific implementation details on each component, refer to the dedicated sections: [FastMCP Server Framework](#2) for high-level server development, [Client Framework](#3) for client implementation, [Transport Layer](#5) for communication mechanisms, and [Development Tools & CLI](#8) for development workflow.

# Overview

The Model Context Protocol (MCP) Python SDK is a comprehensive framework for building servers and clients that enable Large Language Models to access external tools, data, and services in a standardized way. This SDK implements the complete MCP specification, providing both high-level developer-friendly APIs and low-level protocol implementations.

The SDK enables developers to create MCP servers that expose resources (data), tools (functions), and prompts (templates) to LLM applications, as well as MCP clients that can discover and interact with these servers. For detailed implementation guidance on building servers, see [FastMCP Server Framework](#2). For client development, see [Client Framework](#3). For protocol-level details, see [Protocol & Message System](#4).

## System Architecture

The MCP Python SDK is organized into several distinct layers, each serving specific roles in the protocol implementation:

```mermaid
graph TB
    subgraph "Application Layer"
        UserServers["User MCP Servers<br/>(@tool, @resource, @prompt decorators)"]
        UserClients["User MCP Clients<br/>(ClientSession usage)"]
        CLI["mcp CLI<br/>(dev, run, install commands)"]
    end
    
    subgraph "High-Level Frameworks"
        FastMCP["FastMCP<br/>(mcp.server.fastmcp.FastMCP)"]
        ClientSession["ClientSession<br/>(mcp.ClientSession)"]
    end
    
    subgraph "Core Protocol Layer"
        LowLevelServer["Server<br/>(mcp.server.lowlevel.Server)"]
        BaseSession["BaseSession<br/>(mcp.shared.session.BaseSession)"]
        Types["mcp.types<br/>(Protocol Message Definitions)"]
    end
    
    subgraph "Transport Layer"
        StdioTransport["stdio<br/>(mcp.server.stdio, mcp.client.stdio)"]
        SSETransport["sse<br/>(mcp.server.sse, mcp.client.sse)"] 
        StreamableHTTP["streamable-http<br/>(mcp.server.streamablehttp)"]
    end
    
    subgraph "Authentication Layer"
        TokenVerifier["TokenVerifier<br/>(mcp.server.auth.provider)"]
        OAuthClient["OAuthClientProvider<br/>(mcp.client.auth.provider)"]
    end
    
    %% User layer connections
    UserServers --> FastMCP
    UserClients --> ClientSession
    CLI --> FastMCP
    
    %% Framework connections
    FastMCP --> LowLevelServer
    ClientSession --> BaseSession
    
    %% Core connections
    LowLevelServer --> Types
    BaseSession --> Types
    
    %% Transport connections
    LowLevelServer -.-> StdioTransport
    LowLevelServer -.-> SSETransport
    LowLevelServer -.-> StreamableHTTP
    ClientSession -.-> StdioTransport
    ClientSession -.-> SSETransport
    ClientSession -.-> StreamableHTTP
    
    %% Auth connections
    FastMCP --> TokenVerifier
    ClientSession --> OAuthClient
```

**Sources:** [README.md:1-1770](), [src/mcp/server/lowlevel/server.py:1-727](), [src/mcp/types.py:1-1349]()

## Core Components

### Protocol Foundation

The MCP SDK is built on JSON-RPC 2.0 messaging with well-defined protocol types. The `mcp.types` module contains all protocol message definitions, including requests, responses, and notifications that flow between clients and servers.

```mermaid
graph LR
    subgraph "Protocol Types (mcp.types)"
        ClientRequest["ClientRequest<br/>(InitializeRequest, CallToolRequest, etc.)"]
        ServerResult["ServerResult<br/>(CallToolResult, ListToolsResult, etc.)"]
        Notifications["Notifications<br/>(ProgressNotification, LoggingMessageNotification)"]
    end
    
    subgraph "Core Protocol Classes"
        JSONRPCRequest["JSONRPCRequest<br/>(id, method, params)"]
        JSONRPCResponse["JSONRPCResponse<br/>(id, result)"]
        JSONRPCError["JSONRPCError<br/>(id, error)"]
    end
    
    subgraph "Session Management"
        BaseSession["BaseSession<br/>(mcp.shared.session)"]
        ServerSession["ServerSession<br/>(mcp.server.session)"]
        RequestResponder["RequestResponder<br/>(mcp.shared.session)"]
    end
    
    ClientRequest --> JSONRPCRequest
    ServerResult --> JSONRPCResponse
    JSONRPCError --> ServerResult
    
    BaseSession --> RequestResponder
    ServerSession --> BaseSession
```

**Sources:** [src/mcp/types.py:124-192](), [src/mcp/types.py:1248-1349]()

### Server Implementations

The SDK provides two primary approaches for building MCP servers:

**FastMCP Framework** - A decorator-based high-level framework that automatically handles protocol compliance, schema generation, and transport integration. Users define tools, resources, and prompts using Python decorators.

**Low-Level Server** - Direct protocol implementation providing full control over message handling, lifecycle management, and custom protocol extensions.

```mermaid
graph TB
    subgraph "FastMCP Framework (mcp.server.fastmcp)"
        FastMCPClass["FastMCP"]
        ToolDecorator["@mcp.tool()"]
        ResourceDecorator["@mcp.resource()"]
        PromptDecorator["@mcp.prompt()"]
        Context["Context[ServerSession, LifespanContext]"]
    end
    
    subgraph "Low-Level Server (mcp.server.lowlevel)"
        ServerClass["Server[LifespanResultT, RequestT]"]
        ListToolsHandler["@server.list_tools()"]
        CallToolHandler["@server.call_tool()"]
        RequestContext["request_ctx: ContextVar"]
    end
    
    subgraph "Common Infrastructure"
        ServerSession["ServerSession"]
        ToolManager["ToolManager"]
        FuncMetadata["func_metadata"]
    end
    
    ToolDecorator --> ToolManager
    ResourceDecorator --> ToolManager
    PromptDecorator --> ToolManager
    FastMCPClass --> ServerClass
    
    ListToolsHandler --> ServerClass
    CallToolHandler --> ServerClass
    
    ServerClass --> ServerSession
    ToolManager --> FuncMetadata
    Context --> ServerSession
    RequestContext --> ServerSession
```

**Sources:** [README.md:138-170](), [src/mcp/server/lowlevel/server.py:133-158]()

### Client Framework

The client framework centers around `ClientSession` which provides high-level methods for discovering and interacting with MCP servers. It handles transport abstraction, authentication, and protocol message management.

```mermaid
graph LR
    subgraph "Client API (mcp.client)"
        ClientSession["ClientSession"]
        StdioClient["stdio_client"]
        SSEClient["sse_client"] 
        StreamableClient["streamablehttp_client"]
    end
    
    subgraph "Client Operations"
        Initialize["session.initialize()"]
        ListTools["session.list_tools()"]
        CallTool["session.call_tool()"]
        ReadResource["session.read_resource()"]
    end
    
    subgraph "Authentication (mcp.client.auth)"
        OAuthProvider["OAuthClientProvider"]
        TokenStorage["TokenStorage"]
    end
    
    ClientSession --> StdioClient
    ClientSession --> SSEClient
    ClientSession --> StreamableClient
    
    ClientSession --> Initialize
    ClientSession --> ListTools
    ClientSession --> CallTool
    ClientSession --> ReadResource
    
    ClientSession --> OAuthProvider
    OAuthProvider --> TokenStorage
```

**Sources:** [README.md:660-733]()

### Transport Layer

The SDK supports three transport mechanisms for MCP communication, each suited for different deployment scenarios:

| Transport | Use Case | Implementation |
|-----------|----------|----------------|
| `stdio` | Process-based servers, development | `mcp.server.stdio`, `mcp.client.stdio` |
| `sse` | Real-time web applications | `mcp.server.sse`, `mcp.client.sse` |
| `streamable-http` | Production HTTP deployments | `mcp.server.streamablehttp` |

**Sources:** [README.md:1104-1217]()

## Development Workflow

The SDK includes comprehensive development tools accessible through the `mcp` CLI:

```mermaid
graph TB
    subgraph "Development Commands"
        McpDev["mcp dev server.py<br/>(MCP Inspector)"]
        McpRun["mcp run server.py<br/>(Direct execution)"]
        McpInstall["mcp install server.py<br/>(Claude Desktop integration)"]
    end
    
    subgraph "Server Types"
        FastMCPServer["FastMCP Server<br/>(Decorator-based)"]
        LowLevelServer["Low-Level Server<br/>(Protocol handlers)"]
    end
    
    subgraph "Target Environments"
        Inspector["MCP Inspector<br/>(Development)"]
        ClaudeDesktop["Claude Desktop<br/>(Production)"]
        DirectExecution["Direct Process<br/>(Custom deployment)"]
    end
    
    McpDev --> FastMCPServer
    McpRun --> FastMCPServer
    McpInstall --> FastMCPServer
    
    McpDev --> Inspector
    McpInstall --> ClaudeDesktop
    McpRun --> DirectExecution
    
    FastMCPServer -.-> LowLevelServer
```

**Sources:** [README.md:1027-1102]()

For specific implementation details on each component, refer to the dedicated sections: [FastMCP Server Framework](#2) for high-level server development, [Client Framework](#3) for client implementation, [Transport Layer](#5) for communication mechanisms, and [Development Tools & CLI](#8) for development workflow.