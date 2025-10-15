This document covers Inngest's external API layer, including both the modern V2 gRPC/HTTP service and the legacy V1 HTTP API. These services provide external access to account management, function execution, and system health endpoints.

For information about internal service communication and the Connect Gateway system, see [Connect Gateway and WebSocket Workers](#2.4). For details about function execution mechanics, see [Executor and Function Execution](#2.2).

## Architecture Overview

The API layer consists of two primary services: a modern V2 gRPC service with automatic HTTP gateway generation, and a legacy V1 HTTP API that handles function execution checkpointing.

### API Service Architecture

```mermaid
graph TB
    subgraph "External Clients"
        gRPCClient["gRPC Client"]
        HTTPClient["HTTP Client"]
        SDKClient["SDK Client"]
    end
    
    subgraph "V2 API Layer"
        V2Service["Service struct<br/>pkg/api/v2/service.go"]
        GRPCServer["gRPC Server<br/>NewGRPCServer()"]
        HTTPGateway["HTTP Gateway<br/>grpc-gateway"]
        AuthMiddleware["Auth Middleware<br/>apiv2base.Base"]
    end
    
    subgraph "V1 API Layer" 
        V1Router["API Router<br/>pkg/api/apiv1/apiv1.go"]
        CheckpointAPI["Checkpoint API<br/>pkg/api/apiv1/checkpoint.go"]
        CancellationAPI["Cancellation API<br/>pkg/api/apiv1/cancellation.go"]
        EventsAPI["Events API<br/>pkg/api/apiv1/events.go"]
    end
    
    subgraph "Protocol Definitions"
        ProtoService["service.proto<br/>proto/api/v2/service.proto"]
        GeneratedTypes["Generated Types<br/>proto/gen/api/v2/"]
    end
    
    gRPCClient --> GRPCServer
    HTTPClient --> HTTPGateway
    SDKClient --> CheckpointAPI
    
    GRPCServer --> V2Service
    HTTPGateway --> V2Service
    V2Service --> AuthMiddleware
    
    ProtoService --> GeneratedTypes
    GeneratedTypes --> V2Service
    
    V1Router --> CheckpointAPI
    V1Router --> CancellationAPI
    V1Router --> EventsAPI
```

**Sources:** [pkg/api/v2/service.go:16-36](), [pkg/api/apiv1/apiv1.go:74-91](), [proto/api/v2/service.proto:34-821]()

## V2 gRPC Service Implementation

The V2 API service implements a modern gRPC-first design with automatic HTTP REST endpoint generation using grpc-gateway.

### Service Structure

The core `Service` struct implements the generated `V2Server` interface:

```mermaid
graph TB
    subgraph "Service Implementation"
        Service["Service struct<br/>{signingKeys, eventKeys, base}"]
        UnimplementedV2Server["UnimplementedV2Server<br/>Generated base"]
        Base["apiv2base.Base<br/>Common functionality"]
    end
    
    subgraph "Service Methods"
        Health["Health()"]
        CreateAccount["CreatePartnerAccount()"]
        FetchAccount["FetchAccount()"] 
        CreateEnv["CreateEnv()"]
        FetchKeys["FetchAccountEventKeys()"]
        CreateWebhook["CreateWebhook()"]
    end
    
    subgraph "Generated Interfaces"
        V2Server["V2Server interface"]
        V2Client["V2Client interface"]
        Handlers["HTTP Handlers<br/>RegisterV2HandlerServer()"]
    end
    
    Service --> UnimplementedV2Server
    Service --> Base
    Service --> Health
    Service --> CreateAccount
    Service --> FetchAccount
    Service --> CreateEnv
    Service --> FetchKeys
    Service --> CreateWebhook
    
    V2Server --> Service
    V2Client --> V2Server
    Handlers --> Service
```

**Sources:** [pkg/api/v2/service.go:16-36](), [proto/gen/api/v2/service_grpc.pb.go:171-187](), [proto/gen/api/v2/service.pb.gw.go:336-341]()

### Dual Protocol Support

The service simultaneously supports both gRPC and HTTP protocols through different server configurations:

```mermaid
graph LR
    subgraph "Server Creation"
        ServiceOpts["ServiceOptions<br/>{SigningKeysProvider, EventKeysProvider}"]
        GRPCOpts["GRPCServerOptions<br/>{AuthnMiddleware, AuthzMiddleware}"]
        HTTPOpts["HTTPHandlerOptions<br/>{AuthnMiddleware, AuthzMiddleware}"]
    end
    
    subgraph "gRPC Path"
        NewGRPCServer["NewGRPCServer()"]
        GRPCServer["grpc.Server"]
        Interceptors["Unary/Stream Interceptors<br/>auth integration"]
    end
    
    subgraph "HTTP Path"
        NewHTTPHandler["NewHTTPHandler()"]
        ServeMux["runtime.ServeMux<br/>grpc-gateway"]
        ChiRouter["chi.Router<br/>middleware chain"]
    end
    
    ServiceOpts --> NewGRPCServer
    GRPCOpts --> NewGRPCServer
    ServiceOpts --> NewHTTPHandler
    HTTPOpts --> NewHTTPHandler
    
    NewGRPCServer --> GRPCServer
    NewGRPCServer --> Interceptors
    
    NewHTTPHandler --> ServeMux
    NewHTTPHandler --> ChiRouter
```

**Sources:** [pkg/api/v2/service.go:44-66](), [pkg/api/v2/service.go:73-132]()

## V1 Legacy API

The V1 API provides HTTP-only endpoints focused on function execution lifecycle management and system monitoring.

### Core API Components

```mermaid
graph TB
    subgraph "V1 API Structure"
        APIStruct["API struct<br/>{opts Opts}"]
        Router["router struct<br/>{API, chi.Router}"]
        Opts["Opts struct<br/>Dependencies"]
    end
    
    subgraph "Key Dependencies"
        AuthFinder["AuthFinder<br/>Authentication"]
        Executor["execution.Executor<br/>Function execution"]
        Queue["queue.Queue<br/>Job management"]
        FunctionReader["cqrs.FunctionReader<br/>Function metadata"]
        StateService["state.RunService<br/>Execution state"]
    end
    
    subgraph "API Endpoints"
        Checkpoint["/http/runs/*<br/>Function checkpointing"]
        Signals["/signals<br/>Event signals"]
        Events["/events/*<br/>Event management"]
        Runs["/runs/*<br/>Function runs"]
        Cancellations["/cancellations<br/>Run cancellation"]
    end
    
    Router --> APIStruct
    APIStruct --> Opts
    
    Opts --> AuthFinder
    Opts --> Executor
    Opts --> Queue
    Opts --> FunctionReader
    Opts --> StateService
    
    Router --> Checkpoint
    Router --> Signals
    Router --> Events
    Router --> Runs
    Router --> Cancellations
```

**Sources:** [pkg/api/apiv1/apiv1.go:23-72](), [pkg/api/apiv1/apiv1.go:102-161]()

### Checkpoint API for Function Execution

The checkpoint API enables SDK-based function execution by providing stateful function run management:

```mermaid
graph TB
    subgraph "Checkpoint API Flow"
        NewRun["POST /http/runs/<br/>CheckpointNewRun()"]
        Steps["POST /http/runs/{runID}/steps<br/>CheckpointSteps()"]
        Response["POST /http/runs/{runID}/response<br/>CheckpointResponse()"]
        Output["GET /http/runs/{runID}/output<br/>Output()"]
    end
    
    subgraph "Request Types"
        NewRunReq["CheckpointNewRunRequest<br/>{RunID, Event, Steps}"]
        StepsReq["checkpointSteps<br/>{RunID, Steps, AccountID}"]
        ResponseReq["CheckpointResponse<br/>Final result"]
    end
    
    subgraph "State Management"
        StateStore["state.RunService<br/>Execution state"]
        Executor["execution.Executor<br/>Run scheduling"]
        Tracer["tracing.TracerProvider<br/>Observability"]
    end
    
    NewRun --> NewRunReq
    Steps --> StepsReq
    Response --> ResponseReq
    
    NewRunReq --> Executor
    StepsReq --> StateStore
    ResponseReq --> StateStore
    
    StateStore --> Tracer
```

**Sources:** [pkg/api/apiv1/checkpoint.go:111-197](), [pkg/api/apiv1/checkpoint.go:205-224](), [pkg/api/apiv1/checkpoint_types.go:58-77]()

## Authentication and Authorization

Both API versions implement layered authentication and authorization using HTTP middleware that integrates with gRPC interceptors.

### Auth Integration Pattern

```mermaid
graph TB
    subgraph "V2 Auth Flow"
        HTTPMiddleware["HTTP Middleware<br/>func(http.Handler) http.Handler"]
        GRPCInterceptor["gRPC Interceptor<br/>HTTPMiddlewareToGRPCInterceptor()"]
        AuthnMiddleware["Authentication<br/>Token validation"]
        AuthzMiddleware["Authorization<br/>Permission checks"]
    end
    
    subgraph "V1 Auth Flow"  
        AuthFinder["apiv1auth.AuthFinder<br/>Context-based auth"]
        MiddlewareChain["chi middleware chain"]
        CachingMW["CachingMiddleware<br/>Response caching"]
        MetricsMW["MetricsMiddleware<br/>Instrumentation"]
    end
    
    subgraph "Auth Data"
        AuthContext["Authentication context<br/>{AccountID, WorkspaceID}"]
        JWTSecret["JWT secrets<br/>Token signing/verification"]
    end
    
    HTTPMiddleware --> GRPCInterceptor
    GRPCInterceptor --> AuthnMiddleware
    AuthnMiddleware --> AuthzMiddleware
    
    AuthFinder --> AuthContext
    MiddlewareChain --> CachingMW
    MiddlewareChain --> MetricsMW
    
    AuthContext --> JWTSecret
```

**Sources:** [pkg/api/v2/service.go:98-101](), [pkg/api/apiv1/apiv1.go:119-132](), [pkg/api/apiv1/apiv1auth/]()

## Protocol Buffer Definitions

The V2 API uses Protocol Buffers for type-safe service definitions with automatic code generation for multiple languages.

### Service Definition Structure

The service definition in `proto/api/v2/service.proto` defines the complete API surface:

| RPC Method | HTTP Mapping | Purpose |
|------------|--------------|---------|
| `Health` | `GET /health` | System health check |
| `CreatePartnerAccount` | `POST /partner/accounts` | Partner account creation |
| `FetchAccount` | `GET /account` | User account retrieval |
| `CreateEnv` | `POST /envs` | Environment creation |
| `FetchAccountEventKeys` | `GET /keys/events` | Event key management |
| `CreateWebhook` | `POST /env/webhooks` | Webhook configuration |

**Sources:** [proto/api/v2/service.proto:34-821]()

### Generated Code Structure

```mermaid
graph TB
    subgraph "Protocol Buffer Sources"
        ServiceProto["service.proto<br/>RPC definitions"]
        OptionsProto["options.proto<br/>Custom annotations"]
    end
    
    subgraph "Generated Go Code"
        ServicePB["service.pb.go<br/>Message types"]
        ServiceGRPC["service_grpc.pb.go<br/>gRPC server/client"]
        ServiceGW["service.pb.gw.go<br/>HTTP gateway"]
        ConnectGo["service.connect.go<br/>Connect RPC support"]
    end
    
    subgraph "Generated Clients"
        V2Client["V2Client interface<br/>gRPC client"]
        HTTPClient["HTTP REST client<br/>via grpc-gateway"]
        ConnectClient["Connect RPC client<br/>connectrpc.com/connect"]
    end
    
    ServiceProto --> ServicePB
    ServiceProto --> ServiceGRPC
    ServiceProto --> ServiceGW
    ServiceProto --> ConnectGo
    
    ServiceGRPC --> V2Client
    ServiceGW --> HTTPClient
    ConnectGo --> ConnectClient
```

**Sources:** [proto/gen/api/v2/service.pb.go:1-10](), [proto/gen/api/v2/service_grpc.pb.go:1-10](), [proto/gen/api/v2/service.pb.gw.go:1-10](), [proto/gen/api/v2/apiv2connect/service.connect.go:1-10]()

## Error Handling and Response Patterns

Both API versions implement consistent error handling with proper HTTP status codes and structured error responses.

### V2 Error Response Pattern

The V2 API uses structured error responses defined in Protocol Buffers:

```mermaid
graph TB
    subgraph "Error Response Structure"
        ErrorResponse["ErrorResponse<br/>{errors: [Error]}"]
        Error["Error<br/>{code: string, message: string}"]
        ResponseMetadata["ResponseMetadata<br/>{fetchedAt, cachedUntil}"]
    end
    
    subgraph "Error Handling Flow"
        CustomErrorHandler["base.CustomErrorHandler()<br/>grpc-gateway integration"]
        HTTPStatusMapping["HTTP status code mapping"]
        JSONValidation["JSONTypeValidationMiddleware<br/>Request validation"]
    end
    
    ErrorResponse --> Error
    ErrorResponse --> ResponseMetadata
    
    CustomErrorHandler --> HTTPStatusMapping
    CustomErrorHandler --> JSONValidation
```

**Sources:** [pkg/api/v2/service.go:78-80](), [proto/api/v2/service.proto:840-847]()

### V1 Error Handling

The V1 API uses the `publicerr` package for consistent error responses:

```mermaid
graph TB
    subgraph "V1 Error Pattern"
        PublicErr["publicerr.Error<br/>Structured errors"]
        WriteHTTP["publicerr.WriteHTTP()<br/>HTTP error responses"]
        ErrorWrapping["publicerr.Wrap()<br/>Error context"]
    end
    
    subgraph "Common Error Scenarios"
        AuthErrors["401 Unauthorized<br/>Authentication failures"]
        ValidationErrors["400 Bad Request<br/>Input validation"]
        NotFoundErrors["404 Not Found<br/>Resource missing"]
        ServerErrors["500 Internal Server Error<br/>System failures"]
    end
    
    PublicErr --> WriteHTTP
    WriteHTTP --> ErrorWrapping
    
    ErrorWrapping --> AuthErrors
    ErrorWrapping --> ValidationErrors  
    ErrorWrapping --> NotFoundErrors
    ErrorWrapping --> ServerErrors
```

**Sources:** [pkg/api/apiv1/checkpoint.go:116-117](), [pkg/api/apiv1/cancellation.go:26-27](), [pkg/api/apiv1/events.go:30-31]()

# CQRS and Data Layer




## Purpose and Scope

This document covers Inngest's Command Query Responsibility Segregation (CQRS) implementation and data layer architecture. The CQRS system provides a unified interface for database operations across multiple database backends (PostgreSQL and SQLite), handles entity persistence for apps, functions, events, runs, and traces, and integrates with the execution system for state management.

For information about specific API endpoints that use this data layer, see [API Services and gRPC](#6.1). For details about tracing data collection and observability, see [Tracing and Observability](#6.3).

## CQRS Architecture Overview

The CQRS system is built around the `cqrs.Manager` interface, which provides unified access to all database operations. The core implementation uses a wrapper pattern to abstract database-specific details while maintaining type safety through SQLC-generated code.

```mermaid
graph TB
    subgraph "CQRS Interface Layer"
        Manager["cqrs.Manager"]
        TxManager["cqrs.TxManager"]
    end
    
    subgraph "Implementation Layer"
        Wrapper["base_cqrs.wrapper"]
        Queries["sqlc.Querier"]
    end
    
    subgraph "Database Abstraction"
        PostgresQueries["sqlc_postgres.Queries"]
        SqliteQueries["sqlc_sqlite.Queries"]
        Normalizer["NormalizedQueries"]
    end
    
    subgraph "Database Backends"
        PostgreSQL[("PostgreSQL")]
        SQLite[("SQLite")]
    end
    
    Manager --> Wrapper
    TxManager --> Wrapper
    Wrapper --> Queries
    
    Queries --> Normalizer
    Normalizer --> PostgresQueries
    Normalizer --> SqliteQueries
    
    PostgresQueries --> PostgreSQL
    SqliteQueries --> SQLite
```

The `wrapper` struct implements both `cqrs.Manager` and `cqrs.TxManager` interfaces, providing seamless transaction management and database operations. The system automatically detects the database driver and routes operations through the appropriate SQLC-generated queries.

Sources: [pkg/cqrs/base_cqrs/cqrs.go:58-67](), [pkg/cqrs/base_cqrs/cqrs.go:69-75]()

## Database Backend Selection and Normalization

Inngest supports both PostgreSQL and SQLite backends through a normalization layer that ensures consistent interfaces across different database systems. The `NewQueries` function determines the appropriate backend based on the driver string.

```mermaid
graph LR
    subgraph "Driver Detection"
        DriverCheck{"driver == 'postgres'?"}
    end
    
    subgraph "PostgreSQL Path"
        PostgresNormalized["sqlc_postgres.NewNormalized()"]
        PostgresOpts["NewNormalizedOpts"]
    end
    
    subgraph "SQLite Path"
        SqliteQueries["sqlc.New()"]
    end
    
    subgraph "Result"
        UnifiedQuerier["sqlc.Querier"]
    end
    
    DriverCheck -->|Yes| PostgresNormalized
    DriverCheck -->|No| SqliteQueries
    PostgresOpts --> PostgresNormalized
    
    PostgresNormalized --> UnifiedQuerier
    SqliteQueries --> UnifiedQuerier
```

The PostgreSQL backend includes connection pooling configuration through `NewNormalizedOpts`, while SQLite uses simpler direct queries. The normalization layer in `db_normalization.go` converts PostgreSQL-specific responses to match the SQLite interface, ensuring API consistency.

Sources: [pkg/cqrs/base_cqrs/cqrs.go:48-56](), [pkg/cqrs/base_cqrs/sqlc/postgres/db_normalization.go:21-29]()

## Entity Management System

The CQRS layer manages several core entities within Inngest's execution model. Each entity has dedicated CRUD operations and specific business logic handling.

### Core Entity Types

| Entity | Purpose | Key Operations |
|--------|---------|----------------|
| `cqrs.App` | Application registration and metadata | `UpsertApp`, `GetAppByURL`, `UpdateAppError` |
| `cqrs.Function` | Function definitions and configuration | `InsertFunction`, `GetFunctionsByAppID`, `UpdateFunctionConfig` |
| `cqrs.Event` | Event ingestion and storage | `InsertEvent`, `GetEventsByExpressions`, `GetEventsIDbound` |
| `cqrs.FunctionRun` | Function execution tracking | `InsertFunctionRun`, `GetFunctionRun`, `GetFunctionRunsTimebound` |
| `cqrs.OtelSpan` | OpenTelemetry span data | `GetSpansByRunID`, `GetSpansByDebugSessionID` |

### App Management Operations

The system provides comprehensive app lifecycle management with automatic URL normalization and checksum-based deduplication:

```mermaid
graph TB
    subgraph "App Operations"
        UpsertApp["UpsertApp()"]
        GetAppByURL["GetAppByURL()"]
        GetAppByChecksum["GetAppByChecksum()"]
        UpdateAppError["UpdateAppError()"]
        DeleteApp["DeleteApp()"]
    end
    
    subgraph "App Resolution Chain"
        URLNorm["util.NormalizeAppURL()"]
        ChecksumLookup["Checksum-based Lookup"]
        AppEntity["cqrs.App"]
    end
    
    UpsertApp --> URLNorm
    GetAppByURL --> URLNorm
    URLNorm --> ChecksumLookup
    ChecksumLookup --> AppEntity
    
    GetAppByChecksum --> AppEntity
    UpdateAppError --> AppEntity
    DeleteApp --> AppEntity
```

Sources: [pkg/cqrs/base_cqrs/cqrs.go:648-675](), [pkg/cqrs/base_cqrs/cqrs.go:619-627]()

## Transaction Management

The CQRS system provides transaction support through the `TxManager` interface, allowing atomic operations across multiple database calls. Transactions are managed through the `WithTx` method pattern.

```mermaid
sequenceDiagram
    participant Client
    participant Manager as "cqrs.Manager"  
    participant TxWrapper as "wrapper (with tx)"
    participant DB as "Database"
    
    Client->>Manager: WithTx(ctx)
    Manager->>DB: BeginTx(ctx, nil)
    DB-->>Manager: *sql.Tx
    Manager-->>Client: TxManager
    
    Client->>TxWrapper: DatabaseOperation()
    TxWrapper->>DB: SQL Query
    DB-->>TxWrapper: Result
    TxWrapper-->>Client: Response
    
    Client->>TxWrapper: Commit(ctx)
    TxWrapper->>DB: tx.Commit()
    DB-->>TxWrapper: Success/Error
    TxWrapper-->>Client: Error/nil
```

The transaction wrapper maintains the same interface as the non-transactional version, allowing transparent operation switching. Failed transactions can be rolled back using the `Rollback` method.

Sources: [pkg/cqrs/base_cqrs/cqrs.go:435-458](), [pkg/cqrs/base_cqrs/cqrs.go:460-466]()

## OpenTelemetry Span Processing

The CQRS layer includes sophisticated OpenTelemetry span processing capabilities, converting raw span data into structured entities with support for debugging and trace visualization.

### Span Data Transformation

```mermaid
graph TB
    subgraph "Raw Span Data"
        SpanFragments["Span Fragments (JSON)"]
        Attributes["Raw Attributes"]
        Timestamps["Start/End Times"]
    end
    
    subgraph "Processing Pipeline"
        FragmentParser["Fragment Parser"]
        AttributeExtractor["meta.ExtractTypedValues()"]
        SpanBuilder["OtelSpan Builder"]
    end
    
    subgraph "Structured Output"
        OtelSpan["cqrs.OtelSpan"]
        ExtractedValues["meta.ExtractedValues"]
        SpanHierarchy["Parent-Child Relations"]
    end
    
    SpanFragments --> FragmentParser
    Attributes --> AttributeExtractor
    Timestamps --> SpanBuilder
    
    FragmentParser --> SpanBuilder
    AttributeExtractor --> ExtractedValues
    SpanBuilder --> OtelSpan
    OtelSpan --> SpanHierarchy
```

The system handles complex span relationships, including dynamic span IDs for step execution tracking and debug session management. Special processing handles I/O references and span output encoding.

Sources: [pkg/cqrs/base_cqrs/cqrs.go:160-349](), [pkg/cqrs/base_cqrs/cqrs.go:351-370]()

## Queue Snapshot Management

The CQRS system includes functionality for managing execution queue snapshots, providing point-in-time queue state persistence for recovery and debugging purposes.

### Snapshot Storage Strategy

```mermaid
graph LR
    subgraph "Snapshot Creation"
        QueueSnapshot["cqrs.QueueSnapshot"]
        Serializer["JSON Marshal"]
        Chunker["Chunk Splitter"]
    end
    
    subgraph "Storage Layer"
        Chunks["Snapshot Chunks"]
        ChunkTable[("queue_snapshot_chunks")]
        CleanupJob["Cleanup Old Snapshots"]
    end
    
    subgraph "Retrieval"
        ChunkAssembler["Chunk Assembler"]
        Deserializer["JSON Unmarshal"]
        RestoredSnapshot["Restored QueueSnapshot"]
    end
    
    QueueSnapshot --> Serializer
    Serializer --> Chunker
    Chunker --> Chunks
    Chunks --> ChunkTable
    
    ChunkTable --> ChunkAssembler
    ChunkAssembler --> Deserializer
    Deserializer --> RestoredSnapshot
    
    ChunkTable --> CleanupJob
```

Snapshots are automatically chunked based on `consts.StartMaxQueueChunkSize` to handle large queue states, and old snapshots are cleaned up asynchronously to prevent storage bloat.

Sources: [pkg/cqrs/base_cqrs/cqrs.go:514-563](), [pkg/cqrs/base_cqrs/cqrs.go:468-489]()

## Integration with Tracing System

The data layer integrates closely with Inngest's tracing system through the `tracer_sqlc.go` implementation, which exports OpenTelemetry spans directly to the database for persistence and analysis.

### Tracing Data Flow

```mermaid
graph TB
    subgraph "OpenTelemetry Layer"
        TracerProvider["TracerProvider"]
        ReadOnlySpan["ReadOnlySpan[]"]
    end
    
    subgraph "Database Exporter"
        DbExporter["dbExporter"]
        AttributeProcessor["Attribute Processor"]
        SpanInserter["InsertSpan()"]
    end
    
    subgraph "Database Storage"
        SpansTable[("spans")]
        AttributesSeparated["Separated Attributes"]
        OutputData["Output/Input Data"]
    end
    
    TracerProvider --> DbExporter
    ReadOnlySpan --> AttributeProcessor
    AttributeProcessor --> SpanInserter
    SpanInserter --> SpansTable
    
    AttributeProcessor --> AttributesSeparated
    AttributeProcessor --> OutputData
```

The exporter processes spans by extracting key attributes like `RunID`, `AppID`, `FunctionID`, and separating large payload data (input/output) from the main attributes for efficient storage and querying.

Sources: [pkg/tracing/tracer_sqlc.go:18-24](), [pkg/tracing/tracer_sqlc.go:26-262]()