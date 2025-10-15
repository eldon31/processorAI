This document provides practical examples and tutorials for building MCP servers and clients using the Python SDK. It demonstrates both low-level server implementations and high-level patterns, showing how to create functional MCP servers that expose tools, resources, and prompts to clients.

For detailed FastMCP framework usage with decorators, see [FastMCP Server Framework](#2). For client implementation patterns, see [Client Framework](#3). For low-level protocol details, see [Protocol & Message System](#4).

## Overview of Example Categories

The MCP Python SDK includes several reference implementations that demonstrate core functionality:

| Example Type | Purpose | Key Components |
|--------------|---------|----------------|
| **Resource Server** | Expose data and content | `list_resources()`, `read_resource()` handlers |
| **Tool Server** | Provide executable functions | `list_tools()`, `call_tool()` handlers |
| **Prompt Server** | Offer prompt templates | `list_prompts()`, `get_prompt()` handlers |

All examples support multiple transport protocols (stdio, SSE) and follow consistent patterns using the low-level `Server` class from `mcp.server.lowlevel`.

## Low-Level Server Implementation Patterns

### Basic Server Structure

The foundation of all MCP servers follows this pattern:

```mermaid
graph TB
    subgraph "Server Creation & Setup"
        ServerInit["Server('server-name')"]
        HandlerReg["Handler Registration<br/>@app.list_*, @app.call_*, @app.get_*"]
        TransportSetup["Transport Selection<br/>stdio_server() or SSE"]
    end
    
    subgraph "Handler Implementation"
        ListHandlers["List Handlers<br/>list_resources(), list_tools(), list_prompts()"]
        ActionHandlers["Action Handlers<br/>read_resource(), call_tool(), get_prompt()"]
        ResponseTypes["Response Types<br/>types.Resource, types.Tool, types.Prompt"]
    end
    
    subgraph "Runtime Execution"
        StreamSetup["Stream Setup<br/>streams[0], streams[1]"]
        AppRun["app.run()<br/>Message Processing"]
        InitOptions["create_initialization_options()"]
    end
    
    ServerInit --> HandlerReg
    HandlerReg --> TransportSetup
    HandlerReg --> ListHandlers
    HandlerReg --> ActionHandlers
    ListHandlers --> ResponseTypes
    ActionHandlers --> ResponseTypes
    TransportSetup --> StreamSetup
    StreamSetup --> AppRun
    StreamSetup --> InitOptions
```

**Sources:** [examples/servers/simple-resource/mcp_simple_resource/server.py:34-93](), [examples/servers/simple-tool/mcp_simple_tool/server.py:30-93](), [examples/servers/simple-prompt/mcp_simple_prompt/server.py:42-112]()

### Resource Server Example

The resource server demonstrates how to expose readable data sources through the MCP protocol:

```mermaid
graph LR
    subgraph "Resource Server Components"
        SAMPLE_RESOURCES["SAMPLE_RESOURCES<br/>Static Data Dictionary"]
        list_resources_handler["@app.list_resources()<br/>Returns Resource Metadata"]
        read_resource_handler["@app.read_resource()<br/>Returns Resource Content"]
    end
    
    subgraph "MCP Types Integration"
        Resource_Type["types.Resource<br/>uri, name, title, description"]
        FileUrl_Type["FileUrl<br/>file:/// URI scheme"]
        ReadResourceContents["ReadResourceContents<br/>content, mime_type"]
    end
    
    subgraph "Request Flow"
        ListRequest["ListResourcesRequest"]
        ReadRequest["ReadResourceRequest(uri)"]
        ListResponse["List[types.Resource]"]
        ReadResponse["List[ReadResourceContents]"]
    end
    
    SAMPLE_RESOURCES --> list_resources_handler
    SAMPLE_RESOURCES --> read_resource_handler
    list_resources_handler --> Resource_Type
    Resource_Type --> FileUrl_Type
    read_resource_handler --> ReadResourceContents
    
    ListRequest --> list_resources_handler
    ReadRequest --> read_resource_handler
    list_resources_handler --> ListResponse
    read_resource_handler --> ReadResponse
```

**Key Implementation Details:**

- **Resource Registry**: [examples/servers/simple-resource/mcp_simple_resource/server.py:9-22]() defines `SAMPLE_RESOURCES` dictionary containing static content
- **List Handler**: [examples/servers/simple-resource/mcp_simple_resource/server.py:36-47]() creates `types.Resource` objects with `FileUrl` URIs
- **Read Handler**: [examples/servers/simple-resource/mcp_simple_resource/server.py:49-58]() parses URIs and returns `ReadResourceContents`

**Sources:** [examples/servers/simple-resource/mcp_simple_resource/server.py:9-58]()

### Tool Server Example

The tool server shows how to expose executable functions that clients can invoke:

```mermaid
graph TB
    subgraph "Tool Server Architecture"
        fetch_website_func["fetch_website()<br/>Core Function Logic"]
        list_tools_handler["@app.list_tools()<br/>Tool Metadata Registration"]
        call_tool_handler["@app.call_tool()<br/>Tool Execution Handler"]
    end
    
    subgraph "Tool Schema Definition"
        Tool_Type["types.Tool<br/>name, title, description"]
        inputSchema["inputSchema<br/>JSON Schema for Arguments"]
        ContentBlock_Response["List[types.ContentBlock]<br/>TextContent Response"]
    end
    
    subgraph "HTTP Integration"
        create_mcp_http_client["create_mcp_http_client()<br/>Shared HTTP Client"]
        httpx_response["response.text<br/>Web Content Extraction"]
    end
    
    fetch_website_func --> create_mcp_http_client
    create_mcp_http_client --> httpx_response
    httpx_response --> ContentBlock_Response
    
    list_tools_handler --> Tool_Type
    Tool_Type --> inputSchema
    call_tool_handler --> fetch_website_func
    call_tool_handler --> ContentBlock_Response
```

**Key Implementation Details:**

- **Tool Function**: [examples/servers/simple-tool/mcp_simple_tool/server.py:11-18]() implements `fetch_website()` with `create_mcp_http_client`
- **Schema Definition**: [examples/servers/simple-tool/mcp_simple_tool/server.py:47-56]() defines JSON schema for `url` parameter
- **Tool Execution**: [examples/servers/simple-tool/mcp_simple_tool/server.py:32-38]() validates arguments and calls core function

**Sources:** [examples/servers/simple-tool/mcp_simple_tool/server.py:11-58]()

### Prompt Server Example

The prompt server demonstrates how to create parameterized prompt templates:

**Key Implementation Details:**

- **Message Creation**: [examples/servers/simple-prompt/mcp_simple_prompt/server.py:8-30]() implements `create_messages()` function with optional context and topic
- **Prompt Registration**: [examples/servers/simple-prompt/mcp_simple_prompt/server.py:44-64]() defines `types.Prompt` with `types.PromptArgument` specifications
- **Template Logic**: [examples/servers/simple-prompt/mcp_simple_prompt/server.py:66-77]() processes arguments and returns `types.GetPromptResult`

**Sources:** [examples/servers/simple-prompt/mcp_simple_prompt/server.py:8-77]()

## Transport Configuration Patterns

All example servers support dual transport modes using a consistent CLI pattern:

### Transport Selection Logic

```mermaid
graph TD
    subgraph "CLI Transport Options"
        click_command["@click.command()"]
        port_option["--port (default: 8000)"]
        transport_option["--transport (stdio|sse)"]
    end
    
    subgraph "Transport Implementations"
        stdio_branch["stdio Transport"]
        sse_branch["SSE Transport"]
    end
    
    subgraph "stdio Implementation"
        stdio_server_import["from mcp.server.stdio import stdio_server"]
        stdio_streams["stdio_server() context manager"]
        anyio_run["anyio.run(arun)"]
    end
    
    subgraph "SSE Implementation"
        SseServerTransport_import["from mcp.server.sse import SseServerTransport"]
        starlette_app["Starlette ASGI Application"]
        uvicorn_run["uvicorn.run()"]
    end
    
    click_command --> port_option
    click_command --> transport_option
    transport_option --> stdio_branch
    transport_option --> sse_branch
    
    stdio_branch --> stdio_server_import
    stdio_server_import --> stdio_streams
    stdio_streams --> anyio_run
    
    sse_branch --> SseServerTransport_import
    SseServerTransport_import --> starlette_app
    starlette_app --> uvicorn_run
```

**Implementation Details:**

- **CLI Setup**: [examples/servers/simple-resource/mcp_simple_resource/server.py:25-32]() defines consistent command-line interface
- **stdio Transport**: [examples/servers/simple-resource/mcp_simple_resource/server.py:84-91]() uses `stdio_server()` context manager with `anyio.run()`
- **SSE Transport**: [examples/servers/simple-resource/mcp_simple_resource/server.py:60-83]() integrates `SseServerTransport` with Starlette ASGI application

**Sources:** [examples/servers/simple-resource/mcp_simple_resource/server.py:25-93](), [examples/servers/simple-tool/mcp_simple_tool/server.py:21-93](), [examples/servers/simple-prompt/mcp_simple_prompt/server.py:33-112]()

## Common Development Patterns

### Error Handling
All examples implement consistent error handling patterns:
- Resource servers validate URIs and check resource existence [examples/servers/simple-resource/mcp_simple_resource/server.py:50-56]()
- Tool servers validate tool names and required arguments [examples/servers/simple-tool/mcp_simple_tool/server.py:34-37]()
- Prompt servers validate prompt names before processing [examples/servers/simple-prompt/mcp_simple_prompt/server.py:68-69]()

### Type System Integration
Examples demonstrate proper use of MCP type system:
- Import `mcp.types` for protocol types [examples/servers/simple-resource/mcp_simple_resource/server.py:3]()
- Use `types.Resource`, `types.Tool`, `types.Prompt` for metadata [examples/servers/simple-resource/mcp_simple_resource/server.py:39-45]()
- Return appropriate content types like `ReadResourceContents` and `TextContent` [examples/servers/simple-resource/mcp_simple_resource/server.py:58]()

For more advanced server implementations using the FastMCP framework, see [Server Examples](#9.1). For client usage examples, see [Client Examples](#9.2).