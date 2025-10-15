This document covers the installation procedures, dependency management, and initial configuration for the FastMCP framework. It provides step-by-step instructions for setting up a development or production environment.

For information about running FastMCP servers and CLI commands, see [Command Line Interface](#5). For details about server configuration and settings, see [Configuration Management](#8).

## System Requirements

FastMCP requires Python 3.10 or higher and uses UV as the primary package manager for dependency resolution and virtual environment management.

### Python Version Support

| Python Version | Support Status |
|----------------|----------------|
| 3.10 | ✅ Supported |
| 3.11 | ✅ Supported | 
| 3.12 | ✅ Supported |
| < 3.10 | ❌ Not supported |

**Sources:** [pyproject.toml:20](), [pyproject.toml:37-39]()

## Installation Methods

### UV Package Manager Installation

The recommended installation method uses UV for optimal dependency resolution and environment isolation:

```bash