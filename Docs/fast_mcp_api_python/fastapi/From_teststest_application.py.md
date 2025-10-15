@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/api_route", 200, {"message": "Hello World"}),
        ("/non_decorated_route", 200, {"message": "Hello World"}), 
        ("/nonexistent", 404, {"detail": "Not Found"}),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
```

Sources: [tests/test_application.py:10-22](), [tests/test_tutorial/test_cookie_param_models/test_tutorial002.py:17-36]()

# Code Quality and Pre-commit




This document covers the code quality infrastructure and pre-commit hook system used in the FastAPI repository. It details the configuration and usage of linting, formatting, type checking, and automated quality gates that ensure code consistency and reliability.

For information about the actual test framework and testing utilities, see [Test Framework and Tools](#5.1). For CI/CD automation that runs these quality checks, see [CI/CD Pipeline](#6.2).

## Pre-commit Hook System

FastAPI uses a comprehensive pre-commit hook system to enforce code quality standards before commits are made to the repository. The configuration is defined in [.pre-commit-config.yaml:1-26]().

### Hook Configuration

The pre-commit system is configured with Python 3.10 as the default language version and includes two main repository sources:

```mermaid
graph TB
    subgraph "Pre-commit Configuration"
        CONFIG[".pre-commit-config.yaml"]
        PYTHON_VERSION["default_language_version: python3.10"]
    end
    
    subgraph "pre-commit-hooks Repository v6.0.0"
        LARGE_FILES["id: check-added-large-files"]
        CHECK_TOML["id: check-toml"]
        CHECK_YAML["id: check-yaml args: --unsafe"]
        EOF_FIXER["id: end-of-file-fixer"]
        TRAILING_WS["id: trailing-whitespace"]
    end
    
    subgraph "ruff-pre-commit Repository v0.12.10"
        RUFF_LINT["id: ruff args: --fix"]
        RUFF_FORMAT["id: ruff-format"]
    end
    
    subgraph "Pre-commit.ci Integration"
        AUTOFIX["autofix_commit_msg"]
        AUTOUPDATE["autoupdate_commit_msg"]
    end
    
    CONFIG --> PYTHON_VERSION
    CONFIG --> LARGE_FILES
    CONFIG --> CHECK_TOML
    CONFIG --> CHECK_YAML
    CONFIG --> EOF_FIXER
    CONFIG --> TRAILING_WS
    CONFIG --> RUFF_LINT
    CONFIG --> RUFF_FORMAT
    CONFIG --> AUTOFIX
    CONFIG --> AUTOUPDATE
```

The system includes validation hooks for file formats and content, plus automated code quality enforcement through Ruff.

**Sources:** [.pre-commit-config.yaml:1-26]()

### Pre-commit.ci Integration

The configuration includes integration with pre-commit.ci for automated maintenance:

| Feature | Configuration | Description |
|---------|---------------|-------------|
| Auto-fix Messages | `🎨 [pre-commit.ci] Auto format from pre-commit.com hooks` | Commit messages for automatic fixes |
| Auto-update Messages | `⬆ [pre-commit.ci] pre-commit autoupdate` | Commit messages for dependency updates |

**Sources:** [.pre-commit-config.yaml:24-25]()

## Code Linting and Formatting with Ruff

FastAPI uses Ruff as its primary tool for both code linting and formatting, replacing multiple traditional tools with a single, fast implementation.

### Ruff Configuration

The Ruff configuration includes two main hooks:

```mermaid
graph LR
    subgraph "Ruff Integration"
        RUFF_REPO["astral-sh/ruff-pre-commit v0.12.10"]
        RUFF_LINT_HOOK["ruff --fix"]
        RUFF_FORMAT_HOOK["ruff-format"]
    end
    
    subgraph "Target Directories"
        FASTAPI_DIR["fastapi/"]
        TESTS_DIR["tests/"]
        DOCS_SRC_DIR["docs_src/"]
        SCRIPTS_DIR["scripts/"]
    end
    
    RUFF_REPO --> RUFF_LINT_HOOK
    RUFF_REPO --> RUFF_FORMAT_HOOK
    
    RUFF_LINT_HOOK --> FASTAPI_DIR
    RUFF_LINT_HOOK --> TESTS_DIR
    RUFF_LINT_HOOK --> DOCS_SRC_DIR
    RUFF_LINT_HOOK --> SCRIPTS_DIR
    
    RUFF_FORMAT_HOOK --> FASTAPI_DIR
    RUFF_FORMAT_HOOK --> TESTS_DIR
    RUFF_FORMAT_HOOK --> DOCS_SRC_DIR
    RUFF_FORMAT_HOOK --> SCRIPTS_DIR
```

**Sources:** [.pre-commit-config.yaml:16-22](), [scripts/lint.sh:7-8](), [scripts/format.sh:4-5]()

### Manual Code Quality Scripts

The repository provides several scripts for manual execution of code quality tools:

| Script | Purpose | Commands |
|--------|---------|----------|
| `scripts/lint.sh` | Run linting and type checking | `mypy fastapi`, `ruff check`, `ruff format --check` |
| `scripts/format.sh` | Apply code formatting | `ruff check --fix`, `ruff format` |

**Sources:** [scripts/lint.sh:1-9](), [scripts/format.sh:1-6]()

## Type Checking with mypy

FastAPI uses mypy for static type checking to ensure type safety across the codebase.

### mypy Configuration

The mypy version is pinned in the test requirements and executed as part of the linting process:

```mermaid
graph TB
    subgraph "Type Checking Pipeline"
        MYPY_REQ["requirements-tests.txt: mypy ==1.8.0"]
        LINT_SCRIPT["scripts/lint.sh"]
        MYPY_EXEC["mypy fastapi"]
    end
    
    subgraph "Target Analysis"
        FASTAPI_PACKAGE["fastapi/ package"]
        TYPE_ANNOTATIONS["Type annotations"]
        TYPE_ERRORS["Type errors and inconsistencies"]
    end
    
    MYPY_REQ --> LINT_SCRIPT
    LINT_SCRIPT --> MYPY_EXEC
    MYPY_EXEC --> FASTAPI_PACKAGE
    FASTAPI_PACKAGE --> TYPE_ANNOTATIONS
    FASTAPI_PACKAGE --> TYPE_ERRORS
```

**Sources:** [requirements-tests.txt:5](), [scripts/lint.sh:6]()

## Test Coverage Infrastructure

The repository includes comprehensive test coverage tracking using the `coverage` tool.

### Coverage Configuration

```mermaid
graph TB
    subgraph "Coverage Dependencies"
        COV_REQ["coverage[toml] >= 6.5.0,< 8.0"]
        PYTEST_REQ["pytest >=7.1.3,<9.0.0"]
    end
    
    subgraph "Test Execution Scripts"
        TEST_SCRIPT["scripts/test.sh"]
        COV_HTML_SCRIPT["scripts/test-cov-html.sh"]
    end
    
    subgraph "Coverage Process"
        COV_RUN["coverage run -m pytest tests"]
        COV_COMBINE["coverage combine"]
        COV_REPORT["coverage report"]
        COV_HTML["coverage html"]
    end
    
    COV_REQ --> TEST_SCRIPT
    PYTEST_REQ --> TEST_SCRIPT
    
    TEST_SCRIPT --> COV_RUN
    COV_HTML_SCRIPT --> COV_RUN
    COV_HTML_SCRIPT --> COV_COMBINE
    COV_HTML_SCRIPT --> COV_REPORT
    COV_HTML_SCRIPT --> COV_HTML
```

The test execution includes setting `PYTHONPATH=./docs_src` to include documentation source code in the test environment.

**Sources:** [requirements-tests.txt:3-4](), [scripts/test.sh:6-7](), [scripts/test-cov-html.sh:6-9]()

## Testing Infrastructure Dependencies

The testing infrastructure includes several specialized testing libraries and utilities:

| Dependency | Version | Purpose |
|------------|---------|---------|
| `pytest` | `>=7.1.3,<9.0.0` | Main testing framework |
| `coverage[toml]` | `>= 6.5.0,< 8.0` | Test coverage measurement |
| `mypy` | `==1.8.0` | Static type checking |
| `dirty-equals` | `==0.9.0` | Flexible equality testing |
| `inline-snapshot` | `>=0.21.1` | Snapshot testing |

**Sources:** [requirements-tests.txt:3-6](), [requirements-tests.txt:13]()

### Testing Utilities and Patterns

The repository includes specialized testing utilities for handling different Python versions and Pydantic versions:

```mermaid
graph TB
    subgraph "Test Utilities"
        UTILS_MODULE["tests/utils.py"]
        PY39_MARKER["needs_py39"]
        PY310_MARKER["needs_py310"]
        PYDANTIC_V1_MARKER["needs_pydanticv1"]
        PYDANTIC_V2_MARKER["needs_pydanticv2"]
        SNAPSHOT_HELPER["pydantic_snapshot()"]
    end
    
    subgraph "Version-specific Testing"
        PYTHON_VERSIONS["Python 3.9+ and 3.10+ tests"]
        PYDANTIC_VERSIONS["Pydantic v1 and v2 compatibility"]
        CONDITIONAL_SNAPSHOTS["Version-specific test snapshots"]
    end
    
    UTILS_MODULE --> PY39_MARKER
    UTILS_MODULE --> PY310_MARKER
    UTILS_MODULE --> PYDANTIC_V1_MARKER
    UTILS_MODULE --> PYDANTIC_V2_MARKER
    UTILS_MODULE --> SNAPSHOT_HELPER
    
    PY39_MARKER --> PYTHON_VERSIONS
    PY310_MARKER --> PYTHON_VERSIONS
    PYDANTIC_V1_MARKER --> PYDANTIC_VERSIONS
    PYDANTIC_V2_MARKER --> PYDANTIC_VERSIONS
    SNAPSHOT_HELPER --> CONDITIONAL_SNAPSHOTS
```

The `pydantic_snapshot` function enables version-specific snapshot testing for maintaining compatibility across Pydantic versions.

**Sources:** [tests/utils.py:7-12](), [tests/utils.py:15-34]()

## Quality Assurance Integration

The code quality system integrates with the broader development workflow through standardized scripts and dependency management:

### Development Dependencies

The main requirements file includes pre-commit as a development dependency:

```mermaid
graph LR
    subgraph "Development Requirements"
        MAIN_REQ["requirements.txt"]
        ALL_DEPS["-e .[all]"]
        TEST_DEPS["-r requirements-tests.txt"]
        DOCS_DEPS["-r requirements-docs.txt"]
        PRECOMMIT_DEP["pre-commit >=2.17.0,<5.0.0"]
        PLAYWRIGHT_DEP["playwright"]
    end
    
    MAIN_REQ --> ALL_DEPS
    MAIN_REQ --> TEST_DEPS
    MAIN_REQ --> DOCS_DEPS
    MAIN_REQ --> PRECOMMIT_DEP
    MAIN_REQ --> PLAYWRIGHT_DEP
```

**Sources:** [requirements.txt:1-7]()

### Script Integration Patterns

The quality assurance scripts follow consistent patterns for error handling and output:

| Script Feature | Implementation | Purpose |
|----------------|----------------|---------|
| Error Handling | `set -e` | Exit on any command failure |
| Verbose Output | `set -x` | Display executed commands |
| Environment Setup | `export PYTHONPATH=./docs_src` | Include docs in Python path |
| Parameter Passing | `${@}` | Forward all script arguments |

**Sources:** [scripts/test.sh:3-4](), [scripts/lint.sh:3-4](), [scripts/format.sh:2]()

# Project Infrastructure




This document covers the fundamental project infrastructure of FastAPI, including the build system, packaging configuration, dependency management, and development tool configurations. The infrastructure serves as the foundation that enables FastAPI's development workflow, testing, and distribution.

For information about the documentation build system, see [Documentation System](#6.1). For CI/CD automation workflows, see [CI/CD Pipeline](#6.2). For development scripts and contributor workflows, see [Development Workflow](#6.3).

## Build System and Packaging

FastAPI uses a modern Python packaging approach centered around PDM (Python Dependency Manager) as the build backend. The project configuration is entirely defined in `pyproject.toml`, following PEP 518 standards.

### Build Configuration

```mermaid
graph TD
    A["pyproject.toml"] --> B["PDM Backend"]
    B --> C["Package Distribution"]
    C --> D["PyPI Release"]
    
    A --> E["Dynamic Versioning"]
    E --> F["fastapi/__init__.py"]
    F --> G["Version Extraction"]
    
    A --> H["Source Includes"]
    H --> I["tests/"]
    H --> J["docs_src/"]
    H --> K["scripts/"]
    H --> L["requirements*.txt"]
```

**Build System Configuration**

The build system is configured in [pyproject.toml:1-3](), specifying PDM as the backend. The `pdm.backend` handles all packaging operations, from source distribution to wheel creation.

**Dynamic Versioning**

Version management is handled dynamically through [pyproject.toml:127-128](), extracting the version from [fastapi/__init__.py](). This ensures the package version stays synchronized with the codebase version without manual updates.

**Source Distribution Includes**

The build includes additional directories beyond the core package [pyproject.toml:132-139]():
- `tests/` - Test suite for distribution validation
- `docs_src/` - Documentation source examples  
- `scripts/` - Development and utility scripts
- `requirements*.txt` - Dependency specifications
- `docs/en/docs/img/favicon.png` - Required for testing

Sources: [pyproject.toml:1-139]()

### Package Metadata and Dependencies

```mermaid
graph LR
    subgraph "Core Dependencies"
        A["starlette>=0.40.0,<0.48.0"]
        B["pydantic>=1.7.4,<3.0.0"]  
        C["typing-extensions>=4.8.0"]
    end
    
    subgraph "Optional Dependencies"
        D["standard"]
        E["standard-no-fastapi-cloud-cli"]
        F["all"]
    end
    
    subgraph "Standard Set"
        G["fastapi-cli[standard]"]
        H["httpx"]
        I["jinja2"] 
        J["python-multipart"]
        K["email-validator"]
        L["uvicorn[standard]"]
    end
    
    subgraph "All Set"
        M["itsdangerous"]
        N["pyyaml"]
        O["ujson"]
        P["orjson"]
        Q["pydantic-settings"]
        R["pydantic-extra-types"]
    end
    
    A --> D
    B --> D  
    C --> D
    D --> G
    D --> H
    D --> I
    D --> J
    D --> K
    D --> L
    
    F --> M
    F --> N
    F --> O
    F --> P
    F --> Q
    F --> R
```

**Core Dependencies**

FastAPI maintains minimal core dependencies [pyproject.toml:45-49]():
- `starlette` - ASGI framework foundation
- `pydantic` - Data validation and serialization
- `typing-extensions` - Enhanced type hints

**Optional Dependency Sets**

Three optional dependency sets provide different installation profiles [pyproject.toml:58-122]():

| Set | Purpose | Key Components |
|-----|---------|----------------|
| `standard` | Common web app features | CLI, HTTP client, templates, file uploads |
| `standard-no-fastapi-cloud-cli` | Standard without FastAPI Cloud | Same as standard minus cloud CLI |
| `all` | Complete feature set | All standard features plus JSON, sessions, settings |

**CLI Entry Point**

The package provides a command-line interface through [pyproject.toml:124-125](), mapping the `fastapi` command to `fastapi.cli:main`.

Sources: [pyproject.toml:5-125]()

## Development Tool Configuration

FastAPI integrates multiple development tools through centralized configuration, ensuring consistent code quality and development experience across the project.

### Type Checking and Linting

```mermaid
graph TD
    subgraph "mypy Configuration"
        A["strict = true"]
        B["Module Overrides"]
        B --> C["fastapi.concurrency"]
        B --> D["fastapi.tests.*"] 
        B --> E["docs_src.*"]
    end
    
    subgraph "ruff Configuration"
        F["Lint Rules"]
        F --> G["pycodestyle E,W"]
        F --> H["pyflakes F"]
        F --> I["isort I"]
        F --> J["flake8-bugbear B"]
        F --> K["comprehensions C4"]
        F --> L["pyupgrade UP"]
    end
    
    subgraph "Per-file Overrides"
        M["__init__.py"]
        N["docs_src/ examples"]
        O["Security tutorials"]
        P["Dependencies tutorials"]
    end
    
    A --> F
    B --> M
    F --> M
    F --> N
    F --> O
    F --> P
```

**MyPy Type Checking**

Strict type checking is enabled globally [pyproject.toml:144-145]() with targeted overrides for specific modules:
- `fastapi.concurrency` - Relaxed import checking due to threading complexity
- `fastapi.tests.*` - Allow missing imports for test isolation
- `docs_src.*` - Relaxed rules for documentation examples

**Ruff Linting and Formatting**

Comprehensive linting rules [pyproject.toml:211-226]() cover:
- Code style enforcement (pycodestyle)
- Import organization (isort)  
- Bug prevention (flake8-bugbear)
- Code modernization (pyupgrade)

Extensive per-file overrides [pyproject.toml:228-258]() accommodate documentation examples and tutorial code that intentionally demonstrates specific patterns.

Sources: [pyproject.toml:144-266]()

### Testing and Coverage Configuration

```mermaid
graph LR
    subgraph "pytest Configuration"
        A["Strict Config"]
        B["Strict Markers"]
        C["Ignore docs_src"]
        D["XFail Strict"]
        E["JUnit XML"]
    end
    
    subgraph "Coverage Settings"
        F["Parallel Execution"]
        G["Data Directory"]
        H["Source Tracking"]
        I["Dynamic Context"]
        J["HTML Reports"]
    end
    
    subgraph "Filter Warnings"
        K["Starlette Deprecations"]
        L["Passlib Warnings"]
        M["Trio Warnings"]
        N["SQLAlchemy Warnings"]
        O["Coverage Warnings"]
    end
    
    A --> F
    C --> H
    E --> J
    K --> A
    L --> A
    M --> A
    N --> A
    O --> A
```

**Pytest Configuration**

Test execution is configured for strict validation [pyproject.toml:163-170]():
- Strict configuration prevents typos in pytest options
- Strict markers require all test markers to be registered
- Documentation source is excluded from test discovery
- XFail strict mode prevents accidentally passing expected failures

**Coverage Tracking**

Comprehensive coverage configuration [pyproject.toml:189-210]() enables:
- Parallel test execution with data aggregation
- Source tracking across `fastapi`, `tests`, and `docs_src`
- Dynamic context tracking per test function
- HTML reports with test context display

**Warning Filters**

Extensive warning filters [pyproject.toml:171-187]() handle known issues:
- Framework deprecation warnings (Starlette, SQLAlchemy)
- Library compatibility warnings (passlib, trio)
- Python version-specific warnings

Sources: [pyproject.toml:163-210]()

## Project Metadata and Distribution

The project maintains comprehensive metadata for PyPI distribution and ecosystem integration.

### Package Classification and Compatibility

```mermaid
graph TD
    subgraph "Target Audiences"
        A["Information Technology"]
        B["System Administrators"] 
        C["Developers"]
    end
    
    subgraph "Framework Classifications"
        D["AsyncIO"]
        E["FastAPI"]
        F["Pydantic v1/v2"]
    end
    
    subgraph "Python Support"
        G["Python 3.8+"]
        H["Typed Package"]
        I["OS Independent"]
    end
    
    subgraph "Topic Areas"
        J["Web Development"]
        K["HTTP Servers"]
        L["Application Frameworks"]
    end
    
    A --> D
    B --> D
    C --> D
    D --> G
    E --> G
    F --> G
    G --> J
    H --> J
    I --> J
    J --> K
    J --> L
```

**Compatibility Matrix**

FastAPI supports a broad compatibility matrix [pyproject.toml:36-41]():
- Python versions: 3.8 through 3.13
- Framework integrations: AsyncIO, Pydantic v1/v2
- Operating systems: Platform independent
- Development status: Beta (stable API, active development)

**Project URLs and Resources**

The package provides comprehensive resource links [pyproject.toml:51-56]():

| Resource | URL |
|----------|-----|
| Homepage | GitHub repository |
| Documentation | Official docs site |
| Issues | GitHub issue tracker |
| Changelog | Release notes section |

Sources: [pyproject.toml:14-56]()

## Slim Package Variant

FastAPI supports a minimal distribution variant for specialized deployment scenarios.

### Slim Build Configuration

The project includes configuration for generating a `fastapi-slim` package [pyproject.toml:141-142]() through the `tiangolo._internal-slim-build` tool. This variant likely excludes optional dependencies and development tools for reduced installation size.

This configuration enables:
- Lightweight container deployments
- Minimal dependency installations
- Specialized distribution channels

Sources: [pyproject.toml:141-142]()

The project infrastructure provides a robust foundation for FastAPI's development, testing, and distribution processes. The configuration balances strict quality standards with practical development needs, supporting both core maintainers and the broader contributor community through comprehensive tooling and clear dependency management.