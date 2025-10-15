#### On this page

- [Invoke by ID](\docs\reference\python\steps\invoke_by_id#invoke-by-id)
- [Arguments](\docs\reference\python\steps\invoke_by_id#arguments)
- [Examples](\docs\reference\python\steps\invoke_by_id#examples)
- [Within the same app](\docs\reference\python\steps\invoke_by_id#within-the-same-app)
- [Across apps](\docs\reference\python\steps\invoke_by_id#across-apps)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Invoke by ID v0.3.0+

Calls another Inngest function, waits for its completion, and returns its output.

This method behaves identically to the [invoke](\docs\reference\python\steps\invoke) step method, but accepts an ID instead of the function object. This can be useful for a few reasons:

- Trigger a function whose code is in a different codebase.
- Avoid circular dependencies.
- Avoid undesired transitive imports.

## [Arguments](\docs\reference\python\steps\invoke_by_id#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `app_id` Type str Required optional Description App ID of the invoked function.
- Name `function_id` Type str Required required Description ID of the invoked function.
- Name `data` Type object Required optional Description JSON-serializable data that will be passed to the invoked function as `event.data` .
- Name `user` Type object Required optional Description JSON-serializable data that will be passed to the invoked function as `event.user` .

## [Examples](\docs\reference\python\steps\invoke_by_id#examples)

### [Within the same app](\docs\reference\python\steps\invoke_by_id#within-the-same-app)

Copy Copied

```
@inngest_client . create_function (
fn_id = "fn-1" ,
trigger = inngest. TriggerEvent (event = "app/fn-1" ),
)
async def fn_1 ( ctx : inngest . Context) -> str :
return "Hello!"

@inngest_client . create_function (
fn_id = "fn-2" ,
trigger = inngest. TriggerEvent (event = "app/fn-2" ),
)
async def fn_2 ( ctx : inngest . Context) -> None :
output = ctx . step . invoke_by_id (
"invoke" ,
function_id = "fn-1" ,
)

# Prints "Hello!"
print (output)
```

### [Across apps](\docs\reference\python\steps\invoke_by_id#across-apps)

Copy Copied

```
inngest_client_1 = inngest . Inngest (app_id = "app-1" )
inngest_client_2 = inngest . Inngest (app_id = "app-2" )

@inngest_client_1 . create_function (
fn_id = "fn-1" ,
trigger = inngest. TriggerEvent (event = "app/fn-1" ),
)
async def fn_1 ( ctx : inngest . Context) -> str :
return "Hello!"

@inngest_client_2 . create_function (
fn_id = "fn-2" ,
trigger = inngest. TriggerEvent (event = "app/fn-2" ),
)
async def fn_2 ( ctx : inngest . Context) -> None :
output = ctx . step . invoke_by_id (
"invoke" ,
app_id = "app-1" ,
function_id = "fn-1" ,
)

# Prints "Hello!"
print (output)
```