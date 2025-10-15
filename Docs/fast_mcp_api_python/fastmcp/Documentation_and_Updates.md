This page covers the FastMCP documentation system, release management, and how documentation is structured and maintained within the project. It explains the technical infrastructure behind documentation generation, changelog management, and the various output formats designed for both human and LLM consumption.

For information about the CLI system and commands, see [Command Line Interface](#5). For details about project infrastructure and automation, see [Project Infrastructure](#9).

## Documentation Architecture

The FastMCP documentation system consists of several interconnected components that generate and maintain documentation across multiple formats and platforms.

### Documentation Structure Overview

```mermaid
graph TB
    subgraph "Source Documentation"
        ChangelogMDX["docs/changelog.mdx<br/>Detailed Release Notes"]
        UpdatesMDX["docs/updates.mdx<br/>Summary Cards"]
        DocsSource["Documentation Source Files<br/>.mdx format"]
    end
    
    subgraph "Navigation and Schema"
        DocsJSON["docs.json<br/>Navigation Structure"]
        SchemaFiles["Schema Files<br/>fastmcp.json definitions"]
    end
    
    subgraph "Generated Documentation"
        WebDocs["gofastmcp.com<br/>Documentation Website"]
        LLMFormats["LLM-Friendly Formats<br/>llms.txt output"]
        SDKDocs["SDK Documentation<br/>Auto-generated API docs"]
    end
    
    subgraph "Automation Infrastructure"
        StaticWorkflow["run-static.yml<br/>CI/CD Automation"]
        PreCommitHooks[".pre-commit-config.yaml<br/>Quality Gates"]
        SchemaWorkflow["Schema Update Automation<br/>PR-based updates"]
    end
    
    %% Core connections
    ChangelogMDX --> WebDocs
    UpdatesMDX --> WebDocs
    DocsSource --> WebDocs
    DocsJSON --> WebDocs
    
    %% Generation connections
    SchemaFiles --> SDKDocs
    WebDocs --> LLMFormats
    
    %% Automation connections
    StaticWorkflow --> SchemaFiles
    PreCommitHooks --> DocsSource
    SchemaWorkflow --> SchemaFiles
    
    %% Update flow
    ChangelogMDX -.->|"Version updates"| UpdatesMDX
    SchemaFiles -.->|"Auto-generated"| DocsJSON
```

**Sources:** [docs/changelog.mdx:1-10](), [docs/updates.mdx:1-10](), [.github/workflows/run-static.yml:1-20](), [.pre-commit-config.yaml:1-15]()

### Documentation File Organization

The documentation follows a structured hierarchy with specific file types and naming conventions:

| File Type | Location | Purpose | Example |
|-----------|----------|---------|---------|
| Release Notes | `docs/changelog.mdx` | Detailed changelog entries | [docs/changelog.mdx:7-79]() |
| Update Cards | `docs/updates.mdx` | Visual release summaries | [docs/updates.mdx:8-22]() |
| Navigation Schema | `docs.json` | Site structure definition | Referenced in architecture |
| README Documentation | `*/README.md` | Component-specific docs | [src/fastmcp/contrib/mcp_mixin/README.md:1-117]() |

**Sources:** [docs/changelog.mdx:1-5](), [docs/updates.mdx:1-6](), [src/fastmcp/contrib/mcp_mixin/README.md:1-10]()

## Release Management and Updates

FastMCP uses a structured approach to managing releases and communicating updates to users and developers.

### Changelog Structure

The changelog follows a consistent format with version-specific entries:

```mermaid
graph TD
    subgraph "Changelog Entry Structure"
        VersionHeader["Version Header<br/>v2.12.4: OIDC What You Did There"]
        ReleaseDate["Release Date<br/>2025-09-26"]
        Description["Release Description<br/>High-level summary"]
        
        subgraph "Change Categories"
            NewFeatures["New Features 🎉<br/>feat: prefixed items"]
            Enhancements["Enhancements 🔧<br/>Minor improvements"]
            Fixes["Fixes 🐞<br/>Bug fixes and patches"]
            Docs["Docs 📚<br/>Documentation updates"]
            Dependencies["Dependencies 📦<br/>Dependency updates"]
        end
        
        subgraph "Metadata"
            Contributors["New Contributors<br/>First-time contributors"]
            FullChangelog["Full Changelog<br/>GitHub comparison links"]
        end
    end
    
    VersionHeader --> ReleaseDate
    ReleaseDate --> Description
    Description --> NewFeatures
    NewFeatures --> Enhancements
    Enhancements --> Fixes
    Fixes --> Docs
    Docs --> Dependencies
    Dependencies --> Contributors
    Contributors --> FullChangelog
```

**Sources:** [docs/changelog.mdx:7-79](), [docs/changelog.mdx:81-123]()

### Update Card System

The updates system provides visual summaries of releases through structured cards:

```mermaid
graph LR
    subgraph "Update Card Components"
        UpdateWrapper["Update Component<br/>label, description, tags"]
        CardContent["Card Component<br/>title, href, cta"]
        
        subgraph "Card Properties"
            Title["title: Release Name"]
            Href["href: GitHub release URL"]
            CTA["cta: Call-to-action text"]
            Image["img: Optional hero image"]
        end
        
        subgraph "Categorization"
            Tags["tags: ['Releases', 'Blog Posts']"]
            Labels["label: Version identifier"]
            Description["description: Release date"]
        end
    end
    
    UpdateWrapper --> CardContent
    CardContent --> Title
    CardContent --> Href
    CardContent --> CTA
    CardContent --> Image
    UpdateWrapper --> Tags
    UpdateWrapper --> Labels
    UpdateWrapper --> Description
```

**Sources:** [docs/updates.mdx:8-22](), [docs/updates.mdx:54-68]()

## Documentation Generation and Maintenance

FastMCP employs automated systems for maintaining documentation quality and consistency.

### Static Analysis and Quality Gates

The documentation maintenance relies on automated quality checks:

```mermaid
graph TB
    subgraph "Pre-commit Pipeline"
        ValidatePyproject["validate-pyproject<br/>Project file validation"]
        Prettier["prettier<br/>YAML/JSON formatting"]
        RuffCheck["ruff-check<br/>Code linting"]
        RuffFormat["ruff-format<br/>Code formatting"]
        TyCheck["ty check<br/>Type checking"]
        CodeSpell["codespell<br/>Spell checking"]
        NoCommitMain["no-commit-to-branch<br/>Branch protection"]
    end
    
    subgraph "CI/CD Workflow"
        StaticAnalysis["run-static.yml<br/>GitHub Actions"]
        UVSync["uv sync<br/>Dependency management"]
        LockfileCheck["Lockfile validation<br/>uv lock --check"]
        PreCommitRun["Pre-commit execution<br/>All files check"]
    end
    
    %% Pre-commit flow
    ValidatePyproject --> Prettier
    Prettier --> RuffCheck
    RuffCheck --> RuffFormat
    RuffFormat --> TyCheck
    TyCheck --> CodeSpell
    CodeSpell --> NoCommitMain
    
    %% CI/CD flow
    StaticAnalysis --> UVSync
    UVSync --> LockfileCheck
    LockfileCheck --> PreCommitRun
    
    %% Integration
    PreCommitRun -.->|"Runs"| ValidatePyproject
```

**Sources:** [.pre-commit-config.yaml:3-48](), [.github/workflows/run-static.yml:26-54]()

### Automated Documentation Updates

The project uses automated workflows to maintain documentation currency:

| Automation Type | Trigger | Purpose | Implementation |
|------------------|---------|---------|----------------|
| Schema Updates | Code changes | Keep schemas current | PR-based automation |
| SDK Documentation | Post-merge | Generate API docs | GitHub Actions |
| Static Analysis | PR/Push | Quality validation | [.github/workflows/run-static.yml:18-20]() |
| Spell Checking | Pre-commit | Content quality | [.pre-commit-config.yaml:43-48]() |

**Sources:** [.github/workflows/run-static.yml:8-22](), [.pre-commit-config.yaml:25-42]()

## LLM-Friendly Documentation Formats

FastMCP generates documentation in formats optimized for consumption by Large Language Models and AI assistants.

### Documentation Format Bridge

```mermaid
graph LR
    subgraph "Human-Readable Formats"
        WebsiteDocs["gofastmcp.com<br/>HTML Documentation"]
        MarkdownDocs["Markdown Files<br/>.mdx source"]
        GitHubDocs["GitHub README<br/>Repository docs"]
    end
    
    subgraph "LLM-Optimized Formats"
        LLMsTxt["llms.txt<br/>Structured text format"]
        MCPServer["MCP Server<br/>Interactive documentation"]
        StructuredJSON["JSON Schemas<br/>Machine-readable specs"]
    end
    
    subgraph "Code Documentation"
        InlineComments["Inline Comments<br/>Source code docs"]
        DocStrings["Python Docstrings<br/>Function documentation"]
        TypeHints["Type Annotations<br/>Interface specifications"]
    end
    
    %% Transformation flows
    MarkdownDocs --> WebsiteDocs
    WebsiteDocs --> LLMsTxt
    MarkdownDocs --> LLMsTxt
    
    %% Code documentation
    InlineComments --> StructuredJSON
    DocStrings --> MCPServer
    TypeHints --> StructuredJSON
    
    %% Integration
    StructuredJSON --> MCPServer
    MCPServer -.->|"Serves"| LLMsTxt
```

**Sources:** [src/fastmcp/contrib/mcp_mixin/README.md:1-25](), [docs/updates.mdx:1-6]()

### Component Documentation Pattern

FastMCP components follow a standardized documentation pattern, as exemplified by the MCP Mixin:

```mermaid
graph TD
    subgraph "Component Documentation Structure"
        ModuleHeader["Module Header<br/>Purpose and scope"]
        FeatureList["Feature List<br/>Bulleted capabilities"]
        
        subgraph "Usage Examples"
            BasicUsage["Basic Usage<br/>Simple examples"]
            AdvancedUsage["Advanced Usage<br/>Complex scenarios"]
            ConfigOptions["Configuration Options<br/>Parameter details"]
        end
        
        subgraph "Code Examples"
            ImportStatements["Import Statements<br/>Required dependencies"]
            ClassDefinition["Class Definition<br/>Inheritance pattern"]
            MethodExamples["Method Examples<br/>Decorator usage"]
            RegistrationCode["Registration Code<br/>Server integration"]
        end
    end
    
    ModuleHeader --> FeatureList
    FeatureList --> BasicUsage
    BasicUsage --> AdvancedUsage
    AdvancedUsage --> ConfigOptions
    
    BasicUsage --> ImportStatements
    ImportStatements --> ClassDefinition
    ClassDefinition --> MethodExamples
    MethodExamples --> RegistrationCode
```

**Sources:** [src/fastmcp/contrib/mcp_mixin/README.md:3-25](), [src/fastmcp/contrib/mcp_mixin/README.md:26-117]()

The documentation system ensures that FastMCP maintains comprehensive, up-to-date, and accessible documentation across multiple formats and audiences, supporting both human developers and AI systems that need to understand and work with the codebase.