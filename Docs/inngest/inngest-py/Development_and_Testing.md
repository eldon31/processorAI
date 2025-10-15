This document provides a comprehensive guide for developers working with or contributing to the Inngest Python SDK. It covers setting up a development environment, running tests, and understanding the continuous integration and deployment pipeline.

## Development Environment Setup

Setting up a development environment for the Inngest Python SDK requires Python 3.10 or newer. The SDK supports Python versions from 3.10 up to 3.13 as specified in the project configuration.

```mermaid
graph TD
    subgraph "Development Setup"
        Clone["Clone Repository<br/>github.com/inngest/inngest-py"]
        Install["Install Dependencies<br/>make install"]
        Dev["Run Development Server<br/>inngest-cli dev"]
    end
    
    subgraph "SDK Requirements"
        Python["Python >=3.10"]
        CoreDeps["Core Dependencies<br/>httpx, jcs, pydantic, typing-extensions"]
        OptionalDeps["Optional Dependencies<br/>protobuf, psutil, websockets"]
    end
    
    Clone --> Install
    Install --> Dev
    Python --> Install
    CoreDeps --> Install
    OptionalDeps -.-> Install
```

The project uses a Makefile for common development tasks including installation, testing, and building. To set up your development environment:

1. Clone the repository
2. Run `make install` to install all dependencies
3. Run tests with `make utest` (unit tests) or `make itest` (integration tests)

Sources: [pkg/inngest/pyproject.toml:1-36](), [.github/workflows/inngest.yml:42-45]()

## Local Development Server

The Inngest SDK integrates with the Inngest CLI development server for local testing of functions. The `dev_server` module manages a subprocess that runs `inngest-cli dev` with specific configuration.

### Development Server Architecture

```mermaid
graph TD
    subgraph "DevServer Components"
        Server["_Server class"]
        CommandRunner["_CommandRunner"]
        NPX["npx inngest-cli@latest dev"]
    end
    
    subgraph "Server Management"
        Start["start()"]
        WaitForServer["_wait_for_server()"]
        HealthCheck["POST /v0/connect/start"]
        Stop["stop()"]
    end
    
    subgraph "Configuration"
        Port["DEV_SERVER_PORT (default: 8288)"]
        Logs["DEV_SERVER_LOGS"]
        Enabled["DEV_SERVER_ENABLED"]
    end
    
    Server --> CommandRunner
    CommandRunner --> NPX
    Start --> WaitForServer
    WaitForServer --> HealthCheck
    Port --> Server
    Logs --> Server
    Enabled --> Server
```

The development server implementation includes:

- **Process Management**: Uses `subprocess.Popen` to run the Inngest CLI dev server
- **Health Checking**: Polls the `/v0/connect/start` endpoint until the server is ready
- **Configuration**: Supports environment variables for port, logging, and enabling/disabling
- **Artifact Collection**: Optionally writes logs to `artifacts/dev_server.log` for debugging

```mermaid
graph TD
    subgraph "pytest Integration"
        Configure["pytest_configure()"]
        Unconfigure["pytest_unconfigure()"]
        DevServerInstance["dev_server.server"]
    end
    
    subgraph "Test Execution Flow"
        StartServer["server.start()"]
        RunTests["Execute Test Suite"]
        StopServer["server.stop()"]
    end
    
    Configure --> StartServer
    StartServer --> RunTests
    RunTests --> StopServer
    StopServer --> Unconfigure
    DevServerInstance --> Configure
    DevServerInstance --> Unconfigure
```

The development server is automatically managed by pytest hooks in both test packages, ensuring a clean test environment for each test run.

Sources: [pkg/inngest/inngest/experimental/dev_server/dev_server.py:15-94](), [tests/test_inngest/conftest.py:5-10](), [tests/test_inngest_encryption/conftest.py:5-10]()

## Testing Infrastructure

The Inngest Python SDK employs a comprehensive testing infrastructure with specialized test helpers, GraphQL API integration, and structured test case patterns.

### Test Organization and Architecture

```mermaid
graph TD
    subgraph "Test Packages"
        TestInngest["tests/test_inngest/"]
        TestEncryption["tests/test_inngest_encryption/"]
        TestCore["pkg/test_core/"]
    end
    
    subgraph "Test Infrastructure"
        ConfTest["conftest.py<br/>pytest configuration"]
        Helper["test_core.helper<br/>Client utilities"]
        DevServer["dev_server integration"]
    end
    
    subgraph "Test Utilities"
        GQLClient["gql.Client<br/>GraphQL API"]
        RunStatus["RunStatus enum"]
        WaitForRun["wait_for_run_status()"]
        GetStepOutput["get_step_output()"]
    end
    
    TestInngest --> ConfTest
    TestEncryption --> ConfTest
    TestCore --> Helper
    Helper --> GQLClient
    Helper --> RunStatus
    Helper --> WaitForRun
    Helper --> GetStepOutput
    ConfTest --> DevServer
```

### Test Helper System

The `test_core.helper` module provides essential utilities for interacting with the development server's GraphQL API:

```mermaid
graph TD
    subgraph "Helper Client API"
        Client["_Client class"]
        GQLEndpoint["/v0/gql endpoint"]
        
        GetHistory["_get_history(run_id)"]
        GetStepOutput["get_step_output(run_id, step_id)"]
        GetRunIds["get_run_ids_from_event_id()"]
        WaitForStatus["wait_for_run_status()"]
    end
    
    subgraph "GraphQL Queries"
        HistoryQuery["GetHistory query"]
        RunQuery["GetRun query"]
        EventQuery["GetRunFromEventID query"]
    end
    
    subgraph "Run Status Management"
        RunStatus["RunStatus enum<br/>CANCELLED, COMPLETED, FAILED, RUNNING"]
        EndedStatuses["ended_statuses set"]
        RunModel["_Run model"]
    end
    
    Client --> GQLEndpoint
    GetHistory --> HistoryQuery
    GetStepOutput --> HistoryQuery
    GetRunIds --> EventQuery
    WaitForStatus --> RunQuery
    WaitForStatus --> RunStatus
    RunStatus --> EndedStatuses
    WaitForStatus --> RunModel
```

### Test Case Patterns

Test cases follow a structured pattern with case-based organization:

```mermaid
graph TD
    subgraph "Test Case Structure"
        BaseCase["base.Case"]
        TestName["base.create_test_name(__file__)"]
        EventName["base.create_event_name()"]
        FnId["base.create_fn_id()"]
        State["Custom State class"]
    end
    
    subgraph "Test Execution Flow"
        CreateFunction["@client.create_function()"]
        SendEvent["client.send_sync()"]
        WaitForRun["wait_for_run_id()"]
        WaitForCompletion["wait_for_run_status()"]
        Assertions["assert results"]
    end
    
    BaseCase --> TestName
    BaseCase --> EventName
    BaseCase --> FnId
    TestName --> CreateFunction
    CreateFunction --> SendEvent
    SendEvent --> WaitForRun
    WaitForRun --> WaitForCompletion
    WaitForCompletion --> Assertions
    State --> Assertions
```

Test cases are organized in separate files under feature directories (e.g., `test_function/cases/`, `test_registration/cases/`) with each test implementing a complete scenario from function creation to result verification.

Sources: [pkg/test_core/test_core/helper.py:33-216](), [tests/test_inngest/test_function/cases/middleware_parallel_steps.py:26-161](), [tests/conftest.py:3-6]()

### Middleware and Parallel Step Testing

The SDK includes specialized tests for complex scenarios like middleware integration and parallel step execution:

```mermaid
graph TD
    subgraph "Middleware Test Pattern"
        CustomMiddleware["_Middleware class<br/>extends MiddlewareSync"]
        TransformOutput["transform_output()<br/>captures results"]
        StateCollection["_State.results[]"]
    end
    
    subgraph "Parallel Steps Test"
        ParallelGroup["ctx.group.parallel()"]
        Step1["ctx.step.run('1.1')"]
        Step2["ctx.step.run('1.2')"]
        Converge["ctx.step.run('converge')<br/>workaround for server bug"]
    end
    
    subgraph "Test Challenges"
        RaceConditions["Race conditions in parallel execution"]
        Flakiness["Test marked as flaky"]
        ServerBug["Discovery step timing bug"]
    end
    
    CustomMiddleware --> TransformOutput
    TransformOutput --> StateCollection
    ParallelGroup --> Step1
    ParallelGroup --> Step2
    Step1 --> Converge
    Step2 --> Converge
    ParallelGroup --> RaceConditions
    RaceConditions --> Flakiness
    Converge --> ServerBug
```

The parallel steps test demonstrates several important patterns:
- **Middleware Integration**: Custom middleware classes capture step execution results
- **State Management**: Test state classes collect results across async execution
- **Parallel Execution**: Using `ctx.group.parallel()` for concurrent step execution
- **Known Issues**: Workarounds for server-side bugs and race conditions

Test cases include both sync and async variants, with helper functions like `base.asyncify()` to convert sync functions for async contexts.

Sources: [tests/test_inngest/test_function/cases/middleware_parallel_steps.py:1-172]()

## CI/CD Pipeline

The Inngest Python SDK uses GitHub Actions for continuous integration and deployment. The pipeline ensures that all code changes are tested across multiple Python versions before being released.

```mermaid
flowchart TD
    subgraph "GitHub Actions Workflow"
        Trigger["Trigger<br/>Push to main, Tags, or PR"]
        
        subgraph "Test Jobs"
            ITest["Integration Tests<br/>Python 3.10, 3.13"]
            UTest["Unit Tests<br/>Python 3.10, 3.13"]
            TypeCheck["Type Check<br/>Python 3.10, 3.13"]
            Lint["Lint<br/>Python 3.10, 3.13"]
        end
        
        PublishPyPI["Publish to PyPI<br/>Python 3.10"]
    end
    
    Trigger --> ITest
    Trigger --> UTest
    Trigger --> TypeCheck
    Trigger --> Lint
    
    ITest --> PublishPyPI
    UTest --> PublishPyPI
    TypeCheck --> PublishPyPI
    Lint --> PublishPyPI
    
    Tag["Tag starts with<br/>inngest@"] --> PublishPyPI
```

The CI/CD pipeline includes:

1. **Integration Testing**: Runs the integration test suite on Python 3.10 and 3.13
2. **Unit Testing**: Runs the unit test suite on Python 3.10 and 3.13
3. **Type Checking**: Verifies type annotations on Python 3.10 and 3.13
4. **Linting**: Checks code style and quality on Python 3.10 and 3.13
5. **PyPI Publication**: Publishes the package to PyPI when a tag starting with "inngest@" is pushed

The pipeline runs on push to main, tags, and pull requests that affect Python code, Makefiles, pyproject.toml files, or GitHub Actions configuration.

Sources: [.github/workflows/inngest.yml:1-136](), [.github/workflows/inngest_encryption.yml:1-121]()

### Package Publication Process

When a new release is tagged with a version prefixed by "inngest@" or "inngest_encryption@", the GitHub Actions workflow will automatically build the package and publish it to PyPI.

```mermaid
sequenceDiagram
    participant Developer
    participant GitHub as GitHub Actions
    participant PyPI
    
    Developer->>GitHub: Push tag "inngest@x.y.z"
    GitHub->>GitHub: Run test jobs
    GitHub->>GitHub: Build package
    GitHub->>PyPI: Upload package
    PyPI->>PyPI: Publish package
```

The publication process uses GitHub's OIDC token for secure publishing to PyPI without storing credentials in the repository.

Sources: [.github/workflows/inngest.yml:71-102](), [.github/workflows/inngest_encryption.yml:56-86]()

## Cloud Environment Testing

The SDK includes comprehensive tests for cloud environment integration, including branch environment support and request signing validation.

### Cloud Branch Environment Test Pattern

```mermaid
graph TD
    subgraph "Cloud Environment Test Flow"
        ClientSetup["inngest.Inngest(<br/>app_id, env, signing_key)"]
        FunctionDef["@client.create_function()"]
        ServeSetup["self.serve(client, [fn])"]
    end
    
    subgraph "In-Band Sync Request"
        ReqBody["InBandSynchronizeRequest<br/>JSON body"]
        ReqSig["net.sign_request()<br/>HMAC signature"]
        PutRequest["PUT request with headers"]
    end
    
    subgraph "Response Validation"
        StatusCode["assert res.status_code == 200"]
        Headers["x-inngest-env, x-inngest-expected-server-kind"]
        SigValidation["net.validate_response_sig()"]
        ResponseBody["JSON response validation"]
    end
    
    ClientSetup --> FunctionDef
    FunctionDef --> ServeSetup
    ServeSetup --> ReqBody
    ReqBody --> ReqSig
    ReqSig --> PutRequest
    PutRequest --> StatusCode
    StatusCode --> Headers
    Headers --> SigValidation
    SigValidation --> ResponseBody
```

### Environment Configuration Details

```mermaid
graph TD
    subgraph "Test Configuration"
        SigningKey["signing_key: 'signkey-prod-000000'"]
        Environment["env: 'my-env'"]
        AppId["app_id: framework-test_name"]
    end
    
    subgraph "Request Headers"
        Signature["x-inngest-signature"]
        SyncKind["x-inngest-sync-kind: 'in_band'"]
    end
    
    subgraph "Response Headers"
        EnvHeader["x-inngest-env: 'my-env'"]
        ServerKind["x-inngest-expected-server-kind: 'cloud'"]
        SyncResponse["x-inngest-sync-kind: 'in_band'"]
    end
    
    subgraph "Response Validation"
        AppIdCheck["app_id matches client"]
        FrameworkCheck["framework value"]
        FunctionConfig["functions array with steps"]
        InspectionData["inspection object with capabilities"]
    end
    
    SigningKey --> Signature
    Environment --> EnvHeader
    SyncKind --> SyncResponse
    EnvHeader --> AppIdCheck
    ServerKind --> FrameworkCheck
    FrameworkConfig --> FunctionConfig
    InspectionData --> AppIdCheck
```

The test validates that the SDK properly:
- Signs requests using HMAC with the provided signing key
- Includes environment information in response headers
- Returns correctly formatted function configuration data
- Validates response signatures from the cloud service
- Includes comprehensive inspection data with SDK capabilities

Sources: [tests/test_inngest/test_registration/cases/cloud_branch_env.py:12-122]()

## Debugging and Troubleshooting

For easier debugging during development and CI, the SDK includes features to capture and report information about test failures.

### Dev Server Logs

The CI/CD pipeline includes a step to upload development server logs as artifacts when tests fail, making it easier to diagnose issues.

```mermaid
flowchart TD
    subgraph "Debugging Flow"
        TestRun["Run Tests"]
        TestFail{"Tests Failed?"}
        UploadLogs["Upload Dev Server Logs<br/>as Artifact"]
        Continue["Continue"]
    end
    
    TestRun --> TestFail
    TestFail -->|Yes| UploadLogs
    TestFail -->|No| Continue
    UploadLogs --> Continue
```

The server logs are written to `./tests/test_inngest/artifacts/dev_server.log` and are automatically uploaded to GitHub Actions when tests fail in the CI environment.

Sources: [.github/workflows/inngest.yml:47-52]()

## Special Testing Considerations

Some SDK features require special testing approaches due to their asynchronous or concurrent nature.

### Testing Parallel Steps

Testing parallel steps can be challenging due to race conditions inherent in parallel execution. Some tests for parallel steps are marked as expected to fail (`@pytest.mark.xfail`) until parallelism improvements are implemented.

Sources: [tests/test_inngest/test_function/cases/middleware_parallel_steps.py:1-6](), [tests/test_inngest/test_function/cases/middleware_parallel_steps.py:88-88]()

## Development Roadmap

The codebase includes comments indicating planned improvements, such as:

1. Parallelism improvements to address flakiness in parallel step tests
2. Checks to ensure that git tags match package versions during publishing

These upcoming changes are documented in code comments and can be found throughout the codebase.

Sources: [tests/test_inngest/test_function/cases/middleware_parallel_steps.py:87-88](), [.github/workflows/inngest.yml:80-81]()