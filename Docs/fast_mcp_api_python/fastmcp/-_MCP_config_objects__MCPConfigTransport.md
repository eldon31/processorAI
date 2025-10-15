```

Sources: [src/fastmcp/client/transports.py](), [src/fastmcp/server/http.py](), [src/fastmcp/client/client.py]()

## Advanced Server Patterns

FastMCP provides sophisticated patterns for building complex applications:

### Server Composition

FastMCP supports two composition patterns:

1. **Mounting (`mount`)**: Live delegation to child servers
2. **Importing (`import_server`)**: Static copying of components

```python
# Live mounting - changes in child_server are reflected immediately
main_server.mount(child_server, prefix="api")

# Static importing - components are copied at import time  
await main_server.import_server(child_server, prefix="api")
```

### Proxy Servers

The `FastMCP.as_proxy()` method creates servers that act as intermediaries:

```python
proxy_server = FastMCP.as_proxy(
    Client("remote_server.py"),
    name="proxy"
)
```

Sources: [tests/server/test_mount.py:19-67](), [tests/server/test_import_server.py:10-34](), [src/fastmcp/server/proxy.py]()

## Configuration and Settings

FastMCP uses a hierarchical settings system with environment variable support:

### Settings Structure

The `Settings` class provides configuration via environment variables prefixed with `FASTMCP_`:

- `FASTMCP_LOG_LEVEL`: Logging configuration
- `FASTMCP_SERVER_AUTH`: Authentication provider class path  
- `FASTMCP_INCLUDE_TAGS`/`FASTMCP_EXCLUDE_TAGS`: Component filtering
- `FASTMCP_HOST`/`FASTMCP_PORT`: HTTP server configuration

### Global Settings Instance

FastMCP maintains a global settings instance accessible via `fastmcp.settings`:

```python
# From __init__.py:8
settings = Settings()
```

Sources: [src/fastmcp/settings.py:80-381](), [src/fastmcp/__init__.py:8]()

## Authentication and Security

FastMCP provides enterprise-grade authentication through the `AuthProvider` system:

### Authentication Providers

The framework includes built-in providers for major identity systems:
- `GoogleProvider`
- `GitHubProvider` 
- `AzureProvider`
- `Auth0Provider`
- `WorkOSProvider`
- `JWTVerifier`

### Auth Integration

Authentication providers integrate with the server at initialization:

```python