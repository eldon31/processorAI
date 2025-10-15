#### On this page

- [Parallel](\docs\reference\python\steps\parallel#parallel)
- [Arguments](\docs\reference\python\steps\parallel#arguments)
- [Examples](\docs\reference\python\steps\parallel#examples)
- [Frequently Asked Questions](\docs\reference\python\steps\parallel#frequently-asked-questions)
- [Do parallel steps work if I don't use async functions?](\docs\reference\python\steps\parallel#do-parallel-steps-work-if-i-don-t-use-async-functions)
- [Can I use asyncio.gather instead of step.parallel?](\docs\reference\python\steps\parallel#can-i-use-asyncio-gather-instead-of-step-parallel)
- [Why does step.parallel accept a tuple instead of variadic arguments?](\docs\reference\python\steps\parallel#why-does-step-parallel-accept-a-tuple-instead-of-variadic-arguments)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Parallel v0.3.0+

Run steps in parallel. Returns the parallel steps' result as a tuple.

## [Arguments](\docs\reference\python\steps\parallel#arguments)

- Name `callables` Type tuple[Callable[[], object], ...] Required required Description Accepts a tuple of callables. Each callable has no arguments and returns a JSON serializable value. Typically this is just a `lambda` around a `step` method.

## [Examples](\docs\reference\python\steps\parallel#examples)

Running two steps in parallel:

Copy Copied

```
@inngest_client . create_function (
fn_id = "my-function" ,
trigger = inngest. TriggerEvent (event = "my-event" ),
)
async def fn ( ctx : inngest . Context) -> None :
user_id = ctx . event . data [ "user_id" ]

(updated_user , sent_email) = await ctx . group . parallel (
(
lambda : ctx.step. run ( "update-user" , update_user, user_id),
lambda : ctx.step. run ( "send-email" , send_email, user_id),
)
)
```

Dynamically building a tuple of parallel steps:

Copy Copied

```
@client . create_function (
fn_id = "my-function" ,
trigger = inngest. TriggerEvent (event = "my-event" ),
)
async def fn ( ctx : inngest . Context) -> None :
parallel_steps = tuple [ typing . Callable [ [] , typing . Awaitable [ bool ]]]()
for user_id in ctx . event . data [ "user_ids" ]:
parallel_steps += tuple (
[
functools. partial (
ctx.step.run,
f "get-user- { user_id } " ,
functools. partial (update_user, user_id),
)
]
)

updated_users = await ctx . group . parallel (parallel_steps)
```

⚠️ Use `functools.partial` instead of `lambda` when building the tuple in a loop. If `lambda` is used, then the step functions will use the last value of the loop variable. This is due to Python's lack of block scoping.

## [Frequently Asked Questions](\docs\reference\python\steps\parallel#frequently-asked-questions)

### [Do parallel steps work if I don't use async functions?](\docs\reference\python\steps\parallel#do-parallel-steps-work-if-i-don-t-use-async-functions)

Yes, parallel steps work with both `async` and non- `async` functions. Since our execution model uses a separate HTTP request for each step, threaded HTTP frameworks (for example, Flask) will create a separate thread for each step.

### [Can I use asyncio.gather instead of step.parallel ?](\docs\reference\python\steps\parallel#can-i-use-asyncio-gather-instead-of-step-parallel)

No, `asyncio.gather` will not work as expected. Inngest's execution model necessitates a control flow interruption when it encounters a `step` method, but currently that does not work with `asyncio.gather` .

### [Why does step.parallel accept a tuple instead of variadic arguments?](\docs\reference\python\steps\parallel#why-does-step-parallel-accept-a-tuple-instead-of-variadic-arguments)

To properly type-annotate `step.parallel` , the return types of the callables need to be statically "extracted". Python's type-checkers are better at doing this with tuples than with variadic arguments. Mypy still struggles even with tuples, but Pyright is able to properly infer the `step.parallel` return type.