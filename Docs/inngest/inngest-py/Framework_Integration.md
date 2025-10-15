## Purpose and Scope

This document covers the framework integration system that enables Inngest functions to be served through various Python web frameworks. The integration layer provides a unified interface for handling HTTP requests from the Inngest server while adapting to framework-specific patterns and conventions.

For information about the core Inngest client and function definition, see [Core API](#3). For details about the underlying communication protocol and request handling, the relevant components are covered in [System Components](#2.3).

## Architecture Overview

The framework integration system follows a common adapter pattern where each supported framework implements a `serve()` function that creates framework-specific HTTP handlers while delegating core logic to a shared `CommHandler`.

### Framework Integration Architecture

```mermaid
graph TB
    subgraph "User Application"
        UA["User App"]
        WF["Web Framework<br/>(Flask/Django/FastAPI/etc)"]
    end
    
    subgraph "Framework Adapters"
        FA["flask.serve()"]
        DA["django.serve()"]
        FFA["fast_api.serve()"]
        TA["tornado.serve()"]
        DOA["digital_ocean.serve()"]
    end
    
    subgraph "Shared Communication Layer"
        CH["CommHandler"]
        CR["CommRequest"]
        CRE["CommResponse"]
    end
    
    subgraph "Core Inngest"
        IC["Inngest Client"]
        FN["Functions"]
    end
    
    UA --> WF
    WF --> FA
    WF --> DA  
    WF --> FFA
    WF --> TA
    WF --> DOA
    
    FA --> CH
    DA --> CH
    FFA --> CH
    TA --> CH
    DOA --> CH
    
    CH --> CR
    CH --> CRE
    CH --> IC
    IC --> FN
```

**Sources:** [pkg/inngest/inngest/flask.py:20-27](), [pkg/inngest/inngest/django.py:27-33](), [pkg/inngest/inngest/fast_api.py:21-29](), [pkg/inngest/inngest/tornado.py:21-28](), [pkg/inngest/inngest/digital_ocean.py:24-30](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:32-40]()

## Supported Frameworks

The SDK provides native integration for five Python web frameworks, each implementing the same core interface with framework-specific adaptations.

### Framework Implementations

| Framework | Module | Async Support | Streaming Support |
|-----------|---------|---------------|-------------------|
| Flask | `inngest.flask` | Yes | No |
| Django | `inngest.django` | Yes (Django 5+) | No |
| FastAPI | `inngest.fast_api` | Yes | Yes |
| Tornado | `inngest.tornado` | No | No |
| DigitalOcean Functions | `inngest.digital_ocean` | No | No |

**Sources:** [pkg/inngest/inngest/flask.py:17](), [pkg/inngest/inngest/django.py:24](), [pkg/inngest/inngest/fast_api.py:18](), [pkg/inngest/inngest/tornado.py:18](), [pkg/inngest/inngest/digital_ocean.py:21]()

### Common Serve Function Pattern

All framework integrations follow the same `serve()` function signature:

```python
def serve(
    app_or_client: FrameworkApp | client_lib.Inngest,
    client_or_functions: client_lib.Inngest | list[function.Function],
    functions: list[function.Function] | None = None,
    *,
    serve_origin: Optional[str] = None,
    serve_path: Optional[str] = None,
) -> FrameworkSpecificReturn
```

**Sources:** [pkg/inngest/inngest/flask.py:20-27](), [pkg/inngest/inngest/django.py:27-33](), [pkg/inngest/inngest/fast_api.py:21-29]()

## CommHandler: The Core Communication Layer

The `CommHandler` class serves as the central communication hub that processes all HTTP requests from the Inngest server regardless of the originating framework.

### CommHandler Request Processing Flow

```mermaid
sequenceDiagram
    participant Framework as "Framework Adapter"
    participant CH as "CommHandler"
    participant IC as "Inngest Client"
    participant FN as "Function"
    
    Framework->>CH: "CommRequest"
    
    alt GET Request
        CH->>CH: "get_sync()"
        CH->>IC: "build inspection response"
        IC-->>CH: "app metadata"
        CH-->>Framework: "CommResponse"
    end
    
    alt POST Request
        CH->>CH: "post() or post_sync()"
        CH->>CH: "parse_query_params()"
        CH->>CH: "_get_function(fn_id)"
        CH->>FN: "fn.call() or fn.call_sync()"
        FN-->>CH: "CallResult"
        CH->>CH: "CommResponse.from_call_result()"
        CH-->>Framework: "CommResponse"
    end
    
    alt PUT Request
        CH->>CH: "put() or put_sync()"
        CH->>CH: "Syncer.out_of_band()"
        CH->>IC: "register functions"
        IC-->>CH: "registration result"
        CH-->>Framework: "CommResponse"
    end
```

**Sources:** [pkg/inngest/inngest/_internal/comm_lib/handler.py:101-244](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:246-339](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:404-433]()

### CommHandler Key Methods

The `CommHandler` class provides both async and sync versions of HTTP method handlers:

- `post()` / `post_sync()` - Execute Inngest functions
- `get_sync()` - Handle inspection requests (function discovery)
- `put()` / `put_sync()` - Handle function registration/synchronization

**Sources:** [pkg/inngest/inngest/_internal/comm_lib/handler.py:101](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:246](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:366](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:404](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:435]()

## Request/Response Model

The communication layer uses standardized request and response models that abstract away framework-specific HTTP handling.

### CommRequest and CommResponse Structure

```mermaid
classDiagram
    class CommRequest {
        +bytes body
        +dict headers
        +bool is_connect
        +dict query_params
        +object raw_request
        +str request_url
        +Optional[str] serve_origin
        +Optional[str] serve_path
    }
    
    class CommResponse {
        +object body
        +dict headers
        +int status_code
        +Optional[Callable] stream
        +bool no_retry
        +Optional[int] request_version
        +Optional[str] retry_after
        +Optional[str] sdk_version
        +from_call_result() CommResponse
        +from_error() CommResponse
        +create_streaming() CommResponse
    }
    
    CommRequest --> CommResponse : "processed by CommHandler"
```

**Sources:** [pkg/inngest/inngest/_internal/comm_lib/models.py:18-30](), [pkg/inngest/inngest/_internal/comm_lib/models.py:32-47]()

## Framework-Specific Implementation Details

### Flask Integration

Flask integration supports both sync and async modes, automatically detecting the mode based on function signatures.

```python