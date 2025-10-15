def component_customizer(route: HTTPRoute, component: OpenAPITool | OpenAPIResource | OpenAPIResourceTemplate) -> None:
    if "deprecated" in route.extensions:
        component.tags.add("deprecated")
```

**Sources:** [src/fastmcp/server/openapi.py:798-812](), [src/fastmcp/server/openapi.py:930-939]()

### Output Schema Generation

The system extracts output schemas from OpenAPI response definitions for structured tool results:

```python
def extract_output_schema_from_responses(
    responses: dict[str, ResponseInfo],
    schema_definitions: dict[str, JsonSchema],
    openapi_version: str | None
) -> dict[str, Any] | None:
    # Prioritizes 2xx responses
    # Merges multiple response schemas
    # Adds x-fastmcp-wrap-result for structured output control
```

**Sources:** [src/fastmcp/utilities/openapi.py:1098-1200]()

### Error Handling

Comprehensive error handling for HTTP requests, parameter validation, and schema resolution:

- **Parameter Validation**: Missing required path parameters raise `ToolError`
- **HTTP Errors**: 4xx/5xx responses converted to `ValueError` with detailed messages  
- **Schema Resolution**: External references raise clear error messages
- **Connection Errors**: Network issues converted to `ValueError`

**Sources:** [src/fastmcp/server/openapi.py:504-520](), [src/fastmcp/server/openapi.py:623-639](), [tests/utilities/openapi/test_openapi_advanced.py:655-665]()