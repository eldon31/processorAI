#### On this page

- [Sleep until](\docs\reference\python\steps\sleep-until#sleep-until)
- [Arguments](\docs\reference\python\steps\sleep-until#arguments)
- [Examples](\docs\reference\python\steps\sleep-until#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Sleep until

Sleep until a specific time. Accepts a `datetime.datetime` object.

## [Arguments](\docs\reference\python\steps\sleep-until#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `until` Type datetime.datetime Required required Description Time to sleep until.

## [Examples](\docs\reference\python\steps\sleep-until#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "my_function" ,
trigger = inngest. TriggerEvent (event = "app/my_function" ),
)
async def fn ( ctx : inngest . Context) -> None :
await ctx . step . sleep_until (
"zzz" ,
datetime.datetime. now () + datetime. timedelta (seconds = 2 ),
)
```