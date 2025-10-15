if auth is NotSet:
    if fastmcp.settings.server_auth is not None:
        auth = fastmcp.settings.server_auth_class()
    else:
        auth = None
self.auth = cast(AuthProvider | None, auth)
```

Sources: [src/fastmcp/server/server.py:204-211](), [src/fastmcp/server/auth/](), [src/fastmcp/settings.py:363-380]()

## Testing and Development Framework

FastMCP provides comprehensive testing utilities through direct server instance connections:

### In-Memory Testing

The `FastMCPTransport` enables efficient testing without process management:

```python
async with Client(server_instance) as client:
    result = await client.call_tool("test_tool", {})
    assert result.data == expected_value
```

### Test Utilities

The framework includes testing helpers in `fastmcp.utilities.tests`:
- `caplog_for_fastmcp()`: FastMCP-specific log capture
- `temporary_settings()`: Settings isolation for tests

Sources: [tests/server/test_server.py:14-67](), [src/fastmcp/utilities/tests.py](), [src/fastmcp/client/transports.py]()