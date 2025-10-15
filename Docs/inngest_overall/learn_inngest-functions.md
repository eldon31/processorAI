#### On this page

- [Inngest Functions](\docs\learn\inngest-functions#inngest-functions)
- [Anatomy of an Inngest function](\docs\learn\inngest-functions#anatomy-of-an-inngest-function)
- [Config](\docs\learn\inngest-functions#config)
- [Trigger](\docs\learn\inngest-functions#trigger)
- [Handler](\docs\learn\inngest-functions#handler)
- [Config](\docs\learn\inngest-functions#config-2)
- [Trigger](\docs\learn\inngest-functions#trigger-2)
- [Handler](\docs\learn\inngest-functions#handler-2)
- [Config](\docs\learn\inngest-functions#config-3)
- [Trigger](\docs\learn\inngest-functions#trigger-3)
- [Handler](\docs\learn\inngest-functions#handler-3)
- [Kinds of Inngest functions](\docs\learn\inngest-functions#kinds-of-inngest-functions)
- [Background functions](\docs\learn\inngest-functions#background-functions)
- [Scheduled functions](\docs\learn\inngest-functions#scheduled-functions)
- [Delayed functions](\docs\learn\inngest-functions#delayed-functions)
- [Step functions](\docs\learn\inngest-functions#step-functions)
- [Fan-out functions](\docs\learn\inngest-functions#fan-out-functions)
- [Invoking functions directly](\docs\learn\inngest-functions#invoking-functions-directly)
- [Further reading](\docs\learn\inngest-functions#further-reading)

[Inngest tour](\docs\sdk\overview)

# Inngest Functions

Inngest functions enable developers to run reliable background logic, from background jobs to complex workflows. They provide robust tools for retrying, scheduling, and coordinating complex sequences of operations.

This page covers components of an Inngest function, as well as introduces different kinds of functions. If you'd like to learn more about Inngest's execution model, check the ["How Inngest functions are executed"](\docs\learn\how-functions-are-executed) page.

## [Anatomy of an Inngest function](\docs\learn\inngest-functions#anatomy-of-an-inngest-function)

TypeScript Go Python

Let's have a look at the following Inngest function:

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction (
// config
{ id : "import-product-images" } ,
// trigger (event or cron)
{ event : "shop/product.imported" } ,
// handler function
async ({ event , step }) => {
// Here goes the business logic
// By wrapping code in steps, it will be retried automatically on failure
const s3Urls = await step .run ( "copy-images-to-s3" , async () => {
return copyAllImagesToS3 ( event . data .imageURLs);
});
// You can include numerous steps in your function
await step .run ( 'resize-images' , async () => {
await resizer .bulk ({ urls : s3Urls , quality : 0.9 , maxWidth : 1024 });
})
}
);
```

The above code can be explained as:

This Inngest function is called `import-product-images` . When an event called `shop/product.imported` is received, run two steps: `copy-images-to-s3` and `resize-images` .

Let's have a look at each of this function's components.

### [Config](\docs\learn\inngest-functions#config)

The first parameter of the `createFunction` method specifies Inngest function's configuration. In the above example, the `id` is specified, which will be used to identify the function in the Inngest system.

You can see this ID in the [Inngest Dev Server's](\docs\local-development) function list:

Screenshot of the Inngest Dev Server interface showing three functions listed under the 'Functions' tab. The functions are: 'store-events,' 'Generate monthly report,' and 'Customer Onboarding,' each with their respective triggers and App URLs.

<!-- image -->

You can also provide other [configuration options](\docs\reference\functions\create#configuration) , such as `concurrency` , `throttle` , `debounce` , `rateLimit` , `priority` , `batchEvents` , or `idempotency` (learn more about [Flow Control](\docs\guides\flow-control) ). You can also specify how many times the function will retry, what callback function will run on failure, and when to cancel the function.

### [Trigger](\docs\learn\inngest-functions#trigger)

Inngest functions are designed to be triggered by events or crons (schedules). Events can be [sent from your own code](\docs\events) or received from third party webhooks or API requests. When an event is received, it triggers a corresponding function to execute the tasks defined in the function handler (see the ["Handler" section](\docs\learn\inngest-functions#handler) below).

Each function needs at least one trigger. However, you can also work with [multiple triggers](\docs\guides\multiple-triggers) to invoke your function whenever any of the events are received or cron schedule occurs.

### [Handler](\docs\learn\inngest-functions#handler)

A "handler" is the core function that defines what should happen when the function is triggered.

The handler receives context, which includes the event data, tools for managing execution flow, or logging configuration. Let's take a closer look at them.

### [event](\docs\learn\inngest-functions#event)

Handler has access to the data which you pass when sending events to Inngest via [`inngest.send()`](\docs\reference\events\send) or [`step.sendEvent()`](\docs\reference\functions\step-send-event) .

You can see this in the example above in the `event` parameter.

### [step](\docs\learn\inngest-functions#step)

[Inngest steps](\docs\learn\inngest-steps) are fundamental building blocks in Inngest functions. They are used to manage execution flow. Each step is a discrete task, which can be executed, retried, and recovered independently, without re-executing other successful steps.

It's helpful to think of steps as code-level transactions.  If your handler contains several independent tasks, it's good practice to [wrap each one in a step](\docs\guides\multi-step-functions) .

In this way, you can manage complex state easier and if any task fails, it will be retried independently from others.

There are several step methods available at your disposal, for example, `step.run` , `step.sleep()` , or `step.waitForEvent()` .

In the example above, the handler contains two steps: `copy-images-to-s3` and `resize-images` .

## [Kinds of Inngest functions](\docs\learn\inngest-functions#kinds-of-inngest-functions)

### [Background functions](\docs\guides\background-jobs)

Long tasks can be executed outside the critical path of the main flow, which improves app's performance and reliability. Perfect for communicating with third party APIs or executing long-running code.

### [Scheduled functions](\docs\guides\scheduled-functions)

Inngest's scheduled functions enable you to run tasks automatically at specified intervals using cron schedules. These functions ensure consistent and timely execution without manual intervention. Perfect for routine operations like sending weekly reports or clearing caches.

### [Delayed functions](\docs\guides\delayed-functions)

You can enqueue an Inngest function to run at a specific time in the future. The task will be executed exactly when needed without manual intervention. Perfect for actions like sending follow-up emails or processing delayed orders.

### [Step functions](\docs\guides\multi-step-functions)

Step functions allow you to create complex workflows. You can coordinate between multiple steps, including waiting for other events, delaying execution, or running code conditionally based on previous steps or incoming events. Each [step](\docs\learn\inngest-steps) is individually retriable, making the workflow robust against failures. Ideal for scenarios like onboarding flows or conditional notifications.

### [Fan-out functions](\docs\guides\fan-out-jobs)

Inngest's fan-out jobs enable a single event to trigger multiple functions simultaneously. Ideal for parallel processing tasks, like sending notifications to multiple services or processing data across different systems.

## [Invoking functions directly](\docs\learn\inngest-functions#invoking-functions-directly)

You can [call an Inngest function directly](\docs\guides\invoking-functions-directly) from within your event-driven system by using `step.invoke()` , even across different Inngest SDKs.

This is useful when you need to break down complex workflows into simpler, manageable parts or when you want to leverage existing functionality without duplicating code. Direct invocation is ideal for orchestrating dependent tasks, handling complex business logic, or improving code maintainability and readability.

## [Further reading](\docs\learn\inngest-functions#further-reading)

- [Quick Start guide](\docs\getting-started\nextjs-quick-start?ref=docs-inngest-functions) : learn how to build complex workflows.
- ["How Inngest functions are executed"](\docs\learn\how-functions-are-executed) : learn more about Inngest's execution model.
- ["Inngest steps"](\docs\learn\inngest-steps) : understand building Inngest's blocks.
- ["Flow Control"](\docs\guides\flow-control) : learn how to manage execution within Inngest functions.