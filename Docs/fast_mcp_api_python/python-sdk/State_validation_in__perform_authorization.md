if returned_state is None or not secrets.compare_digest(returned_state, state):
    raise OAuthFlowError(f"State parameter mismatch: {returned_state} != {state}")
```

The `secrets.compare_digest()` function provides constant-time comparison to prevent timing attacks. The state parameter is included in the authorization URL and validated when the authorization code is returned via the `callback_handler`.

**Sources:** [src/mcp/client/auth.py:325](), [src/mcp/client/auth.py:349-350](), [src/mcp/client/auth.py:347-353]()

### Token Security

Token management includes several security measures implemented across multiple methods:

- **Secure storage**: Tokens are stored through the `TokenStorage` protocol interface via `storage.set_tokens()`
- **Automatic expiry**: Tokens are validated in `is_token_valid()` against wall-clock expiry time from `update_token_expiry()`
- **Scope validation**: `_handle_token_response()` validates returned token scopes against requested scopes
- **Automatic refresh**: `_refresh_token()` and `_handle_refresh_response()` automatically refresh expired tokens when possible
- **Secure transport**: `validate_issuer_url()` ensures all token exchanges occur over HTTPS (with localhost HTTP exception for development)

The scope validation logic in `_handle_token_response()` prevents privilege escalation:
```python
requested_scopes = set(self.context.client_metadata.scope.split())
returned_scopes = set(token_response.scope.split())
unauthorized_scopes = returned_scopes - requested_scopes
if unauthorized_scopes:
    raise OAuthTokenError(f"Server granted unauthorized scopes: {unauthorized_scopes}")
```

**Sources:** [src/mcp/client/auth.py:398-403](), [src/mcp/client/auth.py:120-133](), [src/mcp/server/auth/routes.py:34-41](), [src/mcp/client/auth.py:388-409]()

### Resource Parameter Support

The SDK implements RFC 8707 resource indicators for enhanced security:

```mermaid
graph TB
    ProtocolVersion{MCP Protocol Version}
    ProtocolVersion -->|>= 2025-06-18| IncludeResource["Include resource parameter"]
    ProtocolVersion -->|< 2025-06-18| CheckPRM["Check for ProtectedResourceMetadata"]
    CheckPRM -->|Present| IncludeResource
    CheckPRM -->|Not Present| ExcludeResource["Exclude resource parameter"]
    
    IncludeResource --> AuthRequest["Authorization Request"]
    IncludeResource --> TokenRequest["Token Exchange Request"]
    IncludeResource --> RefreshRequest["Token Refresh Request"]
```

The resource parameter helps prevent token confusion attacks by explicitly identifying the intended resource server.

**Sources:** [src/mcp/client/auth.py:159-177](), [src/mcp/client/auth.py:377-379](), [src/mcp/client/auth.py:431-433]()

# OAuth 2.0 System




This document covers the comprehensive OAuth 2.0 authentication and authorization implementation in the MCP Python SDK. The OAuth 2.0 system provides secure authentication for both client and server components, implementing RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), RFC 8414 (Authorization Server Metadata), and RFC 9728 (Protected Resource Metadata).

For information about client transport integration, see [Client Transports](#3.2). For server-side transport security, see [Transport Security](#5.5).

## OAuth 2.0 Architecture Overview

The OAuth 2.0 system consists of client-side authentication components and server-side authorization infrastructure, supporting both acting as OAuth clients and providing OAuth authorization services.

```mermaid
graph TB
    subgraph "Client Authentication"
        OAuthClientProvider["OAuthClientProvider<br/>(httpx.Auth)"]
        OAuthContext["OAuthContext<br/>Flow State Management"]
        PKCEParameters["PKCEParameters<br/>PKCE Generation"]
        TokenStorage["TokenStorage Protocol<br/>Persistent Token Storage"]
    end
    
    subgraph "Shared OAuth Types"
        OAuthToken["OAuthToken<br/>RFC 6749 Token Response"]
        OAuthMetadata["OAuthMetadata<br/>RFC 8414 AS Metadata"]
        ProtectedResourceMetadata["ProtectedResourceMetadata<br/>RFC 9728 RS Metadata"]
        OAuthClientMetadata["OAuthClientMetadata<br/>RFC 7591 Client Registration"]
        OAuthClientInformationFull["OAuthClientInformationFull<br/>Complete Client Info"]
    end
    
    subgraph "Server Authorization Routes"
        AuthRoutes["create_auth_routes()<br/>/.well-known/oauth-authorization-server"]
        ProtectedResourceRoutes["create_protected_resource_routes()<br/>/.well-known/oauth-protected-resource"]
        
        subgraph "OAuth Endpoints"
            AuthorizationHandler["/authorize<br/>AuthorizationHandler"]
            TokenHandler["/token<br/>TokenHandler"]
            RegistrationHandler["/register<br/>RegistrationHandler"]
            RevocationHandler["/revoke<br/>RevocationHandler"]
        end
    end
    
    subgraph "Transport Integration"
        StreamableHTTPClient["streamablehttp_client<br/>HTTP + OAuth Integration"]
        StreamableHTTPServer["StreamableHTTPServerTransport<br/>OAuth Resource Server"]
    end
    
    %% Client relationships
    OAuthClientProvider --> OAuthContext
    OAuthClientProvider --> TokenStorage
    OAuthContext --> PKCEParameters
    
    %% Shared type usage
    OAuthClientProvider --> OAuthToken
    OAuthClientProvider --> OAuthMetadata
    OAuthClientProvider --> ProtectedResourceMetadata
    OAuthClientProvider --> OAuthClientMetadata
    RegistrationHandler --> OAuthClientInformationFull
    
    %% Server relationships
    AuthRoutes --> AuthorizationHandler
    AuthRoutes --> TokenHandler
    AuthRoutes --> RegistrationHandler
    AuthRoutes --> RevocationHandler
    
    %% Transport integration
    StreamableHTTPClient --> OAuthClientProvider
    StreamableHTTPServer --> AuthRoutes
    StreamableHTTPServer --> ProtectedResourceRoutes
```

**Sources:** [src/mcp/client/auth.py:179-552](), [src/mcp/shared/auth.py:1-156](), [src/mcp/server/auth/routes.py:68-187]()

## Client Authentication System

The `OAuthClientProvider` class implements the OAuth 2.0 authorization code flow with PKCE as an httpx authentication provider, enabling automatic token management for MCP clients. The provider sets `requires_response_body = True` to access response bodies for OAuth error handling and token processing.

### OAuthClientProvider Implementation

```mermaid
graph TB
    subgraph "OAuthClientProvider Core"
        Provider[OAuthClientProvider]
        AsyncAuthFlow["async_auth_flow()<br/>httpx.Auth Integration"]
        Context["OAuthContext<br/>Flow State & Metadata"]
    end
    
    subgraph "OAuth Discovery Flow"
        DiscoverProtectedResource["_discover_protected_resource()<br/>RFC 9728 Discovery"]
        GetDiscoveryUrls["_get_discovery_urls()<br/>Metadata Endpoint Fallback"]
        HandleOAuthMetadata["_handle_oauth_metadata_response()<br/>Store AS Metadata"]
    end
    
    subgraph "Client Registration"
        RegisterClient["_register_client()<br/>Dynamic Client Registration"]
        HandleRegistration["_handle_registration_response()<br/>Store Client Credentials"]
    end
    
    subgraph "Authorization Flow"
        PerformAuthorization["_perform_authorization()<br/>PKCE + Redirect Flow"]
        ExchangeToken["_exchange_token()<br/>Authorization Code Exchange"]
        RefreshToken["_refresh_token()<br/>Token Refresh"]
    end
    
    subgraph "Token Management"
        HandleTokenResponse["_handle_token_response()<br/>Token Validation & Storage"]
        HandleRefreshResponse["_handle_refresh_response()<br/>Refresh Response Processing"]
        AddAuthHeader["_add_auth_header()<br/>Bearer Token Injection"]
    end
    
    %% Flow relationships
    Provider --> AsyncAuthFlow
    AsyncAuthFlow --> Context
    AsyncAuthFlow --> DiscoverProtectedResource
    AsyncAuthFlow --> GetDiscoveryUrls
    AsyncAuthFlow --> HandleOAuthMetadata
    AsyncAuthFlow --> RegisterClient
    AsyncAuthFlow --> HandleRegistration
    AsyncAuthFlow --> PerformAuthorization
    AsyncAuthFlow --> ExchangeToken
    AsyncAuthFlow --> RefreshToken
    AsyncAuthFlow --> HandleTokenResponse
    AsyncAuthFlow --> HandleRefreshResponse
    AsyncAuthFlow --> AddAuthHeader
```

**Sources:** [src/mcp/client/auth.py:179-206](), [src/mcp/client/auth.py:485-551](), [src/mcp/client/auth.py:185]()

### PKCE Implementation

The system implements Proof Key for Code Exchange (PKCE) as specified in RFC 7636 to enhance security for OAuth flows.

| Component | Implementation | Purpose |
|-----------|---------------|---------|
| `PKCEParameters` | [src/mcp/client/auth.py:49-62]() | Generates cryptographically secure code verifier and challenge |
| Code Verifier | 128-character random string | Client-side secret for authorization code exchange |
| Code Challenge | SHA256 + Base64URL encoding | Server-verifiable challenge derived from verifier |
| Challenge Method | S256 | SHA256-based challenge method (required by RFC) |

**Sources:** [src/mcp/client/auth.py:49-62](), [tests/client/test_auth.py:82-107]()

### Token Storage Protocol

The `TokenStorage` protocol enables persistent token management across client sessions:

```mermaid
graph LR
    subgraph "TokenStorage Protocol"
        GetTokens["get_tokens()<br/>Retrieve Stored Tokens"]
        SetTokens["set_tokens()<br/>Persist Token Response"]
        GetClientInfo["get_client_info()<br/>Retrieve Client Credentials"]
        SetClientInfo["set_client_info()<br/>Persist Registration Info"]
    end
    
    subgraph "Storage Operations"
        TokenRetrieval["Token Retrieval<br/>Session Initialization"]
        TokenPersistence["Token Persistence<br/>After Exchange/Refresh"]
        ClientRegistration["Client Registration<br/>Dynamic Registration Storage"]
    end
    
    GetTokens --> TokenRetrieval
    SetTokens --> TokenPersistence
    GetClientInfo --> ClientRegistration
    SetClientInfo --> ClientRegistration
```

**Sources:** [src/mcp/client/auth.py:64-82](), [tests/client/test_auth.py:17-35]()

## OAuth Flow Implementation

The complete OAuth 2.0 authorization code flow with PKCE is implemented as an asynchronous generator that integrates with httpx's authentication system.

### Authorization Code Flow Sequence

```mermaid
sequenceDiagram
    participant Client as "MCP Client"
    participant Provider as "OAuthClientProvider"
    participant AS as "Authorization Server"
    participant RS as "Resource Server (MCP)"
    
    Note over Client,RS: Initial Request Without Auth
    Client->>Provider: HTTP Request with MCP-Protocol-Version
    Provider->>RS: Forward Request (No Auth Header)
    RS-->>Provider: 401 + WWW-Authenticate Header
    
    Note over Provider,AS: OAuth Discovery Phase
    Provider->>RS: GET /.well-known/oauth-protected-resource
    RS-->>Provider: ProtectedResourceMetadata (RFC 9728)
    Provider->>AS: GET /.well-known/oauth-authorization-server
    AS-->>Provider: OAuthMetadata (RFC 8414)
    
    Note over Provider,AS: Client Registration (If Needed)
    Provider->>AS: POST /register (Dynamic Client Registration)
    AS-->>Provider: Client Credentials + Metadata
    
    Note over Provider,AS: Authorization Flow with RFC 8707
    Provider->>Provider: Generate PKCE Parameters
    Provider->>Client: Redirect to /authorize?code_challenge=...&resource=...
    Client->>AS: User Authorization
    AS-->>Client: Redirect with Authorization Code
    Client->>Provider: Authorization Code + State
    
    Note over Provider,AS: Token Exchange with Resource Parameter
    Provider->>AS: POST /token (code + code_verifier + resource)
    AS-->>Provider: Access Token + Refresh Token
    Provider->>Provider: Store Tokens via TokenStorage
    
    Note over Client,RS: Authenticated Request
    Provider->>RS: Original Request + Authorization Header
    RS-->>Provider: Success Response
    Provider-->>Client: Success Response
```

**Sources:** [src/mcp/client/auth.py:485-551](), [tests/client/test_auth.py:616-714]()

### OAuth Discovery and Fallback

The client implements comprehensive discovery mechanisms with fallback support for legacy servers. The `_get_discovery_urls()` method generates an ordered list of discovery URLs:

| Discovery Type | Endpoint Pattern | RFC Reference | Implementation |
|---------------|------------------|---------------|----------------|
| Protected Resource | `/.well-known/oauth-protected-resource` | RFC 9728 | `_discover_protected_resource()` |
| Authorization Server (Path-aware) | `/.well-known/oauth-authorization-server{path}` | RFC 8414 | `_get_discovery_urls()` |
| Authorization Server (Root) | `/.well-known/oauth-authorization-server` | RFC 8414 | Fallback in ordered list |
| OpenID Configuration (Path-aware) | `/.well-known/openid-configuration{path}` | RFC 8414 §5 | Path-aware discovery |
| OpenID Configuration (Legacy) | `{server}/.well-known/openid-configuration` | OIDC 1.0 | Legacy fallback |

The discovery process includes protocol version header injection (`MCP_PROTOCOL_VERSION`) and WWW-Authenticate header parsing for enhanced resource metadata discovery.

**Sources:** [src/mcp/client/auth.py:254-279](), [src/mcp/client/auth.py:231-240](), [src/mcp/client/auth.py:474-475](), [tests/client/test_auth.py:252-261]()

## Server Authorization System

The server-side OAuth implementation provides a complete authorization server that can issue tokens for MCP resources.

### Authorization Server Routes

```mermaid
graph TB
    subgraph "OAuth Authorization Server"
        CreateAuthRoutes["create_auth_routes()<br/>Route Factory"]
        ValidateIssuer["validate_issuer_url()<br/>RFC 8414 Validation"]
        BuildMetadata["build_metadata()<br/>AS Metadata Generation"]
    end
    
    subgraph "Core Endpoints"
        MetadataEndpoint["/.well-known/oauth-authorization-server<br/>MetadataHandler"]
        AuthorizeEndpoint["/authorize<br/>AuthorizationHandler"]
        TokenEndpoint["/token<br/>TokenHandler + ClientAuthenticator"]
    end
    
    subgraph "Optional Endpoints"
        RegisterEndpoint["/register<br/>RegistrationHandler"]
        RevokeEndpoint["/revoke<br/>RevocationHandler"]
    end
    
    subgraph "Protected Resource Support"
        CreateProtectedResourceRoutes["create_protected_resource_routes()<br/>RFC 9728 Support"]
        ProtectedResourceEndpoint["/.well-known/oauth-protected-resource<br/>ProtectedResourceMetadataHandler"]
    end
    
    CreateAuthRoutes --> ValidateIssuer
    CreateAuthRoutes --> BuildMetadata
    CreateAuthRoutes --> MetadataEndpoint
    CreateAuthRoutes --> AuthorizeEndpoint
    CreateAuthRoutes --> TokenEndpoint
    CreateAuthRoutes --> RegisterEndpoint
    CreateAuthRoutes --> RevokeEndpoint
    
    CreateProtectedResourceRoutes --> ProtectedResourceEndpoint
```

**Sources:** [src/mcp/server/auth/routes.py:68-147](), [src/mcp/server/auth/routes.py:189-227]()

### Client Registration Handler

The `RegistrationHandler` implements RFC 7591 Dynamic Client Registration:

| Validation | Implementation | Error Response |
|------------|---------------|----------------|
| Metadata Validation | Pydantic `OAuthClientMetadata` | `invalid_client_metadata` |
| Scope Validation | `ClientRegistrationOptions.valid_scopes` | `invalid_client_metadata` |
| Grant Type Validation | Must be `["authorization_code", "refresh_token"]` | `invalid_client_metadata` |
| Client Secret Generation | `secrets.token_hex(32)` for non-public clients | N/A |

**Sources:** [src/mcp/server/auth/handlers/register.py:34-120]()

## Token Management

The OAuth system provides comprehensive token lifecycle management including validation, refresh, and expiration handling.

### OAuthToken Model

```mermaid
graph LR
    subgraph "OAuthToken (RFC 6749)"
        AccessToken["access_token: str<br/>Bearer Token"]
        TokenType["token_type: 'Bearer'<br/>Normalized to Title Case"]
        ExpiresIn["expires_in: int | None<br/>Token Lifetime (seconds)"]
        Scope["scope: str | None<br/>Granted Scopes"]
        RefreshToken["refresh_token: str | None<br/>Refresh Capability"]
    end
    
    subgraph "Validation Logic"
        TokenTypeValidation["normalize_token_type()<br/>RFC 6750 Compliance"]
        ExpiryCalculation["update_token_expiry()<br/>Current Time + expires_in"]
        ScopeValidation["Scope Subset Validation<br/>Prevent Scope Escalation"]
    end
    
    AccessToken --> TokenTypeValidation
    ExpiresIn --> ExpiryCalculation
    Scope --> ScopeValidation
```

**Sources:** [src/mcp/shared/auth.py:6-25](), [src/mcp/client/auth.py:120-142]()

### Token Refresh Flow and Resource Parameter Support

The client automatically refreshes expired tokens using stored refresh tokens and includes RFC 8707 resource parameter support:

| Condition | Action | Fallback | Resource Parameter |
|-----------|--------|----------|-------------------|
| Token Valid | Use existing token | N/A | N/A |
| Token Expired + Refresh Available | Automatic refresh | Full re-authorization on failure | Included if PRM exists or protocol ≥ 2025-06-18 |
| Token Expired + No Refresh | Full OAuth flow | N/A | Included in authorization/token requests |
| Refresh Fails | Clear stored tokens | Full OAuth flow | N/A |

The `should_include_resource_param()` method determines when to include the resource parameter based on:
- Presence of Protected Resource Metadata (always include)
- MCP-Protocol-Version ≥ 2025-06-18 (include for newer protocols)

**Sources:** [src/mcp/client/auth.py:411-462](), [src/mcp/client/auth.py:159-176](), [src/mcp/client/auth.py:431-433](), [tests/client/test_auth.py:443-465](), [tests/client/test_auth.py:471-525]()

## Discovery and Metadata Systems

The OAuth implementation supports comprehensive metadata discovery for both authorization servers and protected resources.

### Authorization Server Metadata

The `OAuthMetadata` model implements RFC 8414 Authorization Server Metadata:

```mermaid
graph TB
    subgraph "Required Metadata (RFC 8414)"
        Issuer["issuer: AnyHttpUrl<br/>AS Identifier"]
        AuthEndpoint["authorization_endpoint: AnyHttpUrl<br/>User Authorization"]
        TokenEndpoint["token_endpoint: AnyHttpUrl<br/>Token Exchange"]
    end
    
    subgraph "Optional Metadata"
        RegistrationEndpoint["registration_endpoint: AnyHttpUrl<br/>Dynamic Client Registration"]
        ScopesSupported["scopes_supported: list[str]<br/>Available Scopes"]
        GrantTypesSupported["grant_types_supported: list[str]<br/>Supported Grant Types"]
        RevocationEndpoint["revocation_endpoint: AnyHttpUrl<br/>Token Revocation"]
    end
    
    subgraph "MCP-Specific Extensions"
        CodeChallengeSupported["code_challenge_methods_supported<br/>['S256'] - PKCE Required"]
        ServiceDocumentation["service_documentation: AnyHttpUrl<br/>API Documentation"]
    end
```

**Sources:** [src/mcp/shared/auth.py:105-132](), [src/mcp/server/auth/routes.py:149-186]()

### Protected Resource Metadata

RFC 9728 Protected Resource Metadata enables resource servers to advertise their authorization requirements:

| Field | Purpose | MCP Implementation | Default Value |
|-------|---------|-------------------|---------------|
| `resource` | Resource server identifier | MCP server URL | Server URL |
| `authorization_servers` | List of trusted AS URLs | AS that can issue tokens for this resource | Required field |
| `scopes_supported` | Available scopes | MCP-specific scopes (tools, resources, prompts) | Optional |
| `bearer_methods_supported` | Token presentation methods | `["header"]` (Authorization header only) | `["header"]` |
| `resource_name` | Human-readable name | Optional display name | Optional |
| `resource_documentation` | Documentation URL | API documentation link | Optional |

**Sources:** [src/mcp/shared/auth.py:134-156](), [src/mcp/server/auth/routes.py:189-227]()

## Security Features

The OAuth 2.0 implementation includes comprehensive security measures following current best practices.

### HTTPS and Security Validation

```mermaid
graph LR
    subgraph "URL Security Validation"
        HTTPSRequired["HTTPS Required<br/>(except localhost)"]
        NoFragments["No URL Fragments<br/>Prevent Token Leakage"]
        NoQueryParams["No Query Parameters<br/>Clean Issuer URLs"]
    end
    
    subgraph "PKCE Security"
        SecureVerifier["128-character Verifier<br/>Cryptographically Secure"]
        SHA256Challenge["SHA256 Challenge<br/>S256 Method Required"]
        StateValidation["State Parameter<br/>CSRF Protection"]
    end
    
    subgraph "Token Security"
        BearerOnly["Bearer Tokens Only<br/>RFC 6750 Compliance"]
        ScopeValidation["Scope Validation<br/>Prevent Escalation"]
        SecureStorage["TokenStorage Protocol<br/>Persistent Security"]
    end
```

**Sources:** [src/mcp/server/auth/routes.py:23-47](), [src/mcp/client/auth.py:49-61](), [src/mcp/client/auth.py:347-353]()

### WWW-Authenticate Header Support

The client implements RFC 9728 WWW-Authenticate header parsing for enhanced discovery:

| Header Format | Extraction Pattern | Example |
|---------------|-------------------|---------|
| Quoted URL | `resource_metadata="URL"` | `Bearer resource_metadata="https://api.example.com/.well-known/oauth-protected-resource"` |
| Unquoted URL | `resource_metadata=URL` | `Bearer resource_metadata=https://api.example.com/.well-known/oauth-protected-resource` |
| Complex Header | Multiple parameters | `Bearer realm="api", resource_metadata="URL", error="insufficient_scope"` |

**Sources:** [src/mcp/client/auth.py:207-229](), [tests/client/test_auth.py:844-906]()

# Development Tools & CLI




The MCP Python SDK includes a comprehensive command-line interface (CLI) that streamlines the development workflow for MCP servers. The CLI provides commands for running servers, integrating with development tools, and deploying to client applications like Claude Desktop.

For information about the underlying server frameworks, see [FastMCP Server Framework](#2). For details about transport implementations, see [Transport Layer](#5).

## CLI Architecture

The MCP CLI is built using the `typer` library and provides a unified interface for server development and deployment operations. The system consists of two main modules: the core CLI implementation and Claude Desktop integration utilities.

### CLI Command Structure

```mermaid
graph TB
    subgraph "CLI Entry Point"
        app["typer.Typer()"]
    end
    
    subgraph "Core Commands"
        version_cmd["version()"]
        dev_cmd["dev()"]
        run_cmd["run()"]
        install_cmd["install()"]
    end
    
    subgraph "Helper Functions"
        parse_file["_parse_file_path()"]
        import_server["_import_server()"]
        build_uv["_build_uv_command()"]
        parse_env["_parse_env_var()"]
    end
    
    subgraph "Claude Integration"
        claude_config["claude.update_claude_config()"]
        claude_path["claude.get_claude_config_path()"]
        uv_path["claude.get_uv_path()"]
    end
    
    subgraph "External Tools"
        uv_runner["uv run"]
        npx_inspector["npx @modelcontextprotocol/inspector"]
        fastmcp_server["FastMCP server instance"]
    end
    
    app --> version_cmd
    app --> dev_cmd
    app --> run_cmd
    app --> install_cmd
    
    dev_cmd --> parse_file
    dev_cmd --> import_server
    dev_cmd --> build_uv
    dev_cmd --> npx_inspector
    
    run_cmd --> parse_file
    run_cmd --> import_server
    run_cmd --> fastmcp_server
    
    install_cmd --> parse_file
    install_cmd --> import_server
    install_cmd --> parse_env
    install_cmd --> claude_config
    
    claude_config --> claude_path
    claude_config --> uv_path
    
    style app fill:#f9f9f9
    style fastmcp_server fill:#e8f5e8
```

**Sources:** [src/mcp/cli/cli.py:34-39](), [src/mcp/cli/cli.py:211-488](), [src/mcp/cli/claude.py:44-148]()

### Server Import and Resolution

The CLI includes sophisticated server discovery and import mechanisms that handle various server specification formats and automatically resolve FastMCP server instances.

```mermaid
graph TB
    subgraph "Server Resolution Process"
        file_spec["File Specification Input"]
        parse_path["_parse_file_path()"]
        import_mod["_import_server()"]
        check_obj["_check_server_object()"]
    end
    
    subgraph "File Parsing"
        path_resolve["Path.resolve()"]
        object_split["file:object syntax parsing"]
        windows_drive["Windows drive letter handling"]
    end
    
    subgraph "Module Import"
        spec_loader["importlib.util.spec_from_file_location()"]
        module_exec["spec.loader.exec_module()"]
        sys_path["sys.path.insert()"]
    end
    
    subgraph "Server Discovery"
        auto_names["Auto-discovery: 'mcp', 'server', 'app'"]
        explicit_obj["Explicit object specification"]
        module_obj["module:object syntax"]
    end
    
    subgraph "Validation"
        fastmcp_check["isinstance(server, FastMCP)"]
        lowlevel_warn["LowLevelServer warning"]
    end
    
    file_spec --> parse_path
    parse_path --> path_resolve
    parse_path --> object_split
    parse_path --> windows_drive
    
    parse_path --> import_mod
    import_mod --> spec_loader
    import_mod --> module_exec
    import_mod --> sys_path
    
    import_mod --> auto_names
    import_mod --> explicit_obj
    import_mod --> module_obj
    
    import_mod --> check_obj
    check_obj --> fastmcp_check
    check_obj --> lowlevel_warn
    
    style fastmcp_check fill:#e8f5e8
    style lowlevel_warn fill:#fff3e0
```

**Sources:** [src/mcp/cli/cli.py:88-116](), [src/mcp/cli/cli.py:119-208](), [src/mcp/cli/cli.py:143-159]()

## CLI Commands

### Version Command

The `version` command displays the currently installed MCP package version using Python's metadata system.

```python
# Usage: mcp version
# Implementation: cli.py:212-219
```

**Sources:** [src/mcp/cli/cli.py:212-219]()

### Development Command

The `dev` command runs an MCP server with the MCP Inspector for interactive development and testing. It automatically manages dependencies using `uv` and launches the Node.js-based inspector tool.

```mermaid
graph TB
    subgraph "mcp dev Command Flow"
        dev_input["mcp dev server.py:app"]
        parse_args["Parse file_spec and options"]
        import_server["Import FastMCP server"]
        get_deps["Extract server.dependencies"]
        build_cmd["_build_uv_command()"]
        npx_cmd["_get_npx_command()"]
        run_inspector["subprocess.run(npx + uv_cmd)"]
    end
    
    subgraph "Dependency Management"
        with_editable["--with-editable option"]
        with_packages["--with packages"]
        server_deps["server.dependencies"]
        uv_run["uv run --with mcp[cli]"]
    end
    
    subgraph "Inspector Integration"
        npx_check["Platform-specific npx detection"]
        inspector_pkg["@modelcontextprotocol/inspector"]
        shell_handling["Windows shell=True handling"]
    end
    
    dev_input --> parse_args
    parse_args --> import_server
    import_server --> get_deps
    
    with_editable --> build_cmd
    with_packages --> build_cmd
    server_deps --> build_cmd
    
    build_cmd --> uv_run
    npx_cmd --> npx_check
    npx_check --> inspector_pkg
    
    run_inspector --> shell_handling
    
    style import_server fill:#e8f5e8
    style inspector_pkg fill:#f3e5f5
```

**Sources:** [src/mcp/cli/cli.py:222-303](), [src/mcp/cli/cli.py:42-53](), [src/mcp/cli/cli.py:65-85]()

### Run Command

The `run` command executes an MCP server directly without additional tooling. It supports transport specification and runs the server using the FastMCP framework.

Key features:
- Direct server execution without dependency management
- Transport protocol selection (`stdio` or `sse`)
- Server object import and validation

**Sources:** [src/mcp/cli/cli.py:305-359]()

### Install Command

The `install` command configures MCP servers for use with Claude Desktop by updating the application's configuration file. It handles dependency specification, environment variable management, and cross-platform config file locations.

```mermaid
graph TB
    subgraph "mcp install Command Process"
        install_input["mcp install server.py:app --name myserver"]
        parse_install["Parse arguments and options"]
        claude_check["claude.get_claude_config_path()"]
        import_optional["Optional server import for name/deps"]
        env_processing["Process --env-var and --env-file"]
        update_config["claude.update_claude_config()"]
    end
    
    subgraph "Environment Variable Handling"
        env_vars["--env-var KEY=VALUE"]
        env_file["--env-file .env"]
        dotenv_load["dotenv.dotenv_values()"]
        env_merge["Merge with existing env vars"]
    end
    
    subgraph "Claude Config Update"
        config_path["Platform-specific config path"]
        json_read["Read claude_desktop_config.json"]
        server_entry["Create mcpServers entry"]
        uv_command["Generate uv run command"]
        json_write["Write updated config"]
    end
    
    install_input --> parse_install
    parse_install --> claude_check
    parse_install --> import_optional
    parse_install --> env_processing
    
    env_processing --> env_vars
    env_processing --> env_file
    env_file --> dotenv_load
    env_processing --> env_merge
    
    update_config --> config_path
    update_config --> json_read
    update_config --> server_entry
    update_config --> uv_command
    update_config --> json_write
    
    style claude_check fill:#fff3e0
    style uv_command fill:#e8f5e8
```

**Sources:** [src/mcp/cli/cli.py:362-488](), [src/mcp/cli/cli.py:456-476](), [src/mcp/cli/claude.py:44-148]()

## Claude Desktop Integration

The Claude integration module provides platform-aware configuration management for installing MCP servers into the Claude Desktop application.

### Configuration Path Detection

The system detects Claude Desktop configuration directories across different platforms:

| Platform | Configuration Path |
|----------|-------------------|
| Windows | `%APPDATA%\Claude` |
| macOS | `~/Library/Application Support/Claude` |
| Linux | `$XDG_CONFIG_HOME/Claude` or `~/.config/Claude` |

**Sources:** [src/mcp/cli/claude.py:17-30]()

### Config File Management

The `update_claude_config()` function manages the `claude_desktop_config.json` file, handling:

- Server entry creation and updates
- Environment variable preservation and merging
- Absolute path resolution for server files
- UV command generation with dependency specifications

```mermaid
graph TB
    subgraph "Claude Config Structure"
        config_root["claude_desktop_config.json"]
        mcp_servers["mcpServers object"]
        server_entry["Server configuration entry"]
    end
    
    subgraph "Server Entry Components"
        command_field["command: uv executable path"]
        args_field["args: [run, --with, mcp, run, server.py:app]"]
        env_field["env: environment variables"]
    end
    
    subgraph "UV Command Generation"
        uv_path["get_uv_path()"]
        mcp_package["--with mcp[cli]"]
        additional_packages["--with package1 --with package2"]
        editable_install["--with-editable /path/to/project"]
        mcp_run["mcp run server.py:app"]
    end
    
    config_root --> mcp_servers
    mcp_servers --> server_entry
    
    server_entry --> command_field
    server_entry --> args_field
    server_entry --> env_field
    
    command_field --> uv_path
    args_field --> mcp_package
    args_field --> additional_packages
    args_field --> editable_install
    args_field --> mcp_run
    
    style server_entry fill:#e8f5e8
    style mcp_run fill:#f3e5f5
```

**Sources:** [src/mcp/cli/claude.py:44-148](), [src/mcp/cli/claude.py:101-125](), [src/mcp/cli/claude.py:33-41]()

## Development Workflow Integration

The CLI system integrates with the broader MCP development ecosystem through several key mechanisms:

### Dependency Management with UV

All CLI commands use `uv` for Python dependency management, ensuring reproducible environments and fast package installation. The system automatically includes the `mcp[cli]` package and any server-specific dependencies.

### FastMCP Server Integration

The CLI specifically targets FastMCP servers and includes validation to ensure compatibility. It automatically extracts server metadata including:

- Server name for Claude Desktop registration
- Dependency requirements for installation
- Transport capabilities for runtime configuration

### Inspector Integration

The `dev` command integrates with the Node.js-based MCP Inspector tool, providing a web interface for interactive server testing and debugging.

**Sources:** [src/mcp/cli/cli.py:260-284](), [src/mcp/cli/cli.py:152-159](), [src/mcp/cli/cli.py:442-455]()

# MCP CLI Commands




This document covers the MCP CLI commands that provide development tools for building, testing, and deploying MCP servers. The CLI facilitates server development with dependency management, debugging tools, and integration with Claude Desktop.

For information about the underlying FastMCP server framework that these commands operate on, see [FastMCP Server Framework](#2). For details about Claude Desktop integration configuration, see [Claude Desktop Integration](#8.3).

## Purpose and Scope

The MCP CLI provides three primary commands for MCP server development and deployment:

- `mcp dev` - Development server with MCP Inspector integration
- `mcp run` - Direct server execution 
- `mcp install` - Claude Desktop application integration
- `mcp version` - Version information

All commands support automatic dependency management through `uv` and handle both standalone Python files and package-based servers.

## CLI Architecture Overview

```mermaid
graph TB
    subgraph "CLI Entry Points"
        cli_app["typer.Typer app<br/>(cli.py)"]
        dev_cmd["dev() command"]
        run_cmd["run() command"] 
        install_cmd["install() command"]
        version_cmd["version() command"]
    end
    
    subgraph "Core Functions"
        parse_file_path["_parse_file_path()<br/>Parse file:object syntax"]
        import_server["_import_server()<br/>Import FastMCP instances"]
        build_uv_command["_build_uv_command()<br/>Build uv run commands"]
        parse_env_var["_parse_env_var()<br/>Parse KEY=VALUE env vars"]
    end
    
    subgraph "Claude Integration"
        update_claude_config["update_claude_config()<br/>(claude.py)"]
        get_claude_config_path["get_claude_config_path()<br/>Platform-specific paths"]
        get_uv_path["get_uv_path()<br/>Find uv executable"]
    end
    
    subgraph "External Tools"
        npx_inspector["npx @modelcontextprotocol/inspector"]
        uv_run["uv run command execution"]
        claude_desktop["Claude Desktop App"]
    end
    
    cli_app --> dev_cmd
    cli_app --> run_cmd  
    cli_app --> install_cmd
    cli_app --> version_cmd
    
    dev_cmd --> parse_file_path
    dev_cmd --> import_server
    dev_cmd --> build_uv_command
    dev_cmd --> npx_inspector
    
    run_cmd --> parse_file_path
    run_cmd --> import_server
    
    install_cmd --> parse_file_path
    install_cmd --> import_server
    install_cmd --> parse_env_var
    install_cmd --> update_claude_config
    
    update_claude_config --> get_claude_config_path
    update_claude_config --> get_uv_path
    update_claude_config --> claude_desktop
    
    build_uv_command --> uv_run
```

Sources: [src/mcp/cli/cli.py:34-39](), [src/mcp/cli/cli.py:42-86](), [src/mcp/cli/claude.py:44-148]()

## Development Command (mcp dev)

The `mcp dev` command launches the MCP Inspector for interactive server testing and debugging.

### Command Syntax

```bash
mcp dev <file_spec> [--with-editable PATH] [--with PACKAGE]...
```

### Implementation Flow

```mermaid
sequenceDiagram
    participant CLI as "dev() command"
    participant Parser as "_parse_file_path()"
    participant Importer as "_import_server()"
    participant Builder as "_build_uv_command()"
    participant NPX as "npx inspector"
    participant UV as "uv run"
    participant Server as "FastMCP server"
    
    CLI->>Parser: "Parse file_spec"
    Parser->>CLI: "file_path, server_object"
    
    CLI->>Importer: "Import server for dependencies"
    Importer->>CLI: "FastMCP instance"
    
    CLI->>Builder: "Build uv command with packages"
    Builder->>CLI: "['uv', 'run', '--with', 'mcp', 'mcp', 'run', file_spec]"
    
    CLI->>NPX: "Launch inspector with uv command"
    NPX->>UV: "Execute uv run command"
    UV->>Server: "Start FastMCP server"
    
    Note over NPX,Server: "Interactive debugging session"
```

Sources: [src/mcp/cli/cli.py:222-303](), [src/mcp/cli/cli.py:65-85](), [src/mcp/cli/cli.py:268-283]()

### Key Features

| Feature | Implementation | Purpose |
|---------|---------------|---------|
| Dependency Detection | [src/mcp/cli/cli.py:262-264]() | Automatically includes server.dependencies |
| NPX Integration | [src/mcp/cli/cli.py:268-283]() | Launches MCP Inspector for debugging |
| Cross-Platform | [src/mcp/cli/cli.py:42-53]() | Handles Windows/Unix npx differences |
| Editable Install | [src/mcp/cli/cli.py:228-238]() | Supports --with-editable for development |

Sources: [src/mcp/cli/cli.py:222-303]()

## Run Command (mcp run)

The `mcp run` command executes MCP servers directly without dependency management.

### Command Syntax

```bash
mcp run <file_spec> [--transport TRANSPORT]
```

### Server Import Process

```mermaid
graph TB
    subgraph "File Parsing"
        file_spec["file_spec input<br/>e.g., 'server.py:app'"]
        parse_windows["Windows path detection<br/>Check file_spec[1] == ':'"]
        split_colon["Split on last colon<br/>rsplit(':', 1)"]
        resolve_path["Path resolution<br/>Path.resolve()"]
    end
    
    subgraph "Module Import"
        add_to_path["Add parent dir to sys.path"]
        create_spec["importlib.util.spec_from_file_location()"]
        load_module["spec.loader.exec_module()"]
        find_object["Find server object"]
    end
    
    subgraph "Object Discovery"
        explicit_name["Use specified object name"]
        common_names["Try 'mcp', 'server', 'app'"]
        validate_type["Check isinstance(obj, FastMCP)"]
    end
    
    file_spec --> parse_windows
    parse_windows --> split_colon
    split_colon --> resolve_path
    
    resolve_path --> add_to_path
    add_to_path --> create_spec
    create_spec --> load_module
    load_module --> find_object
    
    find_object --> explicit_name
    find_object --> common_names
    explicit_name --> validate_type
    common_names --> validate_type
```

Sources: [src/mcp/cli/cli.py:88-208](), [src/mcp/cli/cli.py:305-360]()

### Transport Support

The run command supports optional transport specification:

- `stdio` - Standard input/output transport
- `sse` - Server-Sent Events transport
- Default: Server's configured transport

Sources: [src/mcp/cli/cli.py:311-318](), [src/mcp/cli/cli.py:346-350]()

## Install Command (mcp install)

The `mcp install` command configures MCP servers in Claude Desktop's configuration.

### Command Syntax

```bash
mcp install <file_spec> [--name NAME] [--with-editable PATH] [--with PACKAGE]... [--env-var KEY=VALUE]... [--env-file FILE]
```

### Claude Configuration Process

```mermaid
graph TB
    subgraph "Configuration Discovery"
        get_claude_path["get_claude_config_path()<br/>Platform-specific paths"]
        win32_path["Windows:<br/>AppData/Roaming/Claude"]
        darwin_path["macOS:<br/>Library/Application Support/Claude"]
        linux_path["Linux:<br/>XDG_CONFIG_HOME/Claude"]
    end
    
    subgraph "Config File Management"
        config_file["claude_desktop_config.json"]
        create_if_missing["Create empty {} if missing"]
        load_json["json.loads(config.read_text())"]
        ensure_mcpServers["Ensure 'mcpServers' key exists"]
    end
    
    subgraph "Server Configuration"
        build_uv_cmd["Build uv run command"]
        collect_packages["Collect --with packages"]
        merge_env_vars["Merge environment variables"]
        absolute_path["Convert file_spec to absolute"]
    end
    
    subgraph "Final Config"
        server_config_obj["{'command': uv_path, 'args': [...], 'env': {...}}"]
        write_json["Write updated config"]
    end
    
    get_claude_path --> win32_path
    get_claude_path --> darwin_path  
    get_claude_path --> linux_path
    
    win32_path --> config_file
    darwin_path --> config_file
    linux_path --> config_file
    
    config_file --> create_if_missing
    create_if_missing --> load_json
    load_json --> ensure_mcpServers
    
    ensure_mcpServers --> build_uv_cmd
    build_uv_cmd --> collect_packages
    collect_packages --> merge_env_vars
    merge_env_vars --> absolute_path
    
    absolute_path --> server_config_obj
    server_config_obj --> write_json
```

Sources: [src/mcp/cli/claude.py:17-31](), [src/mcp/cli/claude.py:44-148](), [src/mcp/cli/cli.py:362-489]()

### Environment Variable Handling

The install command supports flexible environment variable configuration:

| Method | Implementation | Behavior |
|--------|---------------|----------|
| Command Line | `--env-var KEY=VALUE` | [src/mcp/cli/cli.py:474-476]() |
| .env File | `--env-file path.env` | [src/mcp/cli/cli.py:462-471]() |
| Preservation | Existing vars preserved | [src/mcp/cli/claude.py:92-99]() |
| Merging | New vars override existing | [src/mcp/cli/claude.py:96-97]() |

Sources: [src/mcp/cli/cli.py:394-413](), [src/mcp/cli/cli.py:457-477]()

## Version Command (mcp version)

Simple command that displays the installed MCP package version using `importlib.metadata`.

```python