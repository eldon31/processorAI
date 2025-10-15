This page covers the OAuth 2.0 client authentication implementation in the MCP Python SDK. It provides comprehensive OAuth 2.0 support including PKCE flows, automatic discovery, dynamic client registration, and token management for MCP clients.

For server-side authentication, see [OAuth 2.0 Server](#7.2). For general ClientSession usage, see [ClientSession](#4.1).

## Overview

The client authentication system implements OAuth 2.0 Authorization Code flow with PKCE (Proof Key for Code Exchange) for secure authentication with MCP servers. It supports both modern RFC 9728 protected resource architecture and legacy authorization server patterns for backwards compatibility.

**Key Components:**
- `OAuthClientProvider` - Main authentication provider implementing `httpx.Auth`
- `OAuthContext` - Stateful context managing OAuth flow data
- `PKCEParameters` - PKCE parameter generation and validation
- `TokenStorage` - Protocol for persistent token storage

Sources: [src/mcp/client/auth.py:1-552](), [tests/client/test_auth.py:1-900]()

## Architecture Overview

```mermaid
graph TB
    subgraph "Client Authentication Components"
        OCP["OAuthClientProvider<br/>(httpx.Auth)"]
        CTX["OAuthContext"]
        PKCE["PKCEParameters"]
        TS["TokenStorage<br/>(Protocol)"]
    end
    
    subgraph "Discovery & Registration"
        PRM["Protected Resource<br/>Discovery (RFC 9728)"]
        OAuthMeta["OAuth Metadata<br/>Discovery"]
        DCR["Dynamic Client<br/>Registration"]
    end
    
    subgraph "Token Management"
        AuthFlow["Authorization Flow<br/>(PKCE)"]
        TokenEx["Token Exchange"]
        TokenRef["Token Refresh"]
        TokenVal["Token Validation"]
    end
    
    subgraph "Transport Integration"
        HTTPX["httpx.AsyncClient"]
        AuthFlow_HTTPX["async_auth_flow"]
    end
    
    OCP --> CTX
    OCP --> PKCE
    OCP --> TS
    
    OCP --> PRM
    OCP --> OAuthMeta
    OCP --> DCR
    
    OCP --> AuthFlow
    OCP --> TokenEx
    OCP --> TokenRef
    OCP --> TokenVal
    
    OCP --> AuthFlow_HTTPX
    AuthFlow_HTTPX --> HTTPX
    
    CTX -.-> "Lock for<br/>thread safety"
    CTX -.-> "Protocol version<br/>handling"
```

Sources: [src/mcp/client/auth.py:179-552](), [src/mcp/client/auth.py:84-177]()

## Core Components

### OAuthClientProvider

The `OAuthClientProvider` class is the main entry point for OAuth authentication, implementing the `httpx.Auth` interface for seamless integration with HTTP clients.

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| **Initialization** | Setup OAuth context and handlers | `__init__()` |
| **Discovery** | Find authorization endpoints | `_discover_protected_resource()`, `_get_discovery_urls()` |
| **Registration** | Register OAuth client | `_register_client()` |
| **Authorization** | Perform PKCE flow | `_perform_authorization()` |
| **Token Management** | Exchange and refresh tokens | `_exchange_token()`, `_refresh_token()` |
| **Integration** | HTTPX auth flow | `async_auth_flow()` |

**Key Configuration:**
```python
OAuthClientProvider(
    server_url="https://api.example.com/v1/mcp",
    client_metadata=client_metadata,
    storage=token_storage,
    redirect_handler=redirect_handler,
    callback_handler=callback_handler,
    timeout=300.0
)
```

Sources: [src/mcp/client/auth.py:179-206](), [src/mcp/client/auth.py:485-552]()

### OAuthContext

The `OAuthContext` dataclass maintains all state during the OAuth flow, including discovered metadata, client information, and current tokens.

**State Management:**
- **Discovery metadata**: `protected_resource_metadata`, `oauth_metadata`
- **Client registration**: `client_info` 
- **Token state**: `current_tokens`, `token_expiry_time`
- **Thread safety**: `lock` (anyio.Lock)

**Key Methods:**
- `is_token_valid()` - Check token validity and expiration
- `can_refresh_token()` - Determine if refresh is possible
- `get_resource_url()` - Calculate RFC 8707 resource parameter
- `should_include_resource_param()` - Protocol version-aware parameter inclusion

Sources: [src/mcp/client/auth.py:84-177]()

### PKCEParameters

Implements PKCE (Proof Key for Code Exchange) parameter generation following RFC 7636 for enhanced security.

**Generation Process:**
- **Code verifier**: 128-character random string using `[A-Za-z0-9-._~]`
- **Code challenge**: SHA256 hash of verifier, base64url-encoded (no padding)
- **Challenge method**: Always "S256"

```python
pkce = PKCEParameters.generate()