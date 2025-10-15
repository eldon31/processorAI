This document covers how FastAPI processes and serializes responses from path operation functions into HTTP responses. It explains the default response behavior, serialization pipeline, response model validation, and custom response classes. For information about request handling and parameter validation, see [Parameter Validation and Handling](#2.3). For error handling mechanisms, see [Error Handling](#2.7).

## Default Response Behavior

FastAPI automatically converts path operation return values into HTTP responses using `JSONResponse` as the default response class. When a path operation function returns data, FastAPI applies the following default behavior:

- **Automatic JSON Conversion**: Return values are serialized to JSON using the `jsonable_encoder`
- **Content-Type Headers**: HTTP headers are automatically set to `application/json`
- **Status Codes**: Default status code is 200, unless explicitly specified
- **Response Model Validation**: If a `response_model` is declared, the return value is validated against it

The default response class can be overridden at the application level or per-route using the `response_class` parameter.

Sources: [fastapi/applications.py:354-373](), [fastapi/routing.py:454-456]()

## Response Serialization Pipeline

### Response Content Preparation

```mermaid
graph TD
    A["Path Operation Return Value"] --> B["_prepare_response_content()"]
    B --> C{"Is BaseModel?"}
    C -->|Yes| D["Check ORM Mode"]
    D --> E{"ORM Mode Enabled?"}
    E -->|Yes| F["Return Model As-Is"]
    E -->|No| G["_model_dump()"]
    C -->|No| H{"Is List?"}
    H -->|Yes| I["Process Each Item Recursively"]
    H -->|No| J{"Is Dict?"}
    J -->|Yes| K["Process Each Value Recursively"]
    J -->|No| L{"Is Dataclass?"}
    L -->|Yes| M["dataclasses.asdict()"]
    L -->|No| N["Return Value As-Is"]
    
    G --> O["Serialized Content"]
    I --> O
    K --> O
    M --> O
    N --> O
    F --> O
```

The `_prepare_response_content` function handles the initial content preparation by recursively processing different data types and applying serialization rules based on the `exclude_unset`, `exclude_defaults`, and `exclude_none` parameters.

Sources: [fastapi/routing.py:80-124]()

### JSON Encoding Process

```mermaid
graph TD
    A["Response Content"] --> B["jsonable_encoder()"]
    B --> C{"Custom Encoder?"}
    C -->|Yes| D["Apply Custom Encoder"]
    C -->|No| E{"Pydantic BaseModel?"}
    E -->|Yes| F["_model_dump()"]
    E -->|No| G{"Dataclass?"}
    G -->|Yes| H["dataclasses.asdict()"]
    G -->|No| I{"Built-in Type?"}
    I -->|Yes| J["Return As-Is"]
    I -->|No| K{"In ENCODERS_BY_TYPE?"}
    K -->|Yes| L["Apply Type Encoder"]
    K -->|No| M["Try dict() or vars()"]
    
    D --> N["JSON-Compatible Output"]
    F --> N
    H --> N
    J --> N
    L --> N
    M --> N
```

The `jsonable_encoder` provides comprehensive type conversion with support for custom encoders, Pydantic models, dataclasses, and various Python built-in types including datetime, UUID, Enum, and Path objects.

Sources: [fastapi/encoders.py:102-343]()

## Response Model Validation

### Response Field Creation

When a path operation declares a `response_model`, FastAPI creates response fields during route initialization:

```mermaid
graph TD
    A["APIRoute.__init__()"] --> B{"response_model specified?"}
    B -->|Yes| C["create_model_field()"]
    C --> D["Create Response Field"]
    D --> E["create_cloned_field()"]
    E --> F["Create Secure Cloned Field"]
    B -->|No| G["Set response_field = None"]
    
    F --> H["Store in route.response_field"]
    G --> H
```

The cloned field ensures that Pydantic submodel inheritance doesn't bypass validation, preventing security issues where a subclass with additional fields might be returned directly.

Sources: [fastapi/routing.py:507-530]()

### Response Validation Process

```mermaid
graph TD
    A["Raw Response Content"] --> B["serialize_response()"]
    B --> C{"Response Field Exists?"}
    C -->|Yes| D["_prepare_response_content()"]
    D --> E["field.validate()"]
    E --> F{"Validation Errors?"}
    F -->|Yes| G["Raise ResponseValidationError"]
    F -->|No| H{"Has field.serialize?"}
    H -->|Yes| I["field.serialize()"]
    H -->|No| J["jsonable_encoder()"]
    C -->|No| K["Direct jsonable_encoder()"]
    
    I --> L["Validated Response Content"]
    J --> L
    K --> L
```

The `serialize_response` function validates response content against the declared response model, ensuring type safety and proper serialization. It handles both Pydantic v1 and v2 compatibility through the `hasattr(field, "serialize")` check.

Sources: [fastapi/routing.py:144-203]()

## Custom Response Classes

### Response Class Hierarchy

FastAPI supports various response classes that inherit from Starlette's `Response`:

| Response Class | Media Type | Use Case |
|----------------|------------|----------|
| `JSONResponse` | `application/json` | Default, automatic JSON serialization |
| `ORJSONResponse` | `application/json` | High-performance JSON with `orjson` |
| `HTMLResponse` | `text/html` | HTML content |
| `PlainTextResponse` | `text/plain` | Plain text responses |
| `RedirectResponse` | N/A | HTTP redirects |
| `FileResponse` | Based on file | File downloads |
| `StreamingResponse` | Custom | Streaming content |

### Custom Response Integration

```mermaid
graph TD
    A["Path Operation"] --> B{"Returns Response Instance?"}
    B -->|Yes| C["Use Response Directly"]
    B -->|No| D["Get response_class from Route"]
    D --> E["Create Response Instance"]
    E --> F["Apply Serialized Content"]
    C --> G["Apply Background Tasks"]
    F --> G
    G --> H["Set Status Code"]
    H --> I["Extend Headers"]
    I --> J["Final HTTP Response"]
```

When a path operation returns a `Response` instance directly, FastAPI bypasses the serialization pipeline. Otherwise, it uses the declared `response_class` to wrap the serialized content.

Sources: [fastapi/routing.py:307-342](), [docs/en/docs/advanced/custom-response.md:1-86]()

## Response Generation Flow

### Complete Request-Response Cycle

```mermaid
sequenceDiagram
    participant Client
    participant "get_request_handler" as Handler
    participant "run_endpoint_function" as Endpoint
    participant "serialize_response" as Serializer
    participant "Response Class" as ResponseClass
    
    Client->>Handler: HTTP Request
    Handler->>Endpoint: Call Path Operation
    Endpoint->>Handler: Return Value
    Handler->>Serializer: Raw Response + Response Field
    Serializer->>Serializer: Validate Against Response Model
    Serializer->>Handler: Serialized Content
    Handler->>ResponseClass: Create Response Instance
    ResponseClass->>Handler: HTTP Response Object
    Handler->>Client: HTTP Response
```

### Response Handler Implementation

The `get_request_handler` function orchestrates the complete response generation process:

1. **Endpoint Execution**: Calls the path operation function via `run_endpoint_function`
2. **Response Type Check**: Determines if return value is already a `Response` instance
3. **Content Serialization**: Applies `serialize_response` with response model validation
4. **Response Construction**: Creates response instance with proper status codes and headers
5. **Background Tasks**: Attaches any background tasks to the response
6. **Body Validation**: Ensures response body is allowed for the status code

Sources: [fastapi/routing.py:241-356]()

### Status Code and Header Management

```mermaid
graph TD
    A["Response Generation"] --> B{"Status Code Set?"}
    B -->|Yes| C["Use Explicit Status Code"]
    B -->|No| D{"Route Status Code?"}
    D -->|Yes| E["Use Route Default"]
    D -->|No| F["Use Response Class Default"]
    
    C --> G["Apply Status Code"]
    E --> G
    F --> G
    G --> H["Check Body Allowed for Status"]
    H --> I{"Body Allowed?"}
    I -->|No| J["Set Empty Body"]
    I -->|Yes| K["Keep Response Body"]
    J --> L["Extend Response Headers"]
    K --> L
```

FastAPI automatically manages status codes based on the hierarchy of explicit parameters, route defaults, and response class defaults. It also validates that response bodies are appropriate for the status code (e.g., no body for 204 No Content).

Sources: [fastapi/routing.py:317-342](), [fastapi/utils.py:42-56]()

# Security Components




This document covers FastAPI's security infrastructure, including authentication schemes (OAuth2, HTTP Basic/Bearer, API Key, OpenID Connect), security dependencies, and permission scopes. For broader API documentation concepts, see [API Documentation System](#3). For error handling in security contexts, see [Error Handling](#2.7).

## Overview

FastAPI provides a comprehensive security system with multiple authentication schemes integrated into the dependency injection framework. The security components handle authentication, authorization, token validation, and scope-based permissions through a collection of base classes, concrete implementations, and utilities that automatically integrate with OpenAPI documentation generation.

## Security Component Architecture

```mermaid
graph TB
    subgraph "Base Classes"
        SecurityBase["SecurityBase"]
    end
    
    subgraph "Authentication Schemes"
        OAuth2["OAuth2"]
        HTTPBase["HTTPBase"]
        HTTPBasic["HTTPBasic"]
        HTTPBearer["HTTPBearer"]
        APIKeyQuery["APIKeyQuery"]
        APIKeyHeader["APIKeyHeader"]
        APIKeyCookie["APIKeyCookie"]
        OpenIdConnect["OpenIdConnect"]
    end
    
    subgraph "Request Models"
        OAuth2PasswordRequestForm["OAuth2PasswordRequestForm"]
        HTTPBasicCredentials["HTTPBasicCredentials"]
        HTTPAuthorizationCredentials["HTTPAuthorizationCredentials"]
    end
    
    subgraph "Security Dependencies"
        SecurityRequirement["SecurityRequirement"]
        SecurityScopes["SecurityScopes"]
        SecurityParam["params.Security()"]
    end
    
    subgraph "OpenAPI Integration"
        OpenAPISecurityDef["get_openapi_security_definitions()"]
        SecuritySchemes["securitySchemes"]
    end
    
    SecurityBase --> OAuth2
    SecurityBase --> HTTPBase
    SecurityBase --> APIKeyQuery
    SecurityBase --> APIKeyHeader  
    SecurityBase --> APIKeyCookie
    SecurityBase --> OpenIdConnect
    HTTPBase --> HTTPBasic
    HTTPBase --> HTTPBearer
    
    OAuth2 --> OAuth2PasswordRequestForm
    HTTPBasic --> HTTPBasicCredentials
    HTTPBearer --> HTTPAuthorizationCredentials
    
    SecurityParam --> SecurityRequirement
    SecurityRequirement --> SecurityScopes
    
    SecurityBase --> OpenAPISecurityDef
    OpenAPISecurityDef --> SecuritySchemes
```

Sources: [fastapi/security/base.py](), [fastapi/security/oauth2.py:308-441](), [fastapi/security/http.py:69-340](), [fastapi/security/api_key.py](), [fastapi/dependencies/models.py:8-12](), [fastapi/openapi/utils.py:78-92]()

## Base Security Classes

### SecurityBase

The `SecurityBase` class serves as the foundation for all security schemes in FastAPI. It provides the basic interface that all authentication mechanisms inherit from and ensures consistent integration with the dependency injection system.

Sources: [fastapi/security/base.py]()

### SecurityRequirement

The `SecurityRequirement` dataclass represents security requirements for operations, containing a reference to the security scheme and any required scopes:

| Field | Type | Description |
|-------|------|-------------|
| `security_scheme` | `SecurityBase` | The security scheme instance |
| `scopes` | `Optional[Sequence[str]]` | Required permission scopes |

Sources: [fastapi/dependencies/models.py:8-12]()

## Authentication Schemes

### OAuth2 Components

#### OAuth2

The `OAuth2` class implements OAuth2 authentication flows. It accepts flow configurations and integrates with OpenAPI documentation generation.

```mermaid
graph TB
    OAuth2Class["OAuth2"]
    OAuthFlowsModel["OAuthFlowsModel"]
    OAuth2Model["OAuth2Model"]
    CallMethod["__call__(request: Request)"]
    AuthHeader["request.headers.get('Authorization')"]
    
    OAuth2Class --> OAuthFlowsModel
    OAuth2Class --> OAuth2Model
    OAuth2Class --> CallMethod
    CallMethod --> AuthHeader
```

Key initialization parameters:
- `flows` - OAuth2 flow definitions (`OAuthFlowsModel`)
- `scheme_name` - Security scheme name for OpenAPI
- `description` - Security scheme description
- `auto_error` - Whether to automatically raise errors for missing auth

Sources: [fastapi/security/oauth2.py:308-441]()

#### OAuth2PasswordRequestForm

The `OAuth2PasswordRequestForm` class handles login form data according to OAuth2 password flow specifications:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | `str` | Yes | User identifier |
| `password` | `str` | Yes | User password |
| `scope` | `str` | No | Space-separated scopes |
| `grant_type` | `str` | No | OAuth2 grant type |
| `client_id` | `str` | No | OAuth2 client ID |
| `client_secret` | `str` | No | OAuth2 client secret |

The form data is automatically parsed from request form fields and made available as a dependency.

Sources: [fastapi/security/oauth2.py:16-149]()

### HTTP Authentication Components

#### HTTPBasic

The `HTTPBasic` class implements HTTP Basic authentication, extracting and validating Base64-encoded credentials from the `Authorization` header.

```mermaid
graph LR
    HTTPBasicAuth["HTTPBasic"]
    AuthHeader["Authorization: Basic <base64>"]
    Base64Decode["b64decode()"]
    HTTPBasicCredentials["HTTPBasicCredentials"]
    UsernamePassword["username:password"]
    
    AuthHeader --> HTTPBasicAuth
    HTTPBasicAuth --> Base64Decode
    Base64Decode --> UsernamePassword
    UsernamePassword --> HTTPBasicCredentials
```

Returns `HTTPBasicCredentials` containing `username` and `password` fields.

Sources: [fastapi/security/http.py:97-217]()

#### HTTPBearer

The `HTTPBearer` class implements HTTP Bearer token authentication, extracting tokens from the `Authorization` header.

Returns `HTTPAuthorizationCredentials` containing:
- `scheme` - The authorization scheme (e.g., "Bearer")
- `credentials` - The token value

Sources: [fastapi/security/http.py:220-340]()

### API Key Authentication

FastAPI provides three API key authentication classes for different token locations:

| Class | Token Location | Usage |
|-------|----------------|--------|
| `APIKeyQuery` | Query parameter | `?api_key=token` |
| `APIKeyHeader` | HTTP header | `X-API-Key: token` |
| `APIKeyCookie` | HTTP cookie | `Cookie: api_key=token` |

All API key classes inherit from `APIKeyBase` and return the extracted key value as a string.

Sources: [fastapi/security/api_key.py:23-237]()

### OpenID Connect

The `OpenIdConnect` class implements OpenID Connect authentication with a configurable OpenID Connect URL.

Key parameter:
- `openIdConnectUrl` - The OpenID Connect discovery endpoint URL

Sources: [fastapi/security/open_id_connect_url.py:11-77]()

## Security Dependency Integration

### Dependency Resolution Flow

```mermaid
graph TB
    APIRoute["APIRoute"]
    Dependant["Dependant"]
    SecurityParams["params.Security()"]
    SecurityRequirement["SecurityRequirement"]
    SecurityScopes["SecurityScopes"]
    
    GetSubDependant["get_sub_dependant()"]
    SolveDependencies["solve_dependencies()"]
    SecurityBase["SecurityBase instance"]
    
    APIRoute --> Dependant
    SecurityParams --> GetSubDependant
    GetSubDependant --> SecurityRequirement
    SecurityRequirement --> Dependant
    Dependant --> SolveDependencies
    SolveDependencies --> SecurityScopes
    SecurityBase --> SecurityRequirement
```

The dependency system processes security components through several key functions:

1. **`get_sub_dependant()`** - Creates `SecurityRequirement` objects from `params.Security` annotations
2. **`solve_dependencies()`** - Resolves security dependencies and populates `SecurityScopes`
3. **Security scheme `__call__`** - Executes authentication logic during request processing

Sources: [fastapi/dependencies/utils.py:142-171](), [fastapi/routing.py:292-298]()

### SecurityScopes Integration

The `SecurityScopes` class aggregates all security scopes required by a request's dependency tree. It is automatically injected when security dependencies are present:

```mermaid
graph LR
    SecurityDep["Security(get_user, scopes=['read'])"]
    SecurityScopes["SecurityScopes"]
    UserFunc["get_user(security_scopes: SecurityScopes)"]
    ScopeValidation["validate required scopes"]
    
    SecurityDep --> SecurityScopes
    SecurityScopes --> UserFunc
    UserFunc --> ScopeValidation
```

Key attributes:
- `scopes` - List of all required scope strings
- `scope_str` - Space-separated scope string for WWW-Authenticate headers

Sources: [fastapi/security/oauth2.py:57](), [fastapi/dependencies/utils.py:685-687]()

## OpenAPI Security Documentation

### Security Schema Generation

FastAPI automatically generates OpenAPI security schemas through the `get_openapi_security_definitions()` function:

```mermaid
graph TB
    FlatDependant["get_flat_dependant()"]
    SecurityRequirements["security_requirements"]
    SecurityScheme["security_requirement.security_scheme"]
    JSONEncoder["jsonable_encoder()"]
    SecurityDefinitions["security_definitions"]
    OperationSecurity["operation_security"]
    
    FlatDependant --> SecurityRequirements
    SecurityRequirements --> SecurityScheme
    SecurityScheme --> JSONEncoder
    JSONEncoder --> SecurityDefinitions
    SecurityRequirements --> OperationSecurity
```

The function processes security requirements to generate:
- **Security Definitions**: OpenAPI security scheme objects
- **Operation Security**: Per-operation security requirements with scopes

Sources: [fastapi/openapi/utils.py:78-92]()

### Security Schema Integration

Security schemes are integrated into the OpenAPI specification through several key areas:

| OpenAPI Section | Content | Source |
|----------------|---------|---------|
| `components.securitySchemes` | Security scheme definitions | Security scheme `model` attributes |
| `paths.{path}.{method}.security` | Per-operation security requirements | `SecurityRequirement.scopes` |
| `paths.{path}.{method}.parameters` | Security parameters (API keys) | Parameter extraction logic |

The integration ensures that interactive documentation (Swagger UI, ReDoc) displays proper authentication interfaces and security requirements.

Sources: [fastapi/openapi/utils.py:282-288](), [fastapi/openapi/utils.py:534-537]()

## Token Validation Pipeline

```mermaid
graph TB
    Request["HTTP Request"]
    BearerExtract["OAuth2PasswordBearer"]
    TokenPresent{"Token Present?"}
    JWTDecode["JWT decode & verify"]
    ScopeExtract["Extract token scopes"]
    UserLookup["Database user lookup"]
    ScopeValidation["SecurityScopes validation"]
    UserActive{"User Active?"}
    AuthenticatedUser["Authenticated User"]
    
    HTTPException401["HTTPException(401, 'Not authenticated')"]
    HTTPException403["HTTPException(403, 'Insufficient permissions')"]
    HTTPExceptionInactive["HTTPException(400, 'Inactive user')"]
    
    Request --> BearerExtract
    BearerExtract --> TokenPresent
    TokenPresent -->|No| HTTPException401
    TokenPresent -->|Yes| JWTDecode
    JWTDecode --> ScopeExtract
    ScopeExtract --> UserLookup
    UserLookup --> ScopeValidation
    ScopeValidation -->|Fail| HTTPException403
    ScopeValidation -->|Pass| UserActive
    UserActive -->|No| HTTPExceptionInactive
    UserActive -->|Yes| AuthenticatedUser
    
    style BearerExtract fill:#f9f9f9
    style ScopeValidation fill:#f9f9f9
```

The token validation pipeline processes authentication through multiple stages:

1. **Token Extraction**: `OAuth2PasswordBearer` extracts Bearer token from Authorization header
2. **Token Validation**: Decode and verify JWT signature and expiration
3. **Scope Extraction**: Parse scopes from token payload
4. **User Resolution**: Look up user details from token subject
5. **Scope Authorization**: Validate token scopes against required scopes via `SecurityScopes`
6. **User Status**: Verify user account is active and permitted

Sources: [docs/en/docs/tutorial/security/oauth2-jwt.md:158-166](), [docs/en/docs/advanced/security/oauth2-scopes.md:155-192]()

## Integration with Dependency Injection

Security components integrate seamlessly with FastAPI's dependency injection system through several mechanisms:

| Component | Integration Method | Purpose |
|-----------|-------------------|---------|
| `OAuth2PasswordBearer` | `Depends()` | Token extraction and validation |
| `OAuth2PasswordRequestForm` | `Depends()` | Login form parsing |
| `Security()` | Dependency decorator | Scope-aware authorization |
| `SecurityScopes` | Dependency parameter | Scope aggregation and validation |

```mermaid
graph LR
    PathOperation["@app.get('/protected')"]
    SecurityDep["Security(get_current_user, scopes=['read'])"]
    GetCurrentUser["get_current_user(security_scopes, token=Depends(oauth2_scheme))"]
    OAuth2Scheme["oauth2_scheme: OAuth2PasswordBearer"]
    SecurityScopesParam["security_scopes: SecurityScopes"]
    
    PathOperation --> SecurityDep
    SecurityDep --> GetCurrentUser
    GetCurrentUser --> OAuth2Scheme
    GetCurrentUser --> SecurityScopesParam
    
    style SecurityDep fill:#f9f9f9
    style OAuth2Scheme fill:#f9f9f9
```

The dependency system automatically:
- Injects `SecurityScopes` with aggregated scope requirements
- Resolves `OAuth2PasswordBearer` to extract and return tokens
- Validates dependency chains for proper security configuration
- Documents security requirements in OpenAPI schema

Sources: [docs/en/docs/advanced/security/oauth2-scopes.md:194-234](), [fastapi/__init__.py:20]()

## OpenAPI Security Documentation

FastAPI automatically generates OpenAPI security documentation from security components:

```mermaid
graph TB
    SecurityScheme["OAuth2PasswordBearer(tokenUrl='/token', scopes={'read': 'Read access'})"]
    OpenAPIDoc["OpenAPI Security Scheme"]
    SwaggerUI["Interactive Docs UI"]
    AuthorizeButton["'Authorize' Button"]
    ScopeSelection["Scope Selection UI"]
    
    SecurityScheme --> OpenAPIDoc
    OpenAPIDoc --> SwaggerUI
    SwaggerUI --> AuthorizeButton
    AuthorizeButton --> ScopeSelection
    
    style SecurityScheme fill:#f9f9f9
    style OpenAPIDoc fill:#f9f9f9
```

The security documentation includes:
- OAuth2 flow definitions and token URLs
- Available scopes with descriptions
- Security requirements for each endpoint
- Interactive authentication forms in documentation UI

Sources: [docs/en/docs/tutorial/security/first-steps.md:177-185](), [docs/en/docs/advanced/security/oauth2-scopes.md:76-83]()