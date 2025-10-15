data1 = step.run("fetch_data", fetch_fn, id1)  # step ID internally: "fetch_data"
data2 = step.run("fetch_data", fetch_fn, id2)  # step ID internally: "fetch_data:1" 
```

Sources: [pkg/inngest/inngest/_internal/step_lib/base.py:111-124](), [pkg/inngest/inngest/_internal/step_lib/base.py:133-149]()

## Error Handling in Steps

Steps handle errors in different ways depending on the error type:

| Error Type | Behavior |
|------------|----------|
| Regular exceptions | Automatically retried with exponential backoff |
| `NonRetriableError` | Not retried, bubbled up to the function level |
| `RetryAfterError` | Retried after a specified delay |
| Nested step errors | Rejected with a clear error message |

Error handling code:
```python
try:
    output = handler(*handler_args)
    # Success case
except (errors.NonRetriableError, errors.RetryAfterError) as err:
    # Bubble up these error types to the function level
    raise err
except Exception as err:
    # Regular exceptions are captured and will be retried
    step_info.op = server_lib.Opcode.STEP_ERROR
    raise ResponseInterrupt(...)
```

Sources: [pkg/inngest/inngest/_internal/step_lib/step_async.py:202-236](), [pkg/inngest/inngest/_internal/step_lib/step_sync.py:190-215]()

## Best Practices

### Step ID Naming

- Use descriptive, unique step IDs that reflect what the step does
- Keep IDs consistent between function runs for proper memoization
- Avoid dynamically generated IDs that could change between runs

### Step Design

- Keep steps focused on a single operation
- Make steps deterministic - same inputs should produce same outputs
- Use appropriate timeout values for operations that might take time
- Prefer smaller, more granular steps over large monolithic ones

### Error Handling

- Let the step system handle retriable errors automatically
- Use `NonRetriableError` for errors that shouldn't be retried
- Include contextual information in your error messages
- Test error scenarios to ensure proper recovery