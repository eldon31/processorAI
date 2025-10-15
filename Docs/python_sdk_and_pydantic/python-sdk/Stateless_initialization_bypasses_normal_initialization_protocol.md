ServerSession(read_stream, write_stream, init_options, stateless=True)
```

In stateless mode, the session immediately transitions to `Initialized` state, bypassing the normal MCP initialization handshake.

Sources: [src/mcp/server/session.py:88-93]()

# Authentication & Security




This document covers the OAuth 2.0 authentication system implemented in the MCP Python SDK for securing communication between MCP clients and servers. The authentication system provides both client-side authentication (for MCP clients connecting to protected servers) and server-side authentication (for MCP servers that need to authenticate clients).

The OAuth system integrates seamlessly with MCP's core components:
- **ClientSession**: Automatically handles OAuth authentication when connecting to protected MCP servers
- **FastMCP servers**: Can optionally expose OAuth authorization server endpoints
- **Transport layer**: OAuth authentication works across all transport mechanisms (stdio, SSE, StreamableHTTP)

For detailed OAuth implementation specifics, see [OAuth 2.0 System](#7.1). For transport-level security features like DNS rebinding protection, see [Transport Security](#5.4). For the overall client framework, see [Client Framework](#3).

## MCP Authentication Integration

```mermaid
graph TB
    subgraph "MCP Client Side"
        ClientSession["ClientSession"]
        OAuthClientProvider["OAuthClientProvider"]
        TokenStorage["TokenStorage"]
        HTTPXAuth["httpx.Auth Integration"]
    end
    
    subgraph "MCP Server Side" 
        FastMCPServer["FastMCP Server"]
        AuthRoutes["create_auth_routes()"]
        OAuthProvider["OAuthAuthorizationServerProvider"]
        AuthMiddleware["Authentication Middleware"]
    end
    
    subgraph "Transport Layer"
        StdioTransport["stdio Transport"]
        SSETransport["SSE Transport"] 
        StreamableHTTP["StreamableHTTP Transport"]
    end
    
    subgraph "OAuth Endpoints"
        AuthorizeEndpoint["/authorize"]
        TokenEndpoint["/token"]
        RegisterEndpoint["/register"]
        MetadataEndpoint["/.well-known/oauth-authorization-server"]
    end
    
    ClientSession --> OAuthClientProvider
    OAuthClientProvider --> TokenStorage
    OAuthClientProvider --> HTTPXAuth
    
    FastMCPServer --> AuthRoutes
    AuthRoutes --> AuthorizeEndpoint
    AuthRoutes --> TokenEndpoint
    AuthRoutes --> RegisterEndpoint
    AuthRoutes --> MetadataEndpoint
    AuthRoutes --> OAuthProvider
    FastMCPServer --> AuthMiddleware
    
    HTTPXAuth -.-> StdioTransport
    HTTPXAuth -.-> SSETransport  
    HTTPXAuth -.-> StreamableHTTP
    
    OAuthClientProvider -.-> AuthorizeEndpoint
    OAuthClientProvider -.-> TokenEndpoint
    OAuthClientProvider -.-> RegisterEndpoint
    OAuthClientProvider -.-> MetadataEndpoint
```

**Sources:** [src/mcp/client/auth.py:179-206](), [src/mcp/server/auth/routes.py:68-146](), [src/mcp/client/session.py](), [src/mcp/server/fastmcp/]()

## OAuth 2.0 Client Authentication

The MCP SDK provides a complete OAuth 2.0 client implementation centered around the `OAuthClientProvider` class, which integrates with httpx to provide transparent authentication for HTTP requests.

### Core Client Components Architecture

```mermaid
graph TB
    subgraph "OAuthClientProvider Class"
        OAuthClientProvider["OAuthClientProvider"]
        OAuthContext["OAuthContext"]
        TokenStorage["TokenStorage"]
        PKCEParameters["PKCEParameters"]
    end
    
    subgraph "OAuth Models (mcp.shared.auth)"
        ProtectedResourceMetadata["ProtectedResourceMetadata"]
        OAuthMetadata["OAuthMetadata"] 
        OAuthClientInformationFull["OAuthClientInformationFull"]
        OAuthToken["OAuthToken"]
        OAuthClientMetadata["OAuthClientMetadata"]
    end
    
    subgraph "Client Integration Methods"
        async_auth_flow["async_auth_flow()"]
        _initialize["_initialize()"]
        _refresh_token["_refresh_token()"]
        _add_auth_header["_add_auth_header()"]
    end
    
    subgraph "Discovery Methods"
        _discover_protected_resource["_discover_protected_resource()"]
        _get_discovery_urls["_get_discovery_urls()"]
        _extract_resource_metadata_from_www_auth["_extract_resource_metadata_from_www_auth()"]
    end
    
    OAuthClientProvider --> OAuthContext
    OAuthClientProvider --> TokenStorage
    OAuthClientProvider --> PKCEParameters
    OAuthContext --> ProtectedResourceMetadata
    OAuthContext --> OAuthMetadata
    OAuthContext --> OAuthClientInformationFull
    OAuthContext --> OAuthToken
    OAuthContext --> OAuthClientMetadata
    
    OAuthClientProvider --> async_auth_flow
    OAuthClientProvider --> _initialize
    OAuthClientProvider --> _refresh_token
    OAuthClientProvider --> _add_auth_header
    OAuthClientProvider --> _discover_protected_resource
    OAuthClientProvider --> _get_discovery_urls
    OAuthClientProvider --> _extract_resource_metadata_from_www_auth
```

The `OAuthClientProvider` implements the `httpx.Auth` interface, allowing it to be used as an authentication handler for any HTTP client that supports httpx auth providers. The class is instantiated with server URL, client metadata, token storage, and callback handlers for user interaction.

**Sources:** [src/mcp/client/auth.py:179-206](), [src/mcp/shared/auth.py:6-25](), [src/mcp/shared/auth.py:37-91](), [src/mcp/shared/auth.py:93-103]()

### OAuth Flow Implementation

The client authentication follows the OAuth 2.0 authorization code flow with PKCE (Proof Key for Code Exchange) for enhanced security. The entire flow is implemented in the `async_auth_flow()` method:

```mermaid
sequenceDiagram
    participant OAuthClientProvider as "OAuthClientProvider"
    participant MCPServer as "MCP Server"  
    participant AuthServer as "Authorization Server"
    participant UserBrowser as "User Browser"
    
    OAuthClientProvider->>MCPServer: "Initial request (no auth)"
    MCPServer-->>OAuthClientProvider: "401 + WWW-Authenticate header"
    
    OAuthClientProvider->>MCPServer: "_discover_protected_resource()"
    MCPServer-->>OAuthClientProvider: "ProtectedResourceMetadata"
    
    OAuthClientProvider->>AuthServer: "_create_oauth_metadata_request()"
    AuthServer-->>OAuthClientProvider: "OAuthMetadata"
    
    OAuthClientProvider->>AuthServer: "_register_client()"
    AuthServer-->>OAuthClientProvider: "OAuthClientInformationFull"
    
    OAuthClientProvider->>UserBrowser: "_perform_authorization() + PKCEParameters.generate()"
    UserBrowser->>AuthServer: "Authorization request + code_challenge"
    AuthServer-->>UserBrowser: "Authorization code"
    UserBrowser-->>OAuthClientProvider: "Authorization code + state"
    
    OAuthClientProvider->>AuthServer: "_exchange_token() + code_verifier"
    AuthServer-->>OAuthClientProvider: "OAuthToken"
    
    OAuthClientProvider->>MCPServer: "_add_auth_header() + retry original request"
    MCPServer-->>OAuthClientProvider: "200 Success"
```

The flow includes several key security features implemented in specific methods:

- **PKCE (RFC 7636)**: `PKCEParameters.generate()` prevents authorization code interception attacks
- **State parameter**: `_perform_authorization()` prevents CSRF attacks during authorization  
- **Dynamic Client Registration (RFC 7591)**: `_register_client()` enables automatic client registration
- **Protected Resource Discovery (RFC 9728)**: `_discover_protected_resource()` enables automatic authorization server discovery

**Sources:** [src/mcp/client/auth.py:485-551](), [src/mcp/client/auth.py:312-356](), [src/mcp/client/auth.py:49-61](), [src/mcp/client/auth.py:231-252]()

### Token Management and Storage

The SDK provides a flexible token storage system through the `TokenStorage` protocol interface:

| Method | Purpose | Parameters | Return Type |
|--------|---------|------------|-------------|
| `get_tokens()` | Retrieve stored tokens | None | `OAuthToken \| None` |
| `set_tokens()` | Store new tokens | `OAuthToken` | `None` |
| `get_client_info()` | Retrieve client registration | None | `OAuthClientInformationFull \| None` |
| `set_client_info()` | Store client registration | `OAuthClientInformationFull` | `None` |

Token validation and refresh logic is handled automatically in `async_auth_flow()`:

```mermaid
graph LR
    async_auth_flow["async_auth_flow()"] --> is_token_valid["is_token_valid()"]
    is_token_valid --> TokenValid{"Token Valid?"}
    TokenValid -->|"Yes"| _add_auth_header["_add_auth_header()"]
    TokenValid -->|"No"| can_refresh_token["can_refresh_token()"]
    can_refresh_token -->|"Yes"| _refresh_token["_refresh_token()"]
    can_refresh_token -->|"No"| FullOAuthFlow["Full OAuth Flow"]
    _refresh_token --> _handle_refresh_response["_handle_refresh_response()"]
    _handle_refresh_response --> RefreshSuccess{"Refresh Success?"}
    RefreshSuccess -->|"Yes"| _add_auth_header
    RefreshSuccess -->|"No"| FullOAuthFlow
    FullOAuthFlow --> _add_auth_header
```

The `OAuthContext` class manages token expiry using the `update_token_expiry()` method, which calculates wall-clock time based on the `expires_in` field from token responses. Token validation is performed by `is_token_valid()` which checks both token presence and expiry time.

**Sources:** [src/mcp/client/auth.py:64-82](), [src/mcp/client/auth.py:120-142](), [src/mcp/client/auth.py:411-461](), [src/mcp/client/auth.py:494-501]()

### Protected Resource Discovery

The client implements RFC 9728 for automatic discovery of authorization servers through several methods in `OAuthClientProvider`. The discovery process supports multiple fallback mechanisms:

1. **WWW-Authenticate Header**: `_extract_resource_metadata_from_www_auth()` extracts `resource_metadata` URL from 401 responses
2. **Well-known Resource Discovery**: `_discover_protected_resource()` falls back to `/.well-known/oauth-protected-resource`  
3. **Authorization Server Discovery**: `_get_discovery_urls()` tries multiple OAuth metadata endpoints

```mermaid
graph TB
    Response401["401 Response"] --> _extract_resource_metadata_from_www_auth["_extract_resource_metadata_from_www_auth()"]
    _extract_resource_metadata_from_www_auth --> HasResourceMeta{"Has resource_metadata?"}
    HasResourceMeta -->|"Yes"| UseResourceMeta["Use extracted URL"]
    HasResourceMeta -->|"No"| WellKnownFallback["/.well-known/oauth-protected-resource"]
    
    UseResourceMeta --> _discover_protected_resource["_discover_protected_resource()"]
    WellKnownFallback --> _discover_protected_resource
    
    _discover_protected_resource --> _handle_protected_resource_response["_handle_protected_resource_response()"]
    _handle_protected_resource_response --> ExtractAS["Extract authorization_servers"]
    ExtractAS --> _get_discovery_urls["_get_discovery_urls()"]
    
    _get_discovery_urls --> Endpoint1["/.well-known/oauth-authorization-server/{path}"]
    _get_discovery_urls --> Endpoint2["/.well-known/oauth-authorization-server"]
    _get_discovery_urls --> Endpoint3["/.well-known/openid-configuration/{path}"]
    _get_discovery_urls --> Endpoint4["{server}/.well-known/openid-configuration"]
```

The discovery flow uses regex pattern matching in `_extract_resource_metadata_from_www_auth()` to parse the WWW-Authenticate header: `resource_metadata=(?:"([^"]+)"|([^\s,]+))`. If no resource_metadata is found, it constructs the well-known URL using `get_authorization_base_url()` and `urljoin()`.

**Sources:** [src/mcp/client/auth.py:207-240](), [src/mcp/client/auth.py:254-279](), [src/mcp/client/auth.py:517-530](), [src/mcp/client/auth.py:242-252]()

## OAuth 2.0 Server Implementation

The server-side authentication system provides a complete OAuth 2.0 authorization server implementation that MCP servers can use to authenticate clients. The system is built around the `create_auth_routes()` function and handler classes.

### Server Components Architecture

```mermaid
graph TB
    subgraph "Route Creation (mcp.server.auth.routes)"
        create_auth_routes["create_auth_routes()"]
        build_metadata["build_metadata()"]
        validate_issuer_url["validate_issuer_url()"]
        cors_middleware["cors_middleware()"]
    end
    
    subgraph "OAuth Endpoints"
        WellKnownEndpoint["/.well-known/oauth-authorization-server"]
        AuthorizeEndpoint["/authorize"]
        TokenEndpoint["/token"] 
        RegisterEndpoint["/register"]
        RevokeEndpoint["/revoke"]
    end
    
    subgraph "Handler Classes (mcp.server.auth.handlers)"
        MetadataHandler["MetadataHandler"]
        AuthorizationHandler["AuthorizationHandler"] 
        TokenHandler["TokenHandler"]
        RegistrationHandler["RegistrationHandler"]
        RevocationHandler["RevocationHandler"]
    end
    
    subgraph "Middleware & Authentication"
        ClientAuthenticator["ClientAuthenticator"]
        OAuthAuthorizationServerProvider["OAuthAuthorizationServerProvider"]
    end
    
    subgraph "Configuration Models"
        ClientRegistrationOptions["ClientRegistrationOptions"]
        RevocationOptions["RevocationOptions"]
    end
    
    create_auth_routes --> build_metadata
    create_auth_routes --> validate_issuer_url
    create_auth_routes --> cors_middleware
    create_auth_routes --> ClientRegistrationOptions
    create_auth_routes --> RevocationOptions
    
    create_auth_routes --> WellKnownEndpoint
    create_auth_routes --> AuthorizeEndpoint
    create_auth_routes --> TokenEndpoint
    create_auth_routes --> RegisterEndpoint
    create_auth_routes --> RevokeEndpoint
    
    WellKnownEndpoint --> MetadataHandler
    AuthorizeEndpoint --> AuthorizationHandler
    TokenEndpoint --> TokenHandler
    RegisterEndpoint --> RegistrationHandler
    RevokeEndpoint --> RevocationHandler
    
    TokenHandler --> ClientAuthenticator
    RevocationHandler --> ClientAuthenticator
    
    AuthorizationHandler --> OAuthAuthorizationServerProvider
    TokenHandler --> OAuthAuthorizationServerProvider
    RegistrationHandler --> OAuthAuthorizationServerProvider
    RevocationHandler --> OAuthAuthorizationServerProvider
```

**Sources:** [src/mcp/server/auth/routes.py:68-146](), [src/mcp/server/auth/handlers/](), [src/mcp/server/auth/middleware/client_auth.py](), [src/mcp/server/auth/settings.py]()

### OAuth Metadata Generation

The server automatically generates RFC 8414 compliant OAuth metadata using the `build_metadata()` function based on configuration:

| Field | Value | Source |
|-------|-------|--------|
| `issuer` | Server base URL | `issuer_url` parameter |
| `authorization_endpoint` | `{issuer}/authorize` | `AUTHORIZATION_PATH` constant |
| `token_endpoint` | `{issuer}/token` | `TOKEN_PATH` constant |
| `registration_endpoint` | `{issuer}/register` | `REGISTRATION_PATH` constant (if enabled) |
| `revocation_endpoint` | `{issuer}/revoke` | `REVOCATION_PATH` constant (if enabled) |
| `scopes_supported` | Valid scopes list | `ClientRegistrationOptions.valid_scopes` |
| `grant_types_supported` | `["authorization_code", "refresh_token"]` | Fixed in `build_metadata()` |
| `token_endpoint_auth_methods_supported` | `["client_secret_post"]` | Fixed in `build_metadata()` |
| `code_challenge_methods_supported` | `["S256"]` | Fixed in `build_metadata()` |

The `build_metadata()` function constructs the complete `OAuthMetadata` object with proper URL validation through `validate_issuer_url()` and CORS support via `cors_middleware()`. The metadata is served by `MetadataHandler.handle()` at the well-known endpoint.

**Sources:** [src/mcp/server/auth/routes.py:149-186](), [src/mcp/server/auth/routes.py:23-47](), [src/mcp/server/auth/routes.py:49-52](), [src/mcp/server/auth/handlers/metadata.py]()

### Dynamic Client Registration

The server supports RFC 7591 dynamic client registration through the `RegistrationHandler.handle()` method:

```mermaid
graph LR
    POSTRegister["POST /register"] --> ParseJSON["Parse request.json()"]
    ParseJSON --> ValidateMetadata["OAuthClientMetadata.model_validate()"]
    ValidateMetadata --> ValidateScopes["Validate against ClientRegistrationOptions.valid_scopes"]
    ValidateScopes --> GenerateCredentials["uuid4() + secrets.token_hex(32)"]
    GenerateCredentials --> CreateClientInfo["OAuthClientInformationFull()"]
    CreateClientInfo --> StoreClient["provider.register_client()"]
    StoreClient --> ReturnSuccess["PydanticJSONResponse(201)"]
    
    ParseJSON -->|"ValidationError"| ReturnError["RegistrationErrorResponse(400)"]
    ValidateScopes -->|"Invalid scopes"| ReturnError
    StoreClient -->|"RegistrationError"| ReturnError
```

Key registration features implemented in `RegistrationHandler.handle()`:
- **Automatic client ID generation**: Uses `uuid4()` for unique client identifiers  
- **Client secret generation**: Uses `secrets.token_hex(32)` for 32-byte cryptographically secure random hex string
- **Scope validation**: Ensures requested scopes are within `ClientRegistrationOptions.valid_scopes` 
- **Grant type validation**: Only supports `authorization_code` and `refresh_token` grant types
- **Client secret expiry**: Configurable via `ClientRegistrationOptions.client_secret_expiry_seconds`

**Sources:** [src/mcp/server/auth/handlers/register.py:34-121](), [src/mcp/server/auth/settings.py](), [src/mcp/server/auth/handlers/register.py:51-85]()

### Protected Resource Metadata

The server can also act as a protected resource by exposing RFC 9728 metadata through `create_protected_resource_routes()`:

```mermaid
graph TB
    subgraph "Protected Resource System"
        create_protected_resource_routes["create_protected_resource_routes()"]
        PRMRoute["/.well-known/oauth-protected-resource"]
        ProtectedResourceMetadataHandler["ProtectedResourceMetadataHandler"]
    end
    
    subgraph "ProtectedResourceMetadata Model"
        resource["resource: AnyHttpUrl"]
        authorization_servers["authorization_servers: list[AnyHttpUrl]"]
        scopes_supported["scopes_supported: list[str] | None"]
        bearer_methods_supported["bearer_methods_supported: ['header']"]
        resource_name["resource_name: str | None"]
        resource_documentation["resource_documentation: AnyHttpUrl | None"]
    end
    
    create_protected_resource_routes --> PRMRoute
    PRMRoute --> ProtectedResourceMetadataHandler
    ProtectedResourceMetadataHandler --> resource
    ProtectedResourceMetadataHandler --> authorization_servers
    ProtectedResourceMetadataHandler --> scopes_supported
    ProtectedResourceMetadataHandler --> bearer_methods_supported
    ProtectedResourceMetadataHandler --> resource_name
    ProtectedResourceMetadataHandler --> resource_documentation
```

This enables automatic discovery by OAuth clients using `_discover_protected_resource()` and supports the separation of authorization servers from protected resources as defined in RFC 9728.

**Sources:** [src/mcp/server/auth/routes.py:189-227](), [src/mcp/shared/auth.py:134-156](), [src/mcp/server/auth/handlers/metadata.py]()

## Security Features

### PKCE Implementation

The SDK implements PKCE (Proof Key for Code Exchange) as defined in RFC 7636 through the `PKCEParameters` class to prevent authorization code interception attacks:

```mermaid
graph LR
    PKCEParameters_generate["PKCEParameters.generate()"] --> code_verifier["128-char code_verifier"]
    code_verifier --> hashlib_sha256["hashlib.sha256()"]
    hashlib_sha256 --> base64_urlsafe_b64encode["base64.urlsafe_b64encode()"]
    base64_urlsafe_b64encode --> code_challenge["code_challenge"]
    
    code_challenge --> _perform_authorization["_perform_authorization()"]
    code_verifier --> _exchange_token["_exchange_token()"]
```

PKCE parameters use cryptographically secure random generation in `PKCEParameters.generate()`:
- **Code verifier**: 128 characters from `secrets.choice(string.ascii_letters + string.digits + "-._~")`
- **Code challenge**: SHA256 hash of verifier, Base64URL encoded with `rstrip("=")` to remove padding
- **Challenge method**: Always `S256` (SHA256) as specified in OAuth server metadata

**Sources:** [src/mcp/client/auth.py:49-61](), [src/mcp/client/auth.py:324-325](), [src/mcp/client/auth.py:374](), [src/mcp/client/auth.py:56-61]()

### State Parameter Protection

The OAuth flow includes state parameter validation in `_perform_authorization()` to prevent CSRF attacks:

```python