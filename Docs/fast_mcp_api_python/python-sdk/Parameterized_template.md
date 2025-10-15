@server.resource("data://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    return f"Profile for user {user_id}"
```

The framework automatically detects whether a resource should be treated as a template based on URI parameters and function signature.

Sources: [src/mcp/server/fastmcp/server.py:479-578](), [tests/server/fastmcp/test_server.py:701-827]()

### Prompt Registration

Prompts are registered using the `@prompt()` decorator and return message structures:

```python
@server.prompt()
def analyze_data(dataset_name: str) -> str:
    """Generate analysis prompt for a dataset."""
    return f"Please analyze the dataset: {dataset_name}"
```

Sources: [src/mcp/server/fastmcp/server.py:588-641](), [tests/server/fastmcp/test_server.py:1094-1284]()

## Context System

### Context Injection

The `Context` class provides access to MCP capabilities and is automatically injected into functions that declare it as a parameter:

```mermaid
graph TB
    subgraph "Context Injection Flow"
        FunctionCall["Function Call"]
        ParameterDetection["find_context_parameter()"]
        ContextCreation["get_context()"]
        ContextInjection["Context Injection"]
        FunctionExecution["Function Execution"]
    end
    
    subgraph "Context Capabilities"
        Logging["ctx.log(), ctx.info(), ctx.debug()"]
        Progress["ctx.report_progress()"]
        ResourceAccess["ctx.read_resource()"]
        RequestInfo["ctx.request_id, ctx.client_id"]
    end
    
    FunctionCall --> ParameterDetection
    ParameterDetection --> ContextCreation
    ContextCreation --> ContextInjection
    ContextInjection --> FunctionExecution
    
    ContextInjection --> Logging
    ContextInjection --> Progress
    ContextInjection --> ResourceAccess
    ContextInjection --> RequestInfo
```

### Context Methods

The `Context` class provides several methods for interacting with the MCP session:

| Method | Purpose | Parameters |
|--------|---------|------------|
| `log()` | Send log messages | `level`, `message`, `logger_name` |
| `report_progress()` | Report operation progress | `progress`, `total`, `message` |
| `read_resource()` | Access other resources | `uri` |
| `elicit()` | Request user input | `message`, `schema` |

Sources: [src/mcp/server/fastmcp/server.py:1043-1223](), [tests/server/fastmcp/test_server.py:835-1092]()

## Transport Integration

FastMCP supports multiple transport protocols through dedicated application factories:

### Transport Applications

```mermaid
graph TB
    subgraph "FastMCP Transport Integration"
        FastMCPInstance[FastMCP]
        
        subgraph "Transport Methods"
            RunStdio["run_stdio_async()"]
            RunSSE["run_sse_async()"]
            RunStreamable["run_streamable_http_async()"]
        end
        
        subgraph "App Factories"
            SSEAppFactory["sse_app()"]
            StreamableAppFactory["streamable_http_app()"]
            StdioRunner["stdio_server()"]
        end
        
        subgraph "Underlying Transports"
            SseServerTransport[SseServerTransport]
            StreamableHTTPSessionManager[StreamableHTTPSessionManager]
            StdioTransport["stdio transport"]
        end
        
        subgraph "ASGI Applications"
            StarletteSSE["Starlette App (SSE)"]
            StarletteStreamable["Starlette App (StreamableHTTP)"]
        end
    end
    
    FastMCPInstance --> RunStdio
    FastMCPInstance --> RunSSE
    FastMCPInstance --> RunStreamable
    
    RunStdio --> StdioRunner
    RunSSE --> SSEAppFactory
    RunStreamable --> StreamableAppFactory
    
    SSEAppFactory --> SseServerTransport
    SSEAppFactory --> StarletteSSE
    
    StreamableAppFactory --> StreamableHTTPSessionManager
    StreamableAppFactory --> StarletteStreamable
    
    StdioRunner --> StdioTransport
```

### Transport-Specific Features

Each transport provides specific capabilities:

| Transport | Use Case | Key Features |
|-----------|----------|--------------|
| **stdio** | Process-based communication | Simple stdin/stdout JSON-RPC |
| **SSE** | Web-based real-time communication | Server-sent events with HTTP POST |
| **StreamableHTTP** | Resumable sessions | Bidirectional streaming, session persistence |

Sources: [src/mcp/server/fastmcp/server.py:687-724](), [src/mcp/server/fastmcp/server.py:752-990]()

## Configuration and Settings

### Settings Management

The `Settings` class provides comprehensive configuration management with environment variable support:

```python
class Settings(BaseSettings):
    # Server settings
    debug: bool
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    # HTTP settings
    host: str = "127.0.0.1"
    port: int = 8000
    mount_path: str = "/"
    
    # Authentication
    auth: AuthSettings | None = None
    
    # Transport security
    transport_security: TransportSecuritySettings | None = None
```

Settings can be configured via:
- Environment variables with `FASTMCP_` prefix
- `.env` files
- Direct parameter passing

### Authentication Integration

FastMCP supports OAuth 2.0 authentication through integrated middleware:

```mermaid
graph LR
    subgraph "Authentication Flow"
        AuthSettings[AuthSettings]
        AuthServerProvider[OAuthAuthorizationServerProvider]
        TokenVerifier[TokenVerifier]
        
        subgraph "Middleware Stack"
            AuthenticationMiddleware[AuthenticationMiddleware]
            AuthContextMiddleware[AuthContextMiddleware]
            RequireAuthMiddleware[RequireAuthMiddleware]
        end
        
        subgraph "Route Protection"
            SSERoutes["SSE Routes"]
            StreamableRoutes["StreamableHTTP Routes"]
            CustomRoutes["Custom Routes"]
        end
    end
    
    AuthSettings --> AuthServerProvider
    AuthSettings --> TokenVerifier
    
    AuthServerProvider --> AuthenticationMiddleware
    TokenVerifier --> AuthenticationMiddleware
    
    AuthenticationMiddleware --> AuthContextMiddleware
    AuthContextMiddleware --> RequireAuthMiddleware
    
    RequireAuthMiddleware --> SSERoutes
    RequireAuthMiddleware --> StreamableRoutes
    RequireAuthMiddleware --> CustomRoutes
```

Sources: [src/mcp/server/fastmcp/server.py:56-108](), [src/mcp/server/fastmcp/server.py:152-170](), [src/mcp/server/fastmcp/server.py:792-982]()