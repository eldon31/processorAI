uv run ruff format src tests
```

**Sources:** [.github/workflows/run-tests.yml:50-54](), [.github/workflows/run-static.yml:44-54](), [.pre-commit-config.yaml:27-34]()

## Troubleshooting Common Issues

### Dependency Resolution Issues

If UV fails to resolve dependencies, ensure the lockfile is up to date:

```bash
# Update lockfile
uv lock

# Force reinstall with updated lockfile
uv sync --frozen
```

### Python Version Compatibility

Verify Python version compatibility if installation fails:

```bash