This document covers the automated infrastructure and workflows that maintain the FastMCP project, including AI-driven automation, documentation generation, issue management, and CI/CD pipelines. The infrastructure is primarily built around GitHub Actions workflows and integrates with external AI services for intelligent project maintenance.

For information about testing infrastructure and development workflows, see [Testing and Development Framework](#8).

## AI-Driven Automation System

The core of FastMCP's infrastructure is the Marvin Context Protocol system, which provides AI-powered assistance for project maintenance, issue triage, and development tasks.

### Marvin Context Protocol Workflow

```mermaid
graph TD
    subgraph "Trigger Events"
        IssueComment["issue_comment (created)"]
        PRComment["pull_request_review_comment (created)"]
        PRReview["pull_request_review (submitted)"]
        PullRequest["pull_request (opened, edited)"]
        Issues["issues (opened, edited, assigned, labeled)"]
        Discussion["discussion (created, edited, labeled)"]
        DiscussionComment["discussion_comment (created)"]
    end

    subgraph "Marvin Workflow"
        TriggerCheck["Trigger Check<br/>/marvin phrase detection"]
        TokenGen["Generate Marvin App Token<br/>actions/create-github-app-token"]
        EnvSetup["Environment Setup<br/>- UV package manager<br/>- Python 3.12<br/>- pre-commit hooks"]
        MarvinExec["Claude Code Action<br/>anthropics/claude-code-action@beta"]
    end

    subgraph "Available Tools"
        WebSearch["WebSearch"]
        WebFetch["WebFetch"]
        BashTools["Bash Tools<br/>- uv:*<br/>- pre-commit:*<br/>- pytest:*<br/>- ruff:*<br/>- git:*<br/>- gh:*"]
        GitHubMCP["GitHub MCP Tools<br/>- add_issue_comment<br/>- create_issue<br/>- get_issue<br/>- update_pull_request<br/>- merge_pull_request"]
    end

    subgraph "Authentication"
        MarvinApp["Marvin GitHub App<br/>MARVIN_APP_ID<br/>MARVIN_APP_PRIVATE_KEY"]
        ClaudeAPI["Claude API<br/>ANTHROPIC_API_KEY"]
    end

    IssueComment --> TriggerCheck
    PRComment --> TriggerCheck
    PRReview --> TriggerCheck
    PullRequest --> TriggerCheck
    Issues --> TriggerCheck
    Discussion --> TriggerCheck
    DiscussionComment --> TriggerCheck

    TriggerCheck --> TokenGen
    TokenGen --> EnvSetup
    EnvSetup --> MarvinExec

    MarvinExec --> WebSearch
    MarvinExec --> WebFetch
    MarvinExec --> BashTools
    MarvinExec --> GitHubMCP

    MarvinApp --> TokenGen
    ClaudeAPI --> MarvinExec
```

The main Marvin workflow is defined in [.github/workflows/marvin.yml:1-72]() and triggers on various GitHub events when the `/marvin` phrase is detected. The workflow uses the `anthropics/claude-code-action@beta` action with extensive tool permissions for code analysis and repository interaction.

**Sources:** [.github/workflows/marvin.yml:1-72]()

### Issue Triage Automation

```mermaid
graph TD
    subgraph "Triage Triggers"
        NewIssue["issues: opened"]
        NewPR["pull_request_target: opened"]
        ManualTrigger["workflow_dispatch"]
    end

    subgraph "Triage Process"
        GetLabels["gh label list<br/>Retrieve available labels"]
        GetIssueDetails["mcp__github__get_issue<br/>Fetch issue/PR details"]
        GetComments["mcp__github__get_issue_comments<br/>Read discussion context"]
        GetLinkedIssues["mcp__github__get_issue<br/>Check referenced issues"]
        AnalyzeContent["Claude Analysis<br/>Apply labeling rules"]
        ApplyLabels["mcp__github__update_issue<br/>Apply selected labels"]
    end

    subgraph "Label Categories"
        CoreCategory["Core Categories<br/>- bug<br/>- enhancement<br/>- feature<br/>- documentation"]
        Priority["Priority<br/>- high-priority<br/>- low-priority"]
        Status["Status<br/>- needs more info<br/>- good first issue<br/>- invalid"]
        Area["Area Labels<br/>- cli<br/>- client<br/>- server<br/>- auth<br/>- openapi<br/>- http"]
    end

    NewIssue --> GetLabels
    NewPR --> GetLabels
    ManualTrigger --> GetLabels

    GetLabels --> GetIssueDetails
    GetIssueDetails --> GetComments
    GetComments --> GetLinkedIssues
    GetLinkedIssues --> AnalyzeContent
    AnalyzeContent --> ApplyLabels

    ApplyLabels --> CoreCategory
    ApplyLabels --> Priority
    ApplyLabels --> Status
    ApplyLabels --> Area
```

The triage system is implemented in [.github/workflows/marvin-label-triage.yml:1-158]() and uses sophisticated rules to categorize issues and PRs automatically. The system enforces mutually exclusive core categories and applies area labels only when thematically central.

**Sources:** [.github/workflows/marvin-label-triage.yml:1-158]()

## Documentation Automation

### SDK Documentation Pipeline

```mermaid
graph TD
    subgraph "Documentation Triggers"
        MainPush["push to main<br/>paths: src/**, pyproject.toml"]
        ManualDispatch["workflow_dispatch"]
    end

    subgraph "Documentation Generation"
        UVSetup["UV Setup<br/>astral-sh/setup-uv@v6"]
        InstallDeps["uv sync --python 3.12"]
        InstallJust["extractions/setup-just@v3"]
        GenerateDocs["just api-ref-all<br/>Generate SDK docs"]
        CreatePR["peter-evans/create-pull-request@v7<br/>Auto-create PR"]
    end

    subgraph "Generated Artifacts"
        SDKDocs["docs/python-sdk/**<br/>Auto-generated API reference"]
        PRBranch["marvin/update-sdk-docs<br/>Auto-managed branch"]
    end

    MainPush --> UVSetup
    ManualDispatch --> UVSetup
    UVSetup --> InstallDeps
    InstallDeps --> InstallJust
    InstallJust --> GenerateDocs
    GenerateDocs --> CreatePR
    CreatePR --> SDKDocs
    CreatePR --> PRBranch
```

The SDK documentation workflow [.github/workflows/update-sdk-docs.yml:1-75]() automatically generates API reference documentation from source code docstrings and type annotations using the `just api-ref-all` command.

**Sources:** [.github/workflows/update-sdk-docs.yml:1-75]()

### Configuration Schema Updates

The schema update workflow [.github/workflows/update-config-schema.yml:1-92]() maintains the `fastmcp.json` configuration schema by generating it from the `MCPServerConfig` class definition:

```mermaid
graph TD
    subgraph "Schema Sources"
        ConfigClass["src/fastmcp/utilities/mcp_server_config/**<br/>MCPServerConfig class"]
        ExcludeLocal["!schema.json<br/>Exclude existing schema"]
    end

    subgraph "Generation Process"
        GenerateSchema["generate_schema()<br/>Python function call"]
        PublicLatest["docs/public/schemas/fastmcp.json/latest.json"]
        PublicV1["docs/public/schemas/fastmcp.json/v1.json"]
        LocalSchema["src/fastmcp/utilities/mcp_server_config/v1/schema.json"]
    end

    subgraph "Output Locations"
        WebAccess["Web-accessible schemas<br/>docs/public/schemas/"]
        LocalDev["Local development<br/>src/fastmcp/utilities/"]
    end

    ConfigClass --> GenerateSchema
    GenerateSchema --> PublicLatest
    GenerateSchema --> PublicV1
    GenerateSchema --> LocalSchema

    PublicLatest --> WebAccess
    PublicV1 --> WebAccess
    LocalSchema --> LocalDev
```

**Sources:** [.github/workflows/update-config-schema.yml:1-92]()

## Issue Management Automation

### Duplicate Detection System

```mermaid
graph TD
    subgraph "Detection Process"
        NewIssue["issues: opened"]
        TaskAgent["Task Tool<br/>Multi-agent coordination"]
        ViewIssue["GitHub Issue Analysis<br/>Extract summary"]
        ParallelSearch["3 Parallel Search Agents<br/>Diverse keyword strategies"]
        FilterFalsePositives["Filter Agent<br/>Remove non-duplicates"]
        PostComment["Comment with duplicates<br/>Auto-close warning"]
    end

    subgraph "Search Strategy"
        Agent1["Agent 1<br/>Title-based search"]
        Agent2["Agent 2<br/>Content-based search"]
        Agent3["Agent 3<br/>Label/metadata search"]
    end

    subgraph "Automation Rules"
        ThreeDayGrace["3-day grace period"]
        PreventingReactions["Thumbs down prevents closure"]
        AuthorActivity["Author comments prevent closure"]
        AutoClose["Auto-close with duplicate label"]
    end

    NewIssue --> TaskAgent
    TaskAgent --> ViewIssue
    ViewIssue --> ParallelSearch

    ParallelSearch --> Agent1
    ParallelSearch --> Agent2
    ParallelSearch --> Agent3

    Agent1 --> FilterFalsePositives
    Agent2 --> FilterFalsePositives
    Agent3 --> FilterFalsePositives
    FilterFalsePositives --> PostComment

    PostComment --> ThreeDayGrace
    ThreeDayGrace --> PreventingReactions
    PreventingReactions --> AuthorActivity
    AuthorActivity --> AutoClose
```

The duplicate detection system [.github/workflows/marvin-dedupe-issues.yml:1-81]() uses a multi-agent approach with the Task tool to coordinate parallel searches and intelligent filtering.

**Sources:** [.github/workflows/marvin-dedupe-issues.yml:1-81]()

### Auto-Close Implementation

The auto-close mechanism is implemented in [scripts/auto_close_duplicates.py:1-332]() with the following key components:

| Component | Class | Purpose |
|-----------|-------|---------|
| Issue Management | `Issue` | Represents GitHub issue data |
| Comment Handling | `Comment` | Manages issue comments |
| Reaction Tracking | `Reaction` | Tracks user reactions |
| API Client | `GitHubClient` | GitHub API interaction |

The script implements sophisticated logic in `should_close_as_duplicate()` [scripts/auto_close_duplicates.py:216-254]() to check for preventing conditions before auto-closing issues.

**Sources:** [scripts/auto_close_duplicates.py:1-332](), [.github/workflows/auto-close-duplicates.yml:1-29]()

## CI/CD Pipeline

### Publishing Workflow

```mermaid
graph TD
    subgraph "Release Triggers"
        ReleasePublished["release: published"]
        ManualTrigger["workflow_dispatch"]
    end

    subgraph "Build Process"
        Checkout["actions/checkout@v5<br/>fetch-depth: 0"]
        UVInstall["astral-sh/setup-uv@v6<br/>UV package manager"]
        Build["uv build<br/>Create distribution"]
        Publish["uv publish<br/>Upload to PyPI"]
    end

    subgraph "Authentication"
        TrustedPublishing["id-token: write<br/>PyPI trusted publishing"]
    end

    ReleasePublished --> Checkout
    ManualTrigger --> Checkout
    Checkout --> UVInstall
    UVInstall --> Build
    Build --> Publish

    TrustedPublishing --> Publish
```

The publishing workflow [.github/workflows/publish.yml:1-27]() uses PyPI's trusted publishing feature for secure package deployment without managing API tokens.

**Sources:** [.github/workflows/publish.yml:1-27]()

## Infrastructure Components

### GitHub App Integration

The Marvin Context Protocol system relies on a GitHub App for authentication:

- **App ID**: Stored as `MARVIN_APP_ID` secret
- **Private Key**: Stored as `MARVIN_APP_PRIVATE_KEY` secret
- **Token Generation**: Uses `actions/create-github-app-token@v2`
- **Permissions**: Comprehensive access to contents, issues, pull-requests, discussions, and actions

### External Service Dependencies

| Service | Purpose | Authentication |
|---------|---------|----------------|
| Anthropic Claude | AI-powered code analysis and automation | `ANTHROPIC_API_KEY` |
| GitHub Docker Registry | MCP server containers | App token |
| PyPI | Package publishing | Trusted publishing (OIDC) |

### Automation Bot Identity

All automated actions use the bot identity:
- **Name**: `marvin-context-protocol[bot]`
- **Email**: `225465937+marvin-context-protocol[bot]@users.noreply.github.com`
- **User ID**: `225465937`

This ensures consistent attribution for automated contributions and proper GitHub integration.

**Sources:** [.github/workflows/update-sdk-docs.yml:68-69](), [.github/workflows/update-config-schema.yml:85-86]()