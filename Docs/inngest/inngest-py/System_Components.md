This document provides an overview of the major system components within the Inngest Python SDK, detailing their architecture, interactions, and implementation. It covers the core communication layer, framework integration adapters, step execution engine, and supporting infrastructure that enables event-driven workflow orchestration.

For information about the overall package organization, see [Package Structure](#2.1). For details on framework-specific integration patterns, see [Framework Integration](#4).

## Core Communication System

The communication system forms the backbone of the Inngest SDK, handling HTTP requests from the Inngest server and routing them to appropriate handlers. The system is built around three key components that work together to process incoming requests and generate responses.

### Communication Flow Architecture

```mermaid
graph TB
    subgraph "HTTP Layer"
        FR["Framework Request<br/>(Flask/Django/FastAPI/etc)"]
        FREQ["Framework Response"]
    end
    
    subgraph "Communication Layer"
        CR["CommRequest"]
        CH["CommHandler"]
        CRES["CommResponse"]
    end
    
    subgraph "Request Processing"
        QP["parse_query_params()"]
        WH["wrap_handler()"]
        WHS["wrap_handler_sync()"]
    end
    
    subgraph "Handler Methods"
        GET["get_sync()"]
        POST["post() / post_sync()"]
        PUT["put() / put_sync()"]
    end
    
    subgraph "Core Processing"
        FN["Function Resolution"]
        EX["Function Execution"]
        MW["Middleware Processing"]
    end
    
    FR --> CR
    CR --> QP
    QP --> WH
    QP --> WHS
    WH --> CH
    WHS --> CH
    CH --> GET
    CH --> POST
    CH --> PUT
    GET --> FN
    POST --> FN
    PUT --> FN
    FN --> MW
    MW --> EX
    EX --> CRES
    CRES --> FREQ
```

Sources: [pkg/inngest/inngest/_internal/comm_lib/handler.py:32-465](), [pkg/inngest/inngest/_internal/comm_lib/models.py:18-31](), [pkg/inngest/inngest/_internal/comm_lib/utils.py]()

### CommHandler Class

The `CommHandler` class serves as the central request processor, implementing both synchronous and asynchronous execution patterns. It manages function resolution, middleware execution, and response generation.

| Property | Type | Purpose |
|----------|------|---------|
| `_client` | `client_lib.Inngest` | Reference to the Inngest client instance |
| `_fns` | `dict[str, function.Function]` | Registered functions indexed by ID |
| `_framework` | `server_lib.Framework` | Target web framework type |
| `_mode` | `server_lib.ServerKind` | Execution mode (dev/production) |
| `_thread_pool` | `ThreadPoolExecutor` | Thread pool for sync function execution |

The handler supports three HTTP methods:
- **GET**: Function inspection and discovery ([handler.py:366-402]())
- **POST**: Function execution ([handler.py:102-244]())
- **PUT**: Function registration and synchronization ([handler.py:405-433]())

Sources: [pkg/inngest/inngest/_internal/comm_lib/handler.py:41-100]()

### Request and Response Models

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
        +from_call_result()$
        +from_error()$
        +create_streaming()$
        +sign()
    }
    
    class ErrorData {
        +ErrorCode code
        +str message
        +str name
        +Optional[str] stack
        +from_error()$
    }
    
    CommResponse --> ErrorData : uses
```

Sources: [pkg/inngest/inngest/_internal/comm_lib/models.py:18-46](), [pkg/inngest/inngest/_internal/comm_lib/models.py:342-366]()

## Framework Integration Layer

The framework integration layer provides adapters that bridge web frameworks with the core communication system. Each adapter implements framework-specific request handling while maintaining a consistent interface to the underlying SDK.

### Framework Adapter Architecture

```mermaid
graph LR
    subgraph "Web Frameworks"
        FLASK["Flask<br/>flask.Flask"]
        DJANGO["Django<br/>django.http.HttpRequest"]
        FASTAPI["FastAPI<br/>fastapi.Request"]
        TORNADO["Tornado<br/>tornado.web.RequestHandler"]
        DO["DigitalOcean<br/>Function Event"]
    end
    
    subgraph "Framework Adapters"
        FA["flask.serve()"]
        DA["django.serve()"]
        FFA["fast_api.serve()"]
        TA["tornado.serve()"]
        DOA["digital_ocean.serve()"]
    end
    
    subgraph "Communication Layer"
        CR["CommRequest"]
        CH["CommHandler"]
    end
    
    FLASK --> FA
    DJANGO --> DA
    FASTAPI --> FFA
    TORNADO --> TA
    DO --> DOA
    
    FA --> CR
    DA --> CR
    FFA --> CR
    TA --> CR
    DOA --> CR
    
    CR --> CH
```

Sources: [pkg/inngest/inngest/flask.py:20-68](), [pkg/inngest/inngest/django.py:27-73](), [pkg/inngest/inngest/fast_api.py:21-49](), [pkg/inngest/inngest/tornado.py:21-47](), [pkg/inngest/inngest/digital_ocean.py:24-48]()

### Framework-Specific Implementations

Each framework adapter implements the `serve()` function with framework-specific characteristics:

| Framework | Async Support | Streaming Support | Handler Pattern |
|-----------|---------------|-------------------|-----------------|
| Flask | Mixed (auto-detect) | No | Route decorator |
| Django | Mixed (version-based) | No | URL pattern |
| FastAPI | Full | Yes | Route decorator |
| Tornado | Sync only | No | Request handler class |
| DigitalOcean | Sync only | No | Function wrapper |

The adapters handle:
- Request parsing and normalization
- Response formatting and serialization
- Framework-specific routing and middleware
- Async/sync execution mode detection

Sources: [pkg/inngest/inngest/flask.py:48-68](), [pkg/inngest/inngest/django.py:54-73](), [pkg/inngest/inngest/fast_api.py:44-49]()

## Step Execution Engine

The step execution engine manages the execution of individual steps within Inngest functions, providing memoization, error handling, and flow control capabilities.

### Step Execution Components

```mermaid
graph TB
    subgraph "Step Interfaces"
        STEP["Step<br/>(Async)"]
        STEPS["StepSync<br/>(Sync)"]
        STEPBASE["StepBase<br/>(Common Logic)"]
    end
    
    subgraph "Step Operations"
        RUN["step.run()"]
        INVOKE["step.invoke()"]
        SEND["step.send_event()"]
        SLEEP["step.sleep()"]
        WAIT["step.wait_for_event()"]
    end
    
    subgraph "State Management"
        MEMOS["StepMemos<br/>(Output Caching)"]
        COUNTER["StepIDCounter<br/>(ID Management)"]
        OUTPUT["Output<br/>(Data + Error)"]
    end
    
    subgraph "Flow Control"
        RESP_INT["ResponseInterrupt"]
        SKIP_INT["SkipInterrupt"]
        NESTED_INT["NestedStepInterrupt"]
    end
    
    STEPBASE --> STEP
    STEPBASE --> STEPS
    
    STEP --> RUN
    STEP --> INVOKE
    STEP --> SEND
    STEP --> SLEEP
    STEP --> WAIT
    
    STEPS --> RUN
    STEPS --> INVOKE
    STEPS --> SEND
    STEPS --> SLEEP
    STEPS --> WAIT
    
    RUN --> MEMOS
    INVOKE --> MEMOS
    MEMOS --> OUTPUT
    MEMOS --> COUNTER
    
    RUN --> RESP_INT
    RUN --> SKIP_INT
    RUN --> NESTED_INT
```

Sources: [pkg/inngest/inngest/_internal/step_lib/__init__.py](), [pkg/inngest/inngest/_internal/execution_lib.py]()

### Execution Context Management

The execution system maintains context information throughout function execution:

```mermaid
classDiagram
    class Context {
        +int attempt
        +Event event
        +list events
        +Group group
        +Logger logger
        +str run_id
        +Step step
    }
    
    class ContextSync {
        +int attempt
        +Event event
        +list events
        +GroupSync group
        +Logger logger
        +str run_id
        +StepSync step
    }
    
    class ExecutionV0 {
        +StepMemos memos
        +MiddlewareManager middleware
        +ServerRequest request
        +Optional[str] target_hashed_id
    }
    
    class ExecutionV0Sync {
        +StepMemos memos
        +MiddlewareManager middleware
        +ServerRequest request
        +Optional[str] target_hashed_id
    }
    
    Context --> ExecutionV0 : uses
    ContextSync --> ExecutionV0Sync : uses
```

Sources: [pkg/inngest/inngest/_internal/execution_lib.py]()

## Client and Function Management

The client system manages Inngest configuration, function registration, and event communication with external services.

### Client Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        CLIENT["Inngest<br/>client_lib.Inngest"]
        CONFIG["Client Configuration<br/>app_id, signing_key, etc"]
    end
    
    subgraph "Function Management"
        FUNC["Function<br/>function.Function"]
        FCONFIG["FunctionConfig<br/>Registration Data"]
        DECORATOR["create_function<br/>Decorator"]
    end
    
    subgraph "Event System"
        EVENT["Event<br/>server_lib.Event"]
        SEND["send() / send_sync()"]
        BATCH["SendEventsResult"]
    end
    
    subgraph "Communication"
        HTTP_CLIENT["httpx.AsyncClient"]
        HTTP_CLIENT_SYNC["httpx.Client"]
        API_CALLS["API Communication"]
    end
    
    CLIENT --> CONFIG
    CLIENT --> DECORATOR
    DECORATOR --> FUNC
    FUNC --> FCONFIG
    
    CLIENT --> SEND
    SEND --> EVENT
    SEND --> BATCH
    
    CLIENT --> HTTP_CLIENT
    CLIENT --> HTTP_CLIENT_SYNC
    HTTP_CLIENT --> API_CALLS
    HTTP_CLIENT_SYNC --> API_CALLS
```

Sources: [pkg/inngest/inngest/_internal/client_lib.py](), [pkg/inngest/inngest/_internal/function.py](), [pkg/inngest/inngest/__init__.py:3-60]()

### Function Registration Process

The function registration process involves several stages:

1. **Function Definition**: Using the `@client.create_function()` decorator
2. **Configuration Generation**: Creating `FunctionConfig` objects
3. **Registration**: Synchronizing with Inngest server via PUT requests
4. **Execution**: Handling incoming POST requests for function execution

Sources: [pkg/inngest/inngest/_internal/comm_lib/handler.py:405-465](), [pkg/inngest/inngest/_internal/comm_lib/handler.py:763-777]()

## Middleware System

The middleware system provides hooks for intercepting and modifying function execution at various stages.

### Middleware Processing Flow

```mermaid
sequenceDiagram
    participant CLIENT as "Inngest Client"
    participant MM as "MiddlewareManager"
    participant MW as "Middleware"
    participant FUNC as "Function"
    
    CLIENT->>MM: from_client()
    MM->>MW: before_execution()
    MW->>MM: transform_input()
    MM->>FUNC: execute()
    FUNC->>MM: result
    MM->>MW: after_execution()
    MW->>MM: transform_output()
    MM->>CLIENT: final_result
```

Sources: [pkg/inngest/inngest/_internal/middleware_lib.py]()

## Development and Testing Infrastructure

The SDK includes comprehensive development and testing infrastructure to support local development, CI/CD, and integration testing.

### Development Tools Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DEV_SERVER["Dev Server<br/>inngest-cli"]
        DEV_CLIENT["Dev Server Client<br/>GraphQL API"]
        CMD_RUNNER["CommandRunner<br/>Process Management"]
    end
    
    subgraph "Testing Framework"
        PYTEST["pytest Framework"]
        TEST_CONFIG["Test Configuration<br/>conftest.py"]
        TEST_CASES["Test Cases<br/>Unit & Integration"]
    end
    
    subgraph "Build System"
        MAKEFILE["Makefile<br/>Build Scripts"]
        CONSTRAINTS["constraints.txt<br/>Dependency Pins"]
        PYPROJECT["pyproject.toml<br/>Package Config"]
    end
    
    subgraph "Quality Assurance"
        RUFF["ruff<br/>Linting & Formatting"]
        MYPY["mypy<br/>Type Checking"]
        PRE_COMMIT["Pre-commit Hooks"]
    end
    
    DEV_SERVER --> DEV_CLIENT
    CMD_RUNNER --> DEV_SERVER
    
    PYTEST --> TEST_CONFIG
    TEST_CONFIG --> TEST_CASES
    
    MAKEFILE --> RUFF
    MAKEFILE --> MYPY
    MAKEFILE --> PYTEST
    MAKEFILE --> PRE_COMMIT
    
    PYPROJECT --> CONSTRAINTS
```

Sources: [pkg/inngest/inngest/experimental/dev_server/command_runner.py:13-133](), [Makefile:1-43](), [CONTRIBUTING.md:78-91]()

### Package Organization

The system is organized into multiple packages with clear separation of concerns:

| Package | Purpose |
|---------|---------|
| `pkg/inngest` | Main SDK package with core functionality |
| `pkg/inngest_encryption` | Encryption utilities and extensions |
| `pkg/test_core` | Shared testing infrastructure |
| `examples/` | Framework-specific example applications |

Sources: [Makefile:13-19](), [CONTRIBUTING.md:1-77]()

The modular architecture enables independent development, testing, and deployment of different SDK components while maintaining consistent interfaces and behavior across all supported frameworks.