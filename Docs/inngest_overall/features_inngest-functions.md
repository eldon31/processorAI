#### On this page

- [Inngest Functions](\docs\features\inngest-functions#inngest-functions)
- [Using Inngest Functions](\docs\features\inngest-functions#using-inngest-functions)
- [Learn more about Functions and Steps](\docs\features\inngest-functions#learn-more-about-functions-and-steps)
- [SDK References](\docs\features\inngest-functions#sdk-references)

Features

# Inngest Functions

Inngest functions enable developers to run reliable background logic, from background jobs to complex workflows.

An Inngest Function is composed of 3 main parts that provide robust tools for retrying, scheduling, and coordinating complex sequences of operations:

## [Triggers](\docs\features\events-triggers)

[A list of Events, Cron schedules or webhook events that trigger Function runs.](\docs\features\events-triggers)

## [Flow Control](\docs\guides\flow-control)

[Control how Function runs get distributed in time with Concurrency, Throttling and more.](\docs\guides\flow-control)

## [Steps](\docs\features\inngest-functions\steps-workflows)

[Transform your Inngest Function into a workflow with retriable checkpoints.](\docs\features\inngest-functions\steps-workflows)

TypeScript Python Go

Copy Copied

```
inngest .createFunction ({
id : "sync-systems" ,
// Easily add Throttling with Flow Control
throttle : { limit : 3 , period : "1min" } ,
} ,
// A Function is triggered by events
{ event : "auto/sync.request" } ,
async ({ step }) => {
// step is retried if it throws an error
const data = await step .run ( "get-data" , async () => {
return getDataFromExternalSource ();
});

// Steps can reuse data from previous ones
await step .run ( "save-data" , async () => {
return db . syncs .insertOne (data);
});
}
);
```

## [Using Inngest Functions](\docs\features\inngest-functions#using-inngest-functions)

Start using Inngest Functions by using the pattern that fits your use case:

## [Background jobs](\docs\guides\multi-step-functions)

[Run long-running tasks  out of the critical path of a request.](\docs\guides\multi-step-functions)

## [Delayed Functions](\docs\learn\how-functions-are-executed)

[Schedule Functions that run in the future.](\docs\learn\how-functions-are-executed)

## [Cron Functions](\docs\guides\scheduled-functions)

[Build Inngest Functions as CRONs.](\docs\guides\scheduled-functions)

## [Workflows](\docs\features\inngest-functions\steps-workflows)

[Start creating worflows by leveraging Inngest Function Steps.](\docs\features\inngest-functions\steps-workflows)

## [Learn more about Functions and Steps](\docs\features\inngest-functions#learn-more-about-functions-and-steps)

Functions and Steps are powered by Inngest's Durable Execution Engine. Learn about its inner working by reading the following guides:

## [How Functions are executed](\docs\learn\how-functions-are-executed)

[A deep dive into Inngest's Durable Execution Engine with a step-by-step workflow run example.](\docs\learn\how-functions-are-executed)

## [Thinking in Steps](\docs\guides\multi-step-functions)

[Discover by example how steps enable more reliable and flexible functions with step-level error handling, conditional steps and waits.](\docs\guides\multi-step-functions)

## [SDK References](\docs\features\inngest-functions#sdk-references)

## [TypeScript SDK](\docs\reference\typescript)

[API reference](\docs\reference\typescript)

## [Python SDK](\docs\reference\python)

[API reference](\docs\reference\python)

## [Go SDK](https://pkg.go.dev/github.com/inngest/inngestgo@v0.9.0/step)

[Go API reference](https://pkg.go.dev/github.com/inngest/inngestgo@v0.9.0/step)