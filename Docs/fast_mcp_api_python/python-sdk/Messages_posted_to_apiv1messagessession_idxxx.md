```

The transport automatically handles path prefix resolution using ASGI scope's `root_path` [src/mcp/server/sse.py:152-158]().

Sources: [src/mcp/server/sse.py:6-37](), [tests/shared/test_sse.py:83-104](), [tests/shared/test_sse.py:289-300]()

# STDIO Transport




The STDIO Transport enables MCP clients to communicate with servers by spawning processes and using standard input/output streams for message exchange. This transport is particularly useful for local development, CLI tools, and scenarios where servers are distributed as standalone executables. For HTTP-based transports, see [StreamableHTTP Transport](#5.1) and [SSE Transport](#5.2).

## Configuration

The STDIO transport is configured using the `StdioServerParameters` class, which defines how the server process should be spawned and managed.

### StdioServerParameters

The configuration model provides comprehensive control over process execution:

```mermaid
graph TB
    subgraph "StdioServerParameters Configuration"
        Config[StdioServerParameters]
        Command["command: str<br/>Executable to run"]
        Args["args: list[str]<br/>Command line arguments"]
        Env["env: dict[str, str] | None<br/>Environment variables"]
        Cwd["cwd: str | Path | None<br/>Working directory"]
        Encoding["encoding: str = 'utf-8'<br/>Text encoding"]
        ErrorHandler["encoding_error_handler<br/>strict|ignore|replace"]
    end
    
    Config --> Command
    Config --> Args
    Config --> Env
    Config --> Cwd
    Config --> Encoding
    Config --> ErrorHandler
```

**Sources:** [src/mcp/client/stdio/__init__.py:72-103]()

The `env` parameter controls environment variable inheritance. When `None`, the system uses `get_default_environment()` which provides a secure subset of environment variables filtered for safety.

### Default Environment Security

The transport implements security measures for environment variable inheritance:

```mermaid
graph LR
    subgraph "Environment Variable Filtering"
        AllEnv["All Environment Variables"]
        Filter["get_default_environment()"]
        SafeEnv["Filtered Safe Variables"]
        FunctionCheck["Skip variables starting with '()'"]
    end
    
    subgraph "Platform-Specific Variables"
        Windows["Windows:<br/>APPDATA, PATH, TEMP, etc."]
        Unix["Unix/Linux:<br/>HOME, PATH, SHELL, etc."]
    end
    
    AllEnv --> Filter
    Filter --> FunctionCheck
    FunctionCheck --> SafeEnv
    SafeEnv --> Windows
    SafeEnv --> Unix
```

**Sources:** [src/mcp/client/stdio/__init__.py:51-69](), [src/mcp/client/stdio/__init__.py:27-45]()

## Connection Management

### stdio_client Context Manager

The `stdio_client` function provides the primary interface for establishing STDIO connections. It returns read and write streams for JSON-RPC message exchange:

```mermaid
graph TB
    subgraph "stdio_client Connection Flow"
        Entry["stdio_client(server, errlog)"]
        CreateStreams["Create memory object streams"]
        SpawnProcess["_create_platform_compatible_process()"]
        StartTasks["Start stdout_reader and stdin_writer tasks"]
        YieldStreams["Yield (read_stream, write_stream)"]
        Cleanup["Shutdown sequence:<br/>1. Close stdin<br/>2. Wait for graceful exit<br/>3. Force termination if needed"]
    end
    
    Entry --> CreateStreams
    CreateStreams --> SpawnProcess
    SpawnProcess --> StartTasks
    StartTasks --> YieldStreams
    YieldStreams --> Cleanup
```

**Sources:** [src/mcp/client/stdio/__init__.py:105-216]()

### Message Processing

The transport handles JSON-RPC message serialization automatically:

```mermaid
graph LR
    subgraph "Message Flow"
        SendMsg["SessionMessage"]
        Serialize["JSON serialization"]
        StdinWrite["Write to process stdin"]
        
        StdoutRead["Read from process stdout"]
        ParseJSON["Parse JSON lines"]
        SessionMsg["Create SessionMessage"]
    end
    
    subgraph "Error Handling"
        ParseError["JSON Parse Error"]
        ErrorStream["Send exception to read_stream"]
    end
    
    SendMsg --> Serialize
    Serialize --> StdinWrite
    
    StdoutRead --> ParseJSON
    ParseJSON --> SessionMsg
    ParseJSON --> ParseError
    ParseError --> ErrorStream
```

**Sources:** [src/mcp/client/stdio/__init__.py:139-179]()

## Process Management

### Cross-Platform Process Creation

The transport provides platform-specific process creation to ensure reliable child process management:

```mermaid
graph TB
    subgraph "Platform-Specific Process Creation"
        Create["_create_platform_compatible_process()"]
        PlatformCheck{"sys.platform == 'win32'"}
        
        subgraph "Windows Path"
            WinExec["get_windows_executable_command()"]
            WinProcess["create_windows_process()<br/>Uses Job Objects"]
        end
        
        subgraph "Unix Path"
            UnixProcess["anyio.open_process()<br/>start_new_session=True"]
        end
    end
    
    Create --> PlatformCheck
    PlatformCheck -->|Windows| WinExec
    WinExec --> WinProcess
    PlatformCheck -->|Unix/Linux| UnixProcess
```

**Sources:** [src/mcp/client/stdio/__init__.py:234-258](), [src/mcp/client/stdio/__init__.py:218-232]()

### Process Tree Termination

The transport implements comprehensive child process cleanup using platform-specific mechanisms:

```mermaid
graph TB
    subgraph "Process Tree Termination"
        Terminate["_terminate_process_tree()"]
        PlatformCheck{"Platform Check"}
        
        subgraph "Windows Termination"
            WinJobObjects["Job Objects<br/>Automatic child cleanup"]
            WinTerminate["terminate_windows_process_tree()"]
        end
        
        subgraph "Unix Termination"
            ProcessGroup["Process Group (PGID)"]
            KillPG["os.killpg() for atomic termination"]
            UnixTerminate["terminate_posix_process_tree()"]
        end
    end
    
    Terminate --> PlatformCheck
    PlatformCheck -->|Windows| WinJobObjects
    WinJobObjects --> WinTerminate
    PlatformCheck -->|Unix/Linux| ProcessGroup
    ProcessGroup --> KillPG
    KillPG --> UnixTerminate
```

**Sources:** [src/mcp/client/stdio/__init__.py:261-277]()

## Shutdown and Cleanup

### MCP-Compliant Shutdown Sequence

The transport implements the MCP specification's stdio shutdown sequence for graceful server termination:

```mermaid
sequenceDiagram
    participant Client as stdio_client
    participant Process as Server Process
    participant Stdin as Process stdin
    participant Stdout as Process stdout
    
    Note over Client,Process: Normal Operation
    Client->>Process: JSON-RPC messages via stdin
    Process->>Client: JSON-RPC responses via stdout
    
    Note over Client,Process: Shutdown Sequence (MCP Spec)
    Client->>Stdin: Close stdin stream
    Note over Process: Server detects stdin closure
    Process->>Process: Run cleanup handlers
    Process->>Client: Exit gracefully
    
    alt If process doesn't exit within timeout
        Client->>Process: Send SIGTERM
        Note over Process: 2 second grace period
        alt If still running
            Client->>Process: Send SIGKILL (force)
        end
    end
```

**Sources:** [src/mcp/client/stdio/__init__.py:190-215]()

### Timeout Configuration

The transport uses configurable timeouts for process termination:

- **`PROCESS_TERMINATION_TIMEOUT`**: 2.0 seconds for graceful exit after stdin closure
- Escalation to SIGTERM if graceful exit fails
- Final SIGKILL if SIGTERM is ignored

**Sources:** [src/mcp/client/stdio/__init__.py:47-48]()

## Platform Considerations

### Windows-Specific Handling

Windows requires special handling for executable resolution and process management:

```mermaid
graph TB
    subgraph "Windows Specifics"
        ExecResolve["get_windows_executable_command()<br/>Handle .cmd/.bat extensions"]
        JobObjects["Job Objects for child cleanup"]
        FallbackProcess["FallbackProcess compatibility"]
        ResourceWarnings["Expected ResourceWarnings<br/>due to immediate termination"]
    end
    
    subgraph "Process Tree Management"
        JobObject["Win32 Job Object"]
        ChildProcs["Automatic child process tracking"]
        AtomicCleanup["Atomic tree termination"]
    end
    
    ExecResolve --> JobObjects
    JobObjects --> JobObject
    JobObject --> ChildProcs
    ChildProcs --> AtomicCleanup
```

**Sources:** [src/mcp/client/stdio/__init__.py:228-232](), [src/mcp/client/stdio/__init__.py:16-22]()

### Unix Process Groups

Unix systems use process groups for reliable child process management:

- **Session Creation**: `start_new_session=True` creates new process group
- **Atomic Termination**: `os.killpg()` terminates entire process group
- **Signal Escalation**: SIGTERM → SIGKILL escalation for unresponsive processes

**Sources:** [src/mcp/client/stdio/__init__.py:250-256]()

## Error Handling and Edge Cases

### Connection Failures

The transport handles various failure scenarios:

```mermaid
graph TB
    subgraph "Error Scenarios"
        NonExistent["Non-existent executable"]
        ProcessError["Process spawn failure"]
        InvalidJSON["Invalid JSON from server"]
        ProcessCrash["Server process crash"]
        StdinIgnored["Server ignores stdin closure"]
    end
    
    subgraph "Error Responses"
        OSError["Raises OSError"]
        StreamCleanup["Clean up memory streams"]
        JSONException["Send exception to read_stream"]
        ConnectionClosed["McpError with CONNECTION_CLOSED"]
        ForceTermination["Escalate to SIGTERM/SIGKILL"]
    end
    
    NonExistent --> OSError
    ProcessError --> StreamCleanup
    InvalidJSON --> JSONException
    ProcessCrash --> ConnectionClosed
    StdinIgnored --> ForceTermination
```

**Sources:** [src/mcp/client/stdio/__init__.py:131-137](), [src/mcp/client/stdio/__init__.py:154-161]()

### Child Process Cleanup

The transport includes comprehensive tests for child process scenarios:

- **Basic Parent-Child**: Single child process termination
- **Nested Trees**: Multi-level process hierarchies (parent → child → grandchild)
- **Race Conditions**: Parent exits during cleanup sequence
- **Signal Handling**: Processes that ignore specific signals

**Sources:** [tests/client/test_stdio.py:226-521]()

## Integration Examples

### Basic Usage

```python
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

server_params = StdioServerParameters(
    command="python",
    args=["-m", "my_mcp_server"],
    env={"DEBUG": "1"}
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Use session for MCP operations
```

### Custom Environment

```python
server_params = StdioServerParameters(
    command="./my_server",
    env={
        **get_default_environment(),
        "API_KEY": "secret",
        "LOG_LEVEL": "debug"
    }
)
```

**Sources:** [tests/client/test_stdio.py:37-81](), [src/mcp/client/stdio/__init__.py:127-128]()