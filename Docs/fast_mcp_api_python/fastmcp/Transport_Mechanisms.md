This document covers the transport layer of the FastMCP client system, which handles connection establishment and communication with MCP servers. Transport mechanisms are responsible for the underlying connection details (subprocess management, HTTP connections, in-memory calls), while the `Client` class handles MCP protocol operations.

For information about client operations like calling tools and reading resources, see [Client Operations and Testing](#3.2). For server-side HTTP infrastructure, see [HTTP Server and Deployment](#6).

## Architecture Overview

The FastMCP client system separates concerns between protocol handling and connection management through a two-layer architecture:

### Core Transport Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Client["Client[ClientTransportT]<br/>• ClientSessionState management<br/>• _connect()/_disconnect() lifecycle<br/>• _session_runner() background task"]
    end
    
    subgraph "Transport Layer"
        ClientTransport["ClientTransport (ABC)<br/>• connect_session(**SessionKwargs)<br/>• close() method<br/>• _set_auth() authentication"]
        
        StdioTransport["StdioTransport<br/>• _stdio_transport_connect_task()<br/>• keep_alive parameter<br/>• StdioServerParameters"]
        
        StreamableHttpTransport["StreamableHttpTransport<br/>• streamablehttp_client()<br/>• BearerAuth/OAuth classes<br/>• get_http_headers() forwarding"]
        
        SSETransport["SSETransport<br/>• sse_client()<br/>• Legacy SSE support<br/>• DeprecationWarning"]
        
        FastMCPTransport["FastMCPTransport<br/>• create_client_server_memory_streams()<br/>• anyio.create_task_group()<br/>• raise_exceptions parameter"]
        
        MCPConfigTransport["MCPConfigTransport<br/>• ProxyClient composition<br/>• FastMCPProxy.as_proxy()<br/>• _create_composite_server()"]
        
        ClientTransport --> StdioTransport
        ClientTransport --> StreamableHttpTransport
        ClientTransport --> SSETransport
        ClientTransport --> FastMCPTransport
        ClientTransport --> MCPConfigTransport
    end
    
    subgraph "Stdio Specializations"
        PythonStdioTransport["PythonStdioTransport<br/>• sys.executable command<br/>• .py file validation"]
        NodeStdioTransport["NodeStdioTransport<br/>• node command<br/>• .js file validation"]
        FastMCPStdioTransport["FastMCPStdioTransport<br/>• fastmcp run command<br/>• CLI integration"]
        UvStdioTransport["UvStdioTransport<br/>• UVEnvironment config<br/>• uv run args"]
        UvxStdioTransport["UvxStdioTransport<br/>• uvx tool execution<br/>• with_packages args"]
        NpxStdioTransport["NpxStdioTransport<br/>• npx package execution<br/>• prefer_offline option"]
        
        StdioTransport --> PythonStdioTransport
        StdioTransport --> NodeStdioTransport
        StdioTransport --> FastMCPStdioTransport
        StdioTransport --> UvStdioTransport
        StdioTransport --> UvxStdioTransport
        StdioTransport --> NpxStdioTransport
    end
    
    Client --> ClientTransport
```

**Sources:** [src/fastmcp/client/client.py:97-155](), [src/fastmcp/client/transports.py:75-119](), [src/fastmcp/client/transports.py:301-417]()

The `Client` class is a generic type `Client[ClientTransportT]` that accepts any transport instance or transport-inferrable input and delegates connection management to the transport while handling all MCP protocol details itself. The transport layer provides connection abstraction while the client handles session management including reentrant context managers and initialization.

## Transport Inference System

The client system automatically selects appropriate transports based on input types through the `infer_transport` function:

### Transport Selection Logic

```mermaid
flowchart TD
    Input["Client(transport=...)"] --> infer_transport["infer_transport()<br/>[transports.py:957-1016]"]
    
    infer_transport --> CheckType{"isinstance() checks"}
    
    CheckType --> |"ClientTransport"| DirectUse["return transport"]
    CheckType --> |"FastMCP | FastMCP1Server"| InMemory["FastMCPTransport(mcp)"]
    CheckType --> |"AnyUrl"| URLAnalysis["infer_transport_type_from_url()<br/>[mcp_config.py:56-74]"]
    CheckType --> |"Path"| PathAnalysis["Path.suffix check"]
    CheckType --> |"MCPConfig | dict"| ConfigInput["MCPConfigTransport(config)"]
    CheckType --> |"str"| StringAnalysis["URL or Path parsing"]
    
    URLAnalysis --> |"re.search(r'/sse(/|\\?|&|$)')"| SSETransport["SSETransport(url)"]
    URLAnalysis --> |"default"| StreamableHttp["StreamableHttpTransport(url)"]
    
    PathAnalysis --> |"suffix == '.py'"| PythonScript["PythonStdioTransport(script_path)"]
    PathAnalysis --> |"suffix == '.js'"| NodeScript["NodeStdioTransport(script_path)"]
    PathAnalysis --> |"else"| DefaultPython["PythonStdioTransport(default)"]
    
    StringAnalysis --> |"startswith('http')"| URLString["AnyUrl(transport) -> URLAnalysis"]
    StringAnalysis --> |"else"| PathString["Path(transport) -> PathAnalysis"]
```

**Sources:** [src/fastmcp/client/transports.py:957-1016](), [src/fastmcp/client/client.py:231](), [src/fastmcp/mcp_config.py:56-74]()

The `infer_transport` function provides automatic transport selection with intelligent defaults. HTTP URLs are analyzed for SSE paths (containing `/sse/`) while other HTTP URLs default to `StreamableHttpTransport`. File paths use extension-based selection, and the system gracefully handles edge cases by falling back to sensible defaults.

## Transport Types and Use Cases

### Transport Comparison Matrix

| Transport Type | Best For | Connection Model | Session Persistence | Authentication Support |
|---|---|---|---|---|
| `FastMCPTransport` | Testing, development, in-process | In-memory | N/A | N/A |
| `StreamableHttpTransport` | Production HTTP servers | Remote network | Stateless | Yes (Bearer, OAuth) |
| `SSETransport` | Legacy HTTP servers, SSE endpoints | Remote network | Stateless | Yes (Bearer, OAuth) |
| `StdioTransport` | Local MCP servers, subprocesses | Subprocess pipes | Configurable (`keep_alive`) | N/A |
| `MCPConfigTransport` | Multi-server applications | Mixed transports | Varies by server | Per-server configuration |

### Transport Capabilities

| Transport | Header Forwarding | Timeout Control | Environment Variables | Keep-Alive |
|---|---|---|---|---|
| `StreamableHttpTransport` | Yes (`get_http_headers()`) | Yes (`sse_read_timeout`) | N/A | N/A |
| `SSETransport` | Yes (`get_http_headers()`) | Yes (`sse_read_timeout`) | N/A | N/A |
| `StdioTransport` | N/A | N/A | Yes (`env` parameter) | Yes (configurable) |
| `FastMCPTransport` | N/A | N/A | Inherited from process | N/A |

**Sources:** [src/fastmcp/client/transports.py:160-227](), [src/fastmcp/client/transports.py:230-298](), [src/fastmcp/client/transports.py:301-417](), [src/fastmcp/client/transports.py:783-835]()

## Stdio Transport Family

Stdio transports manage local MCP servers through subprocess execution, communicating via stdin/stdout pipes.

### Base Stdio Transport

```mermaid
graph TB
    subgraph "StdioTransport Lifecycle"
        Create["StdioTransport(command, args, env)"]
        Connect["connect_session()"]
        Launch["_stdio_transport_connect_task()"]
        Session["ClientSession established"]
        KeepAlive{"keep_alive?"}
        Reuse["Session persists"]
        Terminate["Session terminates"]
        
        Create --> Connect
        Connect --> Launch
        Launch --> Session
        Session --> KeepAlive
        KeepAlive --> |"True"| Reuse
        KeepAlive --> |"False"| Terminate
    end
```

**Sources:** [src/fastmcp/client/transports.py:301-417](), [src/fastmcp/client/transports.py:419-463]()

The `StdioTransport` class provides the foundation for all subprocess-based transports. Key features include:

- **Session Persistence**: Controlled via `keep_alive` parameter [src/fastmcp/client/transports.py:315-336]()
- **Environment Isolation**: Explicit environment variable passing [src/fastmcp/client/transports.py:312-314]()
- **Async Task Management**: Background connection task [src/fastmcp/client/transports.py:419-463]()

### Specialized Stdio Implementations

| Class | Command | File Extension | Use Case |
|---|---|---|---|
| `PythonStdioTransport` | `python` | `.py` | Python MCP servers |
| `NodeStdioTransport` | `node` | `.js` | JavaScript MCP servers |
| `FastMCPStdioTransport` | `fastmcp` | `.py` | FastMCP CLI execution |
| `UvStdioTransport` | `uv` | N/A | Python package execution |
| `UvxStdioTransport` | `uvx` | N/A | Python tool execution |
| `NpxStdioTransport` | `npx` | N/A | Node package execution |

**Sources:** [src/fastmcp/client/transports.py:465-509](), [src/fastmcp/client/transports.py:511-536](), [src/fastmcp/client/transports.py:538-577]()

## Remote Transport Types

Remote transports connect to MCP servers running as web services over HTTP connections.

### StreamableHttpTransport Architecture

```mermaid
graph LR
    subgraph "StreamableHttpTransport Flow"
        Client["FastMCP Client"]
        Transport["StreamableHttpTransport"]
        HttpClient["streamablehttp_client"]
        RemoteServer["Remote MCP Server"]
        
        Client --> |"connect_session()"| Transport
        Transport --> |"Bidirectional streaming"| HttpClient
        HttpClient --> |"HTTP requests/responses"| RemoteServer
    end
```

**Sources:** [src/fastmcp/client/transports.py:228-298]()

The `StreamableHttpTransport` provides efficient bidirectional communication for production deployments:

- **Authentication Support**: OAuth and Bearer token authentication [src/fastmcp/client/transports.py:256-261]()
- **Header Forwarding**: Automatic forwarding of HTTP headers in proxy scenarios [src/fastmcp/client/transports.py:274]()
- **Timeout Configuration**: Configurable request timeouts [src/fastmcp/client/transports.py:280-281]()

### SSETransport (Legacy)

The `SSETransport` maintains compatibility with older Server-Sent Events implementations but is superseded by `StreamableHttpTransport` for new deployments [src/fastmcp/client/transports.py:156-226]().

## In-Memory Transport

The `FastMCPTransport` enables direct communication with FastMCP server instances within the same Python process.

### In-Memory Communication Flow

```mermaid
sequenceDiagram
    participant C as "Client"
    participant T as "FastMCPTransport"
    participant M as "Memory Streams"
    participant S as "FastMCP Server"
    
    C->>T: "connect_session()"
    T->>M: "create_client_server_memory_streams()"
    T->>S: "server._mcp_server.run()"
    Note over T,S: "Direct memory communication"
    T->>C: "ClientSession"
    C->>S: "MCP requests via memory"
    S->>C: "MCP responses via memory"
```

**Sources:** [src/fastmcp/client/transports.py:763-815]()

Key characteristics of in-memory transport:
- **Zero Network Overhead**: Direct method calls within same process
- **Shared Environment**: Full access to client process environment variables
- **Exception Control**: Configurable exception raising via `raise_exceptions` parameter [src/fastmcp/client/transports.py:772]()

## Multi-Server Configuration Transport

The `MCPConfigTransport` enables connections to multiple MCP servers through configuration-based routing.

### MCPConfig Architecture

```mermaid
graph TB
    subgraph "MCPConfigTransport Structure"
        Config["MCPConfig Dictionary"]
        Single{"Single Server?"}
        Direct["Direct Transport"]
        Composite["Composite FastMCP Server"]
        
        Config --> Single
        Single --> |"Yes"| Direct
        Single --> |"No"| Composite
        
        subgraph "Multi-Server Composition"
            Mount1["Server 1<br/>prefix: weather_"]
            Mount2["Server 2<br/>prefix: calendar_"]
            Mount3["Server N<br/>prefix: {name}_"]
        end
        
        Composite --> Mount1
        Composite --> Mount2
        Composite --> Mount3
    end
```

**Sources:** [src/fastmcp/client/transports.py:817-926]()

The transport automatically handles server composition:
- **Single Server**: Direct transport to the configured server
- **Multiple Servers**: Creates composite server with prefixed component names
- **Flexible Configuration**: Supports all transport types within the configuration

### Configuration Schema Support

```python
config = {
    "mcpServers": {
        "server_name": {
            "transport": "http",
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": "Bearer token"}
        }
    }
}
```

**Sources:** [src/fastmcp/client/transports.py:865-887]()

## Session Management and Connection Lifecycle

### Session Context Management

The transport layer provides async context manager support for proper session lifecycle, with sophisticated reentrant session management in the `Client` class:

### Client Session State Management

```mermaid
stateDiagram-v2
    [*] --> Disconnected: "ClientSessionState() created"
    
    Disconnected --> Connecting: "_connect() -> __aenter__()"
    Connecting --> SessionTask: "asyncio.create_task(_session_runner())"
    SessionTask --> Ready: "self._session_state.ready_event.set()"
    Ready --> Connected: "ClientSession available"
    
    Connected --> Nested: "Additional async with client:"
    Nested --> Connected: "self._session_state.nesting_counter += 1"
    Connected --> Connected: "session.call_tool() etc"
    
    Connected --> Checking: "_disconnect() -> __aexit__()"
    Checking --> StillNested: "nesting_counter > 0"
    StillNested --> Connected: "max(0, nesting_counter - 1)"
    Checking --> Stopping: "nesting_counter == 0"
    Stopping --> Disconnected: "self._session_state.stop_event.set()"
    
    SessionTask --> Failed: "transport.connect_session() fails"
    Failed --> [*]: "ready_event.set() in finally"
```

**Sources:** [src/fastmcp/client/client.py:80-96](), [src/fastmcp/client/client.py:373-463](), [src/fastmcp/client/client.py:465-488]()

The `Client` implements sophisticated reentrant context manager support using:
- `ClientSessionState` with `nesting_counter`, `session_task`, `ready_event`, and `stop_event`
- Background `_session_runner()` task for session lifecycle management
- Thread-safe session sharing across multiple concurrent `async with client:` blocks
- Automatic cleanup when the last context exits

### Transport Connect Session Protocol

All transports implement the `connect_session` async context manager method:

```python
@abc.abstractmethod
@contextlib.asynccontextmanager
async def connect_session(
    self, **session_kwargs: Unpack[SessionKwargs]
) -> AsyncIterator[ClientSession]:
```

**Sources:** [src/fastmcp/client/transports.py:84-106]()

This protocol ensures consistent connection lifecycle across all transport types while allowing transport-specific connection details.

### Authentication Integration

Remote transports support multiple authentication mechanisms:

| Auth Type | Implementation | Usage |
|---|---|---|
| Bearer Token | `BearerAuth` class | String token passed to `auth` parameter |
| OAuth | `OAuth` class | `auth="oauth"` with URL-based configuration |
| Custom Headers | Direct header passing | Custom authentication schemes |

**Sources:** [src/fastmcp/client/transports.py:184-189](), [src/fastmcp/client/transports.py:256-261]()

# Client Authentication




This page covers client-side authentication in FastMCP, focusing on OAuth flows, token storage, browser-based authentication, and integration with identity providers. This documentation explains how FastMCP clients authenticate with protected servers using industry-standard OAuth 2.0 and OpenID Connect protocols.

For server-side authentication configuration and identity providers, see [Authentication and Security](#4.1). For transport-specific authentication mechanisms, see [Transport Mechanisms](#3.1).

## Overview

FastMCP client authentication is built around OAuth 2.0 with OpenID Connect support, providing secure token-based authentication for MCP clients connecting to protected servers. The authentication system handles the complete OAuth flow, from initial authorization to token refresh and storage.

### Client Authentication Architecture

```mermaid
graph TD
    subgraph "Client Application"
        ClientApp["Client Application"]
        FastMCPClient["FastMCP Client"]
    end
    
    subgraph "Authentication Layer"
        OAuthProvider["OAuth(OAuthClientProvider)<br/>- redirect_handler<br/>- callback_handler<br/>- async_auth_flow"]
        TokenStorage["FileTokenStorage<br/>- get_tokens<br/>- set_tokens<br/>- get_client_info<br/>- set_client_info"]
        CallbackServer["OAuth Callback Server<br/>- uvicorn.Server<br/>- create_oauth_callback_server"]
    end
    
    subgraph "Browser & External"
        Browser["Web Browser<br/>webbrowser.open"]
        AuthServer["Authorization Server<br/>- /authorize endpoint<br/>- /token endpoint"]
    end
    
    subgraph "Storage Layer"
        JSONStorage["JSONFileStorage<br/>~/.fastmcp/oauth-mcp-client-cache/"]
        TokenFiles["Token Files<br/>- {base_url}_tokens.json<br/>- {base_url}_client_info.json"]
    end
    
    ClientApp --> FastMCPClient
    FastMCPClient --> OAuthProvider
    OAuthProvider --> TokenStorage
    OAuthProvider --> CallbackServer
    OAuthProvider --> Browser
    Browser --> AuthServer
    AuthServer --> CallbackServer
    TokenStorage --> JSONStorage
    JSONStorage --> TokenFiles
```

Sources: [src/fastmcp/client/auth/oauth.py:242-428](), [src/fastmcp/client/oauth_callback.py](), [src/fastmcp/utilities/storage.py]()

## OAuth Flow Implementation

The `OAuth` class implements the complete OAuth 2.0 authorization code flow with PKCE support, handling dynamic client registration, browser-based authorization, and token management.

### OAuth Provider Class Structure

```mermaid
graph TB
    subgraph "OAuth Class Hierarchy"
        OAuthClientProvider["mcp.client.auth.OAuthClientProvider<br/>Base OAuth implementation"]
        OAuth["fastmcp.client.auth.oauth.OAuth<br/>FastMCP OAuth implementation"]
        OAuth --> OAuthClientProvider
    end
    
    subgraph "OAuth Methods"
        redirect_handler["redirect_handler()<br/>- Pre-flight client validation<br/>- Opens browser to auth URL"]
        callback_handler["callback_handler()<br/>- Starts local server<br/>- Waits for OAuth callback<br/>- Returns (code, state)"]
        async_auth_flow["async_auth_flow()<br/>- HTTPX auth flow<br/>- Automatic retry on stale credentials<br/>- Token refresh handling"]
    end
    
    subgraph "Configuration"
        client_metadata["OAuthClientMetadata<br/>- client_name<br/>- redirect_uris<br/>- grant_types<br/>- response_types<br/>- scope"]
        storage["FileTokenStorage<br/>- Server-specific isolation<br/>- Token expiry handling"]
    end
    
    OAuth --> redirect_handler
    OAuth --> callback_handler
    OAuth --> async_auth_flow
    OAuth --> client_metadata
    OAuth --> storage
```

Sources: [src/fastmcp/client/auth/oauth.py:242-311](), [src/fastmcp/client/auth/oauth.py:322-374](), [src/fastmcp/client/auth/oauth.py:376-427]()

### Authorization Flow Process

The OAuth authorization flow follows these steps:

| Step | Method | Description | Error Handling |
|------|--------|-------------|----------------|
| 1 | `redirect_handler()` | Pre-flight validation, opens browser | Detects stale client_id (400 response) |
| 2 | `callback_handler()` | Starts local callback server | 5-minute timeout with graceful shutdown |
| 3 | Token Exchange | Exchanges auth code for tokens | Automatic retry on client errors |
| 4 | Token Storage | Saves tokens with absolute expiry | Validates token format and expiry |

Sources: [src/fastmcp/client/auth/oauth.py:322-341](), [src/fastmcp/client/auth/oauth.py:343-374]()

## Token Storage and Management

FastMCP implements sophisticated token storage with automatic expiry handling, server isolation, and format validation through the `FileTokenStorage` class.

### Token Storage Architecture

```mermaid
graph TB
    subgraph "Token Storage Components"
        FileTokenStorage["FileTokenStorage<br/>TokenStorage protocol"]
        JSONFileStorage["JSONFileStorage<br/>File operations & validation"]
        StoredToken["StoredToken (BaseModel)<br/>- token_payload: OAuthToken<br/>- expires_at: datetime"]
    end
    
    subgraph "Storage Operations"
        get_tokens["get_tokens()<br/>- Load from disk<br/>- Check expiry<br/>- Recalculate expires_in"]
        set_tokens["set_tokens()<br/>- Calculate absolute expiry<br/>- Save to disk<br/>- Format validation"]
        get_client_info["get_client_info()<br/>- Load client credentials<br/>- Validate with tokens<br/>- Clear if incomplete"]
        set_client_info["set_client_info()<br/>- Save client registration<br/>- Validate format"]
    end
    
    subgraph "File System"
        cache_dir["~/.fastmcp/oauth-mcp-client-cache/"]
        token_file["{base_url}_tokens.json<br/>JSON wrapper format"]
        client_file["{base_url}_client_info.json<br/>Client registration data"]
    end
    
    FileTokenStorage --> JSONFileStorage
    FileTokenStorage --> StoredToken
    FileTokenStorage --> get_tokens
    FileTokenStorage --> set_tokens  
    FileTokenStorage --> get_client_info
    FileTokenStorage --> set_client_info
    JSONFileStorage --> cache_dir
    cache_dir --> token_file
    cache_dir --> client_file
```

Sources: [src/fastmcp/client/auth/oauth.py:59-196](), [src/fastmcp/client/auth/oauth.py:44-52]()

### Token Expiry Handling

The token storage system uses absolute timestamps rather than relative `expires_in` values to ensure accurate expiry checking across application restarts:

```mermaid
graph LR
    subgraph "Token Save Process"
        OAuthToken["OAuthToken<br/>expires_in: 3600"]
        Calculate["Calculate Absolute Expiry<br/>now + expires_in"]
        StoredToken["StoredToken<br/>expires_at: 2024-01-01T12:00:00Z"]
        SaveToDisk["Save to Disk<br/>JSON format"]
    end
    
    subgraph "Token Load Process"
        LoadFromDisk["Load from Disk<br/>Parse JSON"]
        CheckExpiry["Check Expiry<br/>now >= expires_at?"]
        RecalculateExpiresIn["Recalculate expires_in<br/>expires_at - now"]
        ReturnToken["Return OAuthToken<br/>Updated expires_in"]
        ReturnNull["Return None<br/>Token expired"]
    end
    
    OAuthToken --> Calculate
    Calculate --> StoredToken
    StoredToken --> SaveToDisk
    
    LoadFromDisk --> CheckExpiry
    CheckExpiry -->|Valid| RecalculateExpiresIn
    CheckExpiry -->|Expired| ReturnNull
    RecalculateExpiresIn --> ReturnToken
```

Sources: [src/fastmcp/client/auth/oauth.py:132-147](), [src/fastmcp/client/auth/oauth.py:96-130](), [tests/client/auth/test_oauth_token_expiry.py:13-164]()

## Browser-Based Authentication

FastMCP uses a browser-based OAuth flow that opens the user's default browser for authorization and runs a temporary local server to receive the OAuth callback.

### Browser Flow Implementation

```mermaid
graph TD
    subgraph "Authorization Flow"
        StartAuth["Start OAuth Flow<br/>redirect_handler()"]
        PreflightCheck["Pre-flight Check<br/>GET authorization_url"]
        ValidateResponse["Validate Response<br/>Check for 400 (bad client_id)"]
        OpenBrowser["Open Browser<br/>webbrowser.open(auth_url)"]
    end
    
    subgraph "Callback Handling"
        StartCallbackServer["Start Callback Server<br/>create_oauth_callback_server()"]
        WaitForCallback["Wait for Callback<br/>response_future.await"]
        HandleTimeout["Handle Timeout<br/>300 second limit"]
        ExtractCode["Extract Auth Code<br/>Return (code, state)"]
    end
    
    subgraph "Error Handling"
        ClientNotFound["ClientNotFoundError<br/>Invalid client_id detected"]
        ClearCache["Clear Cached Credentials<br/>storage.clear()"]
        RetryFlow["Retry OAuth Flow<br/>Fresh registration"]
    end
    
    StartAuth --> PreflightCheck
    PreflightCheck --> ValidateResponse
    ValidateResponse -->|Valid| OpenBrowser
    ValidateResponse -->|400 Error| ClientNotFound
    OpenBrowser --> StartCallbackServer
    StartCallbackServer --> WaitForCallback
    WaitForCallback -->|Success| ExtractCode
    WaitForCallback -->|Timeout| HandleTimeout
    ClientNotFound --> ClearCache
    ClearCache --> RetryFlow
```

Sources: [src/fastmcp/client/auth/oauth.py:322-341](), [src/fastmcp/client/auth/oauth.py:343-374](), [src/fastmcp/client/auth/oauth.py:395-427]()

### Callback Server Configuration

The OAuth callback server uses dynamic port allocation and graceful shutdown:

| Configuration | Default | Description |
|---------------|---------|-------------|
| Port | `find_available_port()` | Dynamically allocated available port |
| Timeout | 300 seconds | Maximum wait time for user authorization |
| Redirect URI | `http://localhost:{port}/callback` | OAuth callback endpoint |
| Server Type | `uvicorn.Server` | ASGI server for handling callbacks |

Sources: [src/fastmcp/client/auth/oauth.py:275-276](), [src/fastmcp/utilities/http.py](), [src/fastmcp/client/oauth_callback.py]()

## Identity Provider Integration

FastMCP supports multiple identity providers through standardized OAuth 2.0 and OpenID Connect protocols. The authentication system is provider-agnostic, requiring only standard OAuth endpoints.

### Provider Configuration

```mermaid
graph TB
    subgraph "Identity Providers"
        Auth0["Auth0<br/>/.well-known/openid-configuration"]
        Google["Google<br/>accounts.google.com"]
        GitHub["GitHub OAuth<br/>/login/oauth/authorize"]
        Azure["Azure AD<br/>login.microsoftonline.com"]
        Custom["Custom OIDC<br/>Any RFC-compliant provider"]
    end
    
    subgraph "OAuth Configuration"
        OIDCDiscovery["OIDC Discovery<br/>/.well-known/openid-configuration"]
        AuthEndpoint["authorization_endpoint<br/>User login page"]
        TokenEndpoint["token_endpoint<br/>Token exchange"]
        JWKSUri["jwks_uri<br/>Public key validation"]
    end
    
    subgraph "Client Requirements"
        ClientID["client_id<br/>Public identifier"]
        RedirectURI["redirect_uri<br/>http://localhost:{port}/callback"]
        Scopes["scopes<br/>Requested permissions"]
        GrantType["grant_types<br/>authorization_code, refresh_token"]
    end
    
    Auth0 --> OIDCDiscovery
    Google --> OIDCDiscovery
    GitHub --> AuthEndpoint
    Azure --> OIDCDiscovery
    Custom --> OIDCDiscovery
    
    OIDCDiscovery --> AuthEndpoint
    OIDCDiscovery --> TokenEndpoint
    OIDCDiscovery --> JWKSUri
    
    AuthEndpoint --> ClientID
    TokenEndpoint --> ClientID
    ClientID --> RedirectURI
    RedirectURI --> Scopes
    Scopes --> GrantType
```

Sources: [src/fastmcp/server/auth/oidc_proxy.py:27-169](), [src/fastmcp/server/auth/providers/auth0.py:36-175]()

### Authentication Pre-flight Check

Before initiating OAuth flows, FastMCP can check if authentication is required:

```python
# Usage example from oauth.py
async def check_if_auth_required(
    mcp_url: str, httpx_kwargs: dict[str, Any] | None = None
) -> bool:
    """Check if the MCP endpoint requires authentication."""
```

This function tests the endpoint and returns `True` if authentication appears required based on HTTP status codes (401, 403) or WWW-Authenticate headers.

Sources: [src/fastmcp/client/auth/oauth.py:212-240]()

## Configuration and Usage

### Basic OAuth Configuration

```python
from fastmcp.client.auth.oauth import OAuth

oauth_provider = OAuth(
    mcp_url="https://api.example.com/mcp/",
    scopes=["openid", "profile", "email"],
    client_name="My FastMCP Client",
    token_storage_cache_dir=Path("~/.my-app/oauth-cache"),
    callback_port=8080  # Optional: fixed port
)
```

### Client Integration

```python
from fastmcp import Client

async with Client(
    "https://api.example.com/mcp/",
    auth=oauth_provider
) as client:
    # Client automatically handles OAuth flow
    tools = await client.list_tools()
```

### Token Storage Locations

The `FileTokenStorage` class stores tokens in server-specific files:

| File Type | Path Pattern | Purpose |
|-----------|--------------|---------|
| Tokens | `{base_url}_tokens.json` | Access/refresh tokens with expiry |
| Client Info | `{base_url}_client_info.json` | OAuth client registration data |
| Cache Dir | `~/.fastmcp/oauth-mcp-client-cache/` | Default storage location |

Sources: [src/fastmcp/client/auth/oauth.py:250-311](), [src/fastmcp/client/auth/oauth.py:55-86]()

### Error Handling and Recovery

The OAuth implementation includes automatic error recovery:

- **Stale Credentials**: Detects invalid client_id and clears cache for retry
- **Token Expiry**: Automatically refreshes expired tokens
- **Network Errors**: Graceful handling of connection issues
- **Timeout Handling**: 5-minute timeout with user-friendly messages

Sources: [src/fastmcp/client/auth/oauth.py:376-427](), [src/fastmcp/client/auth/oauth.py:38-41]()