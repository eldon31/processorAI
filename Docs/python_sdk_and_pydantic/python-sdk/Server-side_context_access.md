@server.call_tool()
async def handle_call_tool(name: str, args: dict[str, Any]) -> list[TextContent]:
    context = server.request_context
    if context.request:
        headers = dict(context.request.headers)
        # Use headers for authentication, tracing, etc.
```

Sources: [tests/shared/test_sse.py:183-201](), [tests/shared/test_sse.py:404-433](), [src/mcp/server/sse.py:244-245]()

## Usage Examples

### Basic Starlette Integration

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport

# Create SSE transport
sse = SseServerTransport("/messages/")

# Define route handlers
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())
    return Response()

# Create Starlette application
app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse, methods=["GET"]),
    Mount("/messages/", app=sse.handle_post_message),
])
```

### Mounted Application Support

The transport supports deployment under path prefixes using Starlette's `Mount`:

```python