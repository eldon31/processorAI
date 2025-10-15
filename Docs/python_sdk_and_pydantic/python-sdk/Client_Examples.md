This document provides practical examples of MCP client implementations, focusing on real-world usage patterns and architectures. The primary example is the simple-chatbot client that demonstrates comprehensive integration with MCP servers, LLM providers, and user interaction patterns.

For server-side examples, see [Server Examples](#9.1). For core client framework documentation, see [Client Framework](#3).

## Simple Chatbot Example Overview

The simple-chatbot example demonstrates a complete MCP client implementation that connects to multiple MCP servers, discovers their tools, and integrates with an LLM provider to create an interactive chatbot experience.

```mermaid
graph TB
    subgraph "Simple Chatbot Architecture"
        Config["Configuration<br/>Environment & Config Management"]
        ChatSession["ChatSession<br/>Main Orchestrator"]
        LLMClient["LLMClient<br/>Groq API Integration"]
        
        subgraph "Server Management"
            Server1["Server<br/>MCP Server Connection 1"]
            Server2["Server<br/>MCP Server Connection 2"]
            ServerN["Server<br/>MCP Server Connection N"]
        end
        
        subgraph "MCP Integration"
            ClientSession["ClientSession<br/>MCP Protocol Handler"]
            StdioTransport["stdio_client<br/>Process Communication"]
            StdioParams["StdioServerParameters<br/>Server Configuration"]
        end
        
        subgraph "Tool System"
            ToolDiscovery["list_tools()<br/>Tool Discovery"]
            ToolExecution["call_tool()<br/>Tool Execution"]
            ToolFormatting["Tool.format_for_llm()<br/>LLM Integration"]
        end
    end
    
    Config --> ChatSession
    ChatSession --> LLMClient
    ChatSession --> Server1
    ChatSession --> Server2
    ChatSession --> ServerN
    
    Server1 --> ClientSession
    Server2 --> ClientSession
    ServerN --> ClientSession
    
    ClientSession --> StdioTransport
    StdioTransport --> StdioParams
    
    Server1 --> ToolDiscovery
    Server1 --> ToolExecution
    ToolDiscovery --> ToolFormatting
    
    LLMClient --> ToolExecution
```

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:1-409]()

## Client Architecture Components

The simple-chatbot demonstrates four main architectural components that work together to provide a complete MCP client experience.

### Configuration Management

The `Configuration` class handles environment setup and server configuration loading:

```mermaid
graph LR
    subgraph "Configuration System"
        LoadEnv["load_env()<br/>Environment Variables"]
        LoadConfig["load_config()<br/>JSON Configuration"]
        APIKey["llm_api_key<br/>LLM Provider Access"]
    end
    
    EnvFile[".env File"] --> LoadEnv
    ConfigJSON["servers_config.json"] --> LoadConfig
    LoadEnv --> APIKey
```

The configuration system supports:
- Environment variable management via `python-dotenv`
- JSON-based server configuration loading
- API key validation and access

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:18-61]()

### Server Connection Management

The `Server` class manages individual MCP server connections with proper lifecycle management:

```mermaid
graph TB
    subgraph "Server Lifecycle"
        Initialize["initialize()<br/>Setup Connection"]
        Discovery["list_tools()<br/>Tool Discovery"] 
        Execution["execute_tool()<br/>Tool Execution"]
        Cleanup["cleanup()<br/>Resource Management"]
    end
    
    subgraph "Transport Layer"
        StdioParams["StdioServerParameters<br/>command, args, env"]
        StdioClient["stdio_client()<br/>Process Transport"]
        ClientSession["ClientSession<br/>Protocol Handler"]
    end
    
    Initialize --> StdioParams
    StdioParams --> StdioClient
    StdioClient --> ClientSession
    ClientSession --> Discovery
    ClientSession --> Execution
    Cleanup --> ClientSession
```

Key features include:
- `AsyncExitStack` for proper resource cleanup
- Retry logic with configurable attempts and delays
- Error handling and recovery mechanisms

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:63-169]()

## Connection and Session Management

The client demonstrates proper MCP session establishment and management patterns:

```mermaid
sequenceDiagram
    participant Client as "ChatSession"
    participant Server as "Server"
    participant Transport as "stdio_client"
    participant Session as "ClientSession"
    participant Process as "MCP Server Process"
    
    Client->>Server: initialize()
    Server->>Transport: stdio_client(server_params)
    Transport->>Process: spawn command + args
    Transport-->>Server: read, write streams
    Server->>Session: ClientSession(read, write)
    Session->>Process: initialize()
    Process-->>Session: capabilities response
    Session-->>Server: initialized session
    Server-->>Client: ready for operations
```

The session management includes:
- Process spawning with `shutil.which()` for command resolution
- Stream-based communication setup
- Capability negotiation through `session.initialize()`
- Proper error handling and cleanup on failure

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:74-94]()

## Tool Discovery and Execution

The client implements comprehensive tool management with LLM integration:

### Tool Discovery Pattern

```mermaid
graph LR
    subgraph "Tool Discovery Flow"
        ListTools["session.list_tools()"]
        ParseResponse["Parse ListToolsResult"]
        CreateTool["Tool(name, description, inputSchema, title)"]
        FormatLLM["format_for_llm()"]
    end
    
    ListTools --> ParseResponse
    ParseResponse --> CreateTool
    CreateTool --> FormatLLM
```

The discovery process extracts tool metadata and formats it for LLM consumption:
- Tool name and description
- JSON schema for input parameters
- Required vs optional parameter identification
- Human-readable formatting for LLM prompts

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:96-115](), [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:171-213]()

### Tool Execution with Retry Logic

```mermaid
graph TB
    subgraph "Tool Execution Flow"
        Start["call_tool(name, arguments)"]
        Attempt["Execute via session.call_tool()"]
        Success["Return Result"]
        Error["Handle Exception"]
        Retry["Check Retry Count"]
        Delay["Sleep with Delay"]
        Fail["Raise Exception"]
    end
    
    Start --> Attempt
    Attempt --> Success
    Attempt --> Error
    Error --> Retry
    Retry -->|"< max_retries"| Delay
    Delay --> Attempt
    Retry -->|">= max_retries"| Fail
```

The execution system provides:
- Configurable retry attempts (default: 2)
- Exponential backoff with configurable delay
- Comprehensive error logging
- Progress reporting for long-running tools

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:117-158]()

## LLM Integration Patterns

The client demonstrates how to integrate MCP tools with LLM providers through structured prompting and tool calling protocols.

### LLM Communication Flow

```mermaid
sequenceDiagram
    participant User as "User Input"
    participant Chat as "ChatSession"
    participant LLM as "LLMClient"
    participant Tools as "Tool System"
    participant Server as "MCP Server"
    
    User->>Chat: User message
    Chat->>LLM: get_response(messages)
    LLM-->>Chat: Response (text or JSON tool call)
    Chat->>Chat: process_llm_response()
    
    alt Tool Call Detected
        Chat->>Tools: Parse JSON tool call
        Tools->>Server: execute_tool(name, args)
        Server-->>Tools: Tool result
        Tools-->>Chat: Formatted result
        Chat->>LLM: get_response(with tool result)
        LLM-->>Chat: Final natural language response
    else Direct Response
        Chat->>User: Pass through response
    end
```

### Tool Call Protocol

The client implements a JSON-based tool calling protocol:

```json
{
    "tool": "tool-name",
    "arguments": {
        "argument-name": "value"
    }
}
```

The system message instructs the LLM on tool usage patterns and response formatting, ensuring consistent tool invocation and natural language result processing.

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:283-321](), [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:341-361]()

## Usage Examples

### Basic Client Setup

The simple-chatbot can be configured through a JSON configuration file:

```json
{
    "mcpServers": {
        "filesystem": {
            "command": "node",
            "args": ["path/to/filesystem-server.js"],
            "env": {}
        },
        "database": {
            "command": "python",
            "args": ["-m", "database_server"],
            "env": {
                "DB_PATH": "/path/to/database"
            }
        }
    }
}
```

### Environment Configuration

Required environment variables:
- `LLM_API_KEY`: API key for the LLM provider (Groq in this example)

The client uses `python-dotenv` for environment management, supporting `.env` files for development.

Sources: [examples/clients/simple-chatbot/mcp_simple_chatbot/main.py:397-404]()

### Test Integration Patterns

The codebase includes several test patterns that demonstrate client usage:

#### Resource Testing with Client Sessions

```mermaid
graph LR
    subgraph "Test Client Pattern"
        TestSetup["Test Setup"]
        ClientSession["create_connected_server_and_client_session"]
        Operations["list_resources(), read_resource()"]
        Assertions["Assert Results"]
    end
    
    TestSetup --> ClientSession
    ClientSession --> Operations
    Operations --> Assertions
```

This pattern is used extensively in tests for validating server behavior from a client perspective.

Sources: [tests/issues/test_152_resource_mime_type.py:36-61](), [tests/issues/test_141_resource_templates.py:81-114]()

The examples demonstrate comprehensive MCP client implementation patterns, from basic connection management to advanced tool integration with LLM providers, providing a solid foundation for building sophisticated MCP client applications.