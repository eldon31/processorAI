The FastMCP middleware system provides a flexible framework for intercepting, monitoring, and modifying MCP message processing. This system allows developers to add cross-cutting concerns like logging, timing, error handling, and rate limiting without modifying core server logic.

This document covers the middleware architecture, built-in middleware implementations, and patterns for creating custom middleware. For authentication-specific middleware functionality, see [Authentication and Security](#4.1). For HTTP server deployment patterns, see [HTTP Server and Deployment](#4).

## Core Middleware Architecture

The middleware system is built around a pipeline pattern where each middleware can inspect, modify, or handle MCP messages before passing control to the next middleware in the chain.

### Middleware Pipeline Flow

```mermaid
graph TD
    Client["MCP Client Request"]
    Server["FastMCP Server"]
    
    subgraph "Middleware Pipeline"
        MW1["Middleware 1<br/>LoggingMiddleware"]
        MW2["Middleware 2<br/>TimingMiddleware"] 
        MW3["Middleware 3<br/>ErrorHandlingMiddleware"]
        Handler["MCP Handler<br/>@server.tool<br/>@server.resource"]
    end
    
    Client --> Server
    Server --> MW1
    MW1 --> MW2
    MW2 --> MW3
    MW3 --> Handler
    
    Handler --> MW3
    MW3 --> MW2
    MW2 --> MW1
    MW1 --> Server
    Server --> Client
```

Sources: [src/fastmcp/server/middleware/middleware.py:1-200](), [tests/server/middleware/test_logging.py:506-775]()

### Core Middleware Components

```mermaid
classDiagram
    class Middleware {
        +on_message(context, call_next)
        +on_request(context, call_next) 
        +on_notification(context, call_next)
        +on_call_tool(context, call_next)
        +on_read_resource(context, call_next)
        +on_get_prompt(context, call_next)
        +on_list_tools(context, call_next)
        +on_list_resources(context, call_next)
        +on_list_prompts(context, call_next)
    }
    
    class MiddlewareContext~T~ {
        +method: str | None
        +source: Literal["server", "client"]
        +type: Literal["request", "notification"]
        +message: T
        +timestamp: datetime
    }
    
    class CallNext~T_R~ {
        <<type alias>>
        +__call__(context: MiddlewareContext[T]) -> Awaitable[R]
    }
    
    Middleware --> MiddlewareContext : uses
    Middleware --> CallNext : calls
```

Sources: [src/fastmcp/server/middleware/middleware.py:11-50]()

The `Middleware` base class provides hook methods for different MCP operations. The `MiddlewareContext[T]` carries message data and metadata through the pipeline, while `CallNext[T, R]` represents the continuation of the middleware chain.

## Built-in Middleware Types

FastMCP includes several production-ready middleware implementations for common server needs.

### Logging Middleware

The logging system provides two complementary approaches for request monitoring and debugging.

```mermaid
graph LR
    subgraph "Logging Middleware Types"
        LM["LoggingMiddleware<br/>fastmcp.requests logger<br/>Human-readable format"]
        SLM["StructuredLoggingMiddleware<br/>fastmcp.structured logger<br/>JSON format"]
    end
    
    subgraph "Configuration Options"
        Payloads["include_payloads: bool<br/>include_payload_length: bool<br/>estimate_payload_tokens: bool"]
        Filtering["methods: list[str]<br/>max_payload_length: int"]
        Serialization["payload_serializer: Callable"]
    end
    
    LM --> Payloads
    SLM --> Payloads
    LM --> Filtering  
    SLM --> Filtering
    SLM --> Serialization
```

Sources: [src/fastmcp/server/middleware/logging.py:143-196](), [src/fastmcp/server/middleware/logging.py:198-246]()

| Middleware | Logger Name | Output Format | Use Case |
|------------|-------------|---------------|----------|
| `LoggingMiddleware` | `fastmcp.requests` | Key-value pairs | Development, human debugging |
| `StructuredLoggingMiddleware` | `fastmcp.structured` | JSON objects | Production, log aggregation |

Key features include payload serialization via `default_serializer()` using `pydantic_core.to_json()`, token estimation at approximately 4 characters per token, and configurable payload truncation via `max_payload_length`.

### Timing and Performance Middleware

Performance monitoring middleware provides request timing and operation-specific measurements.

```mermaid
graph TD
    subgraph "Timing Middleware Architecture"
        TM["TimingMiddleware<br/>fastmcp.timing logger<br/>Overall request timing"]
        DTM["DetailedTimingMiddleware<br/>fastmcp.timing.detailed logger<br/>Per-operation timing"]
    end
    
    subgraph "Timing Hooks"
        Operations["on_call_tool()<br/>on_read_resource()<br/>on_get_prompt()<br/>on_list_tools()<br/>on_list_resources()<br/>on_list_prompts()"]
    end
    
    TM --> |"measures"| RequestLevel["Request-level timing<br/>time.perf_counter()"]
    DTM --> |"measures"| Operations
    DTM --> |"_time_operation()"| RequestLevel
```

Sources: [src/fastmcp/server/middleware/timing.py:10-58](), [src/fastmcp/server/middleware/timing.py:60-157]()

Both middleware use `time.perf_counter()` for high-precision timing measurements and log results in milliseconds with 2 decimal precision.

### Error Handling and Retry Middleware

Error management middleware provides consistent error transformation and automatic retry capabilities.

```mermaid
graph TD
    subgraph "Error Handling Pipeline"
        EHM["ErrorHandlingMiddleware"]
        RM["RetryMiddleware"]
    end
    
    subgraph "Error Processing"
        LogError["_log_error()<br/>Track error_counts<br/>Call error_callback"]
        Transform["_transform_error()<br/>Convert to McpError<br/>Map exception types"]
    end
    
    subgraph "Retry Logic"
        ShouldRetry["_should_retry()<br/>Check retry_exceptions"]
        CalcDelay["_calculate_delay()<br/>Exponential backoff"]
    end
    
    EHM --> LogError
    EHM --> Transform
    RM --> ShouldRetry
    RM --> CalcDelay
    
    Transform --> |"ValueError → -32602"| InvalidParams["Invalid params"]
    Transform --> |"FileNotFoundError → -32001"| NotFound["Resource not found"] 
    Transform --> |"PermissionError → -32000"| PermissionDenied["Permission denied"]
    Transform --> |"TimeoutError → -32000"| Timeout["Request timeout"]
```

Sources: [src/fastmcp/server/middleware/error_handling.py:15-124](), [src/fastmcp/server/middleware/error_handling.py:126-207]()

The `ErrorHandlingMiddleware` transforms Python exceptions into MCP-compliant `McpError` instances with appropriate error codes, while `RetryMiddleware` implements exponential backoff retry logic for transient failures.

### Rate Limiting Middleware

Rate limiting middleware protects servers from abuse using token bucket and sliding window algorithms.

```mermaid
graph LR
    subgraph "Rate Limiting Strategies"
        TBRM["RateLimitingMiddleware<br/>TokenBucketRateLimiter<br/>Burst capacity support"]
        SWRM["SlidingWindowRateLimitingMiddleware<br/>SlidingWindowRateLimiter<br/>Precise time windows"]
    end
    
    subgraph "Token Bucket Algorithm"
        TB["capacity: int<br/>refill_rate: float<br/>tokens: float<br/>consume(tokens=1)"]
    end
    
    subgraph "Sliding Window Algorithm"
        SW["max_requests: int<br/>window_seconds: int<br/>requests: deque<br/>is_allowed()"]
    end
    
    TBRM --> TB
    SWRM --> SW
    
    TB --> |"Allow bursts"| BurstTraffic["Handle burst traffic<br/>Refill over time"]
    SW --> |"Precise limits"| PreciseControl["Exact request counting<br/>Memory per client"]
```

Sources: [src/fastmcp/server/middleware/rate_limiting.py:92-168](), [src/fastmcp/server/middleware/rate_limiting.py:170-232]()

Both implementations support per-client rate limiting via `get_client_id` functions and use `asyncio.Lock()` for thread-safe operation.

## Custom Middleware Development

Creating custom middleware involves extending the `Middleware` base class and implementing the appropriate hook methods.

### Middleware Hook Methods

| Hook Method | Trigger | Context Type | Use Case |
|-------------|---------|--------------|----------|
| `on_message()` | All messages | Generic | Universal logging, authentication |
| `on_request()` | Request messages | Generic | Timing, rate limiting |
| `on_notification()` | Notification messages | Generic | Event tracking |
| `on_call_tool()` | Tool execution | `CallToolRequest` | Tool-specific logic |
| `on_read_resource()` | Resource access | `ReadResourceRequest` | Resource security |
| `on_get_prompt()` | Prompt retrieval | `GetPromptRequest` | Prompt customization |

Sources: [src/fastmcp/server/middleware/middleware.py:11-200]()

### Custom Middleware Example Pattern

```mermaid
sequenceDiagram
    participant Client
    participant CustomMiddleware
    participant CallNext
    participant Handler
    
    Client->>CustomMiddleware: MCP Request
    CustomMiddleware->>CustomMiddleware: Pre-processing
    CustomMiddleware->>CallNext: call_next(context)
    CallNext->>Handler: Execute handler
    Handler->>CallNext: Return result
    CallNext->>CustomMiddleware: Return result
    CustomMiddleware->>CustomMiddleware: Post-processing
    CustomMiddleware->>Client: Modified result
```

Sources: [tests/server/middleware/test_logging.py:110-141](), [tests/server/middleware/test_timing.py:47-70]()

Custom middleware should call `await call_next(context)` to continue the pipeline and can modify the context or result before/after the call.

## Integration with FastMCP Server

Middleware integration occurs through the `FastMCP.add_middleware()` method, which builds the middleware pipeline in registration order.

### Middleware Registration and Execution

```mermaid
graph TD
    subgraph "FastMCP Server Integration"
        Server["FastMCP(name='MyServer')"]
        AddMW["add_middleware(middleware)"]
        Pipeline["Middleware Pipeline"]
    end
    
    subgraph "Execution Context"
        LowLevel["Low-level MCP Server<br/>Protocol handlers"]
        Managers["Component Managers<br/>ToolManager<br/>ResourceManager<br/>PromptManager"]
    end
    
    Server --> AddMW
    AddMW --> Pipeline
    Pipeline --> LowLevel
    LowLevel --> Managers
    
    Pipeline --> |"on_call_tool"| ToolFlow["Tool execution flow"]
    Pipeline --> |"on_read_resource"| ResourceFlow["Resource access flow"] 
    Pipeline --> |"on_get_prompt"| PromptFlow["Prompt retrieval flow"]
```

Sources: [tests/server/middleware/test_logging.py:543-575](), [tests/server/middleware/test_timing.py:192-224]()

Middleware executes in the order registered, forming a chain where each middleware can inspect, modify, or terminate request processing. The system supports both synchronous and asynchronous middleware operations through the `CallNext` continuation pattern.

## Middleware Configuration Patterns

Production deployments typically combine multiple middleware types for comprehensive server monitoring and protection.

### Common Middleware Stack Configuration

```mermaid
graph TB
    subgraph "Production Middleware Stack"
        Order1["1. RateLimitingMiddleware<br/>Protect against abuse"]
        Order2["2. LoggingMiddleware<br/>Request/response logging"]  
        Order3["3. TimingMiddleware<br/>Performance monitoring"]
        Order4["4. ErrorHandlingMiddleware<br/>Error transformation"]
        Order5["5. RetryMiddleware<br/>Transient failure handling"]
    end
    
    Order1 --> Order2
    Order2 --> Order3  
    Order3 --> Order4
    Order4 --> Order5
    Order5 --> |"Reaches"| CoreHandler["Core MCP Handlers"]
```

Sources: [tests/server/middleware/test_error_handling.py:589-624](), [tests/server/middleware/test_logging.py:710-744]()

This ordering ensures that rate limiting occurs first to protect server resources, followed by comprehensive monitoring and error handling capabilities. The middleware system's flexibility allows for custom combinations based on specific deployment requirements.

# Command Line Interface




The FastMCP CLI provides a comprehensive command-line interface for running, developing, installing, and inspecting MCP servers. Built with `cyclopts`, it serves as the primary entry point for all FastMCP operations from development to production deployment.

For information about the underlying server architecture that the CLI manages, see [FastMCP Server Core](#2). For details about client-server communication patterns, see [FastMCP Client System](#3).

## CLI Application Architecture

The FastMCP CLI is implemented as a `cyclopts.App` with modular command structure supporting both direct execution and subprocess delegation through `uv`.

### Main CLI Application Structure

```mermaid
graph TB
    subgraph "Entry Point"
        app["app: cyclopts.App<br/>name: 'fastmcp'<br/>version: fastmcp.__version__"]
    end
    
    subgraph "Core Commands"
        version_cmd["version()"]
        run_cmd["run()"] 
        dev_cmd["dev()"]
        inspect_cmd["inspect()"]
    end
    
    subgraph "Install Commands"
        install_app["install_app: cyclopts.App"]
        claude_code["claude_code_command()"]
        claude_desktop["claude_desktop_command()"] 
        cursor["cursor_command()"]
        mcp_json["mcp_json_command()"]
    end
    
    subgraph "Project Commands"
        project_app["project_app: cyclopts.App"]
        prepare["prepare()"]
    end
    
    app --> version_cmd
    app --> run_cmd
    app --> dev_cmd
    app --> inspect_cmd
    app --> install_app
    app --> project_app
    
    install_app --> claude_code
    install_app --> claude_desktop
    install_app --> cursor
    install_app --> mcp_json
    
    project_app --> prepare
```

**Sources:** [src/fastmcp/cli/cli.py:36-40](), [src/fastmcp/cli/cli.py:781-782](), [src/fastmcp/cli/cli.py:871-874]()

### Configuration and Environment Management

```mermaid
graph LR
    subgraph "Configuration Loading"
        load_and_merge["load_and_merge_config()"]
        config_file["fastmcp.json"]
        cli_overrides["CLI arguments"]
    end
    
    subgraph "Environment Execution"
        needs_uv_check["needs_uv?"]
        direct_exec["Direct execution"]
        uv_subprocess["uv run subprocess"]
    end
    
    subgraph "Configuration Objects"
        mcp_config["MCPServerConfig"]
        uv_env["UVEnvironment"]
        deployment["Deployment"]
        source["FileSystemSource"]
    end
    
    config_file --> load_and_merge
    cli_overrides --> load_and_merge
    load_and_merge --> mcp_config
    
    mcp_config --> uv_env
    mcp_config --> deployment
    mcp_config --> source
    
    uv_env --> needs_uv_check
    needs_uv_check -->|true| uv_subprocess
    needs_uv_check -->|false| direct_exec
```

**Sources:** [src/fastmcp/utilities/cli.py:23](), [src/fastmcp/cli/cli.py:465-469](), [src/fastmcp/cli/cli.py:497-517]()

## Core CLI Commands

### Version Command

The `version()` command provides comprehensive version and platform information for debugging and support purposes.

| Option | Flag | Description |
|--------|------|-------------|
| Copy | `--copy` | Copy version information to clipboard using `pyperclip` |

Information displayed:
- `fastmcp.__version__` - FastMCP version
- `importlib.metadata.version("mcp")` - MCP protocol version  
- `platform.python_version()` - Python version
- `platform.platform()` - Platform details
- `Path(fastmcp.__file__).resolve().parents[1]` - FastMCP root path

**Sources:** [src/fastmcp/cli/cli.py:92-127]()

### Run Command

The `run()` command executes MCP servers with flexible server specification parsing and multiple execution modes.

#### Server Specification Resolution

```mermaid
graph LR
    subgraph "run_command() Flow"
        run_cmd["run()"]
        config_load["load_and_merge_config()"]
        spec_check["server_spec analysis"]
    end
    
    subgraph "Specification Types"
        url_spec["is_url(server_spec)"]
        json_spec["server_spec.endswith('.json')"]
        file_spec["file path"]
    end
    
    subgraph "Server Creation"
        create_client["create_client_server()"]
        create_mcp_config["create_mcp_config_server()"] 
        filesystem_source["FileSystemSource"]
    end
    
    run_cmd --> config_load
    config_load --> spec_check
    
    spec_check --> url_spec
    spec_check --> json_spec  
    spec_check --> file_spec
    
    url_spec --> create_client
    json_spec --> create_mcp_config
    file_spec --> filesystem_source
```

**Sources:** [src/fastmcp/cli/run.py:79-198](), [src/fastmcp/cli/run.py:25-29](), [src/fastmcp/cli/run.py:31-49](), [src/fastmcp/cli/run.py:51-60]()

#### Transport Configuration

| Transport | Default Host | Default Port | Default Path |
|-----------|--------------|--------------|-------------|
| `stdio` | N/A | N/A | N/A |
| `http` / `streamable-http` | `127.0.0.1` | `8000` | `/mcp/` |
| `sse` | `127.0.0.1` | `8000` | `/sse/` |

The run command supports both direct execution and `uv run` subprocess execution based on environment configuration.

**Sources:** [src/fastmcp/cli/cli.py:313-333](), [src/fastmcp/cli/cli.py:465-517]()

### Dev Command

The `dev()` command launches the MCP Inspector with automatic environment setup and dependency management.

#### Development Workflow

```mermaid
graph TB
    subgraph "dev() Command Flow"
        dev_start["dev()"]
        load_config["load_and_merge_config()"]
        load_server["config.source.load_server()"]
        check_deps["server.dependencies check"]
    end
    
    subgraph "Environment Setup"
        build_cmd["config.environment.build_command()"]
        set_env["env vars: CLIENT_PORT, SERVER_PORT"]
        get_npx["_get_npx_command()"]
    end
    
    subgraph "Inspector Launch" 
        inspector_cmd["@modelcontextprotocol/inspector"]
        subprocess_run["subprocess.run()"]
    end
    
    dev_start --> load_config
    load_config --> load_server
    load_server --> check_deps
    check_deps --> build_cmd
    build_cmd --> set_env
    set_env --> get_npx
    get_npx --> inspector_cmd
    inspector_cmd --> subprocess_run
```

The `dev` command always runs via `uv run` subprocess and includes deprecation warnings for servers using the legacy `dependencies` parameter.

**Sources:** [src/fastmcp/cli/cli.py:129-307](), [src/fastmcp/cli/cli.py:43-56](), [src/fastmcp/cli/cli.py:234-251]()

### Inspect Command  

The `inspect()` command analyzes FastMCP servers and generates detailed reports in multiple formats.

| Option | Flag | Description |
|--------|------|-------------|
| Format | `--format` / `-f` | Output format: `fastmcp` or `mcp` |
| Output | `--output` / `-o` | Save to file (requires `--format`) |

#### Inspection Process

```mermaid
graph LR
    subgraph "inspect() Flow"
        inspect_start["inspect()"]
        load_config["load_and_merge_config()"]
        load_server["config.source.load_server()"]
        inspect_server["inspect_fastmcp()"]
    end
    
    subgraph "Output Generation"
        format_check["format specified?"]
        text_summary["console.print() summary"]
        format_info["format_info()"]
        json_output["JSON output"]
    end
    
    inspect_start --> load_config
    load_config --> load_server
    load_server --> inspect_server
    inspect_server --> format_check
    
    format_check -->|false| text_summary
    format_check -->|true| format_info
    format_info --> json_output
```

**Sources:** [src/fastmcp/cli/cli.py:543-777](), [src/fastmcp/utilities/inspect.py:26-28]()

## Install Commands

The FastMCP CLI provides installation commands for multiple MCP clients through a dedicated install subcommand structure.

### Install Command Architecture

```mermaid
graph TB
    subgraph "Install App Structure"
        install_app["install_app: cyclopts.App"]
        claude_code_cmd["claude_code_command()"]
        claude_desktop_cmd["claude_desktop_command()"]
        cursor_cmd["cursor_command()"]
        mcp_json_cmd["mcp_json_command()"]
    end
    
    subgraph "Client Integrations"
        claude_code_install["install_claude_code()"]
        claude_desktop_install["install_claude_desktop()"]
        cursor_install["install_cursor()"]
        mcp_json_install["install_mcp_json()"]
    end
    
    subgraph "Common Processing"
        process_common["process_common_args()"]
        uv_env["UVEnvironment.build_command()"]
        stdio_config["StdioMCPServer"]
    end
    
    claude_code_cmd --> process_common
    claude_desktop_cmd --> process_common
    cursor_cmd --> process_common
    mcp_json_cmd --> process_common
    
    process_common --> uv_env
    uv_env --> stdio_config
    
    claude_code_cmd --> claude_code_install
    claude_desktop_cmd --> claude_desktop_install
    cursor_cmd --> cursor_install
    mcp_json_cmd --> mcp_json_install
```

**Sources:** [src/fastmcp/cli/cli.py:874](), [src/fastmcp/cli/install/claude_code.py:153-244](), [src/fastmcp/cli/install/claude_desktop.py:125-214](), [src/fastmcp/cli/install/cursor.py:234-331](), [src/fastmcp/cli/install/mcp_json.py:98-196]()

### Client-Specific Installation

#### Claude Desktop Integration

```mermaid
graph LR
    subgraph "Claude Desktop Install"
        find_config_path["get_claude_config_path()"]
        config_file["claude_desktop_config.json"]
        build_command["env_config.build_command()"]
        stdio_server["StdioMCPServer"]
        update_config["update_config_file()"]
    end
    
    subgraph "Platform Paths"
        windows_path["AppData/Roaming/Claude"]
        macos_path["Library/Application Support/Claude"]
        linux_path["~/.config/Claude"]
    end
    
    find_config_path --> windows_path
    find_config_path --> macos_path
    find_config_path --> linux_path
    find_config_path --> config_file
    config_file --> update_config
```

**Sources:** [src/fastmcp/cli/install/claude_desktop.py:20-36](), [src/fastmcp/cli/install/claude_desktop.py:38-123]()

#### Cursor Integration

```mermaid
graph LR
    subgraph "Cursor Install Flow"
        generate_deeplink["generate_cursor_deeplink()"]
        base64_encode["base64.urlsafe_b64encode()"]
        deeplink_url["cursor://anysphere.cursor-deeplink/mcp/install"]
        open_deeplink["open_deeplink()"]
    end
    
    subgraph "Platform Commands"
        macos_open["subprocess.run(['open', deeplink])"]
        windows_start["subprocess.run(['start', deeplink])"]
        linux_xdg["subprocess.run(['xdg-open', deeplink])"]
    end
    
    generate_deeplink --> base64_encode
    base64_encode --> deeplink_url
    deeplink_url --> open_deeplink
    
    open_deeplink --> macos_open
    open_deeplink --> windows_start
    open_deeplink --> linux_xdg
```

**Sources:** [src/fastmcp/cli/install/cursor.py:21-43](), [src/fastmcp/cli/install/cursor.py:45-66]()

### Project Preparation

The `project prepare` command creates persistent environments for repeated server execution.

#### Project Prepare Flow

```mermaid
graph TB
    subgraph "prepare() Command"
        prepare_start["prepare()"]
        find_config["MCPServerConfig.find_config()"]
        load_config["MCPServerConfig.from_file()"]
        prepare_env["config.prepare()"]
    end
    
    subgraph "Environment Creation"
        create_pyproject["pyproject.toml creation"]
        uv_sync["uv sync"]
        venv_setup[".venv setup"]
        source_prep["source preparation"]
    end
    
    prepare_start --> find_config
    find_config --> load_config
    load_config --> prepare_env
    prepare_env --> create_pyproject
    prepare_env --> uv_sync
    prepare_env --> venv_setup
    prepare_env --> source_prep
```

**Sources:** [src/fastmcp/cli/cli.py:784-867](), [src/fastmcp/utilities/mcp_server_config/__init__.py:31](), [src/fastmcp/utilities/mcp_server_config/__init__.py:55-57]()

## Configuration System Integration

### Configuration Loading and Merging

The CLI integrates with the FastMCP configuration system to provide seamless operation across different deployment scenarios.

```mermaid
graph LR
    subgraph "Config Resolution"
        cli_args["CLI arguments"]
        fastmcp_json["fastmcp.json"]
        auto_detect["MCPServerConfig.find_config()"]
        load_merge["load_and_merge_config()"]
    end
    
    subgraph "Config Objects"
        mcp_server_config["MCPServerConfig"]
        filesystem_source["FileSystemSource"]
        uv_environment["UVEnvironment"] 
        deployment["Deployment"]
    end
    
    subgraph "Execution Modes"
        direct_import["Direct import"]
        uv_subprocess["uv run subprocess"]
        needs_uv_check["environment.build_command() != test_cmd"]
    end
    
    cli_args --> load_merge
    fastmcp_json --> auto_detect
    auto_detect --> load_merge
    load_merge --> mcp_server_config
    
    mcp_server_config --> filesystem_source
    mcp_server_config --> uv_environment
    mcp_server_config --> deployment
    
    uv_environment --> needs_uv_check
    needs_uv_check -->|true| uv_subprocess
    needs_uv_check -->|false| direct_import
```

**Sources:** [src/fastmcp/utilities/cli.py:23](), [src/fastmcp/cli/cli.py:424-439](), [src/fastmcp/cli/cli.py:467-469]()

## Error Handling and Platform Support

### Cross-Platform Command Detection

The CLI handles platform-specific differences for external tool detection and subprocess execution.

```mermaid
graph TB
    subgraph "NPX Detection (_get_npx_command)"
        platform_check["sys.platform check"]
        windows_detection["Try npx.cmd, npx.exe, npx"]
        unix_detection["Use npx directly"]
        subprocess_test["subprocess.run(['cmd', '--version'])"]
    end
    
    subgraph "Claude Code Detection (find_claude_command)"
        shutil_which["shutil.which('claude')"]
        common_paths["Check installation paths"]
        version_check["subprocess.run(['path', '--version'])"]
        claude_code_verify["'Claude Code' in stdout"]
    end
    
    subgraph "Error Recovery"
        calledprocesserror["subprocess.CalledProcessError"]
        filenotfounderror["FileNotFoundError"]
        graceful_fallback["Return None or False"]
    end
    
    platform_check -->|win32| windows_detection
    platform_check -->|unix-like| unix_detection
    
    subprocess_test --> calledprocesserror
    subprocess_test --> filenotfounderror
    calledprocesserror --> graceful_fallback
    filenotfounderror --> graceful_fallback
```

**Sources:** [src/fastmcp/cli/cli.py:43-56](), [src/fastmcp/cli/install/claude_code.py:20-66](), [src/fastmcp/cli/install/cursor.py:45-66]()

## Command Execution Patterns

### UV Integration

The CLI leverages `uv` for modern Python dependency management and isolated execution environments:

```mermaid
graph LR
    subgraph "UV Command Construction"
        build_start["_build_uv_command()"]
        
        build_start --> base_cmd["['uv', 'run']"]
        base_cmd --> add_python["--python version"]
        add_python --> add_project["--project path"]
        add_project --> add_fastmcp["--with fastmcp"]
        add_fastmcp --> add_packages["--with packages"]
        add_packages --> add_requirements["--with-requirements"]
        add_requirements --> add_fastmcp_run["['fastmcp', 'run', server_spec]"]
        add_fastmcp_run --> add_flags["Transport/logging flags"]
    end
    
    subgraph "Execution Modes"
        direct_mode["Direct import<br/>run_command()"]
        uv_mode["UV subprocess<br/>run_with_uv()"]
        
        condition["UV options provided?"]
        condition -->|true| uv_mode
        condition -->|false| direct_mode
    end
    
    style build_start fill:#f9f9f9,stroke:#333,stroke-width:2px
    style condition fill:#e8f5e8,stroke:#333,stroke-width:2px
```

**Sources:** [src/fastmcp/cli/cli.py:60-100](), [src/fastmcp/cli/cli.py:389-413](), [src/fastmcp/cli/run.py:174-250]()

### Cross-Platform Considerations

The CLI handles platform-specific differences, particularly for Windows systems:

| Platform | NPX Detection | Shell Usage | Path Handling |
|----------|---------------|-------------|---------------|
| Windows | Try `npx.cmd`, `npx.exe`, `npx` | `shell=True` | Drive letter colon handling |
| Unix-like | Use `npx` directly | `shell=False` | Standard path parsing |

**Sources:** [src/fastmcp/cli/cli.py:35-49](), [src/fastmcp/cli/cli.py:257-262]()

## Error Handling and Validation

The CLI implements comprehensive error handling with structured logging:

- **File validation**: Checks for file existence and type during path parsing
- **Module import errors**: Graceful handling of import failures with descriptive messages
- **Server validation**: Ensures imported objects are valid FastMCP instances
- **Subprocess errors**: Captures and reports subprocess execution failures
- **Configuration validation**: Validates MCP config files using Pydantic models

Exit codes follow standard conventions:
- `0`: Success
- `1`: General errors (file not found, import failures, validation errors)

**Sources:** [src/fastmcp/cli/run.py:52-57](), [src/fastmcp/cli/run.py:94-100](), [src/fastmcp/cli/run.py:118-124](), [src/fastmcp/cli/cli.py:265-282]()

# OpenAPI Integration




FastMCP's OpenAPI integration enables automatic generation of FastMCP servers from OpenAPI specifications, converting HTTP API definitions into MCP Tools, Resources, and ResourceTemplates. This system parses OpenAPI schemas and creates appropriate MCP components based on configurable route mapping rules.

For general FastMCP server functionality, see [FastMCP Server Core](#2). For HTTP server deployment, see [HTTP Server and Deployment](#4). For client-side API consumption, see [FastMCP Client System](#3).

## Architecture Overview

The OpenAPI integration consists of three main layers: schema parsing, route mapping, and component generation. The system transforms OpenAPI specifications into FastMCP components through an intermediate representation.

```mermaid
graph TB
    subgraph "Input Layer"
        OpenAPISpec["OpenAPI Specification<br/>(JSON/YAML)"]
    end
    
    subgraph "Parsing Layer"
        OpenAPIParser["OpenAPIParser<br/>parse_openapi_to_http_routes()"]
        HTTPRoute["HTTPRoute<br/>Intermediate Representation"]
    end
    
    subgraph "Mapping Layer"
        RouteMap["RouteMap Objects<br/>Mapping Rules"]
        DetermineType["_determine_route_type()"]
        MCPType["MCPType Enum<br/>(TOOL/RESOURCE/RESOURCE_TEMPLATE)"]
    end
    
    subgraph "Generation Layer"
        FastMCPOpenAPI["FastMCPOpenAPI<br/>Main Server Class"]
        OpenAPITool["OpenAPITool"]
        OpenAPIResource["OpenAPIResource"] 
        OpenAPIResourceTemplate["OpenAPIResourceTemplate"]
    end
    
    subgraph "Execution Layer"
        HTTPClient["httpx.AsyncClient<br/>HTTP Execution"]
        MCPProtocol["MCP Protocol<br/>Tool/Resource Calls"]
    end
    
    OpenAPISpec --> OpenAPIParser
    OpenAPIParser --> HTTPRoute
    HTTPRoute --> DetermineType
    RouteMap --> DetermineType
    DetermineType --> MCPType
    HTTPRoute --> FastMCPOpenAPI
    MCPType --> FastMCPOpenAPI
    FastMCPOpenAPI --> OpenAPITool
    FastMCPOpenAPI --> OpenAPIResource
    FastMCPOpenAPI --> OpenAPIResourceTemplate
    OpenAPITool --> HTTPClient
    OpenAPIResource --> HTTPClient
    OpenAPIResourceTemplate --> HTTPClient
    HTTPClient --> MCPProtocol
```

**Sources:** [src/fastmcp/server/openapi.py:1-100](), [src/fastmcp/utilities/openapi.py:200-250]()

## Core Components

### FastMCPOpenAPI Server Class

The `FastMCPOpenAPI` class extends `FastMCP` to provide OpenAPI-based server creation. It parses OpenAPI specifications and automatically generates appropriate MCP components.

```mermaid
graph LR
    FastMCPOpenAPI["FastMCPOpenAPI"]
    
    subgraph "Configuration"
        RouteMapsList["route_maps: list[RouteMap]"]
        RouteMapFn["route_map_fn: RouteMapFn"]
        MCPComponentFn["mcp_component_fn: ComponentFn"]
        MCPNames["mcp_names: dict[str, str]"]
    end
    
    subgraph "Processing"
        HTTPRoutes["http_routes: list[HTTPRoute]"]
        UsedNames["_used_names: Counter"]
        GenerateDefaultName["_generate_default_name()"]
        GetUniqueName["_get_unique_name()"]
    end
    
    subgraph "Component Creation"
        CreateOpenAPITool["_create_openapi_tool()"]
        CreateOpenAPIResource["_create_openapi_resource()"]
        CreateOpenAPITemplate["_create_openapi_template()"]
    end
    
    FastMCPOpenAPI --> RouteMapsList
    FastMCPOpenAPI --> RouteMapFn
    FastMCPOpenAPI --> MCPComponentFn
    FastMCPOpenAPI --> MCPNames
    FastMCPOpenAPI --> HTTPRoutes
    FastMCPOpenAPI --> UsedNames
    HTTPRoutes --> GenerateDefaultName
    UsedNames --> GetUniqueName
    FastMCPOpenAPI --> CreateOpenAPITool
    FastMCPOpenAPI --> CreateOpenAPIResource
    FastMCPOpenAPI --> CreateOpenAPITemplate
```

**Sources:** [src/fastmcp/server/openapi.py:696-831](), [src/fastmcp/server/openapi.py:833-887]()

### OpenAPI Component Types

Three specialized component classes handle different types of HTTP endpoints:

| Component | Purpose | HTTP Methods | Use Case |
|-----------|---------|--------------|----------|
| `OpenAPITool` | Executable operations | POST, PUT, PATCH, DELETE | API actions, data modification |
| `OpenAPIResource` | Static data endpoints | GET (no path params) | Fixed data retrieval |
| `OpenAPIResourceTemplate` | Parameterized data | GET (with path params) | Dynamic data retrieval |

**Sources:** [src/fastmcp/server/openapi.py:229-521](), [src/fastmcp/server/openapi.py:523-640](), [src/fastmcp/server/openapi.py:642-694]()

## Route Mapping System

### MCPType Enumeration

The `MCPType` enum defines the target component types for HTTP routes:

```python
class MCPType(enum.Enum):
    TOOL = "TOOL"                    # Executable operations
    RESOURCE = "RESOURCE"            # Static data endpoints  
    RESOURCE_TEMPLATE = "RESOURCE_TEMPLATE"  # Parameterized endpoints
    EXCLUDE = "EXCLUDE"              # Skip route conversion
```

**Sources:** [src/fastmcp/server/openapi.py:78-94]()

### RouteMap Configuration

`RouteMap` objects define mapping rules from HTTP routes to MCP component types:

```mermaid
graph TD
    RouteMap["RouteMap Configuration"]
    
    subgraph "Matching Criteria"
        Methods["methods: list[HttpMethod] | '*'"]
        Pattern["pattern: Pattern[str] | str"]
        Tags["tags: set[str]"]
    end
    
    subgraph "Target Configuration"
        MCPType["mcp_type: MCPType"]
        MCPTags["mcp_tags: set[str]"]
    end
    
    subgraph "Matching Process"
        DetermineRouteType["_determine_route_type()"]
        MethodCheck["HTTP Method Match"]
        PatternCheck["Path Pattern Match"]
        TagCheck["Tag Match (AND)"]
    end
    
    RouteMap --> Methods
    RouteMap --> Pattern
    RouteMap --> Tags
    RouteMap --> MCPType
    RouteMap --> MCPTags
    
    Methods --> DetermineRouteType
    Pattern --> DetermineRouteType
    Tags --> DetermineRouteType
    DetermineRouteType --> MethodCheck
    DetermineRouteType --> PatternCheck
    DetermineRouteType --> TagCheck
```

**Sources:** [src/fastmcp/server/openapi.py:110-182](), [src/fastmcp/server/openapi.py:184-227]()

### Default Route Mapping

By default, all routes are converted to Tools unless custom mappings specify otherwise:

```python
DEFAULT_ROUTE_MAPPINGS = [
    RouteMap(mcp_type=MCPType.TOOL),
]
```

**Sources:** [src/fastmcp/server/openapi.py:177-181]()

## Schema Parsing System

### HTTPRoute Intermediate Representation

The parsing system converts OpenAPI specifications into `HTTPRoute` objects that capture all necessary information for component generation:

```mermaid
graph LR
    subgraph "OpenAPI Elements"
        Operation["OpenAPI Operation"]
        Parameters["Parameters[]"]
        RequestBody["RequestBody"]
        Responses["Responses{}"]
        Components["Components/Schemas"]
    end
    
    subgraph "HTTPRoute IR"
        HTTPRouteObj["HTTPRoute"]
        ParameterInfo["ParameterInfo[]"]
        RequestBodyInfo["RequestBodyInfo"]
        ResponseInfo["ResponseInfo{}"]
        SchemaDefinitions["schema_definitions: dict"]
    end
    
    subgraph "Parsing Functions"
        ParseOpenAPI["parse_openapi_to_http_routes()"]
        ExtractParameters["_extract_parameters()"]
        ExtractRequestBody["_extract_request_body()"]
        ExtractResponses["_extract_responses()"]
        ResolveRef["_resolve_ref()"]
    end
    
    Operation --> ParseOpenAPI
    Parameters --> ExtractParameters
    RequestBody --> ExtractRequestBody
    Responses --> ExtractResponses
    Components --> ResolveRef
    
    ParseOpenAPI --> HTTPRouteObj
    ExtractParameters --> ParameterInfo
    ExtractRequestBody --> RequestBodyInfo
    ExtractResponses --> ResponseInfo
    ResolveRef --> SchemaDefinitions
```

**Sources:** [src/fastmcp/utilities/openapi.py:201-253](), [src/fastmcp/utilities/openapi.py:379-477](), [src/fastmcp/utilities/openapi.py:479-543]()

### Parameter Processing

The system handles complex parameter scenarios including location conflicts and array formatting:

| Parameter Location | Handling | Example |
|-------------------|----------|---------|
| `path` | Required, URL substitution | `/users/{userId}` |
| `query` | Optional, query string | `?limit=10&offset=0` |
| `header` | Optional, HTTP headers | `X-API-Key: secret` |
| `cookie` | Optional, cookie values | `session=abc123` |

**Sources:** [src/fastmcp/utilities/openapi.py:124-135](), [src/fastmcp/server/openapi.py:264-418]()

## Component Creation Process

### Schema Combination

The `_combine_schemas` function merges parameter schemas with request body schemas, handling name collisions by suffixing parameter names with their location:

```mermaid
graph TD
    subgraph "Input Schemas"
        RouteParameters["Route Parameters"]
        RequestBodySchema["Request Body Schema"]
    end
    
    subgraph "Processing"
        CombineSchemas["_combine_schemas()"]
        DetectCollisions["Name Collision Detection"]
        SuffixParameters["Parameter Name Suffixing"]
        MergeProperties["Schema Property Merging"]
    end
    
    subgraph "Output"
        CombinedSchema["Combined JSON Schema"]
        ParameterProperties["Parameter Properties"]
        BodyProperties["Body Properties"]
        RequiredFields["Required Fields Array"]
    end
    
    RouteParameters --> CombineSchemas
    RequestBodySchema --> CombineSchemas
    CombineSchemas --> DetectCollisions
    DetectCollisions --> SuffixParameters
    SuffixParameters --> MergeProperties
    MergeProperties --> CombinedSchema
    CombinedSchema --> ParameterProperties
    CombinedSchema --> BodyProperties
    CombinedSchema --> RequiredFields
```

**Sources:** [src/fastmcp/utilities/openapi.py:892-1050]()

### Name Generation and Collision Handling

The system generates unique component names using operation IDs, summaries, or path-based naming with collision detection:

```python
def _generate_default_name(self, route: HTTPRoute, mcp_names_map: dict[str, str] | None = None) -> str:
    # Priority: custom mapping > operationId > summary > path-based
    # Truncated to 56 characters maximum
    # Processed through _slugify() for URL-safe names
```

**Sources:** [src/fastmcp/server/openapi.py:833-856](), [src/fastmcp/server/openapi.py:858-886](), [src/fastmcp/server/openapi.py:44-64]()

## HTTP Request Execution

### Parameter Serialization

OpenAPI components handle complex parameter serialization including arrays, objects, and style-specific formatting:

```mermaid
graph TD
    subgraph "Parameter Types"
        PathParams["Path Parameters"]
        QueryParams["Query Parameters"]
        HeaderParams["Header Parameters"]
        BodyParams["Request Body"]
    end
    
    subgraph "Serialization Strategies"
        SimpleStyle["Simple Style (path)"]
        FormStyle["Form Style (query)"]
        DeepObjectStyle["deepObject Style"]
        ArrayFormatting["Array Parameter Formatting"]
    end
    
    subgraph "HTTP Request"
        URLConstruction["URL Construction"]
        QueryString["Query String Building"]
        HeaderMapping["Header Mapping"]
        JSONBody["JSON Body Serialization"]
    end
    
    PathParams --> SimpleStyle
    QueryParams --> FormStyle
    QueryParams --> DeepObjectStyle
    QueryParams --> ArrayFormatting
    HeaderParams --> HeaderMapping
    BodyParams --> JSONBody
    
    SimpleStyle --> URLConstruction
    FormStyle --> QueryString
    DeepObjectStyle --> QueryString
    ArrayFormatting --> QueryString
    HeaderMapping --> HTTPRequest["HTTP Request"]
    JSONBody --> HTTPRequest
    URLConstruction --> HTTPRequest
    QueryString --> HTTPRequest
```

**Sources:** [src/fastmcp/server/openapi.py:288-417](), [src/fastmcp/utilities/openapi.py:41-121]()

### Response Processing

The system handles various response types and content negotiation:

| Content Type | Processing | Output |
|-------------|------------|--------|
| `application/json` | JSON parsing, structured output | `ToolResult(structured_content=...)` |
| `text/*` | Text content | `ToolResult(content=...)` |
| `application/xml` | Text content | `ToolResult(content=...)` |
| Binary | Raw bytes | `ToolResult(content=...)` |

**Sources:** [src/fastmcp/server/openapi.py:482-502](), [src/fastmcp/server/openapi.py:614-621]()

## Advanced Features

### Custom Route Mapping Functions

Advanced route mapping through `route_map_fn` and `mcp_component_fn` callbacks:

```python