#### On this page

- [Invoke](\docs\reference\python\steps\invoke#invoke)
- [Arguments](\docs\reference\python\steps\invoke#arguments)
- [Examples](\docs\reference\python\steps\invoke#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Invoke v0.3.0+

Calls another Inngest function, waits for its completion, and returns its output.

## [Arguments](\docs\reference\python\steps\invoke#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `function` Type Function Required required Description Invoked function.
- Name `data` Type object Required optional Description JSON-serializable data that will be passed to the invoked function as `event.data` .
- Name `user` Type object Required optional Description JSON-serializable data that will be passed to the invoked function as `event.user` .

## [Examples](\docs\reference\python\steps\invoke#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "fn-1" ,
trigger = inngest. TriggerEvent (event = "app/fn-1" ),
)
async def fn_1 ( ctx : inngest . Context) -> None :
return "Hello!"

@inngest_client . create_function (
fn_id = "fn-2" ,
trigger = inngest. TriggerEvent (event = "app/fn-2" ),
)
async def fn_2 ( ctx : inngest . Context) -> None :
output = await ctx . step . invoke (
"invoke" ,
function = fn_1,
)

# Prints "Hello!"
print (output)
```

💡 `step.invoke` works within a single app or across apps, since the app ID is built into the function object.