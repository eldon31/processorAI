#### On this page

- [Run](\docs\reference\python\steps\run#run)
- [Arguments](\docs\reference\python\steps\run#arguments)
- [Examples](\docs\reference\python\steps\run#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Run

Turn a normal function into a durable function. Any function passed to `step.run` will be executed in a durable way, including retries and memoization.

## [Arguments](\docs\reference\python\steps\run#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `handler` Type Callable Required required Description A callable that has no arguments and returns a JSON serializable value.
- Name `*handler_args` Type Required optional Description Positional arguments for the handler. This is type-safe since we infer the types from the handler using generics.

## [Examples](\docs\reference\python\steps\run#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "my_function" ,
trigger = inngest. TriggerEvent (event = "app/my_function" ),
)
async def fn ( ctx : inngest . Context) -> None :
# Pass a function to step.run
await ctx . step . run ( "my_fn" , my_fn)

# Args are passed after the function
await ctx . step . run ( "my_fn_with_args" , my_fn_with_args, 1 , "a" )

# Kwargs require functools.partial
await ctx . step . run (
"my_fn_with_args_and_kwargs" ,
functools. partial (my_fn_with_args_and_kwargs, 1 , b = "a" ),
)

# Defining functions like this gives you easy access to scoped variables
def use_scoped_variable () -> None :
print (ctx.event.data[ "user_id" ])

await ctx . step . run ( "use_scoped_variable" , use_scoped_variable)

async def my_fn () -> None :
pass

async def my_fn_with_args ( a : int , b : str ) -> None :
pass

async def my_fn_with_args_and_kwargs ( a : int , * , b : str ) -> None :
pass
```