Server composition and proxying enables FastMCP servers to combine functionality from multiple other servers, either through live delegation (mounting) or static copying (importing). This system allows complex applications to be built by composing smaller, focused servers while maintaining clean separation of concerns.

For information about the core FastMCP server architecture, see [2](#2). For details about component management and registration, see [2.1](#2.1).

## Overview

FastMCP provides three primary mechanisms for server composition:

- **Mounting** - Live delegation to child servers with automatic prefix handling
- **Importing** - Static copying of components from other servers  
- **Proxying** - Transparent forwarding to remote MCP-compliant servers

All composition methods support automatic prefixing of component names to avoid conflicts and provide clear namespacing.

## Mount System Architecture

The mount system enables live delegation to child FastMCP servers. When a component is requested, the parent server forwards the request to the appropriate mounted server in real-time.

### Mount System Core Components

```mermaid
graph TB
    subgraph "Parent Server"
        ParentServer["FastMCP Parent Server"]
        MountedServers["_mounted_servers: list[MountedServer]"]
        ToolManager["ToolManager"]
        ResourceManager["ResourceManager"] 
        PromptManager["PromptManager"]
    end
    
    subgraph "MountedServer Dataclass"
        MountedServerData["MountedServer"]
        ServerRef["server: FastMCP"]
        PrefixField["prefix: str | None"]
    end
    
    subgraph "Child Servers"
        ChildServer1["Child FastMCP Server 1"]
        ChildServer2["Child FastMCP Server 2"]
        ChildServer3["Child FastMCP Server 3"]
    end
    
    ParentServer --> MountedServers
    MountedServers --> MountedServerData
    MountedServerData --> ServerRef
    MountedServerData --> PrefixField
    
    ServerRef -.->|"Live Delegation"| ChildServer1
    ServerRef -.->|"Live Delegation"| ChildServer2  
    ServerRef -.->|"Live Delegation"| ChildServer3
    
    ParentServer --> ToolManager
    ParentServer --> ResourceManager
    ParentServer --> PromptManager
    
    ToolManager -.->|"get_tools()"| MountedServers
    ResourceManager -.->|"get_resources()"| MountedServers
    PromptManager -.->|"get_prompts()"| MountedServers
```

**Sources:** [src/fastmcp/server/server.py:175](), [src/fastmcp/server/server.py:1260-1332]()

### Mount Method Implementation

The `mount` method in `FastMCP` registers child servers for live delegation:

```mermaid
sequenceDiagram
    participant Client
    participant ParentServer as "Parent FastMCP"
    participant MountedServers as "_mounted_servers"
    participant ChildServer as "Child FastMCP"
    
    Client->>ParentServer: mount(child_server, "prefix")
    ParentServer->>MountedServers: append(MountedServer)
    Note over MountedServers: Store server + prefix
    
    Client->>ParentServer: call_tool("prefix_tool_name", args)
    ParentServer->>MountedServers: find server for "prefix_tool_name"
    MountedServers->>ChildServer: call_tool("tool_name", args)
    ChildServer-->>Client: ToolResult
```

**Sources:** [src/fastmcp/server/server.py:1260-1332](), [tests/server/test_mount.py:16-68]()

## Import System Architecture  

The import system performs static copying of components from other servers. Components are copied once at import time and become part of the importing server.

### Import vs Mount Comparison

```mermaid
graph LR
    subgraph "Mount System (Live Delegation)"
        ParentMountServer["Parent Server"]
        ChildMountServer["Child Server"]
        ParentMountServer -.->|"Runtime calls"| ChildMountServer
    end
    
    subgraph "Import System (Static Copy)"
        ParentImportServer["Parent Server"]
        CopiedComponents["Copied Components<br/>- Tools<br/>- Resources<br/>- Prompts"]
        SourceServer["Source Server"]
        SourceServer -->|"One-time copy"| CopiedComponents
        ParentImportServer --> CopiedComponents
    end
```

**Sources:** [src/fastmcp/server/server.py:1334-1421](), [tests/server/test_import_server.py:10-34]()

### Import Method Implementation

The `import_server` method copies components with prefix handling:

```mermaid
flowchart TD
    ImportCall["import_server(source, prefix)"]
    GetTools["source.get_tools()"]
    GetResources["source.get_resources()"]  
    GetPrompts["source.get_prompts()"]
    
    ApplyToolPrefix["Apply prefix to tool names"]
    ApplyResourcePrefix["Apply prefix to resource URIs"]
    ApplyPromptPrefix["Apply prefix to prompt names"]
    
    AddToManagers["Add to local managers"]
    
    ImportCall --> GetTools
    ImportCall --> GetResources
    ImportCall --> GetPrompts
    
    GetTools --> ApplyToolPrefix
    GetResources --> ApplyResourcePrefix
    GetPrompts --> ApplyPromptPrefix
    
    ApplyToolPrefix --> AddToManagers
    ApplyResourcePrefix --> AddToManagers
    ApplyPromptPrefix --> AddToManagers
```

**Sources:** [src/fastmcp/server/server.py:1334-1421](), [tests/server/test_import_server.py:61-89]()

## Proxy System Architecture

The proxy system enables FastMCP servers to act as transparent proxies to remote MCP-compliant servers. This is implemented through specialized managers and components.

### Proxy System Core Components

```mermaid
graph TB
    subgraph "FastMCPProxy Server"
        ProxyServer["FastMCPProxy"]
        ClientFactory["client_factory: ClientFactoryT"]
    end
    
    subgraph "Proxy Managers"
        ProxyToolManager["ProxyToolManager"]
        ProxyResourceManager["ProxyResourceManager"]
        ProxyPromptManager["ProxyPromptManager"]
    end
    
    subgraph "Proxy Components"
        ProxyTool["ProxyTool"]
        ProxyResource["ProxyResource"]  
        ProxyPrompt["ProxyPrompt"]
        ProxyTemplate["ProxyTemplate"]
    end
    
    subgraph "Remote Connection"
        Client["Client"]
        RemoteServer["Remote MCP Server"]
    end
    
    ProxyServer --> ClientFactory
    ProxyServer --> ProxyToolManager
    ProxyServer --> ProxyResourceManager
    ProxyServer --> ProxyPromptManager
    
    ProxyToolManager --> ProxyTool
    ProxyResourceManager --> ProxyResource
    ProxyResourceManager --> ProxyTemplate
    ProxyPromptManager --> ProxyPrompt
    
    ClientFactory --> Client
    Client --> RemoteServer
    
    ProxyTool -.->|"Forward calls"| Client
    ProxyResource -.->|"Forward calls"| Client
    ProxyPrompt -.->|"Forward calls"| Client
```

**Sources:** [src/fastmcp/server/proxy.py:454-519](), [src/fastmcp/server/proxy.py:69-121]()

### FastMCPProxy Creation Methods

FastMCP provides two ways to create proxy servers:

```mermaid
graph LR
    subgraph "Direct FastMCPProxy Constructor"
        ProxyConstructor["FastMCPProxy(client_factory=...)"]
        ClientFactoryArg["Explicit client_factory"]
        ProxyConstructor --> ClientFactoryArg
    end
    
    subgraph "FastMCP.as_proxy() Class Method"  
        AsProxyMethod["FastMCP.as_proxy(backend=client)"]
        AutoClientFactory["Automatic client_factory creation"]
        AsProxyMethod --> AutoClientFactory
    end
    
    ClientFactoryArg -.->|"Manual session management"| ProxyResult["FastMCPProxy Instance"]
    AutoClientFactory -.->|"Simplified session strategy"| ProxyResult
```

**Sources:** [src/fastmcp/server/server.py:1555-1610](), [src/fastmcp/server/proxy.py:460-508]()

## Prefix Handling System

All composition methods support automatic prefixing to avoid component name conflicts. The prefix handling varies by component type.

### Prefix Application Rules

```mermaid
graph TD
    ComponentType{"Component Type"}
    
    ComponentType -->|"Tool"| ToolPrefix["prefix + '_' + tool.name"]
    ComponentType -->|"Resource"| ResourcePrefix["protocol://prefix/path"]
    ComponentType -->|"Resource Template"| TemplatePrefix["protocol://prefix/{params}"]
    ComponentType -->|"Prompt"| PromptPrefix["prefix + '_' + prompt.name"]
    
    ToolPrefix --> ToolExample["'api_get_user'"]
    ResourcePrefix --> ResourceExample["'data://api/users'"]
    TemplatePrefix --> TemplateExample["'users://api/{id}'"]
    PromptPrefix --> PromptExample["'api_greeting'"]
```

**Sources:** [src/fastmcp/server/server.py:1423-1553](), [src/fastmcp/server/server.py:2157-2205]()

### Resource Prefix Utilities

FastMCP provides utility functions for resource prefix manipulation:

| Function | Purpose | Example |
|----------|---------|---------|
| `add_resource_prefix()` | Add prefix to resource URI | `data://users` → `data://api/users` |
| `remove_resource_prefix()` | Remove prefix from URI | `data://api/users` → `data://users` |
| `has_resource_prefix()` | Check if URI has prefix | Returns `True` for `data://api/users` |

**Sources:** [src/fastmcp/server/server.py:2157-2205](), [tests/server/test_server.py:22-26]()

## Component Request Flow

The following diagram shows how requests flow through the composition system:

```mermaid
sequenceDiagram
    participant Client
    participant ParentServer as "Parent FastMCP"
    participant ToolManager as "ToolManager"
    participant MountedServer as "Mounted Server"
    participant ProxyManager as "ProxyToolManager"
    participant RemoteClient as "Remote Client"
    
    Client->>ParentServer: call_tool("api_get_user", args)
    ParentServer->>ToolManager: _call_tool("api_get_user", args)
    
    alt Local Tool Found
        ToolManager-->>ParentServer: Local tool result
    else Mounted Server Tool
        ToolManager->>MountedServer: call_tool("get_user", args)
        MountedServer-->>ToolManager: Tool result
        ToolManager-->>ParentServer: Tool result
    else Proxy Tool
        ToolManager->>ProxyManager: call_tool("api_get_user", args)
        ProxyManager->>RemoteClient: call_tool("get_user", args)
        RemoteClient-->>ProxyManager: Remote result
        ProxyManager-->>ToolManager: Tool result
        ToolManager-->>ParentServer: Tool result
    end
    
    ParentServer-->>Client: Final result
```

**Sources:** [src/fastmcp/server/server.py:729-752](), [src/fastmcp/server/proxy.py:107-121](), [src/fastmcp/server/proxy.py:280-296]()

## Advanced Composition Patterns

### Multi-Level Composition

Servers can be composed in multiple levels, with prefixes accumulating:

```mermaid
graph TD
    MainApp["Main App"]
    ServiceLayer["Service Layer<br/>(prefix: 'service')"]
    APILayer["API Layer<br/>(prefix: 'api')"]
    DataProvider["Data Provider"]
    
    MainApp -->|"mount('service')"| ServiceLayer
    ServiceLayer -->|"mount('api')"| APILayer
    APILayer -->|"import_server('data')"| DataProvider
    
    FinalTool["Final Tool: 'service_api_data_get_user'"]
    MainApp -.-> FinalTool
```

**Sources:** [tests/server/test_import_server.py:249-283](), [tests/server/test_mount.py:466-509]()

### Mixed Composition Strategies

A single parent server can use multiple composition strategies simultaneously:

```mermaid
graph TB
    ParentServer["Parent FastMCP Server"]
    
    subgraph "Mounted Servers (Live)"
        MountedAuth["Auth Server<br/>(mounted: 'auth')"]
        MountedAPI["API Server<br/>(mounted: 'api')"]
    end
    
    subgraph "Imported Components (Static)"
        ImportedUtils["Utils Components<br/>(imported: 'utils')"]
        ImportedData["Data Components<br/>(imported: 'data')"]
    end
    
    subgraph "Proxy Servers (Remote)"
        RemoteAnalytics["Analytics Server<br/>(proxy: 'analytics')"]
        RemoteML["ML Server<br/>(proxy: 'ml')"]
    end
    
    ParentServer --> MountedAuth
    ParentServer --> MountedAPI
    ParentServer --> ImportedUtils
    ParentServer --> ImportedData
    ParentServer --> RemoteAnalytics
    ParentServer --> RemoteML
```

**Sources:** [tests/server/test_mount.py:210-238](), [tests/server/test_import_server.py:36-58](), [src/fastmcp/server/proxy.py:454-519]()