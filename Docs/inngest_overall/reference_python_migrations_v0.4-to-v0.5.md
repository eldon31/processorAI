#### On this page

- [Python SDK migration guide: v0.4 to v0.5](\docs\reference\python\migrations\v0.4-to-v0.5#python-sdk-migration-guide-v0-4-to-v0-5)
- [New features](\docs\reference\python\migrations\v0.4-to-v0.5#new-features)
- [Breaking changes](\docs\reference\python\migrations\v0.4-to-v0.5#breaking-changes)
- [Move step into ctx](\docs\reference\python\migrations\v0.4-to-v0.5#move-step-into-ctx)
- [Parallel steps](\docs\reference\python\migrations\v0.4-to-v0.5#parallel-steps)
- [Remove event.user](\docs\reference\python\migrations\v0.4-to-v0.5#remove-event-user)
- [Disallow mixed async-ness within Inngest functions](\docs\reference\python\migrations\v0.4-to-v0.5#disallow-mixed-async-ness-within-inngest-functions)
- [Static error when passing a non-async callback to an async step.run](\docs\reference\python\migrations\v0.4-to-v0.5#static-error-when-passing-a-non-async-callback-to-an-async-step-run)
- [inngest.Function is generic](\docs\reference\python\migrations\v0.4-to-v0.5#inngest-function-is-generic)
- [Middleware order](\docs\reference\python\migrations\v0.4-to-v0.5#middleware-order)
- [Remove middleware hooks](\docs\reference\python\migrations\v0.4-to-v0.5#remove-middleware-hooks)
- [Remove experimental stuff](\docs\reference\python\migrations\v0.4-to-v0.5#remove-experimental-stuff)
- [Dependencies](\docs\reference\python\migrations\v0.4-to-v0.5#dependencies)

References [Python SDK](\docs\reference\python) [Migrations](\docs\reference\python\migrations\v0.4-to-v0.5)

# Python SDK migration guide: v0.4 to v0.5

This guide will help you migrate your Inngest Python SDK from v0.4 to v0.5.

## [New features](\docs\reference\python\migrations\v0.4-to-v0.5#new-features)

- First-class Pydantic support in step and function output ( [docs](\docs\reference\python\guides\pydantic) )
- Python 3.13 support
- Function singletons ( [docs](\docs\guides\singleton) )
- Function timeouts ( [docs](\docs\features\inngest-functions\cancellation\cancel-on-timeouts) )
- Experimental step.infer ( [docs](\docs\features\inngest-functions\steps-workflows\step-ai-orchestration) )
- Improved parallel step performance

## [Breaking changes](\docs\reference\python\migrations\v0.4-to-v0.5#breaking-changes)

### [Move step into ctx](\docs\reference\python\migrations\v0.4-to-v0.5#move-step-into-ctx)

The `step` object will be moved to `ctx.step` .

Before:

Copy Copied

```
@inngest_client . create_function (
fn_id = "provision-user" ,
trigger = inngest. TriggerEvent (event = "user.signup" ),
)
async def fn ( ctx : inngest . Context , step : inngest . Step) -> None :
await step . run ( "create-user" , create_db_user)
```

After:

Copy Copied

```
@inngest_client . create_function (
fn_id = "provision-user" ,
trigger = inngest. TriggerEvent (event = "user.signup" ),
)
async def fn ( ctx : inngest . Context) -> None :
await ctx . step . run ( "create-user" , create_db_user)
```

### [Parallel steps](\docs\reference\python\migrations\v0.4-to-v0.5#parallel-steps)

`step.parallel` will be removed in favor of a new `ctx.group.parallel` method. This method will behave the same way, so it's a drop-in replacement for `step.parallel` .

Copy Copied

```
@inngest_client . create_function (
fn_id = "my-fn" ,
trigger = inngest. TriggerEvent (event = "my-event" ),
)
async def fn ( ctx : inngest . Context) -> None :
user_id = ctx . event . data [ "user_id" ]

await ctx . group . parallel (
(
lambda : ctx.step. run ( "update-user" , update_user, user_id),
lambda : ctx.step. run ( "send-email" , send_email, user_id),
)
)
```

### [Remove event.user](\docs\reference\python\migrations\v0.4-to-v0.5#remove-event-user)

We're sunsetting `event.user` . It's already incompatible with some features (e.g. function run replay).

### [Disallow mixed async-ness within Inngest functions](\docs\reference\python\migrations\v0.4-to-v0.5#disallow-mixed-async-ness-within-inngest-functions)

Setting an async `on_failure` on a non-async Inngest function will throw an error:

Copy Copied

```
async def on_failure ( ctx : inngest . Context) -> None :
pass

@inngest_client . create_function (
fn_id = "foo" ,
trigger = inngest. TriggerEvent (event = "foo" ),
on_failure = on_failure,
)
def fn ( ctx : inngest . ContextSync) -> None :
pass
```

Setting a non-async `on_failure` on an async Inngest function will throw an error:

Copy Copied

```
def on_failure ( ctx : inngest . ContextSync) -> None :
pass

@inngest_client . create_function (
fn_id = "foo" ,
trigger = inngest. TriggerEvent (event = "foo" ),
on_failure = on_failure,
)
async def fn ( ctx : inngest . Context) -> None :
pass
```

### [Static error when passing a non-async callback to an async step.run](\docs\reference\python\migrations\v0.4-to-v0.5#static-error-when-passing-a-non-async-callback-to-an-async-step-run)

When passing a non-async callback to an async `step.run` , it will work at runtime but there will be a static type error.

Copy Copied

```
@inngest_client . create_function (
fn_id = "foo" ,
trigger = inngest. TriggerEvent (event = "foo" ),
)
async def fn ( ctx : inngest . Context) -> None :
# Type error because `lambda: "hello"` is non-async.
msg = await ctx . step . run ( "step" , lambda : "hello" )

# Runtime value is "hello", as expected.
print (msg)
```

### [inngest.Function is generic](\docs\reference\python\migrations\v0.4-to-v0.5#inngest-function-is-generic)

The `inngest.Function` class is now a generic that represents the return type. So if an Inngest function returns `str` then it would be `inngest.Function[str]` .

### [Middleware order](\docs\reference\python\migrations\v0.4-to-v0.5#middleware-order)

Use LIFO for the "after" hooks. In other words, when multiple middleware is specified then the "after" hooks are run in reverse order.

For example, let's say the following middleware is defined and used:

Copy Copied

```
class A ( inngest . MiddlewareSync ):
def before_execution ( self ) -> None :
pass

def after_execution ( self ) -> None :
pass

class B ( inngest . MiddlewareSync ):
def before_execution ( self ) -> None :
pass

def after_execution ( self ) -> None :
pass

inngest . Inngest (
app_id = "my-app" ,
middleware = [A, B],
)
```

The middleware will be executed in the following order for each hook:

- `before_execution` -- `A` then `B` .
- `after_execution` -- `B` then `A` .

The "before" hooks are:

Copy Copied

```
before_execution
before_response
before_send_events
transform_input
```

The "after" hooks are:

Copy Copied

```
after_execution
after_send_events
transform_output
```

### [Remove middleware hooks](\docs\reference\python\migrations\v0.4-to-v0.5#remove-middleware-hooks)

- before\_memoization
- after\_memoization

### [Remove experimental stuff](\docs\reference\python\migrations\v0.4-to-v0.5#remove-experimental-stuff)

- `inngest.experimental.encryption_middleware` (it's now the [inngest-encryption](https://pypi.org/project/inngest-encryption/) package).
- `experimental_execution` option on functions. We won't support native `asyncio` methods (e.g. `asyncio.gather` ) going forward.

### [Dependencies](\docs\reference\python\migrations\v0.4-to-v0.5#dependencies)

Drop support for Python `3.9` .

Bump dependency minimum versions:

Copy Copied

```
httpx>=0.26.0
pydantic>=2.11.0
typing-extensions>=4.13.0
```

Bump peer dependency minimum versions:

Copy Copied

```
Django>=5.0
Flask>=3.0.0
fastapi>=0.110.0
tornado>=6.4
```