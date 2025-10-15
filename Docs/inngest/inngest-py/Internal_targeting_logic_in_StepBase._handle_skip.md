is_targeting_enabled = self._target_hashed_id is not None
is_targeted = self._target_hashed_id == parsed_step_id.hashed
if is_targeting_enabled and not is_targeted:
    raise SkipInterrupt(parsed_step_id.user_facing)
```

Sources: [pkg/inngest/inngest/_internal/step_lib/step_async.py:153-235](), [pkg/inngest/inngest/_internal/step_lib/step_sync.py:151-224](), [pkg/inngest/inngest/_internal/step_lib/base.py:96-109]()

### Step.invoke

`invoke` allows you to call another Inngest function from within a step:

```python
# Invoke by function object
result = step.invoke(
    "invoke_other_fn",
    function=other_function,
    data={"key": "value"},
    timeout=10000  # milliseconds
)

# Invoke by function ID
result = step.invoke_by_id(
    "invoke_by_id",
    function_id="my_function",
    app_id="my_app",  # optional, defaults to current app
    data={"key": "value"}
)
```

Sources: [pkg/inngest/inngest/_internal/step_lib/step_async.py:36-138](), [pkg/inngest/inngest/_internal/step_lib/step_sync.py:41-143]()

### Step.send_event

`send_event` allows you to send one or more events from within a step:

```python