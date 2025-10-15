## Purpose and Scope

This document covers how Inngest manages function execution lifecycle and persistent state throughout a function's run. It details the event-driven lifecycle tracking system, the Redis-backed state persistence layer, and the history recording mechanisms that enable function execution monitoring and debugging.

For information about the queue system that schedules function execution, see [Distributed Queue System](#2.1). For details on how functions are defined and configured, see [Function Schema and CUE Configuration](#3.1).

## Function Lifecycle Overview

Functions in Inngest progress through a well-defined lifecycle with state changes tracked at both the function and individual step levels. The lifecycle system provides hooks for observability, history recording, and coordination between different system components.

### High-Level Lifecycle Flow

```mermaid
stateDiagram-v2
    [*] --> Scheduled: "Event triggers function"
    Scheduled --> Started: "Capacity available"
    Scheduled --> Skipped: "Function paused/disabled"
    Started --> StepExecution: "Begin first step"
    StepExecution --> StepWaiting: "step.waitForEvent(), step.sleep()"
    StepWaiting --> StepExecution: "Event received/timer expired"
    StepExecution --> StepExecution: "Next step in sequence"
    StepExecution --> Completed: "All steps finished successfully"
    StepExecution --> Failed: "Permanent failure"
    Started --> Cancelled: "Cancel request received"
    Cancelled --> [*]
    Completed --> [*]
    Failed --> [*]
    Skipped --> [*]
```

*Sources: [pkg/execution/lifecycle.go:29-202](), [pkg/execution/history/lifecycle.go:49-263]()*

## Lifecycle Event System

The lifecycle system is built around the `LifecycleListener` interface, which defines hooks for all major state transitions. Multiple listeners can be registered to handle different concerns like history recording, metrics collection, and debugging.

### Core Lifecycle Interface

The `LifecycleListener` interface defines callbacks for function and step lifecycle events:

```mermaid
graph TB
    LifecycleListener["LifecycleListener Interface"]
    
    subgraph "Function-Level Events"
        OnFunctionScheduled["OnFunctionScheduled()"]
        OnFunctionStarted["OnFunctionStarted()"] 
        OnFunctionFinished["OnFunctionFinished()"]
        OnFunctionCancelled["OnFunctionCancelled()"]
        OnFunctionSkipped["OnFunctionSkipped()"]
    end
    
    subgraph "Step-Level Events"
        OnStepScheduled["OnStepScheduled()"]
        OnStepStarted["OnStepStarted()"]
        OnStepFinished["OnStepFinished()"]
        OnStepGatewayRequestFinished["OnStepGatewayRequestFinished()"]
    end
    
    subgraph "Special Step Events"
        OnWaitForEvent["OnWaitForEvent()"]
        OnWaitForEventResumed["OnWaitForEventResumed()"]
        OnSleep["OnSleep()"]
        OnInvokeFunction["OnInvokeFunction()"]
        OnInvokeFunctionResumed["OnInvokeFunctionResumed()"]
    end
    
    LifecycleListener --> OnFunctionScheduled
    LifecycleListener --> OnFunctionStarted
    LifecycleListener --> OnFunctionFinished
    LifecycleListener --> OnFunctionCancelled
    LifecycleListener --> OnFunctionSkipped
    LifecycleListener --> OnStepScheduled
    LifecycleListener --> OnStepStarted
    LifecycleListener --> OnStepFinished
    LifecycleListener --> OnStepGatewayRequestFinished
    LifecycleListener --> OnWaitForEvent
    LifecycleListener --> OnWaitForEventResumed
    LifecycleListener --> OnSleep
    LifecycleListener --> OnInvokeFunction
    LifecycleListener --> OnInvokeFunctionResumed
```

*Sources: [pkg/execution/lifecycle.go:29-202]()*

### Lifecycle Event Flow

Each lifecycle event carries specific metadata about the function run and execution context:

| Event Type | Trigger Condition | Key Data |
|------------|------------------|----------|
| `OnFunctionScheduled` | Function queued for execution | `Metadata`, `queue.Item`, tracked events |
| `OnFunctionStarted` | Function begins execution | `Metadata`, `queue.Item`, latency metrics |
| `OnStepScheduled` | Step queued for execution | `Metadata`, `queue.Item`, step name |
| `OnStepStarted` | Step begins execution | `Metadata`, `inngest.Edge`, execution URL |
| `OnStepFinished` | Step completes or fails | `Metadata`, `state.DriverResponse`, execution error |
| `OnFunctionFinished` | Function completes or fails permanently | `Metadata`, final `state.DriverResponse` |

*Sources: [pkg/execution/lifecycle.go:33-202]()*

## State Storage Architecture

Function state is persisted using a two-tier architecture with both v1 (legacy) and v2 interfaces. The v2 interface provides a cleaner abstraction while maintaining backward compatibility through an adapter pattern.

### State Storage Components

```mermaid
graph TB
    subgraph "V2 State Interface"
        RunService["state.RunService"]
        StateLoader["state.StateLoader"] 
        CreateState["state.CreateState"]
        State["state.State"]
    end
    
    subgraph "V2 Adapter Layer"
        V2Adapter["redis_state.v2"]
        MustRunServiceV2["MustRunServiceV2()"]
    end
    
    subgraph "V1 Redis Implementation" 
        RedisMgr["redis_state.mgr"]
        RedisClient["rueidis.Client"]
        LuaScripts["Lua Scripts"]
    end
    
    subgraph "State Components"
        Metadata["state.Metadata"]
        Events["Events []json.RawMessage"]
        Steps["Steps map[string]json.RawMessage"]
        Stack["Stack []string"]
    end
    
    RunService --> V2Adapter
    V2Adapter --> RedisMgr
    RedisMgr --> RedisClient
    RedisMgr --> LuaScripts
    
    State --> Metadata
    State --> Events  
    State --> Steps
    State --> Stack
    
    CreateState --> State
```

*Sources: [pkg/execution/state/v2/interfaces.go:23-75](), [pkg/execution/state/redis_state/v2_adapter.go:18-40]()*

### State Metadata Structure

The state metadata contains comprehensive information about a function run:

```mermaid
graph LR
    subgraph "state.Metadata"
        ID["state.ID"]
        Config["state.Config"] 
        Metrics["state.RunMetrics"]
        Stack["Stack []string"]
    end
    
    subgraph "state.ID" 
        RunID["RunID ulid.ULID"]
        FunctionID["FunctionID uuid.UUID"]
        Tenant["state.Tenant"]
    end
    
    subgraph "state.Config"
        FunctionVersion["FunctionVersion int"]
        SpanID["SpanID string"]
        EventIDs["EventIDs []ulid.ULID"]
        RequestVersion["RequestVersion int"]
        Idempotency["Idempotency string"]
        Context["Context map[string]any"]
    end
    
    subgraph "state.RunMetrics"
        StateSize["StateSize int"]
        EventSize["EventSize int"]
        StepCount["StepCount int"]
    end
    
    ID --> RunID
    ID --> FunctionID
    ID --> Tenant
    Config --> FunctionVersion
    Config --> SpanID  
    Config --> EventIDs
    Config --> RequestVersion
    Config --> Idempotency
    Config --> Context
    Metrics --> StateSize
    Metrics --> EventSize
    Metrics --> StepCount
```

*Sources: [pkg/execution/state/v2/state_metadata.go:88-144](), [pkg/execution/state/v2/state_metadata.go:482-507]()*

## State Operations

The state management system provides comprehensive CRUD operations for function runs, with built-in retry logic and error handling.

### Core State Operations

| Operation | Purpose | Return Values |
|-----------|---------|---------------|
| `Create()` | Initialize new function run state | `State`, `error` |
| `LoadState()` | Retrieve complete run state | `State`, `error` |  
| `LoadMetadata()` | Get run metadata only | `Metadata`, `error` |
| `LoadEvents()` | Get triggering events | `[]json.RawMessage`, `error` |
| `LoadSteps()` | Get all step outputs | `map[string]json.RawMessage`, `error` |
| `SaveStep()` | Store step output | `hasPending bool`, `error` |
| `UpdateMetadata()` | Update run configuration | `error` |
| `Delete()` | Remove all run data | `bool`, `error` |

*Sources: [pkg/execution/state/v2/interfaces.go:34-52]()*

### State Creation and Lifecycle

```mermaid
sequenceDiagram
    participant Executor
    participant V2Adapter
    participant RedisMgr  
    participant Redis
    
    Executor->>V2Adapter: Create(CreateState)
    V2Adapter->>RedisMgr: New(statev1.Input)
    RedisMgr->>Redis: Execute new.lua script
    Redis-->>RedisMgr: Run ID or error
    RedisMgr-->>V2Adapter: State instance
    V2Adapter-->>Executor: state.State
    
    Note over Executor,Redis: Step execution and state updates
    
    Executor->>V2Adapter: SaveStep(stepID, data)
    V2Adapter->>RedisMgr: SaveResponse(stepID, data)
    RedisMgr->>Redis: Execute saveResponse.lua
    Redis-->>RedisMgr: Success/duplicate/error
    RedisMgr-->>V2Adapter: hasPending, error
    V2Adapter-->>Executor: hasPending, error
```

*Sources: [pkg/execution/state/redis_state/v2_adapter.go:59-161](), [pkg/execution/state/redis_state/lua/new.lua:1-58](), [pkg/execution/state/redis_state/lua/saveResponse.lua:1-48]()*

### Retry Logic and Error Handling

The v2 adapter includes sophisticated retry logic with configurable backoff and error classification:

```mermaid
graph TB
    subgraph "Retry Configuration"
        RetryConf["util.RetryConf"]
        MaxAttempts["MaxAttempts int"]
        InitialBackoff["InitialBackoff time.Duration"] 
        MaxBackoff["MaxBackoff time.Duration"]
        RetryableErrors["RetryableErrors func(error) bool"]
    end
    
    subgraph "Error Classification"
        ErrIdempotentResponse["ErrIdempotentResponse"]
        ErrDuplicateResponse["ErrDuplicateResponse"]  
        NetworkErrors["Network/Redis Errors"]
    end
    
    subgraph "Retry Decision"
        IsRetryable{"Error Retryable?"}
        AttemptCount{"Attempts < Max?"}
        Backoff["Exponential Backoff"]
        Execute["Execute Operation"]
    end
    
    Execute --> IsRetryable
    IsRetryable -->|Yes| AttemptCount
    IsRetryable -->|No| Return["Return Error"]
    AttemptCount -->|Yes| Backoff
    AttemptCount -->|No| Return
    Backoff --> Execute
    
    ErrIdempotentResponse --> IsRetryable
    ErrDuplicateResponse --> IsRetryable
    NetworkErrors --> IsRetryable
```

*Sources: [pkg/execution/state/redis_state/v2_adapter.go:395-412](), [pkg/util/retry.go:76-142]()*

## History Tracking

The history system records all lifecycle events for observability, debugging, and auditing. History entries are written through pluggable drivers that can store data in different backends.

### History Data Model

The `History` struct captures comprehensive information about each lifecycle event:

| Field | Type | Purpose |
|-------|------|---------|
| `Type` | `string` | Event type (see `enums.HistoryType`) |
| `RunID` | `ulid.ULID` | Function run identifier |
| `FunctionID` | `uuid.UUID` | Function identifier |
| `StepName` | `*string` | Human-readable step name |
| `StepID` | `*string` | Step identifier for correlation |
| `Result` | `*Result` | Step output, timing, SDK info |
| `CreatedAt` | `time.Time` | Timestamp of event |
| `Attempt` | `int64` | Retry attempt number |
| `LatencyMS` | `*int64` | System latency metrics |

*Sources: [pkg/execution/history/history.go:18-54]()*

### History Event Types

The history system tracks different categories of events with specific data structures:

```mermaid
graph TB
    subgraph "Function Events"
        FunctionScheduled["HistoryTypeFunctionScheduled"]
        FunctionStarted["HistoryTypeFunctionStarted"] 
        FunctionCompleted["HistoryTypeFunctionCompleted"]
        FunctionFailed["HistoryTypeFunctionFailed"]
        FunctionCancelled["HistoryTypeFunctionCancelled"]
        FunctionSkipped["HistoryTypeFunctionSkipped"]
    end
    
    subgraph "Step Events"
        StepScheduled["HistoryTypeStepScheduled"]
        StepStarted["HistoryTypeStepStarted"]
        StepCompleted["HistoryTypeStepCompleted"] 
        StepErrored["HistoryTypeStepErrored"]
        StepFailed["HistoryTypeStepFailed"]
    end
    
    subgraph "Special Step Events"
        StepSleeping["HistoryTypeStepSleeping"]
        StepWaiting["HistoryTypeStepWaiting"]
        StepInvoking["HistoryTypeStepInvoking"]
    end
    
    subgraph "Data Structures"
        Sleep["Sleep{Until}"]
        WaitForEvent["WaitForEvent{EventName,Timeout}"]
        InvokeFunction["InvokeFunction{FunctionID,EventID}"]
        Result["Result{Output,Duration,SDKInfo}"]
    end
    
    StepSleeping --> Sleep
    StepWaiting --> WaitForEvent  
    StepInvoking --> InvokeFunction
    StepCompleted --> Result
    StepErrored --> Result
    StepFailed --> Result
```

*Sources: [pkg/execution/history/lifecycle.go:70-91](), [pkg/execution/history/history.go:55-116]()*

## Integration with Execution System

The lifecycle and state management systems integrate closely with the core execution engine to provide a complete function execution platform.

### Component Integration Flow

```mermaid
graph TB
    subgraph "Execution Layer"
        Executor["execution.Executor"]
        Runner["execution.Runner"] 
        DriverResponse["state.DriverResponse"]
    end
    
    subgraph "State Management"
        StateManager["state.Manager"]
        RunService["state.RunService"]
        StateStore["Redis State Store"]
    end
    
    subgraph "Lifecycle Tracking"
        LifecycleListener["LifecycleListener"]
        HistoryDriver["history.Driver"]
        DevServerLifecycle["devserver.Lifecycle"]
    end
    
    subgraph "Queue Integration" 
        QueueManager["queue.Manager"]
        QueueItem["queue.Item"]
        Edge["inngest.Edge"]
    end
    
    Runner --> Executor
    Executor --> StateManager
    Executor --> LifecycleListener
    StateManager --> RunService
    RunService --> StateStore
    LifecycleListener --> HistoryDriver
    LifecycleListener --> DevServerLifecycle
    Executor --> QueueManager
    QueueManager --> QueueItem
    QueueItem --> Edge
    
    Executor -->|"OnFunctionStarted"| LifecycleListener
    Executor -->|"SaveStep"| StateManager  
    Executor -->|"OnStepFinished"| LifecycleListener
    DriverResponse --> LifecycleListener
```

*Sources: [pkg/execution/history/lifecycle.go:26-34](), [pkg/devserver/lifecycle.go:15-21](), [pkg/execution/state/redis_state/v2_adapter.go:18-56]()*

The state management and lifecycle systems work together to provide reliable function execution with comprehensive observability. State is persisted at each step to enable recovery from failures, while lifecycle events create an audit trail for debugging and monitoring function behavior.