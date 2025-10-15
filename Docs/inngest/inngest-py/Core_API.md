This document provides a comprehensive overview of the main user-facing APIs in the Inngest Python SDK. The Core API encompasses the essential classes and methods developers use to create event-driven functions, manage execution flow, and interact with the Inngest platform.

The Core API consists of four primary components: the Inngest client for initialization and configuration, function definition and registration, step-based execution control, and event sending/handling. For detailed information about framework-specific integration, see [Framework Integration](#4). For advanced middleware functionality, see [Middleware System](#5).

```mermaid
graph TB
    subgraph "Core API Components"
        IC["Inngest Client<br/>(inngest.Inngest)"]
        CF["create_function<br/>decorator"]
        F["Function<br/>execution"]
        S["Step System<br/>(step.run, step.invoke)"]
        E["Event System<br/>(send, Event)"]
    end
    
    subgraph "User Code"
        UC["User Function<br/>Handler"]
        UE["User Events<br/>& Data"]
    end
    
    subgraph "Configuration Objects"
        FO["FunctionOpts"]
        TC["TriggerCron"]
        TE["TriggerEvent"]
        B["Batch"]
        RT["RateLimit"]
        TH["Throttle"]
    end
    
    IC --> CF
    CF --> F
    F --> UC
    F --> S
    IC --> E
    E --> UE
    
    CF --> FO
    CF --> TC
    CF --> TE
    FO --> B
    FO --> RT
    FO --> TH
    
    S --> UC
    UC --> S
    
    style IC fill:#f9f9f9,stroke:#333,stroke-width:2px
    style F fill:#f9f9f9,stroke:#333,stroke-width:2px
    style S fill:#f9f9f9,stroke:#333,stroke-width:2px
    style E fill:#f9f9f9,stroke:#333,stroke-width:2px
```

**Core API Architecture Overview**

Sources: [README.md:24-207](), [pkg/inngest/inngest/_internal/client_lib/client.py:41-301](), [pkg/inngest/inngest/_internal/function.py:65-350]()

## API Surface and Entry Points

The Core API provides a clean, decorator-based interface that follows Python conventions. The main entry point is the `Inngest` client class, which serves as both a configuration container and function factory.

```mermaid
graph LR
    subgraph "Primary API Classes"
        Inngest["inngest.Inngest<br/>Client Class"]
        Function["inngest.Function<br/>Internal Representation"]
        Context["inngest.Context<br/>Execution Context"]
        Step["inngest.Step<br/>Execution Control"]
        Event["inngest.Event<br/>Data Structure"]
    end
    
    subgraph "Decorator Pattern"
        createFunction["@client.create_function()"]
        userHandler["def my_function(ctx, step)"]
    end
    
    subgraph "Configuration Types"
        TriggerEvent["inngest.TriggerEvent"]
        TriggerCron["inngest.TriggerCron"]
        Batch["inngest.Batch"]
        Cancel["inngest.Cancel"]
    end
    
    Inngest --> createFunction
    createFunction --> Function
    createFunction --> TriggerEvent
    createFunction --> TriggerCron
    Function --> userHandler
    userHandler --> Context
    userHandler --> Step
    
    Inngest --> Event
    
    TriggerEvent --> Function
    TriggerCron --> Function
    Batch --> Function
    Cancel --> Function
```

**API Entry Points and Decorator Pattern**

The API design follows a fluent interface pattern where the `Inngest` client creates function decorators that return configured `Function` objects. This provides type safety and clear separation of concerns.

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:205-301](), [pkg/inngest/inngest/_internal/function.py:107-129]()

## Client Initialization and Configuration

The `Inngest` client class serves as the primary configuration point and factory for creating functions. It manages authentication, server endpoints, and global settings that apply to all functions created by that client instance.

| Parameter | Type | Purpose |
|-----------|------|---------|
| `app_id` | `str` | Unique identifier for the application |
| `is_production` | `bool` | Controls server endpoint and security settings |
| `api_base_url` | `str` | Custom Inngest API endpoint |
| `event_api_base_url` | `str` | Custom event API endpoint |
| `event_key` | `str` | Authentication key for event sending |
| `signing_key` | `str` | Request signature verification key |
| `middleware` | `list` | Global middleware applied to all functions |

```mermaid
sequenceDiagram
    participant User as "User Code"
    participant Client as "Inngest Client"
    participant Config as "Configuration"
    participant HTTP as "HTTP Client"
    
    User->>Client: "inngest.Inngest(app_id='my-app')"
    Client->>Config: "Load environment variables"
    Client->>Config: "Validate configuration"
    Client->>HTTP: "Initialize HTTP clients"
    Client-->>User: "Configured client instance"
    
    User->>Client: "@client.create_function(...)"
    Client->>Client: "Create function decorator"
    Client-->>User: "Function decorator"
    
    User->>Client: "client.send(event)"
    Client->>HTTP: "POST to event API"
    HTTP-->>Client: "Response"
    Client-->>User: "Event IDs"
```

**Client Initialization Flow**

The client initialization process loads configuration from multiple sources including constructor arguments, environment variables, and defaults. It establishes both synchronous and asynchronous HTTP clients for different use cases.

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:68-153](), [pkg/inngest/inngest/_internal/client_lib/client.py:614-636]()

## Function Definition System

Functions are defined using the `create_function` decorator, which accepts configuration parameters and returns a decorator that can be applied to user-defined handler functions. The system supports both synchronous and asynchronous handlers.

```mermaid
graph TD
    subgraph "Function Configuration"
        fnId["fn_id: str<br/>Unique function identifier"]
        name["name: str<br/>Human-readable name"]
        trigger["trigger: Union[TriggerEvent, TriggerCron]<br/>Execution trigger"]
        retries["retries: int<br/>Retry attempts"]
        timeout["timeouts: Timeouts<br/>Execution limits"]
    end
    
    subgraph "Advanced Configuration"
        batch["batch_events: Batch<br/>Event batching"]
        concurrency["concurrency: Concurrency<br/>Concurrent execution limits"]
        rateLimit["rate_limit: RateLimit<br/>Rate limiting"]
        throttle["throttle: Throttle<br/>Throttling"]
        cancel["cancel: Cancel<br/>Cancellation conditions"]
    end
    
    subgraph "Function Creation"
        decorator["@client.create_function()"]
        opts["FunctionOpts"]
        func["Function instance"]
    end
    
    fnId --> opts
    name --> opts
    trigger --> opts
    retries --> opts
    timeout --> opts
    
    batch --> opts
    concurrency --> opts
    rateLimit --> opts
    throttle --> opts
    cancel --> opts
    
    decorator --> opts
    opts --> func
```

**Function Configuration Options**

The function configuration system provides extensive control over execution behavior, from basic retry logic to advanced features like event batching and rate limiting.

Sources: [pkg/inngest/inngest/_internal/function.py:29-64](), [pkg/inngest/inngest/_internal/client_lib/client.py:205-301](), [pkg/inngest/inngest/_internal/server_lib/registration.py:22-202]()

## Handler Function Signatures

Inngest functions receive two primary parameters: a context object containing execution metadata and event data, and a step object for controlling execution flow. The system supports both async and sync variants.

```mermaid
graph LR
    subgraph "Async Handlers"
        asyncDef["async def my_function"]
        asyncCtx["ctx: inngest.Context"]
        asyncStep["step: inngest.Step"]
    end
    
    subgraph "Sync Handlers"
        syncDef["def my_function"]  
        syncCtx["ctx: inngest.ContextSync"]
        syncStep["step: inngest.StepSync"]
    end
    
    subgraph "Context Properties"
        eventData["ctx.event.data"]
        runId["ctx.run_id"]
        attemptData["ctx.attempt"]
    end
    
    subgraph "Step Operations"
        stepRun["step.run()"]
        stepInvoke["step.invoke()"]
        stepSend["step.send_event()"]
        stepSleep["step.sleep()"]
    end
    
    asyncDef --> asyncCtx
    asyncDef --> asyncStep
    syncDef --> syncCtx  
    syncDef --> syncStep
    
    asyncCtx --> eventData
    asyncCtx --> runId
    asyncCtx --> attemptData
    
    asyncStep --> stepRun
    asyncStep --> stepInvoke
    asyncStep --> stepSend
    asyncStep --> stepSleep
```

**Handler Function Interface**

The handler interface provides access to execution context and step-based control flow. Both sync and async variants follow the same pattern but use different base classes for type safety.

Sources: [README.md:67-76](), [README.md:117-149](), [README.md:169-177]()

## Event System Integration

The Core API provides methods for sending events both from within functions and from external application code. Events are the primary mechanism for triggering function execution and inter-function communication.

```mermaid
sequenceDiagram
    participant App as "Application Code"
    participant Client as "Inngest Client"
    participant API as "Event API"
    participant Server as "Inngest Server"
    participant Func as "Function Handler"
    
    App->>Client: "client.send(Event(name='user.created'))"
    Client->>API: "POST /e/{event_key}"
    API->>Server: "Process event"
    Server->>Func: "Trigger matching functions"
    Func->>Client: "step.send_event()"
    Client->>API: "Send new event"
    API-->>Client: "Event ID"
    Client-->>Func: "Continue execution"
```

**Event Flow and Function Triggering**

Events flow through the system to trigger function execution and enable inter-function communication. The API provides both synchronous and asynchronous event sending methods.

| Method | Usage | Return Type |
|--------|-------|-------------|
| `client.send()` | Async event sending | `list[str]` (event IDs) |
| `client.send_sync()` | Sync event sending | `list[str]` (event IDs) |
| `step.send_event()` | Send from within function | Event ID |

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:452-585](), [README.md:179-191]()

## Type System and Error Handling

The Core API uses Python's type system extensively to provide compile-time safety and runtime validation. Configuration objects inherit from `BaseModel` and provide automatic validation and serialization.

```mermaid
graph TB
    subgraph "Type Hierarchy"
        BaseModel["types.BaseModel<br/>Pydantic base"]
        FunctionOpts["function.FunctionOpts"]
        ServerConfig["server_lib configs"]
    end
    
    subgraph "Validation System"
        pydantic["Pydantic Validation"]
        customValidation["Custom convert_validation_error"]
        inngestErrors["errors.FunctionConfigInvalidError"]
    end
    
    subgraph "Error Types"
        configError["FunctionConfigInvalidError"]
        executionError["ExecutionError"]
        sendError["SendEventsError"]
    end
    
    BaseModel --> FunctionOpts
    BaseModel --> ServerConfig  
    FunctionOpts --> pydantic
    ServerConfig --> pydantic
    pydantic --> customValidation
    customValidation --> inngestErrors
    
    inngestErrors --> configError
    inngestErrors --> executionError
    inngestErrors --> sendError
```

**Type System and Validation Architecture**

The type system provides runtime validation and clear error messages for configuration issues. All configuration classes implement custom error conversion to provide Inngest-specific error messages.

Sources: [pkg/inngest/inngest/_internal/function.py:58-62](), [pkg/inngest/inngest/_internal/server_lib/registration.py:14-20]()

# Inngest Client




The Inngest Client is the central component of the Inngest Python SDK that enables applications to interact with the Inngest service. It provides functionality for registering serverless functions, sending events, and managing the communication between your application and the Inngest platform. This document focuses on the client's initialization, configuration options, and core methods.

For information about defining functions with the client, see [Functions](#3.2). For details on event handling, see [Events](#3.4).

## Overview

The Inngest Client initializes the connection to the Inngest service and serves as the primary interface for registering functions and sending events. It can operate in either development mode with the local Dev Server or production mode connecting to Inngest Cloud.

```mermaid
graph TD
    subgraph "Application"
        App["Your Python Application"]
    end
    
    subgraph "Inngest SDK"
        Client["Inngest Client"]
        FunctionRegistry["Function Registry"]
        EventSender["Event Sender"]
        Middleware["Middleware"]
    end
    
    subgraph "Inngest Platform"
        DevServer["Dev Server"]
        Cloud["Inngest Cloud"]
    end
    
    App -->|"Initializes"| Client
    Client -->|"Registers"| FunctionRegistry
    Client -->|"Sends events"| EventSender
    Client -->|"Applies"| Middleware
    
    FunctionRegistry -->|"Development"| DevServer
    FunctionRegistry -->|"Production"| Cloud
    EventSender -->|"Development"| DevServer
    EventSender -->|"Production"| Cloud
```

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:32-85](), [README.md:60-63]()

## Client Initialization

The Inngest Client is instantiated with configuration parameters that determine how it communicates with the Inngest service.

### Constructor Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_id` | str | Yes | Unique identifier for your application |
| `is_production` | bool | No | Whether to use production mode (Inngest Cloud) or development mode (Dev Server) |
| `api_base_url` | str | No | Custom base URL for the Inngest API |
| `event_api_base_url` | str | No | Custom base URL for the Inngest Event API |
| `event_key` | str | No | Authentication key for sending events |
| `signing_key` | str | No | Authentication key for validating requests |
| `env` | str | No | Branch environment name |
| `logger` | Logger | No | Custom logger |
| `middleware` | list | No | List of middleware to use |

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:59-89]()

### Example Initialization

Basic client initialization:

```python
import inngest