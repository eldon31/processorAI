The Core Execution System is the heart of Inngest's serverless function platform, responsible for orchestrating the entire lifecycle of function execution from event ingestion to completion. This system manages the scheduling, execution, state persistence, and coordination of distributed function runs across multiple workers and runtime environments.

For information about the specific queue implementation and job distribution, see [Distributed Queue System](#2.1). For details about function step execution and driver communication, see [Executor and Function Execution](#2.2). For HTTP-based SDK communication, see [HTTP Driver and SDK Communication](#2.3). For WebSocket-based worker connections, see [Connect Gateway and WebSocket Workers](#2.4).

## System Architecture Overview

The core execution system consists of several interconnected components that work together to provide reliable, scalable function execution:

```mermaid
graph TB
    subgraph "Event Ingestion"
        EventAPI["Event API<br/>pkg/api"]
        DevServer["Dev Server<br/>pkg/devserver"]
    end
    
    subgraph "Orchestration Layer"
        Runner["Runner Service<br/>pkg/execution/runner"]
        ExecutorService["Executor Service<br/>pkg/execution/executor/service"]
    end
    
    subgraph "Execution Engine"
        Executor["Executor<br/>pkg/execution/executor/executor"]
        StateManager["State Manager<br/>pkg/execution/state"]
        QueueSystem["Queue System<br/>pkg/execution/queue"]
    end
    
    subgraph "Function Drivers"
        HTTPDriver["HTTP Driver<br/>pkg/execution/driver/httpdriver"]
        ConnectDriver["Connect Driver<br/>pkg/execution/driver/connectdriver"]
    end
    
    subgraph "Storage Layer"
        RedisState["Redis State<br/>pkg/execution/state/redis_state"]
        PauseManager["Pause Manager<br/>pkg/execution/pauses"]
    end
    
    EventAPI --> Runner
    DevServer --> Runner
    
    Runner --> Executor
    ExecutorService --> Executor
    
    Executor --> StateManager
    Executor --> QueueSystem
    Executor --> HTTPDriver
    Executor --> ConnectDriver
    
    StateManager --> RedisState
    StateManager --> PauseManager
    
    QueueSystem --> RedisState
```

Sources: pkg/execution/executor/executor.go:1-115, pkg/execution/runner/runner.go:1-124, pkg/execution/executor/service.go:1-116, pkg/execution/state/state.go:1-53

## Key System Components

The execution system is built around several core interfaces and implementations that provide clear separation of concerns:

### Primary Execution Interfaces

| Component | Interface | Implementation | Purpose |
|-----------|-----------|----------------|---------|
| **Runner** | `Runner` | `runner.svc` | Event handling and function triggering |
| **Executor** | `execution.Executor` | `executor.executor` | Function step execution and orchestration |
| **State Manager** | `state.Manager` | `redis_state.mgr` | Function state persistence and retrieval |
| **Queue** | `queue.Queue` | `redis_state` implementation | Job scheduling and distribution |
| **Pause Manager** | `pauses.Manager` | Redis-backed implementation | Wait state management |

```mermaid
graph LR
    subgraph "Core Interfaces"
        ExecutorIface["execution.Executor<br/>Schedule(), Execute(), Resume()"]
        StateManagerIface["state.Manager<br/>New(), Load(), SaveResponse()"]
        QueueIface["queue.Queue<br/>Enqueue(), Run()"]
        RunnerIface["Runner<br/>handleMessage(), functions()"]
    end
    
    subgraph "Implementations" 
        ExecutorImpl["executor.executor<br/>pkg/execution/executor"]
        StateImpl["redis_state.mgr<br/>pkg/execution/state/redis_state"]
        QueueImpl["redis_state queue<br/>pkg/execution/state/redis_state"]
        RunnerImpl["runner.svc<br/>pkg/execution/runner"]
    end
    
    ExecutorIface -.-> ExecutorImpl
    StateManagerIface -.-> StateImpl
    QueueIface -.-> QueueImpl
    RunnerIface -.-> RunnerImpl
    
    ExecutorImpl --> StateImpl
    ExecutorImpl --> QueueImpl
    RunnerImpl --> ExecutorImpl
```

Sources: pkg/execution/execution.go:53-134, pkg/execution/state/state.go:322-376, pkg/execution/runner/runner.go:46-56, pkg/execution/executor/executor.go:80-115

## Function Execution Flow

The execution flow demonstrates how events trigger function execution through the coordinated interaction of system components:

```mermaid
sequenceDiagram
    participant Event as "Event Source"
    participant Runner as "runner.svc"
    participant Executor as "executor.executor" 
    participant State as "redis_state.mgr"
    participant Queue as "redis_state queue"
    participant Driver as "Function Driver"
    
    Event->>Runner: "Publish Event"
    Runner->>Runner: "handleMessage()"
    Runner->>Runner: "functions() - Find matching functions"
    Runner->>Executor: "Schedule(ScheduleRequest)"
    
    Executor->>State: "New() - Create function state"
    Executor->>Queue: "Enqueue() - Schedule execution"
    
    Queue->>Executor: "Execute() - Process queue item"
    Executor->>State: "Load() - Get function state"
    Executor->>Driver: "Execute function step"
    Driver-->>Executor: "Step result"
    Executor->>State: "SaveResponse() - Persist result"
    
    alt "Has more steps"
        Executor->>Queue: "Enqueue next step"
    else "Function complete"
        Executor->>State: "Mark complete"
    end
```

Sources: pkg/execution/runner/runner.go:325-406, pkg/execution/executor/executor.go:520-903, pkg/execution/executor/executor.go:919-1170, pkg/execution/state/redis_state/redis_state.go:233-362

## State Management Architecture

The state management system provides durable storage for function execution data, including events, step results, and execution metadata:

```mermaid
graph TB
    subgraph "State Operations"
        CreateState["New()<br/>Create run state"]
        LoadState["Load()<br/>Retrieve full state"]
        SaveStep["SaveResponse()<br/>Save step output"]
        UpdateMeta["UpdateMetadata()<br/>Update run info"]
    end
    
    subgraph "Redis Storage Structure"
        RunMetadata["Run Metadata<br/>kg.RunMetadata()"]
        Events["Event Data<br/>kg.Events()"]
        Actions["Step Results<br/>kg.Actions()"]
        Stack["Execution Stack<br/>kg.Stack()"]
        Pauses["Wait States<br/>pause keys"]
    end
    
    subgraph "State Components"
        Identifier["state.Identifier<br/>RunID, FunctionID, AccountID"]
        Metadata["state.Metadata<br/>Status, StartedAt, Context"]
        MemoizedStep["state.MemoizedStep<br/>Step results and data"]
    end
    
    CreateState --> RunMetadata
    CreateState --> Events
    LoadState --> RunMetadata
    LoadState --> Events
    LoadState --> Actions
    SaveStep --> Actions
    SaveStep --> Stack
    UpdateMeta --> RunMetadata
    
    RunMetadata --> Identifier
    RunMetadata --> Metadata
    Actions --> MemoizedStep
```

Sources: pkg/execution/state/redis_state/redis_state.go:233-396, pkg/execution/state/state.go:61-102, pkg/execution/state/state.go:199-252, pkg/execution/state/state.go:814-857

## Queue and Work Distribution

The queue system manages the scheduling and distribution of function execution work across available workers:

```mermaid
graph LR
    subgraph "Queue Operations"
        Enqueue["Enqueue()<br/>Schedule work"]
        Run["Run()<br/>Process queue items"]
        Dequeue["Dequeue()<br/>Claim work item"]
    end
    
    subgraph "Queue Item Types"
        KindStart["KindStart<br/>Initial function execution"]
        KindEdge["KindEdge<br/>Step execution"]
        KindPause["KindPause<br/>Timeout handling"]
        KindSleep["KindSleep<br/>Delayed execution"]
    end
    
    subgraph "Queue Item Structure"
        QueueItem["queue.Item<br/>JobID, Identifier, Payload"]
        PayloadEdge["queue.PayloadEdge<br/>Edge execution data"]
        PayloadPause["queue.PayloadPauseTimeout<br/>Timeout data"]
    end
    
    Enqueue --> KindStart
    Enqueue --> KindEdge
    Enqueue --> KindSleep
    Run --> Dequeue
    Dequeue --> QueueItem
    
    QueueItem --> PayloadEdge
    QueueItem --> PayloadPause
```

Sources: pkg/execution/executor/service.go:235-280, pkg/execution/executor/executor.go:824-880, pkg/execution/state/redis_state/redis_state.go queue operations

## Pause and Resume Mechanism

The execution system supports pausing function execution for external events, timeouts, and manual intervention through a sophisticated pause management system:

```mermaid
graph TB
    subgraph "Pause Creation"
        WaitForEvent["step.waitForEvent"]
        Invoke["step.invoke"]  
        Sleep["step.sleep"]
        Signal["step.waitForSignal"]
    end
    
    subgraph "Pause Storage"
        SavePause["SavePause()<br/>Store pause state"]
        PauseData["state.Pause<br/>ID, Expression, Timeout"]
        PauseIndex["Pause Indexes<br/>By event, by ID"]
    end
    
    subgraph "Resume Operations"
        HandlePauses["HandlePauses()<br/>Match incoming events"]
        ResumePause["Resume()<br/>Continue execution"]
        PauseTimeout["ResumePauseTimeout()<br/>Handle timeouts"]
    end
    
    WaitForEvent --> SavePause
    Invoke --> SavePause
    Sleep --> SavePause
    Signal --> SavePause
    
    SavePause --> PauseData
    SavePause --> PauseIndex
    
    PauseIndex --> HandlePauses
    HandlePauses --> ResumePause
    PauseTimeout --> ResumePause
```

Sources: pkg/execution/state/pause.go:1-52, pkg/execution/state/redis_state/lua/savePause.lua:1-79, pkg/execution/state/redis_state/lua/consumePause.lua:1-45, pkg/execution/executor/executor.go:2890-3020

The Core Execution System orchestrates these components to provide reliable, scalable function execution with support for complex workflows, error handling, retries, and stateful operations across distributed environments.