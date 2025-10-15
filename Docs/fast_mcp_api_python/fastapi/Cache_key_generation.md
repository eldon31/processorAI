cache_key = (dependant.call, tuple(sorted(set(dependant.security_scopes or []))))
```

Cache behavior is controlled by the `use_cache` parameter in `Depends()` and can be disabled for dependencies that should be called multiple times.

Sources: [fastapi/dependencies/models.py:36-37](), [fastapi/dependencies/utils.py:631-644]()

### Generator Dependencies

Generator dependencies support resource management with automatic cleanup using context managers. The system distinguishes between sync and async generators:

- **Sync Generators**: Wrapped with `contextmanager_in_threadpool`
- **Async Generators**: Used directly as async context managers

Sources: [fastapi/dependencies/utils.py:553-560](), [fastapi/dependencies/utils.py:633-636]()

### Security Dependencies

Security dependencies integrate with FastAPI's security system through `SecurityRequirement` objects, which specify security schemes and required scopes.

Sources: [fastapi/dependencies/models.py:9-11](), [fastapi/dependencies/utils.py:150-171]()

## Integration with Routing

### Route Handler Integration

The routing system integrates dependency injection through the `get_request_handler` function, which creates request handlers that automatically resolve dependencies.

```mermaid
graph LR
    ROUTE["APIRoute.__init__()"] --> GET_DEP["get_dependant()"]
    GET_DEP --> FLAT_DEP["get_flat_dependant()"]
    FLAT_DEP --> HANDLER["get_request_handler()"]
    
    subgraph "Request Processing"
        REQUEST["HTTP Request"] --> SOLVE["solve_dependencies()"]
        SOLVE --> EXECUTE["run_endpoint_function()"]
        EXECUTE --> RESPONSE["HTTP Response"]
    end
    
    HANDLER --> REQUEST
```

The route analysis phase extracts dependency information and creates optimized structures for runtime resolution.

Sources: [fastapi/routing.py:555-561](), [fastapi/routing.py:292-299](), [fastapi/routing.py:218-358]()

### Dependency Overrides

The system supports dependency overrides through the `dependency_overrides_provider`, allowing replacement of dependencies during testing or runtime configuration.

Sources: [fastapi/dependencies/utils.py:599-613]()