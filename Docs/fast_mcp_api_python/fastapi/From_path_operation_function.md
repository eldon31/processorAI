background_tasks.add_task(task_function, *args, **kwargs)
```

### Task Function Parameter Handling

```mermaid
graph TD
    AddTaskCall[".add_task(func, arg1, arg2, key=value)"] --> ParseArgs["Parse Arguments"]
    ParseArgs --> StoreFunc["Store Function Reference"]
    ParseArgs --> StorePos["Store Positional Args"]
    ParseArgs --> StoreKW["Store Keyword Args"]
    
    StoreFunc --> TaskObj["Background Task Object"]
    StorePos --> TaskObj
    StoreKW --> TaskObj
    
    TaskObj --> QueueTask["Add to Execution Queue"]
```

The `.add_task()` method accepts:
- A callable function as the first argument
- Any positional arguments to pass to the function
- Any keyword arguments to pass to the function

Sources: [docs/en/docs/tutorial/background-tasks.md:42-46]()

## Dependency Injection Integration

### Multi-Level Background Task Usage

```mermaid
graph TD
    PathOp["Path Operation Function"] --> BGTasks1["BackgroundTasks Parameter"]
    Dependency["Dependency Function"] --> BGTasks2["BackgroundTasks Parameter"]
    SubDep["Sub-Dependency"] --> BGTasks3["BackgroundTasks Parameter"]
    
    BGTasks1 --> Shared["Shared BackgroundTasks Instance"]
    BGTasks2 --> Shared
    BGTasks3 --> Shared
    
    Shared --> MergedQueue["Merged Task Queue"]
    MergedQueue --> Execute["Execute All Tasks"]
```

FastAPI automatically reuses the same `BackgroundTasks` instance across all dependency levels within a single request, ensuring all background tasks are collected and executed together.

### Dependency Injection Example Flow

```mermaid
sequenceDiagram
    participant Request
    participant FastAPI
    participant Dependency as "write_log()"
    participant PathOp as "send_notification()"
    participant BGTasks as "BackgroundTasks"

    Request->>FastAPI: "GET /send-notification/email"
    FastAPI->>BGTasks: "Create instance"
    FastAPI->>Dependency: "Call with BackgroundTasks"
    Dependency->>BGTasks: "add_task(log_message)"
    FastAPI->>PathOp: "Call with BackgroundTasks + email"
    PathOp->>BGTasks: "add_task(write_notification)"
    PathOp->>Request: "HTTP Response"
    
    Note over BGTasks: After response sent
    BGTasks->>BGTasks: "Execute log_message"
    BGTasks->>BGTasks: "Execute write_notification"
```

Sources: [docs/en/docs/tutorial/background-tasks.md:48-63]()

## Technical Implementation Details

### Starlette Integration

FastAPI's background task system is a thin wrapper around Starlette's implementation:

| Component | FastAPI | Starlette |
|-----------|---------|-----------|
| Import Path | `from fastapi import BackgroundTasks` | `from starlette.background import BackgroundTasks` |
| Class | Re-exported reference | Original implementation |
| Alternative | `BackgroundTask` (single) | `BackgroundTask` (single) |

The key difference is that FastAPI provides `BackgroundTasks` (plural) as a dependency injection parameter, while `BackgroundTask` (singular) requires manual instantiation and response handling.

### Response Integration Mechanism

```mermaid
graph TD
    PathOpReturn["Path Operation Returns"] --> FastAPIProc["FastAPI Processing"]
    FastAPIProc --> CheckBG{"BackgroundTasks Used?"}
    CheckBG -->|Yes| AttachBG["Attach Tasks to Response"]
    CheckBG -->|No| StandardResp["Standard Response"]
    
    AttachBG --> SendResp["Send Response to Client"]
    StandardResp --> SendResp
    
    SendResp --> ExecuteBG["Execute Background Tasks"]
    ExecuteBG --> Cleanup["Cleanup Resources"]
```

When `BackgroundTasks` is used as a parameter, FastAPI automatically attaches the queued tasks to the response object, ensuring they execute after the response is sent.

Sources: [docs/en/docs/tutorial/background-tasks.md:66-74]()

## Use Cases and Limitations

### Appropriate Use Cases

Background tasks are suitable for:
- Email notifications after user actions
- File processing that can be asynchronous
- Logging and analytics
- Cache warming
- Cleanup operations

### Performance Considerations

```mermaid
graph LR
    LightTasks["Light Background Tasks"] --> BGTasks["BackgroundTasks"]
    HeavyTasks["Heavy Computation"] --> Celery["External Queue (Celery)"]
    DistribTasks["Distributed Processing"] --> Celery
    
    BGTasks --> SameProcess["Same Process Execution"]
    Celery --> MultiProcess["Multi-Process/Server"]
    
    SameProcess --> SharedMem["Shared Memory Access"]
    MultiProcess --> ScalableArch["Scalable Architecture"]
```

For heavy computational tasks or distributed processing, external task queue systems like Celery are recommended over FastAPI's built-in background tasks.

### Memory and Resource Sharing

Background tasks in FastAPI:
- Run in the same process as the web application
- Have access to shared memory and variables
- Are suitable for lightweight operations
- Should not be used for long-running or resource-intensive tasks

Sources: [docs/en/docs/tutorial/background-tasks.md:76-87]()