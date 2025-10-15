#### On this page

- [Sleep](\docs\reference\python\steps\sleep#sleep)
- [Arguments](\docs\reference\python\steps\sleep#arguments)
- [Examples](\docs\reference\python\steps\sleep#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Sleep

Sleep for a period of time. Accepts either a `datetime.timedelta` object or a number of milliseconds.

## [Arguments](\docs\reference\python\steps\sleep#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `duration` Type int | datetime.timedelta Required required Description How long to sleep. Can be either a number of milliseconds or a `datetime.timedelta` object.

## [Examples](\docs\reference\python\steps\sleep#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "my_function" ,
trigger = inngest. TriggerEvent (event = "app/my_function" ),
)
async def fn ( ctx : inngest . Context) -> None :
await ctx . step . sleep ( "zzz" , datetime. timedelta (seconds = 2 ))
```