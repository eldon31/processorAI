#### On this page

- [Create Function](\docs\reference\python\functions\create#create-function)
- [create\_function](\docs\reference\python\functions\create#create-function-2)
- [Configuration](\docs\reference\python\functions\create#configuration)
- [Triggers](\docs\reference\python\functions\create#triggers)
- [TriggerEvent](\docs\reference\python\functions\create#trigger-event)
- [TriggerCron](\docs\reference\python\functions\create#trigger-cron)
- [Multiple Triggers](\docs\reference\python\functions\create#multiple-triggers)
- [Handler](\docs\reference\python\functions\create#handler)
- [ctx](\docs\reference\python\functions\create#ctx)
- [step](\docs\reference\python\functions\create#step)

References [Python SDK](\docs\reference\python)

# Create Function

Define your functions using the `create_function` decorator.

Copy Copied

```
import inngest

@inngest_client . create_function (
fn_id = "import-product-images" ,
trigger = inngest. TriggerEvent (event = "shop/product.imported" ),
)
async def fn ( ctx : inngest . Context):
# Your function code
```

## [create\_function](\docs\reference\python\functions\create#create-function-2)

The `create_function` decorator accepts a configuration and wraps a plain function.

### [Configuration](\docs\reference\python\functions\create#configuration)

- Name `batch_events` Type Batch Required optional Description Configure how the function should consume batches of events ( [reference](\docs\guides\batching) ) Show nested properties
- Name `cancel` Type Cancel Required optional Description Define an event that can be used to cancel a running or sleeping function ( [guide](\docs\guides\cancel-running-functions) ) Show nested properties
- Name `debounce` Type Debounce Required optional Description Options to configure function debounce ( [reference](\docs\reference\functions\debounce) ) Show nested properties
- Name `fn_id` Type str Required required Description A unique identifier for your function. This should not change between deploys.
- Name `name` Type str Required optional Description A name for your function. If defined, this will be shown in the UI as a friendly display name instead of the ID.
- Name `on_failure` Type function Required optional Description A function that will be called only when this Inngest function fails after all retries have been attempted ( [reference](\docs\reference\functions\handling-failures) )
- Name `priority` Type Priority Required optional Version 0.4.0+ Description Configure function run prioritization. Show nested properties
- Name `rate_limit` Type RateLimit Required optional Description Options to configure how to rate limit function execution ( [reference](\docs\reference\functions\rate-limit) ) Show nested properties
- Name `retries` Type int Required optional Description Configure the number of times the function will be retried from `0` to `20` . Default: `4`
- Name `throttle` Type Throttle Required optional Description Options to configure how to throttle function execution Show nested properties
- Name `idempotency` Type string Required optional Description A key expression used to prevent duplicate events from triggering a function more than once in 24 hours. [Read the idempotency guide here](\docs\guides\handling-idempotency) . Expressions are defined using the Common Expression Language (CEL) with the original event accessible using dot-notation. Read [our guide to writing expressions](\docs\guides\writing-expressions) for more information.
- Name `trigger` Type TriggerEvent | TriggerCron | list[TriggerEvent | TriggerCron] Required required Description What should trigger the function to run. Either an event or a cron schedule. Use a list to specify multiple triggers.

## [Triggers](\docs\reference\python\functions\create#triggers)

### [TriggerEvent](\docs\reference\python\functions\create#trigger-event)

- Name `event` Type str Required required Description The name of the event.
- Name `expression` Type str Required optional Description A match expression using arbitrary event data. For example, `event.data.user_id == async.data.user_id` will only match events whose `data.user_id` matches the original trigger event's `data.user_id` .

### [TriggerCron](\docs\reference\python\functions\create#trigger-cron)

- Name `cron` Type str Required required Description A [unix-cron](https://crontab.guru/) compatible schedule string. Optional timezone prefix, e.g. `TZ=Europe/Paris 0 12 * * 5` .

### [Multiple Triggers](\docs\reference\python\functions\create#multiple-triggers)

Multiple triggers can be defined by setting the `trigger` option to a list of `TriggerEvent` or `TriggerCron` objects:

Copy Copied

```
import inngest

@inngest_client . create_function (
fn_id = "import-product-images" ,
trigger = [
inngest. TriggerEvent (event = "shop/product.imported" ),
inngest. TriggerEvent (event = "shop/product.updated" ),
],
)
async def fn ( ctx : inngest . Context):
# Your function code
```

For more information, see the [Multiple](\docs\guides\multiple-triggers)

[Triggers](\docs\guides\multiple-triggers)

guide.

## [Handler](\docs\reference\python\functions\create#handler)

The handler is your code that runs whenever the trigger occurs. Every function handler receives a single object argument which can be deconstructed. The key arguments are `event` and `step` . Note, that scheduled functions that use a `cron` trigger will not receive an `event` argument.

Copy Copied

```
@inngest_client . create_function (
# Function options
)
async def fn ( ctx : inngest . Context):
# Function code
```

### [ctx](\docs\reference\python\functions\create#ctx)

- Name `attempt` Type int Description The current zero-indexed attempt number for this function execution. The first attempt will be 0, the second 1, and so on. The attempt number is incremented every time the function throws an error and is retried.
- Name `event` Type Event Description The event payload `object` that triggered the given function run. The event payload object will match what you send with [`inngest.send()`](\docs\reference\events\send) . Below is an example event payload object: Properties
- Name `events` Type list[Event] Description A list of `event` objects that's accessible when the `batch_events` is set on the function configuration. If batching is not configured, the list contains a single event payload matching the `event` argument.
- Name `logger` Type logging.Logger Description A proxy object around either the logger you provided or the default logger.
- Name `run_id` Type str Description The unique ID for the given function run. This can be useful for logging and looking up specific function runs in the Inngest dashboard.

### [step](\docs\reference\python\functions\create#step)

The `step` object has a method for each kind of step in the Inngest platform.

If your function is `async` then its type is `Step` and you can use `await` to call its methods. If your function is not `async` then its type is `SyncStep` .

- Name `run` Type Callable Description [Docs](\docs\reference\python\steps\run)
- Name `send_event` Type Callable Description [Docs](\docs\reference\python\steps\send-event)
- Name `sleep` Type Callable Description [Docs](\docs\reference\python\steps\sleep)
- Name `sleep_until` Type Callable Description [Docs](\docs\reference\python\steps\sleep-until)
- Name `_experimental_parallel` Type Callable Version 0.2.0+ Description [Docs](\docs\reference\python\steps\parallel)