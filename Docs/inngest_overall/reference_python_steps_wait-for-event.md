#### On this page

- [Wait for event](\docs\reference\python\steps\wait-for-event#wait-for-event)
- [Arguments](\docs\reference\python\steps\wait-for-event#arguments)
- [Examples](\docs\reference\python\steps\wait-for-event#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Wait for event

Wait until the Inngest server receives a specific event.

If an event is received before the timeout then the event is returned. If the timeout is reached then `None` is returned.

## [Arguments](\docs\reference\python\steps\wait-for-event#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `event` Type str Required required Description Name of the event to wait for.
- Name `if_exp` Type str | None Required optional Description Only match events that match this CEL expression. For example, `"event.data.height == async.data.height"` will only match incoming events whose `data.height` matches the `data.height` value for the trigger event.
- Name `timeout` Type int | datetime.timedelta Required required Description In milliseconds.

## [Examples](\docs\reference\python\steps\wait-for-event#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "my_function" ,
trigger = inngest. TriggerEvent (event = "app/my_function" ),
)
async def fn ( ctx : inngest . Context) -> None :
res = await ctx . step . wait_for_event (
"wait" ,
event = "app/wait_for_event.fulfill" ,
timeout = datetime. timedelta (seconds = 2 ),
)
```