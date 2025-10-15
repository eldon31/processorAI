This document covers the security features implemented for MCP transport layers, focusing on DNS rebinding protection and request validation middleware. The security system provides configurable protection against malicious cross-origin requests targeting locally-hosted MCP servers.

For information about specific transport implementations, see [StreamableHTTP Transport](#5.1), [SSE Transport](#5.2), and [WebSocket Transport](#5.4). For authentication mechanisms, see [Authentication & Security](#7).

## Security Architecture Overview

The transport security system implements a middleware-based architecture that validates incoming HTTP requests before they reach the MCP protocol handlers. The system is designed to prevent DNS rebinding attacks while maintaining compatibility with legitimate client connections.

```mermaid
graph TB
    subgraph "Client Request Flow"
        ClientReq["Client HTTP Request"]
        SecurityMW["TransportSecurityMiddleware"]
        TransportLayer["Transport Handler<br/>(StreamableHTTP/SSE)"]
        MCPServer["MCP Server"]
    end
    
    subgraph "Security Validation"
        HostVal["Host Header Validation"]
        OriginVal["Origin Header Validation"] 
        ContentTypeVal["Content-Type Validation"]
        DNSRebindCheck["DNS Rebinding Protection"]
    end
    
    subgraph "Configuration"
        SecuritySettings["TransportSecuritySettings"]
        AllowedHosts["allowed_hosts[]"]
        AllowedOrigins["allowed_origins[]"]
        ProtectionFlag["enable_dns_rebinding_protection"]
    end
    
    ClientReq --> SecurityMW
    SecurityMW --> HostVal
    SecurityMW --> OriginVal
    SecurityMW --> ContentTypeVal
    HostVal --> DNSRebindCheck
    OriginVal --> DNSRebindCheck
    
    SecuritySettings --> SecurityMW
    AllowedHosts --> HostVal
    AllowedOrigins --> OriginVal
    ProtectionFlag --> DNSRebindCheck
    
    SecurityMW --> TransportLayer
    TransportLayer --> MCPServer
    
    SecurityMW -.->|"Error Response"| ClientReq
```

Sources: [src/mcp/server/transport_security.py:37-128](), [src/mcp/server/streamable_http_manager.py:24-68]()

## DNS Rebinding Protection

DNS rebinding attacks occur when malicious websites trick browsers into making requests to local servers using specially crafted DNS responses. The MCP security system prevents these attacks by validating request headers that browsers automatically include.

### Threat Model

| Attack Vector | Validation Method | HTTP Status | Error Message |
|---------------|-------------------|-------------|---------------|
| Malicious Host header | Host whitelist validation | 421 | "Invalid Host header" |
| Cross-origin requests | Origin header validation | 400 | "Invalid Origin header" |
| Wrong content type | Content-Type validation | 400 | "Invalid Content-Type header" |

```mermaid
graph LR
    subgraph "Attack Scenario"
        Attacker["evil.com"]
        Browser["User Browser"]
        LocalServer["localhost:8080<br/>MCP Server"]
    end
    
    subgraph "Protection Mechanism"
        HostHeader["Host: evil.com"]
        ValidationFail["Host Validation Fails"]
        Block["Request Blocked<br/>Status 421"]
    end
    
    Attacker -->|"DNS Rebinding"| Browser
    Browser -->|"HTTP Request"| HostHeader
    HostHeader --> ValidationFail
    ValidationFail --> Block
    Block -.->|"Blocked"| LocalServer
```

Sources: [src/mcp/server/transport_security.py:45-66](), [tests/server/test_streamable_http_security.py:110-136]()

## Configuration Settings

The `TransportSecuritySettings` class provides flexible configuration for security features:

### Basic Configuration

```python
TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=["localhost", "127.0.0.1:8080"],
    allowed_origins=["http://localhost", "http://127.0.0.1:8080"]
)
```

### Wildcard Port Patterns

The system supports wildcard port patterns for development environments:

| Pattern | Matches | Example |
|---------|---------|---------|
| `"localhost:*"` | Any port on localhost | `localhost:3000`, `localhost:8080` |
| `"127.0.0.1:*"` | Any port on 127.0.0.1 | `127.0.0.1:5000`, `127.0.0.1:9999` |
| `"http://localhost:*"` | Any port in origins | `http://localhost:3000` |

```mermaid
graph TB
    subgraph "TransportSecuritySettings"
        EnableProtection["enable_dns_rebinding_protection: bool"]
        AllowedHosts["allowed_hosts: list[str]"]
        AllowedOrigins["allowed_origins: list[str]"]
    end
    
    subgraph "Validation Logic"
        HostValidator["_validate_host()"]
        OriginValidator["_validate_origin()"]
        ContentTypeValidator["_validate_content_type()"]
    end
    
    subgraph "Pattern Matching"
        ExactMatch["Exact String Match"]
        WildcardMatch["Wildcard Port Pattern<br/>host:*"]
    end
    
    EnableProtection --> HostValidator
    AllowedHosts --> HostValidator
    AllowedOrigins --> OriginValidator
    
    HostValidator --> ExactMatch
    HostValidator --> WildcardMatch
    OriginValidator --> ExactMatch
    OriginValidator --> WildcardMatch
```

Sources: [src/mcp/server/transport_security.py:12-35](), [src/mcp/server/transport_security.py:56-63](), [tests/server/test_sse_security.py:226-256]()

## Security Middleware Implementation

The `TransportSecurityMiddleware` class implements the core validation logic:

### Validation Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `_validate_host()` | Validates Host header against whitelist | `bool` |
| `_validate_origin()` | Validates Origin header (optional) | `bool` |
| `_validate_content_type()` | Ensures JSON content type for POST | `bool` |
| `validate_request()` | Main validation entry point | `Response | None` |

### Validation Flow

```mermaid
graph TD
    Request["Incoming Request"]
    IsPost{"POST Request?"}
    ContentTypeCheck["Validate Content-Type"]
    ContentTypeFail["Return 400<br/>Invalid Content-Type"]
    
    ProtectionEnabled{"DNS Protection<br/>Enabled?"}
    HostCheck["Validate Host Header"]
    HostFail["Return 421<br/>Invalid Host"]
    
    OriginCheck["Validate Origin Header"]
    OriginFail["Return 400<br/>Invalid Origin"]
    
    Success["Return None<br/>(Validation Passed)"]
    
    Request --> IsPost
    IsPost -->|Yes| ContentTypeCheck
    IsPost -->|No| ProtectionEnabled
    ContentTypeCheck -->|Invalid| ContentTypeFail
    ContentTypeCheck -->|Valid| ProtectionEnabled
    
    ProtectionEnabled -->|No| Success
    ProtectionEnabled -->|Yes| HostCheck
    HostCheck -->|Invalid| HostFail
    HostCheck -->|Valid| OriginCheck
    OriginCheck -->|Invalid| OriginFail
    OriginCheck -->|Valid| Success
```

Sources: [src/mcp/server/transport_security.py:102-128](), [src/mcp/server/transport_security.py:89-101]()

## Transport Integration

Security middleware integrates with multiple transport types through a common pattern:

### StreamableHTTP Integration

The `StreamableHTTPSessionManager` accepts security settings and passes them to transport instances:

```mermaid
graph LR
    subgraph "StreamableHTTPSessionManager"
        Constructor["__init__(security_settings)"]
        HandleRequest["handle_request()"]
        CreateTransport["StreamableHTTPServerTransport"]
    end
    
    subgraph "Transport Security"
        SecuritySettings["TransportSecuritySettings"]
        SecurityMiddleware["TransportSecurityMiddleware"]
    end
    
    SecuritySettings --> Constructor
    Constructor --> CreateTransport
    CreateTransport --> SecurityMiddleware
    HandleRequest --> SecurityMiddleware
```

### SSE Integration

The `SseServerTransport` similarly integrates security validation:

| Transport Type | Security Integration Point | Error Handling |
|----------------|----------------------------|----------------|
| StreamableHTTP | `StreamableHTTPServerTransport` constructor | Middleware returns error response |
| SSE | `SseServerTransport` constructor | Validation in `connect_sse()` |
| WebSocket | Not implemented | N/A |
| STDIO | Not applicable | Local process communication |

Sources: [src/mcp/server/streamable_http_manager.py:62-68](), [src/mcp/server/streamable_http_manager.py:224-229](), [tests/server/test_sse_security.py:45-58]()

## Default Security Behavior

The security system uses conservative defaults to maintain backward compatibility:

### Default Settings

| Setting | Default Value | Rationale |
|---------|---------------|-----------|
| `enable_dns_rebinding_protection` | `True` in settings, `False` in middleware | Backwards compatibility |
| `allowed_hosts` | `[]` (empty list) | Must be explicitly configured |
| `allowed_origins` | `[]` (empty list) | Must be explicitly configured |

### Backward Compatibility

```mermaid
graph TD
    NoSettings["No Security Settings Provided"]
    DefaultMiddleware["TransportSecurityMiddleware<br/>enable_dns_rebinding_protection=False"]
    ContentTypeOnly["Only Content-Type Validation<br/>for POST requests"]
    
    WithSettings["Security Settings Provided"]
    ConfiguredMiddleware["TransportSecurityMiddleware<br/>with user settings"]
    FullValidation["Full DNS Rebinding Protection"]
    
    NoSettings --> DefaultMiddleware
    DefaultMiddleware --> ContentTypeOnly
    
    WithSettings --> ConfiguredMiddleware
    ConfiguredMiddleware --> FullValidation
```

Sources: [src/mcp/server/transport_security.py:40-43](), [src/mcp/server/transport_security.py:114-115]()

## Testing and Validation

The security system includes comprehensive tests covering various attack scenarios and configuration options:

### Test Coverage

| Test Category | File | Key Test Cases |
|---------------|------|----------------|
| StreamableHTTP Security | `test_streamable_http_security.py` | Host/Origin validation, Content-Type checks |
| SSE Security | `test_sse_security.py` | GET/POST validation, wildcard patterns |
| Integration | Both files | Real server processes, multiprocessing tests |

### Security Test Scenarios

```mermaid
graph TB
    subgraph "Attack Simulations"
        InvalidHost["Invalid Host Header<br/>evil.com"]
        InvalidOrigin["Invalid Origin Header<br/>http://evil.com"]
        WrongContentType["Wrong Content-Type<br/>text/plain"]
    end
    
    subgraph "Valid Requests"
        ValidHost["Valid Host<br/>localhost, 127.0.0.1"]
        ValidOrigin["Valid Origin<br/>http://localhost"]
        ValidContentType["Valid Content-Type<br/>application/json"]
    end
    
    subgraph "Test Results"
        Block421["HTTP 421<br/>Invalid Host"]
        Block400Origin["HTTP 400<br/>Invalid Origin"]
        Block400ContentType["HTTP 400<br/>Invalid Content-Type"]
        Allow200["HTTP 200<br/>Success"]
    end
    
    InvalidHost --> Block421
    InvalidOrigin --> Block400Origin
    WrongContentType --> Block400ContentType
    
    ValidHost --> Allow200
    ValidOrigin --> Allow200
    ValidContentType --> Allow200
```

Sources: [tests/server/test_streamable_http_security.py:85-294](), [tests/server/test_sse_security.py:78-294]()