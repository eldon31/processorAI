This document covers the FastMCP component system, which provides a unified framework for managing Tools, Resources, Prompts, and Resource Templates. It explains how these components are created, registered, managed, and composed within FastMCP servers.

For information about server composition and mounting mechanisms, see [Server Composition and Proxying](#2.3). For details about dependency injection and the Context system, see [Context System and Dependencies](#2.2).

## Component Type Hierarchy

FastMCP organizes all server capabilities into four main component types, each sharing common functionality through a base class architecture.

### Component Class Structure

```mermaid
graph TD
    FastMCPComponent["FastMCPComponent<br/>src/fastmcp/utilities/components.py"]
    
    subgraph "Tool Components"
        Tool["Tool<br/>src/fastmcp/tools/tool.py"]
        FunctionTool["FunctionTool<br/>src/fastmcp/tools/tool.py"] 
        TransformedTool["TransformedTool<br/>src/fastmcp/tools/tool_transform.py"]
    end
    
    subgraph "Resource Components"
        Resource["Resource<br/>src/fastmcp/resources/resource.py"]
        FunctionResource["FunctionResource<br/>src/fastmcp/resources/resource.py"]
        ResourceTemplate["ResourceTemplate<br/>src/fastmcp/resources/template.py"]
        FunctionResourceTemplate["FunctionResourceTemplate<br/>src/fastmcp/resources/template.py"]
    end
    
    subgraph "Prompt Components"
        Prompt["Prompt<br/>src/fastmcp/prompts/prompt.py"]
        FunctionPrompt["FunctionPrompt<br/>src/fastmcp/prompts/prompt.py"]
    end
    
    FastMCPComponent --> Tool
    FastMCPComponent --> Resource
    FastMCPComponent --> ResourceTemplate
    FastMCPComponent --> Prompt
    
    Tool --> FunctionTool
    Tool --> TransformedTool
    Resource --> FunctionResource
    ResourceTemplate --> FunctionResourceTemplate
    Prompt --> FunctionPrompt
```

**Sources**: [src/fastmcp/utilities/components.py:28-125](), [src/fastmcp/tools/tool.py:105-240](), [src/fastmcp/resources/resource.py:34-219](), [src/fastmcp/resources/template.py:53-314](), [src/fastmcp/prompts/prompt.py:65-262]()

### Base Component Properties

All FastMCP components inherit from `FastMCPComponent` and share these properties:

| Property | Type | Purpose |
|----------|------|---------|
| `name` | `str` | Unique identifier for the component |
| `title` | `str \| None` | Display title for UI purposes |
| `description` | `str \| None` | Human-readable description |
| `tags` | `set[str]` | Categorization tags for filtering |
| `meta` | `dict[str, Any] \| None` | Additional metadata |
| `enabled` | `bool` | Whether component is active |
| `key` | `str` | Internal bookkeeping identifier (may include prefixes) |

**Sources**: [src/fastmcp/utilities/components.py:28-69]()

## Component Manager Architecture

Each component type has a dedicated manager class that handles registration, retrieval, and execution. The managers follow a consistent pattern and support server composition through mounting.

### Manager System Overview

```mermaid
graph TD
    subgraph "FastMCP Server"
        Server["FastMCP<br/>server instance"]
        
        ToolManager["ToolManager<br/>_tool_manager"]
        ResourceManager["ResourceManager<br/>_resource_manager"] 
        PromptManager["PromptManager<br/>_prompt_manager"]
        
        Server --> ToolManager
        Server --> ResourceManager
        Server --> PromptManager
    end
    
    subgraph "Local Storage"
        LocalTools["_tools: dict[str, Tool]"]
        LocalResources["_resources: dict[str, Resource]"]
        LocalTemplates["_templates: dict[str, ResourceTemplate]"]
        LocalPrompts["_prompts: dict[str, Prompt]"]
        
        ToolManager --> LocalTools
        ResourceManager --> LocalResources
        ResourceManager --> LocalTemplates
        PromptManager --> LocalPrompts
    end
    
    subgraph "Mounted Servers"
        MountedServer1["MountedServer 1<br/>prefix: 'weather'"]
        MountedServer2["MountedServer 2<br/>prefix: 'db'"]
        
        ToolManager --> MountedServer1
        ToolManager --> MountedServer2
        ResourceManager --> MountedServer1
        ResourceManager --> MountedServer2
        PromptManager --> MountedServer1
        PromptManager --> MountedServer2
    end
    
    subgraph "Transformations"
        ToolTransformations["transformations:<br/>dict[str, ToolTransformConfig]"]
        ToolManager --> ToolTransformations
    end
```

**Sources**: [src/fastmcp/tools/tool_manager.py:25-255](), [src/fastmcp/resources/resource_manager.py:28-344](), [src/fastmcp/prompts/prompt_manager.py:21-204]()

### Manager Responsibilities

Each manager provides these core operations:

| Operation | Tool Manager | Resource Manager | Prompt Manager |
|-----------|--------------|------------------|----------------|
| **Add Component** | `add_tool(tool)` | `add_resource(resource)` | `add_prompt(prompt)` |
| **Get Component** | `get_tool(key)` | `read_resource(uri)` | `get_prompt(key)` |
| **List Components** | `list_tools()` | `list_resources()` | `list_prompts()` |
| **Execute/Use** | `call_tool(key, args)` | Templates: `create_resource()` | `render_prompt(name, args)` |

**Sources**: [src/fastmcp/tools/tool_manager.py:108-254](), [src/fastmcp/resources/resource_manager.py:275-344](), [src/fastmcp/prompts/prompt_manager.py:91-204]()

## Component Creation from Functions

FastMCP provides a consistent pattern for creating components from Python functions using static factory methods.

### Function-to-Component Creation Flow

```mermaid
graph LR
    subgraph "Python Function"
        PyFunc["def my_function(args):<br/>    return result"]
    end
    
    subgraph "Parsing & Validation"
        ParsedFunction["ParsedFunction.from_function()<br/>- Extract signature<br/>- Generate JSON schema<br/>- Validate constraints"]
    end
    
    subgraph "Component Creation"
        ToolFromFunction["Tool.from_function()"]
        ResourceFromFunction["Resource.from_function()"] 
        PromptFromFunction["Prompt.from_function()"]
        TemplateFromFunction["ResourceTemplate.from_function()"]
    end
    
    subgraph "Component Instances"
        FunctionTool_["FunctionTool<br/>- parameters: JSON schema<br/>- output_schema: JSON schema<br/>- fn: Callable"]
        FunctionResource_["FunctionResource<br/>- uri: AnyUrl<br/>- mime_type: str<br/>- fn: Callable"]
        FunctionPrompt_["FunctionPrompt<br/>- arguments: PromptArgument[]<br/>- fn: Callable"]
        FunctionResourceTemplate_["FunctionResourceTemplate<br/>- uri_template: str<br/>- parameters: JSON schema<br/>- fn: Callable"]
    end
    
    PyFunc --> ParsedFunction
    ParsedFunction --> ToolFromFunction
    ParsedFunction --> ResourceFromFunction
    ParsedFunction --> PromptFromFunction
    ParsedFunction --> TemplateFromFunction
    
    ToolFromFunction --> FunctionTool_
    ResourceFromFunction --> FunctionResource_
    PromptFromFunction --> FunctionPrompt_
    TemplateFromFunction --> FunctionResourceTemplate_
```

**Sources**: [src/fastmcp/tools/tool.py:354-491](), [src/fastmcp/resources/resource.py:168-219](), [src/fastmcp/prompts/prompt.py:156-262](), [src/fastmcp/resources/template.py:214-313]()

### Context Injection

All function-based components support automatic Context injection for accessing server capabilities:

```python
# Context parameter is automatically detected and injected
def my_tool(query: str, ctx: Context) -> str:
    ctx.logger.info(f"Processing query: {query}")
    return f"Result for {query}"
```

The parameter detection uses `find_kwarg_by_type()` to identify Context parameters and excludes them from the component's public schema.

**Sources**: [src/fastmcp/utilities/types.py:find_kwarg_by_type](), [src/fastmcp/tools/tool.py:407-412](), [src/fastmcp/resources/template.py:245-246]()

## Tool Transformation System

Tools can be transformed to create modified versions with different schemas, argument mappings, or custom behavior. This enables adaptation without code duplication.

### Tool Transformation Architecture

```mermaid
graph TD
    subgraph "Original Tool"
        ParentTool["Tool<br/>name: 'search'<br/>args: {q, category}"]
    end
    
    subgraph "Transformation Configuration"
        TransformConfig["ToolTransformConfig<br/>- name: 'find_products'<br/>- description: 'Search products'<br/>- arguments: ArgTransformConfig[]"]
        
        ArgTransform1["ArgTransform<br/>q -> query<br/>description: 'Search query'"]
        ArgTransform2["ArgTransform<br/>category<br/>hide: true, default: 'products'"]
        
        TransformConfig --> ArgTransform1
        TransformConfig --> ArgTransform2
    end
    
    subgraph "Transform Function (Optional)"
        CustomFunction["async def custom_fn(query: str):<br/>    result = await forward(query=query)<br/>    return format_result(result)"]
    end
    
    subgraph "Transformed Tool"
        TransformedTool_["TransformedTool<br/>name: 'find_products'<br/>args: {query}<br/>parent_tool: Tool<br/>forwarding_fn: Callable"]
    end
    
    ParentTool --> TransformedTool_
    TransformConfig --> TransformedTool_
    CustomFunction --> TransformedTool_
    
    subgraph "Runtime Context"
        ForwardFunction["forward(**kwargs)<br/>- Maps transformed args<br/>- Calls parent tool"]
        ForwardRawFunction["forward_raw(**kwargs)<br/>- Direct parent call<br/>- No argument mapping"]
        
        TransformedTool_ --> ForwardFunction
        TransformedTool_ --> ForwardRawFunction
    end
```

**Sources**: [src/fastmcp/tools/tool_transform.py:232-517](), [src/fastmcp/tools/tool_transform.py:37-91](), [src/fastmcp/tools/tool_transform.py:93-207]()

### Argument Transformation Options

The `ArgTransform` class provides fine-grained control over individual arguments:

| Transform Type | Purpose | Example |
|----------------|---------|---------|
| **Rename** | Change argument name | `name="new_name"` |
| **Hide** | Remove from public schema | `hide=True, default="constant"` |
| **Default Value** | Add/change default | `default=42` |
| **Default Factory** | Dynamic defaults | `default_factory=lambda: time.time()` |
| **Type Change** | Modify expected type | `type=str` |
| **Make Required** | Remove default value | `required=True` |

**Sources**: [src/fastmcp/tools/tool_transform.py:93-207]()

## Server Composition and Component Mounting

Managers support mounting other servers to create hierarchical component structures. This enables composition of multiple FastMCP servers into larger systems.

### Component Loading Paths

```mermaid
graph TD
    subgraph "Component Manager"
        Manager["ToolManager/ResourceManager/PromptManager"]
    end
    
    subgraph "Loading Methods"
        LoadViaServer["_load_components(via_server=True)<br/>Filtered Protocol Path<br/>For MCP requests"]
        LoadViaManager["_load_components(via_server=False)<br/>Manager-to-Manager Path<br/>Complete inventory"]
    end
    
    subgraph "Local Components"
        LocalDict["_tools/_resources/_prompts<br/>Local component storage"]
    end
    
    subgraph "Mounted Servers"
        MountedList["_mounted_servers: list[MountedServer]<br/>- server: FastMCP<br/>- prefix: str<br/>- resource_prefix_format"]
        
        ChildServer1["Child Server 1<br/>Filtered via ._list_tools()"]
        ChildServer2["Child Server 2<br/>Direct via ._tool_manager"]
    end
    
    Manager --> LoadViaServer
    Manager --> LoadViaManager
    
    LoadViaServer --> LocalDict
    LoadViaServer --> ChildServer1
    
    LoadViaManager --> LocalDict  
    LoadViaManager --> ChildServer2
    
    MountedList --> ChildServer1
    MountedList --> ChildServer2
    
    subgraph "Prefixing"
        PrefixLogic["if mounted.prefix:<br/>    prefixed_key = f'{prefix}_{key}'<br/>    component.key = prefixed_key"]
    end
    
    ChildServer1 --> PrefixLogic
    ChildServer2 --> PrefixLogic
```

**Sources**: [src/fastmcp/tools/tool_manager.py:55-101](), [src/fastmcp/resources/resource_manager.py:72-190](), [src/fastmcp/prompts/prompt_manager.py:49-89]()

## Component Lifecycle Management

Components support enable/disable operations and automatic notifications to trigger list change events in the MCP protocol.

### Component State Management

Each component can be enabled or disabled, and state changes automatically notify the Context system:

```python