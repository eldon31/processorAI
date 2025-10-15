This document covers FastAPI's application and routing system, including the core `FastAPI` application class, route organization through `APIRouter`, individual route handling via `APIRoute` and `APIWebSocketRoute`, and the request processing pipeline. For information about dependency injection mechanics, see [Dependency Injection](#2.2). For details about parameter validation and handling, see [Parameter Validation and Handling](#2.3).

## FastAPI Application Class

The `FastAPI` class serves as the main application entry point, inheriting from Starlette's `Starlette` class while adding FastAPI-specific functionality including automatic API documentation, dependency injection, and enhanced routing capabilities.

### Application Structure

```mermaid
graph TD
    FastAPI["FastAPI"] --> Starlette["starlette.Starlette"]
    FastAPI --> router["self.router: APIRouter"]
    FastAPI --> openapi_schema["openapi_schema: Dict"]
    FastAPI --> docs_url["docs_url: str"]
    FastAPI --> redoc_url["redoc_url: str"]
    
    router --> routes["List[BaseRoute]"]
    routes --> APIRoute["APIRoute"]
    routes --> APIWebSocketRoute["APIWebSocketRoute"]
    routes --> Mount["starlette.Mount"]
    
    FastAPI --> middleware["middleware: List[Middleware]"]
    FastAPI --> exception_handlers["exception_handlers: Dict"]
```

The `FastAPI` constructor accepts extensive configuration options for OpenAPI documentation, CORS, middleware, and routing behavior. Key configuration includes `title`, `description`, `version` for API metadata, `docs_url` and `redoc_url` for documentation endpoints, and `default_response_class` for response handling.

Sources: [fastapi/applications.py:48-640](), [fastapi/__init__.py:7]()

### Route Definition Methods

The `FastAPI` class provides HTTP method decorators that create `APIRoute` instances:

```mermaid
graph LR
    FastAPI --> get["@app.get()"]
    FastAPI --> post["@app.post()"]
    FastAPI --> put["@app.put()"]
    FastAPI --> delete["@app.delete()"]
    FastAPI --> patch["@app.patch()"]
    FastAPI --> head["@app.head()"]
    FastAPI --> options["@app.options()"]
    FastAPI --> trace["@app.trace()"]
    
    get --> APIRoute["APIRoute"]
    post --> APIRoute
    put --> APIRoute
    delete --> APIRoute
    patch --> APIRoute
    head --> APIRoute
    options --> APIRoute
    trace --> APIRoute
```

Each decorator method creates an `APIRoute` instance with the specified HTTP method, path, and endpoint function, then adds it to the application's router.

Sources: [fastapi/applications.py:697-1007]()

## APIRouter System

The `APIRouter` class enables modular route organization by grouping related path operations that can be included in the main application or other routers.

### Router Hierarchy

```mermaid
graph TD
    FastAPI --> include_router["app.include_router()"]
    include_router --> APIRouter1["APIRouter(prefix='/users')"]
    include_router --> APIRouter2["APIRouter(prefix='/items')"]
    
    APIRouter1 --> user_routes["User Routes"]
    APIRouter2 --> item_routes["Item Routes"]
    
    user_routes --> get_users["@router.get('/')"]
    user_routes --> create_user["@router.post('/')"]
    
    item_routes --> get_items["@router.get('/')"]
    item_routes --> create_item["@router.post('/')"]
    
    get_users --> final_path1["Final: GET /users/"]
    create_user --> final_path2["Final: POST /users/"]
    get_items --> final_path3["Final: GET /items/"]
    create_item --> final_path4["Final: POST /items/"]
```

The `APIRouter` constructor accepts parameters including `prefix` for path prefixing, `tags` for OpenAPI organization, `dependencies` for shared dependencies, and `default_response_class` for response handling.

Sources: [fastapi/routing.py:596-621](), [fastapi/routing.py:623-740]()

### Router Registration

The `include_router` method merges an `APIRouter` into the application by copying its routes and applying prefix, tag, and dependency transformations:

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `router` | APIRouter instance to include | `user_router` |
| `prefix` | Path prefix for all routes | `"/api/v1"` |
| `tags` | OpenAPI tags to apply | `["users"]` |
| `dependencies` | Dependencies to add to all routes | `[Depends(get_current_user)]` |

Sources: [fastapi/applications.py:1009-1106]()

## Route Classes

### APIRoute

The `APIRoute` class represents individual HTTP endpoints, handling path compilation, dependency analysis, and request processing setup.

```mermaid
graph TD
    APIRoute --> path["path: str"]
    APIRoute --> endpoint["endpoint: Callable"]
    APIRoute --> methods["methods: Set[str]"]
    APIRoute --> dependant["dependant: Dependant"]
    APIRoute --> response_model["response_model: Any"]
    APIRoute --> status_code["status_code: int"]
    
    dependant --> path_params["path_params: List[ModelField]"]
    dependant --> query_params["query_params: List[ModelField]"]
    dependant --> header_params["header_params: List[ModelField]"]
    dependant --> body_params["body_params: List[ModelField]"]
    dependant --> dependencies_list["dependencies: List[Dependant]"]
    
    APIRoute --> get_route_handler["get_route_handler()"]
    get_route_handler --> request_handler["Callable[[Request], Response]"]
```

The `APIRoute` constructor analyzes the endpoint function signature using `get_dependant()` to extract parameter information and build the dependency tree.

Sources: [fastapi/routing.py:429-593]()

### APIWebSocketRoute

The `APIWebSocketRoute` class handles WebSocket connections with similar dependency resolution but different connection lifecycle:

```mermaid
sequenceDiagram
    participant Client
    participant APIWebSocketRoute
    participant get_websocket_app
    participant solve_dependencies
    participant endpoint
    
    Client->>APIWebSocketRoute: WebSocket connection
    APIWebSocketRoute->>get_websocket_app: Create WebSocket app
    get_websocket_app->>solve_dependencies: Resolve dependencies
    solve_dependencies->>endpoint: Call with resolved values
    endpoint->>Client: WebSocket communication
```

Sources: [fastapi/routing.py:389-427]()

## Request Processing Pipeline

### Request Handler Creation

The `get_request_handler` function creates the actual ASGI application that processes HTTP requests:

```mermaid
graph TD
    get_request_handler --> dependant_analysis["Analyze Dependant"]
    get_request_handler --> body_field["Create body_field"]
    get_request_handler --> response_config["Configure response"]
    
    dependant_analysis --> async_check["Check if async"]
    body_field --> form_check["Check if form data"]
    response_config --> response_class["Set response_class"]
    
    get_request_handler --> request_app["async def app(request)"]
    
    request_app --> parse_body["Parse request body"]
    request_app --> solve_dependencies_call["solve_dependencies()"]
    request_app --> run_endpoint["run_endpoint_function()"]
    request_app --> serialize_response["serialize_response()"]
    request_app --> create_response["Create Response object"]
```

Sources: [fastapi/routing.py:218-358]()

### Request Flow

The generated request handler follows this processing sequence:

```mermaid
sequenceDiagram
    participant Request
    participant Handler as "Request Handler"
    participant Dependencies as "Dependency Resolver" 
    participant Endpoint as "Endpoint Function"
    participant Response as "Response Serializer"
    
    Request->>Handler: HTTP Request
    Handler->>Handler: Parse body (JSON/Form)
    Handler->>Dependencies: solve_dependencies()
    Dependencies->>Dependencies: Resolve path/query/header params
    Dependencies->>Dependencies: Resolve function dependencies
    Dependencies->>Handler: Resolved values + errors
    
    alt No validation errors
        Handler->>Endpoint: Call with resolved values
        Endpoint->>Handler: Return value
        Handler->>Response: serialize_response()
        Response->>Handler: Serialized content
        Handler->>Request: HTTP Response
    else Validation errors
        Handler->>Request: 422 Validation Error
    end
```

Sources: [fastapi/routing.py:241-356](), [fastapi/dependencies/utils.py:572-689]()

## Route Registration Process

### Route Creation and Registration

When routes are defined using decorators, the following process occurs:

```mermaid
graph TD
    decorator["@app.get('/items/{item_id}')"] --> create_route["Create APIRoute"]
    create_route --> compile_path["compile_path()"]
    create_route --> get_dependant_call["get_dependant()"]
    create_route --> analyze_signature["Analyze function signature"]
    
    compile_path --> path_regex["path_regex: Pattern"]
    compile_path --> param_convertors["param_convertors: Dict"]
    
    get_dependant_call --> extract_params["Extract parameters"]
    extract_params --> path_params_list["path_params: List[ModelField]"]
    extract_params --> query_params_list["query_params: List[ModelField]"]
    extract_params --> body_params_list["body_params: List[ModelField]"]
    
    analyze_signature --> response_model_field["Create response_field"]
    analyze_signature --> unique_id["Generate unique_id"]
    
    create_route --> add_to_router["Add to router.routes"]
```

The route registration process includes path compilation using Starlette's `compile_path`, dependency analysis via `get_dependant`, and OpenAPI schema preparation.

Sources: [fastapi/routing.py:430-571](), [fastapi/dependencies/utils.py:265-314]()

### Dependency Tree Construction

The `get_dependant` function recursively builds a dependency tree by analyzing function signatures:

| Component | Purpose | Location |
|-----------|---------|----------|
| `path_params` | URL path parameters | `dependant.path_params` |
| `query_params` | Query string parameters | `dependant.query_params` |
| `header_params` | HTTP header parameters | `dependant.header_params` |
| `cookie_params` | Cookie parameters | `dependant.cookie_params` |
| `body_params` | Request body parameters | `dependant.body_params` |
| `dependencies` | Sub-dependency functions | `dependant.dependencies` |

Sources: [fastapi/dependencies/utils.py:265-314](), [fastapi/dependencies/models.py:15-37]()

## OpenAPI Integration

### Schema Generation

The routing system automatically generates OpenAPI schemas through the `get_openapi_path` function:

```mermaid
graph TD
    APIRoute --> get_openapi_path["get_openapi_path()"]
    get_openapi_path --> operation_metadata["get_openapi_operation_metadata()"]
    get_openapi_path --> parameters_schema["_get_openapi_operation_parameters()"]
    get_openapi_path --> request_body_schema["get_openapi_operation_request_body()"]
    get_openapi_path --> security_schemes["get_openapi_security_definitions()"]
    
    operation_metadata --> operation_id["operationId"]
    operation_metadata --> summary["summary"]
    operation_metadata --> description["description"]
    operation_metadata --> tags["tags"]
    
    parameters_schema --> path_parameters["Path parameters"]
    parameters_schema --> query_parameters["Query parameters"]  
    parameters_schema --> header_parameters["Header parameters"]
    
    request_body_schema --> body_schema["Request body schema"]
    security_schemes --> security_definitions["Security definitions"]
```

Each `APIRoute` contributes to the OpenAPI schema by providing operation metadata, parameter schemas, request/response body schemas, and security definitions.

Sources: [fastapi/openapi/utils.py:254-439]()

### Route Matching

The route matching process uses Starlette's routing system with FastAPI enhancements:

```mermaid
sequenceDiagram
    participant Request
    participant Router
    participant Route as "APIRoute/APIWebSocketRoute"
    participant Handler
    
    Request->>Router: Incoming request
    Router->>Router: Iterate through routes
    Router->>Route: route.matches(scope)
    Route->>Route: Check path_regex
    Route->>Route: Check HTTP method
    
    alt Route matches
        Route->>Router: Match.FULL + child_scope
        Router->>Handler: route.app(scope, receive, send)
        Handler->>Request: Process request
    else No match
        Route->>Router: Match.NONE
        Router->>Router: Try next route
    end
```

The `matches` method on `APIRoute` and `APIWebSocketRoute` determines if a route should handle a specific request based on path pattern and HTTP method.

Sources: [fastapi/routing.py:589-593](), [fastapi/routing.py:422-426]()