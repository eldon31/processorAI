self._tool_manager = ToolManager(
    duplicate_behavior=on_duplicate_tools,
    mask_error_details=mask_error_details,
    transformations=tool_transformations,
)
self._resource_manager = ResourceManager(
    duplicate_behavior=on_duplicate_resources,
    mask_error_details=mask_error_details,
)
self._prompt_manager = PromptManager(
    duplicate_behavior=on_duplicate_prompts,
    mask_error_details=mask_error_details,
)
```

Sources: [src/fastmcp/server/server.py:176-188](), [src/fastmcp/tools/tool_manager.py](), [src/fastmcp/resources/resource_manager.py](), [src/fastmcp/prompts/prompt_manager.py]()

### Protocol Handler Registration

FastMCP registers MCP protocol handlers during initialization via `_setup_handlers()`:

```python
# From server.py:387-395
def _setup_handlers(self) -> None:
    """Set up core MCP protocol handlers."""
    self._mcp_server.list_tools()(self._mcp_list_tools)
    self._mcp_server.list_resources()(self._mcp_list_resources)
    self._mcp_server.list_resource_templates()(self._mcp_list_resource_templates)
    self._mcp_server.list_prompts()(self._mcp_list_prompts)
    self._mcp_server.call_tool()(self._mcp_call_tool)
    self._mcp_server.read_resource()(self._mcp_read_resource)
    self._mcp_server.get_prompt()(self._mcp_get_prompt)
```

Sources: [src/fastmcp/server/server.py:387-395](), [src/fastmcp/server/low_level.py]()

## Transport and Client Architecture

FastMCP supports multiple transport mechanisms for different deployment scenarios:

### Transport Types

| Transport | Use Case | Implementation |
|-----------|----------|----------------|
| `stdio` | Local development, CLI tools | `stdio_server()` from MCP SDK |
| `http`/`sse` | Web deployment, remote access | `create_sse_app()`, `create_streamable_http_app()` |
| `FastMCPTransport` | In-memory testing, embedding | Direct server instance connection |

### Client Transport Resolution

The client automatically selects appropriate transports via `infer_transport()` based on the connection target:

```python