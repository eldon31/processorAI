def version() -> None:
    try:
        version = importlib.metadata.version("mcp")
        print(f"MCP version {version}")
    except importlib.metadata.PackageNotFoundError:
        print("MCP version unknown (package not installed)")
        sys.exit(1)
```

Sources: [src/mcp/cli/cli.py:211-219]()

## Dependency Management Integration

All CLI commands integrate with `uv` for dependency management:

### UV Command Construction

```mermaid
graph LR
    subgraph "Package Collection"
        base_mcp["'mcp[cli]' base package"]
        server_deps["server.dependencies list"]
        with_packages["--with command args"]
        deduplicate["Remove duplicates via set()"]
    end
    
    subgraph "Command Building"
        uv_run["['uv', 'run']"]
        add_with["Add --with for each package"]
        add_editable["Add --with-editable if specified"]
        add_mcp_run["Add ['mcp', 'run', file_spec]"]
    end
    
    base_mcp --> deduplicate
    server_deps --> deduplicate
    with_packages --> deduplicate
    
    deduplicate --> add_with
    uv_run --> add_with
    add_with --> add_editable
    add_editable --> add_mcp_run
```

Sources: [src/mcp/cli/cli.py:65-85](), [src/mcp/cli/claude.py:101-125]()

### UV Path Resolution

The CLI automatically locates the `uv` executable using platform-appropriate methods:

- Uses `shutil.which("uv")` to find full path
- Falls back to `"uv"` string if not found in PATH
- Provides clear error messages for missing uv installation

Sources: [src/mcp/cli/claude.py:33-41]()