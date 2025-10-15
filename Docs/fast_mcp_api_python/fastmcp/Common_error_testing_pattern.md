async def test_timeout(self, server_url: str):
    with pytest.raises(McpError, match="Timed out"):
        async with Client(transport=Transport(server_url), timeout=0.02) as client:
            await client.call_tool("sleep", {"seconds": 0.05})
```

### Authentication Test Patterns

```python
# OAuth testing pattern
async def test_unauthorized_access(self, mcp_server_url: str):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        async with Client(mcp_server_url) as client:
            await client.list_tools()
    
    assert exc_info.value.response.status_code == 401
```

Sources: [tests/client/test_streamable_http.py:222-248](), [tests/server/auth/providers/test_descope.py:156-164]()