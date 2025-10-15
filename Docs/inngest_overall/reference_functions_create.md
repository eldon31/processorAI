#### On this page

- [Create Function](\docs\reference\functions\create#create-function)
- [inngest.createFunction(configuration, trigger, handler): InngestFunction](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function)
- [Configuration](\docs\reference\functions\create#configuration)
- [Trigger](\docs\reference\functions\create#trigger)
- [Handler](\docs\reference\functions\create#handler)

References [TypeScript SDK](\docs\reference\typescript)

# Create Function

Define your functions using the `createFunction` method on the [Inngest client](\docs\reference\client\create) .

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction (
{ id : "import-product-images" } ,
{ event : "shop/product.imported" } ,
async ({ event , step , runId }) => {
// Your function code
}
);
```

## [inngest.createFunction(configuration, trigger, handler): InngestFunction](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function)

The `createFunction` method accepts a series of arguments to define your function.

### [Configuration](\docs\reference\functions\create#configuration)

- Name `id` Type string Required required Description A unique identifier for your function. This should not change between deploys.
- Name `name` Type string Required optional Description A name for your function. If defined, this will be shown in the UI as a friendly display name instead of the ID.
- Name `concurrency` Type number | object | [object, object] Required optional Description Limit the number of concurrently running functions ( [reference](\docs\functions\concurrency) ) Show nested properties
- Name `throttle` Type object Required optional Description Limits the number of new function runs started over a given period of time ( [guide](\docs\guides\throttling) ). Show nested properties
- Name `idempotency` Type string Required optional Description A key expression which is used to prevent duplicate events from triggering a function more than once in 24 hours. This is equivalent to setting `rateLimit` with a `key` , a `limit` of `1` and `period` of `24hr` . [Read the idempotency guide here](\docs\guides\handling-idempotency) . Expressions are defined using the Common Expression Language (CEL) with the original event accessible using dot-notation. Read [our guide to writing expressions](\docs\guides\writing-expressions) for more info. Examples:
- Name `rateLimit` Type object Required optional Description Options to configure how to rate limit function execution ( [reference](\docs\reference\functions\rate-limit) ) Show nested properties
- Name `debounce` Type object Required optional Description Options to configure function debounce ( [reference](\docs\reference\functions\debounce) ) Show nested properties
- Name `priority` Type object Required optional Description Options to configure how to prioritize functions Show nested properties
- Name `batchEvents` Type object Required optional Description Configure how the function should consume batches of events ( [reference](\docs\guides\batching) ) Show nested properties
- Name `retries` Type number Required optional Description Configure the number of times the function will be retried from `0` to `20` . Default: `4`
- Name `onFailure` Type function Required optional Description A function that will be called only when this Inngest function fails after all retries have been attempted ( [reference](\docs\reference\functions\handling-failures) )
- Name `cancelOn` Type array of objects Required optional Description Define events that can be used to cancel a running or sleeping function ( [reference](\docs\reference\typescript\functions\cancel-on) ) Show nested properties
- Name `timeouts` Type object Required optional Description Options to configure timeouts for cancellation ( [reference](\docs\features\inngest-functions\cancellation\cancel-on-timeouts) ) Show nested properties

### [Trigger](\docs\reference\functions\create#trigger)

One of the following function triggers is **Required** .

You can also specify an array of up to 10 of the following triggers to invoke

your function with multiple events or crons. See the

[Multiple Triggers](\docs\guides\multiple-triggers) guide.

Cron triggers with overlapping schedules for a single function will be deduplicated.

- Name `event` Type string Required optional Description The name of the event that will trigger this event to run
- Name `cron` Type string Required optional Description A [unix-cron](https://crontab.guru/) compatible schedule string. Optional timezone prefix, e.g. `TZ=Europe/Paris 0 12 * * 5` .

When using an `event` trigger, you can optionally combine it with the `if` option to filter events:

Additional options

- Name `if` Type string Required optional Description A comparison expression that returns true or false whether the function should handle or ignore a given matching event. Expressions are defined using the Common Expression Language (CEL) with the original event accessible using dot-notation. Read [our guide to writing expressions](\docs\guides\writing-expressions) for more info. Examples:

### [Handler](\docs\reference\functions\create#handler)

The handler is your code that runs whenever the trigger occurs. Every function handler receives a single object argument which can be deconstructed. The key arguments are `event` and `step` . Note, that scheduled functions that use a `cron` trigger will not receive an `event` argument.

Copy Copied

```
function handler ({ event , events , step , runId , logger , attempt }) { /* ... */ }
```

### [event](\docs\reference\functions\create#event)

The event payload `object` that triggered the given function run. The event payload object will match what you send with [`inngest.send()`](\docs\reference\events\send) . Below is an example event payload object:

Copy Copied

```
{
name : "app/account.created" ,
data : {
userId : "1234567890"
} ,
v : "2023-05-12.1" ,
ts : 1683898268584
}
```

### [events v2.2.0+](\docs\reference\functions\create#events)

`events` is an array of `event` payload objects that's accessible when the `batchEvents` is set on the function configuration.

If batching is not configured, the array contains a single event payload matching the

`event` argument.

### [step](\docs\reference\functions\create#step)

The `step` object has methods that enable you to define

- [`step.run()`](\docs\reference\functions\step-run) - Run synchronous or asynchronous code as a retriable step in your function
- [`step.sleep()`](\docs\reference\functions\step-sleep) - Sleep for a given amount of time
- [`step.sleepUntil()`](\docs\reference\functions\step-sleep-until) - Sleep until a given time
- [`step.invoke()`](\docs\reference\functions\step-invoke) - Invoke another Inngest function as a step, receiving the result of the invoked function
- [`step.waitForEvent()`](\docs\reference\functions\step-wait-for-event) - Pause a function's execution until another event is received
- [`step.sendEvent()`](\docs\reference\functions\step-send-event) - Send event(s) reliability within your function. Use this instead of `inngest.send()` to ensure reliable event delivery from within functions.

### [runId](\docs\reference\functions\create#run-id)

The unique ID for the given function run. This can be useful for logging and looking up specific function runs in the Inngest dashboard.

### [logger v2.0.0+](\docs\reference\functions\create#logger)

The `logger` object exposes the following interfaces.

Copy Copied

```
export interface Logger {
info ( ... args : any []) : void ;
warn ( ... args : any []) : void ;
error ( ... args : any []) : void ;
debug ( ... args : any []) : void ;
}
```

It is a proxy object that is either backed by `console` or the logger you provided ( [reference](\docs\guides\logging) ).

### [attempt v2.5.0+](\docs\reference\functions\create#attempt)

The current zero-indexed attempt number for this function execution. The first attempt will be 0, the second 1, and so on. The attempt number is incremented every time the function throws an error and is retried.