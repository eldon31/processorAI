This document covers FastMCP's configuration management system, which enables declarative server definitions, multi-server orchestration, and standardized MCP client configurations. The system provides both programmatic and file-based configuration approaches for defining MCP servers, their connections, authentication, and behavioral transformations.

For information about HTTP server deployment configuration, see [HTTP Server and Deployment](#4). For CLI-based configuration commands, see [Command Line Interface](#5). For project build and dependency configuration, see [Installation and Setup](#1.1).

## Configuration System Architecture

The configuration management system centers around the `MCPConfig` class hierarchy, which provides both standard and canonical configuration formats for defining MCP servers and their properties.

```mermaid
graph TB
    subgraph "Configuration Classes"
        MCPConfig["MCPConfig<br/>Standard format with transformations"]
        CanonicalMCPConfig["CanonicalMCPConfig<br/>Normalized format without transformations"]
        MCPServerTypes["MCPServerTypes<br/>Union[StdioMCPServer, RemoteMCPServer, TransformingStdioMCPServer]"]
        CanonicalMCPServerTypes["CanonicalMCPServerTypes<br/>Union[StdioMCPServer, RemoteMCPServer]"]
    end
    
    subgraph "Server Definitions"
        StdioMCPServer["StdioMCPServer<br/>Local subprocess servers"]
        RemoteMCPServer["RemoteMCPServer<br/>HTTP/SSE remote servers"]
        TransformingStdioMCPServer["TransformingStdioMCPServer<br/>Stdio with tool/resource transforms"]
    end
    
    subgraph "Transport Generation"
        MCPConfigTransport["MCPConfigTransport<br/>Multi-server client transport"]
        StdioTransport["StdioTransport"]
        StreamableHttpTransport["StreamableHttpTransport"]
        SSETransport["SSETransport"]
    end
    
    subgraph "Configuration Sources"
        DictConfig["Dictionary Configuration"]
        JSONFile["fastmcp.json"]
        ProgrammaticConfig["Programmatic Construction"]
    end
    
    MCPConfig --> MCPServerTypes
    CanonicalMCPConfig --> CanonicalMCPServerTypes
    MCPServerTypes --> StdioMCPServer
    MCPServerTypes --> RemoteMCPServer  
    MCPServerTypes --> TransformingStdioMCPServer
    CanonicalMCPServerTypes --> StdioMCPServer
    CanonicalMCPServerTypes --> RemoteMCPServer
    
    StdioMCPServer --> StdioTransport
    RemoteMCPServer --> StreamableHttpTransport
    RemoteMCPServer --> SSETransport
    TransformingStdioMCPServer --> StdioTransport
    
    DictConfig --> MCPConfig
    JSONFile --> MCPConfig
    ProgrammaticConfig --> MCPConfig
    
    MCPConfig --> MCPConfigTransport
    CanonicalMCPConfig --> MCPConfigTransport
```

Sources: [tests/test_mcp_config.py:25-33](), [src/fastmcp/mcp_config.py]()

## Server Configuration Types

FastMCP supports three primary server configuration types, each designed for different deployment scenarios and capability requirements.

### StdioMCPServer Configuration

`StdioMCPServer` configurations define local subprocess-based MCP servers that communicate via standard input/output streams.

```mermaid
graph LR
    subgraph "StdioMCPServer Properties"
        Command["command: str<br/>Executable path"]
        Args["args: list[str]<br/>Command arguments"]
        Env["env: dict[str, str]<br/>Environment variables"]
        Cwd["cwd: str | None<br/>Working directory"]
    end
    
    subgraph "Generated Transport"
        StdioTransport["StdioTransport<br/>subprocess communication"]
    end
    
    Command --> StdioTransport
    Args --> StdioTransport
    Env --> StdioTransport
    Cwd --> StdioTransport
```

Example configuration structure:
```json
{
  "mcpServers": {
    "local_server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {"DEBUG": "1"}
    }
  }
}
```

Sources: [tests/test_mcp_config.py:50-63](), [tests/test_mcp_config.py:177-202]()

### RemoteMCPServer Configuration

`RemoteMCPServer` configurations define HTTP-based remote MCP servers with automatic transport inference and authentication support.

```mermaid
graph LR
    subgraph "RemoteMCPServer Properties"
        URL["url: str<br/>Server endpoint"]
        Transport["transport: str | None<br/>Override transport type"]
        Auth["auth: str | None<br/>Authentication configuration"]
    end
    
    subgraph "Transport Inference"
        URLAnalysis["URL Path Analysis"]
        TransportSelection["Transport Selection"]
    end
    
    subgraph "Generated Transports"
        StreamableHTTP["StreamableHttpTransport<br/>Default HTTP transport"]
        SSE["SSETransport<br/>/sse/ path detected"]
    end
    
    URL --> URLAnalysis
    URLAnalysis --> TransportSelection
    TransportSelection --> StreamableHTTP
    TransportSelection --> SSE
    Transport --> TransportSelection
    Auth --> StreamableHTTP
    Auth --> SSE
```

The system automatically infers `SSETransport` for URLs containing `/sse/` paths, while defaulting to `StreamableHttpTransport` for other HTTP endpoints.

Sources: [tests/test_mcp_config.py:134-175](), [tests/test_mcp_config.py:412-467]()

### TransformingStdioMCPServer Configuration

`TransformingStdioMCPServer` extends stdio servers with tool and resource transformation capabilities, enabling name remapping, argument transformation, and selective inclusion/exclusion.

```mermaid
graph TB
    subgraph "TransformingStdioMCPServer"
        BaseConfig["Base StdioMCPServer properties"]
        Tools["tools: dict<br/>Tool transformations"]
        Resources["resources: dict<br/>Resource transformations"] 
        Prompts["prompts: dict<br/>Prompt transformations"]
        IncludeTags["include_tags: list[str]"]
        ExcludeTags["exclude_tags: list[str]"]
    end
    
    subgraph "Tool Transformation"
        ToolName["name: str<br/>Renamed tool name"]
        ToolArgs["arguments: dict<br/>Argument remapping"]
        ToolTags["tags: list[str]<br/>Applied tags"]
    end
    
    subgraph "Filtering Logic"
        TagFilter["Tag-based filtering<br/>include/exclude logic"]
        ComponentFilter["Component selection"]
    end
    
    Tools --> ToolName
    Tools --> ToolArgs
    Tools --> ToolTags
    IncludeTags --> TagFilter
    ExcludeTags --> TagFilter
    TagFilter --> ComponentFilter
```

Sources: [tests/test_mcp_config.py:534-588](), [tests/test_mcp_config.py:639-698]()

## Configuration File Formats

FastMCP supports multiple configuration input formats with automatic normalization and validation.

### Dictionary-based Configuration

The system accepts both nested `mcpServers` format and root-level server definitions:

```mermaid
graph LR
    subgraph "Input Formats"
        NestedFormat["Nested Format<br/>{mcpServers: {name: config}}"]
        RootFormat["Root Format<br/>{name: config}"]
    end
    
    subgraph "Normalization"
        Parser["MCPConfig.from_dict()"]
        Validation["Pydantic validation"]
    end
    
    subgraph "Output"
        StandardizedConfig["Standardized MCPConfig"]
    end
    
    NestedFormat --> Parser
    RootFormat --> Parser
    Parser --> Validation
    Validation --> StandardizedConfig
```

The parser automatically detects and normalizes root-level server definitions to the standard nested format.

Sources: [tests/test_mcp_config.py:86-99](), [tests/test_mcp_config.py:66-84]()

### Configuration Discrimination

The system uses discriminated unions to automatically select appropriate server types based on configuration content:

```mermaid
graph TD
    subgraph "Discrimination Logic"
        ConfigInput["Server Configuration"]
        HasTransforms["Has tools/resources/prompts?"]
        HasURL["Has url property?"]
        ServerType["Selected Server Type"]
    end
    
    ConfigInput --> HasURL
    HasURL -->|Yes| RemoteServer["RemoteMCPServer"]
    HasURL -->|No| HasTransforms
    HasTransforms -->|Yes| TransformingServer["TransformingStdioMCPServer"]
    HasTransforms -->|No| StdioServer["StdioMCPServer"]
    
    RemoteServer --> ServerType
    TransformingServer --> ServerType
    StdioServer --> ServerType
```

Sources: [tests/test_mcp_config.py:101-132]()

## Transport Configuration and Generation

The configuration system generates appropriate transport instances based on server definitions, with automatic inference and override capabilities.

### Transport Generation Pipeline

```mermaid
graph TB
    subgraph "Server Configs"
        StdioConfig["StdioMCPServer<br/>TransformingStdioMCPServer"]
        RemoteConfig["RemoteMCPServer"]
    end
    
    subgraph "Transport Factory"
        ToTransport["to_transport() method"]
        URLInference["URL-based inference"]
        TransportOverride["Explicit transport override"]
    end
    
    subgraph "Generated Transports"
        StdioT["StdioTransport<br/>command, args, env"]
        StreamableT["StreamableHttpTransport<br/>url, auth"]
        SSET["SSETransport<br/>url, auth"]
    end
    
    subgraph "Multi-Server Transport"
        MCPConfigTransport["MCPConfigTransport<br/>Aggregates multiple servers"]
    end
    
    StdioConfig --> ToTransport
    RemoteConfig --> ToTransport
    ToTransport --> URLInference
    ToTransport --> TransportOverride
    URLInference --> StdioT
    URLInference --> StreamableT
    URLInference --> SSET
    TransportOverride --> StreamableT
    TransportOverride --> SSET
    
    StdioT --> MCPConfigTransport
    StreamableT --> MCPConfigTransport
    SSET --> MCPConfigTransport
```

Sources: [tests/test_mcp_config.py:142-175](), [src/fastmcp/client/transports.py]()

## Authentication Configuration

FastMCP provides flexible authentication configuration supporting bearer tokens and OAuth flows for remote servers.

### Authentication Types

```mermaid
graph LR
    subgraph "Auth Configuration Values"
        NoAuth["null<br/>No authentication"]
        TokenAuth["string token<br/>Bearer authentication"]  
        OAuthLiteral["'oauth' literal<br/>OAuth flow"]
    end
    
    subgraph "Generated Auth Providers"
        NoAuthProvider["None"]
        BearerAuth["BearerAuth<br/>token: SecretStr"]
        OAuthProvider["OAuthClientProvider<br/>Dynamic token acquisition"]
    end
    
    subgraph "Transport Integration"
        HTTPTransport["HTTP Transport<br/>auth parameter"]
        SSETransport["SSE Transport<br/>auth parameter"]
    end
    
    NoAuth --> NoAuthProvider
    TokenAuth --> BearerAuth
    OAuthLiteral --> OAuthProvider
    
    NoAuthProvider --> HTTPTransport
    BearerAuth --> HTTPTransport
    OAuthProvider --> HTTPTransport
    
    NoAuthProvider --> SSETransport
    BearerAuth --> SSETransport
    OAuthProvider --> SSETransport
```

Authentication is automatically applied to both `StreamableHttpTransport` and `SSETransport` instances based on the remote server configuration.

Sources: [tests/test_mcp_config.py:425-467]()

## Multi-Server Orchestration

The `MCPConfigTransport` enables simultaneous connection to multiple MCP servers with unified tool/resource/prompt namespacing.

### Multi-Server Architecture

```mermaid
graph TB
    subgraph "MCPConfig Definition"
        Server1["Server1: stdio server"]
        Server2["Server2: remote server"]
        Server3["Server3: transforming server"]
    end
    
    subgraph "MCPConfigTransport"
        TransportAggregator["Transport Aggregator"]
        NamespaceManager["Namespace Manager"]
        ConnectionPool["Connection Pool"]
    end
    
    subgraph "Unified Client Interface"
        ListTools["list_tools()<br/>server1_tool, server2_tool"]
        CallTool["call_tool('server1_tool', args)"]
        Logging["Centralized logging"]
        Elicitation["Elicitation forwarding"]
    end
    
    Server1 --> TransportAggregator
    Server2 --> TransportAggregator
    Server3 --> TransportAggregator
    
    TransportAggregator --> NamespaceManager
    TransportAggregator --> ConnectionPool
    
    NamespaceManager --> ListTools
    NamespaceManager --> CallTool
    ConnectionPool --> Logging
    ConnectionPool --> Elicitation
```

Each server's tools, resources, and prompts are prefixed with the server name (e.g., `server_name_tool_name`) to avoid conflicts while maintaining clear attribution.

Sources: [tests/test_mcp_config.py:204-244](), [tests/test_mcp_config.py:469-532](), [tests/test_mcp_config.py:700-740]()

## Environment and Project Configuration

FastMCP integrates with standard Python project configuration through `pyproject.toml` and supports environment-based configuration management.

### Project Configuration Structure

```mermaid
graph TB
    subgraph "pyproject.toml Sections"
        ProjectMeta["[project]<br/>name, version, dependencies"]
        Scripts["[project.scripts]<br/>fastmcp = 'fastmcp.cli:app'"]
        OptionalDeps["[project.optional-dependencies]<br/>websockets, openai"]
        DepGroups["[dependency-groups]<br/>dev dependencies"]
    end
    
    subgraph "Build Configuration"
        BuildSystem["[build-system]<br/>hatchling, uv-dynamic-versioning"]
        HatchVersion["[tool.hatch.version]<br/>source = 'uv-dynamic-versioning'"]
    end
    
    subgraph "Tool Configuration"
        PytestConfig["[tool.pytest.ini_options]<br/>Test configuration"]
        RuffConfig["[tool.ruff.lint]<br/>Linting rules"]
        TyConfig["[tool.ty.*]<br/>Type checking"]
    end
    
    subgraph "Runtime Environment"
        EnvVars["Environment Variables<br/>FASTMCP_*"]
        UVLock["uv.lock<br/>Dependency resolution"]
    end
    
    ProjectMeta --> Scripts
    Scripts --> OptionalDeps
    OptionalDeps --> DepGroups
    
    BuildSystem --> HatchVersion
    
    PytestConfig --> TyConfig
    TyConfig --> RuffConfig
    
    EnvVars --> PytestConfig
    UVLock --> ProjectMeta
```

The configuration system supports environment variable-based test configuration through `FASTMCP_TEST_MODE`, `FASTMCP_LOG_LEVEL`, and other `FASTMCP_*` prefixed variables.

Sources: [pyproject.toml:1-147](), [.github/workflows/run-tests.yml:78-81]()

# Testing and Development Framework




This document covers FastMCP's comprehensive testing infrastructure, development utilities, and testing patterns. It explains the testing utilities, fixtures, and methodologies used to test FastMCP servers, clients, transports, and integrations.

For information about deployment and production configuration, see [HTTP Server and Deployment](#4). For development workflow tools like the CLI, see [Command Line Interface](#5).

## Testing Infrastructure Overview

FastMCP provides a robust testing framework designed to handle the complexities of testing distributed MCP systems, including process isolation, network communication, authentication flows, and transport mechanisms.

```mermaid
graph TB
    subgraph "Testing Utilities"
        TestUtils["fastmcp.utilities.tests"]
        ProcessMgmt["run_server_in_process()"]
        SettingsOverride["temporary_settings()"]
        LogCapture["caplog_for_fastmcp()"]
        HeadlessAuth["HeadlessOAuth"]
    end
    
    subgraph "Test Fixtures"
        ConfTest["tests/conftest.py"]
        PortMgmt["free_port_factory()"]
        WorkerID["worker_id fixture"]
        IntegrationMarker["integration marker"]
    end
    
    subgraph "Transport Testing"
        HTTPTests["StreamableHttpTransport tests"]
        SSETests["SSETransport tests"]
        StdioTests["StdioTransport tests"]
        MemoryTests["FastMCPTransport tests"]
    end
    
    subgraph "Server Testing"
        ServerFixtures["FastMCP server fixtures"]
        AuthTesting["OAuth/JWT testing"]
        ComponentTesting["Tool/Resource/Prompt testing"]
        MiddlewareTesting["Middleware testing"]
    end
    
    subgraph "Client Testing"
        ClientFixtures["Client fixtures"]
        AuthClientTesting["Client authentication"]
        TimeoutTesting["Timeout behavior"]
        ErrorHandling["Error handling"]
    end
    
    TestUtils --> ProcessMgmt
    TestUtils --> SettingsOverride
    TestUtils --> LogCapture
    TestUtils --> HeadlessAuth
    
    ConfTest --> PortMgmt
    ConfTest --> WorkerID
    ConfTest --> IntegrationMarker
    
    ProcessMgmt --> ServerFixtures
    PortMgmt --> ServerFixtures
    
    ServerFixtures --> HTTPTests
    ServerFixtures --> SSETests
    ServerFixtures --> AuthTesting
    
    HeadlessAuth --> AuthClientTesting
    ClientFixtures --> TimeoutTesting
```

**Testing Framework Architecture**

Sources: [src/fastmcp/utilities/tests.py:1-200](), [tests/conftest.py:1-60]()

## Core Testing Utilities

### Process Management

The `run_server_in_process()` function provides isolated server testing by running FastMCP servers in separate processes:

```mermaid
graph LR
    TestProcess["Test Process"]
    ServerProcess["Server Process"]
    NetworkComm["Network Communication"]
    
    TestProcess -->|"spawn"| ServerProcess
    TestProcess <-->|"HTTP/TCP"| NetworkComm
    NetworkComm <-->|"MCP Protocol"| ServerProcess
    
    subgraph "Server Lifecycle"
        Start["server_fn()"]
        WaitReady["Socket check"]
        TestExecution["Test execution"]
        Cleanup["Process termination"]
        
        Start --> WaitReady
        WaitReady --> TestExecution
        TestExecution --> Cleanup
    end
```

**Process Isolation for Server Testing**

The utility handles server lifecycle, port allocation, and cleanup automatically:

| Function | Purpose | Key Parameters |
|----------|---------|----------------|
| `run_server_in_process()` | Spawns server in separate process | `server_fn`, `host`, `port`, `**kwargs` |
| Socket readiness check | Waits for server to accept connections | `max_attempts=30` |
| Process cleanup | Terminates server process | `timeout=5` for graceful, then `kill()` |

Sources: [src/fastmcp/utilities/tests.py:74-140]()

### Settings Override System

The `temporary_settings()` context manager allows safe modification of FastMCP configuration during tests:

```python
# Example usage pattern from tests
with temporary_settings(log_level='DEBUG', experimental_feature=True):
    # Test code runs with modified settings
    assert fastmcp.settings.log_level == 'DEBUG'
# Settings automatically restored
```

Sources: [src/fastmcp/utilities/tests.py:24-55]()

### Authentication Testing

The `HeadlessOAuth` class simulates OAuth flows without browser interaction:

```mermaid
sequenceDiagram
    participant Test as "Test Code"
    participant HeadlessOAuth as "HeadlessOAuth"
    participant Server as "MCP Server"
    participant AuthProvider as "OAuth Provider"
    
    Test->>HeadlessOAuth: Initialize with mcp_url
    HeadlessOAuth->>Server: GET /auth/authorize
    Server->>AuthProvider: Redirect to OAuth
    AuthProvider-->>HeadlessOAuth: HTTP redirect response
    HeadlessOAuth->>HeadlessOAuth: Parse authorization code
    HeadlessOAuth->>Server: POST /auth/token
    Server-->>HeadlessOAuth: Access token
    HeadlessOAuth-->>Test: Authenticated client
```

**Headless OAuth Flow for Testing**

The implementation bypasses browser interaction by making direct HTTP requests and parsing redirect responses:

| Method | Purpose | Returns |
|--------|---------|---------|
| `redirect_handler()` | Makes HTTP request to auth URL | Stores response |
| `callback_handler()` | Extracts auth code from redirect | `(auth_code, state)` |

Sources: [src/fastmcp/utilities/tests.py:154-200]()

## Test Fixtures and Configuration

### Port Management

FastMCP provides utilities for managing network ports in test environments:

```python
# Free port fixtures from conftest.py
@pytest.fixture
def free_port():
    """Get a free port for the test to use."""
    
@pytest.fixture 
def free_port_factory(worker_id):
    """Factory to get free ports that tracks used ports per test session."""
```

The `free_port_factory` tracks used ports to prevent conflicts in parallel test execution.

Sources: [tests/conftest.py:34-59]()

### Integration Test Marking

Tests are automatically categorized based on their location:

```python
def pytest_collection_modifyitems(items):
    """Automatically mark tests in integration_tests folder with 'integration' marker."""
    for item in items:
        if "integration_tests" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
```

Sources: [tests/conftest.py:8-13]()

## Transport Testing Patterns

### HTTP Transport Testing

FastMCP tests HTTP transports using real server instances with comprehensive scenarios:

```mermaid
graph TB
    subgraph "HTTP Transport Test Patterns"
        ServerFixture["fastmcp_server() fixture"]
        StatelessTest["Stateless HTTP testing"]
        StatefulTest["Stateful HTTP testing"]
        HeaderTest["Header propagation"]
        TimeoutTest["Timeout behavior"]
        ProgressTest["Progress reporting"]
        ElicitationTest["User elicitation"]
    end
    
    subgraph "Test Scenarios"
        BasicPing["Ping operations"]
        ToolCalls["Tool execution"]
        ResourceRead["Resource reading"]
        PromptGet["Prompt retrieval"]
        ErrorHandling["Error conditions"]
    end
    
    ServerFixture --> StatelessTest
    ServerFixture --> StatefulTest
    
    StatelessTest --> BasicPing
    StatefulTest --> ToolCalls
    HeaderTest --> ResourceRead
    TimeoutTest --> ErrorHandling
    ProgressTest --> ToolCalls
    ElicitationTest --> ToolCalls
```

**HTTP Transport Testing Architecture**

Key test patterns include:

- **Parameterized testing**: Tests run against both stateless and stateful HTTP modes
- **Header propagation**: Verification that client headers reach server components
- **Timeout handling**: Testing both client-level and operation-level timeouts
- **Progress reporting**: Async progress updates during long-running operations

Sources: [tests/client/test_streamable_http.py:21-248]()

### SSE Transport Testing

Server-Sent Events transport testing follows similar patterns with transport-specific considerations:

| Test Category | Key Features | Example Test |
|---------------|--------------|--------------|
| Basic connectivity | Ping, list operations | `test_ping()` |
| Header handling | Client header propagation | `test_http_headers()` |
| Timeout behavior | Platform-specific timeout handling | `TestTimeout` class |
| Nested routing | Complex URL path resolution | `test_nested_sse_server_resolves_correctly()` |

Sources: [tests/client/test_sse.py:19-167]()

## Authentication Testing Framework

### JWT Provider Testing

FastMCP includes comprehensive JWT testing with both RSA and symmetric key scenarios:

```mermaid
graph TB
    subgraph "JWT Testing Components"
        RSAKeyPair["RSAKeyPair helper"]
        SymmetricHelper["SymmetricKeyHelper"]
        JWTVerifier["JWTVerifier provider"]
        MockJWKS["JWKS mocking"]
    end
    
    subgraph "Test Scenarios"
        ValidTokens["Valid token validation"]
        ExpiredTokens["Expired token rejection"]
        InvalidIssuer["Invalid issuer rejection"]
        InvalidAudience["Invalid audience rejection"]
        ScopeExtraction["Scope parsing"]
        AlgorithmValidation["Algorithm verification"]
    end
    
    subgraph "Key Management"
        KeyGeneration["RSA key generation"]
        TokenCreation["JWT token creation"]
        SignatureValidation["Signature verification"]
    end
    
    RSAKeyPair --> KeyGeneration
    SymmetricHelper --> TokenCreation
    JWTVerifier --> ValidTokens
    MockJWKS --> SignatureValidation
    
    ValidTokens --> ScopeExtraction
    ExpiredTokens --> AlgorithmValidation
    InvalidIssuer --> InvalidAudience
```

**JWT Authentication Testing Framework**

The testing framework provides helpers for various JWT scenarios:

- **RSA key management**: `RSAKeyPair.generate()` creates test key pairs
- **Symmetric keys**: `SymmetricKeyHelper` for HMAC algorithms
- **Token validation**: Comprehensive issuer, audience, and scope testing
- **JWKS mocking**: HTTP mocking for JWKS URI endpoints

Sources: [tests/server/auth/test_jwt_provider.py:14-871]()

### OAuth Provider Testing

OAuth providers are tested using integration patterns with real HTTP servers:

```python
# Example OAuth provider test pattern
def run_mcp_server(host: str, port: int) -> None:
    mcp = FastMCP(auth=DescopeProvider(...))
    
    @mcp.tool
    def add(a: int, b: int) -> int:
        return a + b
    
    mcp.run(host=host, port=port, transport="http")

@pytest.fixture  
def mcp_server_url() -> Generator[str]:
    with run_server_in_process(run_mcp_server) as url:
        yield f"{url}/mcp"
```

Sources: [tests/server/auth/providers/test_descope.py:121-141](), [tests/server/auth/providers/test_workos.py:160-178]()

## Component Testing Patterns

### Tool Testing with BulkToolCaller

The `BulkToolCaller` provides patterns for testing tool execution at scale:

```mermaid
graph LR
    subgraph "Bulk Tool Testing"
        BulkCaller["BulkToolCaller"]
        LiveServer["Live FastMCP Server"]
        ToolRegistry["Tool registration"]
        
        BulkCaller --> LiveServer
        LiveServer --> ToolRegistry
    end
    
    subgraph "Test Scenarios"
        SingleSuccess["Single tool success"]
        MultipleSuccess["Multiple tool success"] 
        ErrorHandling["Error propagation"]
        ContinueOnError["Continue on error"]
    end
    
    subgraph "Tool Types"
        EchoTool["echo_tool()"]
        ErrorTool["error_tool()"]
        NoReturnTool["no_return_tool()"]
    end
    
    ToolRegistry --> EchoTool
    ToolRegistry --> ErrorTool  
    ToolRegistry --> NoReturnTool
    
    BulkCaller --> SingleSuccess
    BulkCaller --> MultipleSuccess
    BulkCaller --> ErrorHandling
    BulkCaller --> ContinueOnError
```

**Bulk Tool Testing Framework**

Key testing patterns include:

- **Live server integration**: Tests use actual `FastMCP` instances with registered tools
- **Error propagation**: Testing both fail-fast and continue-on-error modes
- **Result validation**: Snapshot testing for consistent output verification

Sources: [tests/contrib/test_bulk_tool_caller.py:70-289]()

### HTTP Dependencies Testing

FastMCP tests dependency injection in HTTP contexts across multiple transports:

| Component | Test Pattern | Verification |
|-----------|--------------|--------------|
| `get_http_request()` | Tool, Resource, Prompt usage | Header extraction from HTTP request |
| StreamableHttp | Direct header propagation | Client headers in server context |
| SSE | Event stream headers | Header preservation across SSE |

Sources: [tests/server/http/test_http_dependencies.py:13-124]()

## Development Workflow Testing

### OpenAPI Integration Testing

FastMCP tests OpenAPI server generation with both legacy and experimental parsers:

```python
# Test pattern for OpenAPI integration
def fastmcp_server_for_headers() -> FastMCP:
    app = FastAPI()
    
    @app.get("/headers")  
    def get_headers(request: Request):
        return request.headers
    
    mcp = FastMCP.from_fastapi(
        app,
        httpx_client_kwargs={"headers": {"x-server-header": "test-abc"}},
        route_maps=[
            RouteMap(methods=["GET"], pattern=r".*\{.*\}.*", mcp_type=MCPType.RESOURCE_TEMPLATE),
            RouteMap(methods=["GET"], pattern=r".*", mcp_type=MCPType.RESOURCE),
        ],
    )
    return mcp
```

The testing verifies:
- **Route mapping**: HTTP routes to MCP components
- **Header propagation**: Client and server headers through proxy chains
- **Resource templates**: Dynamic URI pattern matching

Sources: [tests/client/test_openapi_legacy.py:13-47](), [tests/client/test_openapi_experimental.py:14-46]()

## Best Practices and Patterns

### Test Organization

FastMCP follows these testing organization principles:

1. **Fixture-based setup**: Reusable server and client configurations
2. **Process isolation**: Each test gets clean server instances  
3. **Transport agnostic**: Tests run across multiple transport types
4. **Integration marking**: Automatic categorization of integration vs unit tests
5. **Parallel execution**: xdist compatibility with port management

### Error Testing Patterns

```python