This document covers the development environment, build system, and contribution workflow for AgentKit framework contributors and maintainers. It focuses on the technical infrastructure and tooling used to develop the framework itself.

For detailed repository setup instructions, see [Repository Setup](#7.1). For information about using AgentKit in your applications, see [Getting Started](#3).

## Development Overview

AgentKit is developed as a TypeScript monorepo using modern development practices and tooling. The development environment emphasizes code quality, automated testing, and streamlined release management through a comprehensive toolchain.

The framework follows a workspace-based architecture where the core `@inngest/agent-kit` package is developed alongside example applications that demonstrate various usage patterns. This co-location enables rapid iteration and ensures examples stay current with API changes.

**Development Toolchain Architecture**

```mermaid
graph TD
    subgraph "Package Management"
        pnpm["pnpm"]
        pnpm_lock["pnpm-lock.yaml"]
        package_json["package.json"]
    end
    
    subgraph "Code Quality"
        eslint["eslint"]
        prettier["prettier"]
        typescript["TypeScript"]
        eslint_config["eslint.config.mjs"]
    end
    
    subgraph "Git Hooks"
        husky["husky"]
        lint_staged["lint-staged"]
    end
    
    subgraph "CI/CD"
        github_actions[".github/workflows/pr.yml"]
        build_job["build job"]
        lint_job["lint job"] 
        test_job["test job"]
    end
    
    subgraph "Version Management"
        changesets["@changesets/cli"]
        version_script["version script"]
        release_script["release script"]
    end
    
    package_json --> pnpm
    pnpm --> pnpm_lock
    eslint_config --> eslint
    eslint_config --> prettier
    eslint_config --> typescript
    
    husky --> lint_staged
    lint_staged --> eslint
    
    github_actions --> build_job
    github_actions --> lint_job
    github_actions --> test_job
    
    changesets --> version_script
    changesets --> release_script
```

Sources: [package.json:1-33](), [eslint.config.mjs:1-33](), [.github/workflows/pr.yml:1-33](), [pnpm-lock.yaml:1-50]()

## Monorepo Structure

The codebase is organized as a pnpm workspace with the following key components:

| Component | Purpose | Location |
|-----------|---------|----------|
| Core Package | Main `@inngest/agent-kit` framework | `packages/agent-kit/` |
| Examples | Usage demonstrations and test applications | `examples/` |
| Tooling Config | Development tool configurations | Root directory |
| CI/CD | GitHub Actions workflows | `.github/workflows/` |

**Workspace Dependencies Flow**

```mermaid
graph LR
    subgraph "Root Workspace"
        root_pkg["package.json"]
        pnpm_workspace["pnpm-workspace.yaml"]
    end
    
    subgraph "Core Package"
        agent_kit["packages/agent-kit"]
        ak_pkg["package.json"]
        ak_src["src/"]
        ak_dist["dist/"]
    end
    
    subgraph "Examples"
        swebench["examples/swebench"]
        demo["examples/demo"]
        support["examples/support-agent"]
        quickstart["examples/quickstart"]
    end
    
    subgraph "Development Tools"
        eslint_conf["eslint.config.mjs"]
        gitignore[".gitignore"]
        husky_conf[".husky/"]
    end
    
    root_pkg --> pnpm_workspace
    pnpm_workspace --> agent_kit
    pnpm_workspace --> swebench
    pnpm_workspace --> demo
    pnpm_workspace --> support
    pnpm_workspace --> quickstart
    
    agent_kit --> ak_pkg
    ak_pkg --> ak_src
    ak_src --> ak_dist
    
    swebench --> agent_kit
    demo --> agent_kit
    support --> agent_kit
    quickstart --> agent_kit
```

Sources: [package.json:1-33](), [examples/swebench/Makefile:1-8]()

## Development Workflow

The development workflow is built around three core scripts defined in the root `package.json`:

### Build Process

The `build` script executes builds across all workspace packages that define a build command:

```
pnpm run --if-present --recursive build
```

This ensures the core framework is compiled and examples can consume the latest changes during development.

### Code Quality Pipeline

Code quality is enforced through multiple layers:

1. **Linting**: `eslint` with TypeScript integration via `typescript-eslint`
2. **Formatting**: `prettier` for consistent code style  
3. **Git Hooks**: `husky` + `lint-staged` for pre-commit validation
4. **CI Validation**: GitHub Actions for automated checks on pull requests

**Code Quality Enforcement Flow**

```mermaid
sequenceDiagram
    participant Dev as "Developer"
    participant Git as "Git Hooks"
    participant ESLint as "eslint"
    participant Prettier as "prettier"
    participant CI as "GitHub Actions"
    
    Dev->>Git: "git commit"
    Git->>ESLint: "lint-staged execution"
    ESLint->>ESLint: "eslint --cache --fix"
    ESLint->>Prettier: "prettier formatting"
    Prettier-->>Git: "formatted code"
    Git-->>Dev: "commit success"
    
    Dev->>CI: "git push / PR"
    CI->>CI: "pnpm install"
    CI->>CI: "pnpm run build"
    CI->>CI: "pnpm run lint"
    CI->>CI: "pnpm run test"
    CI-->>Dev: "PR status"
```

Sources: [package.json:22-24](), [eslint.config.mjs:1-33](), [.github/workflows/pr.yml:1-33]()

### Testing Strategy

Tests are executed via the `test` script which runs tests in all packages that define test commands:

```
pnpm run --if-present --recursive test
```

The CI pipeline validates all packages through the standardized test workflow defined in [.github/workflows/pr.yml:26-32]().

## Release Management

AgentKit uses `@changesets/cli` for automated version management and publishing. The release process involves two primary commands:

### Version Management

The `version` script handles version bumping and lockfile updates:

```
changeset version && pnpm install --lockfile-only
```

This command:
- Applies pending changesets to update package versions
- Updates `pnpm-lock.yaml` to reflect new version constraints
- Generates changelog entries

### Publishing Process  

The `release` script handles the complete build and publish workflow:

```
pnpm run build && changeset publish
```

This ensures:
- All packages are built with latest changes
- Packages are published to npm with correct versions
- Release tags are created in the repository

**Release Workflow**

```mermaid
graph TD
    changeset_add["changeset add"]
    changeset_version["changeset version"]
    pnpm_install["pnpm install --lockfile-only"]
    build["pnpm run build"]
    changeset_publish["changeset publish"]
    
    changeset_add --> changeset_version
    changeset_version --> pnpm_install
    pnpm_install --> build
    build --> changeset_publish
    
    changeset_version -.-> package_json_update["package.json versions"]
    changeset_version -.-> changelog_gen["CHANGELOG.md generation"]
    changeset_publish -.-> npm_publish["npm publish"]
    changeset_publish -.-> git_tags["git tags"]
```

Sources: [package.json:6-7](), [pnpm-lock.yaml:10-13]()

## Build System Configuration

The build system leverages several configuration files that define development behavior:

### TypeScript Configuration

TypeScript compilation is configured through project-specific `tsconfig.json` files in each package, with ESLint integration providing type-aware linting via `typescript-eslint`.

### ESLint Configuration

The modern flat config format in [eslint.config.mjs:1-33]() defines:

- **Ignored Patterns**: `**/dist`, `eslint.config.mjs`, `examples/**`
- **Rule Sets**: `@eslint/js` recommended + `typescript-eslint` recommended + `prettier` integration
- **TypeScript Integration**: Project service with automatic tsconfig detection
- **Custom Rules**: Prettier warnings, namespace allowance, consistent type imports

### Git Integration

Git workflow is enhanced through:

- **Pre-commit Hooks**: [package.json:22-24]() defines `lint-staged` configuration for `*.{j,t}s` files
- **Ignored Files**: [.gitignore:1-13]() excludes build artifacts, dependencies, and environment files
- **CI Triggers**: [.github/workflows/pr.yml:4-5]() activates on pull requests and manual dispatch

Sources: [eslint.config.mjs:8-31](), [package.json:22-31](), [.gitignore:1-13](), [.github/workflows/pr.yml:1-33]()