#### On this page

- [Steps &amp; Workflows](\docs\features\inngest-functions\steps-workflows#steps-and-workflows)
- [How steps work](\docs\features\inngest-functions\steps-workflows#how-steps-work)
- [SDK References](\docs\features\inngest-functions\steps-workflows#sdk-references)

Features [Inngest Functions](\docs\features\inngest-functions)

# Steps &amp; Workflows

Steps are fundamental building blocks of Inngest, turning your Inngest Functions into reliable workflows that can runs for months and recover from failures.

## [Thinking in Steps](\docs\guides\multi-step-functions)

[Discover by example how steps enable more reliable and flexible functions with step-level error handling, conditional steps and waits.](\docs\guides\multi-step-functions)

Once you are familiar with Steps, start adding new capabilities to your Inngest Functions:

## [Add sleeps](\docs\features\inngest-functions\steps-workflows\sleeps)

[Enable your Inngest Functions to pause by waiting from minutes to months.](\docs\features\inngest-functions\steps-workflows\sleeps)

## [Wait for events](\docs\features\inngest-functions\steps-workflows\wait-for-event)

[Write functions that react to incoming events.](\docs\features\inngest-functions\steps-workflows\wait-for-event)

## [Loop over steps](\docs\guides\working-with-loops)

[Iterate over large datasets by looping with steps.](\docs\guides\working-with-loops)

## [Parallelize steps](\docs\guides\step-parallelism)

[Discover how to apply the map-reduce pattern with Steps.](\docs\guides\step-parallelism)

## [How steps work](\docs\features\inngest-functions\steps-workflows#how-steps-work)

You might wonder: how do Steps work? Why doesn't an Inngest Function get timed out when running on a Serverless environment?

You can think of steps as an API for expressing checkpoints in your workflow, such as waits or work that might benefit from retries or parallelism:

TypeScript Python Go

Copy Copied

```
inngest .createFunction (
{ id : "sync-systems" } ,
{ event : "auto/sync.request" } ,
async ({ step }) => {
// By wrapping code in step.run, the code will be retried if it throws an error and when successfuly.
// It's result is saved to prevent unnecessary re-execution
const data = await step .run ( "get-data" , async () => {
return getDataFromExternalSource ();
});

// Can also be retried up to 4 times
await step .run ( "save-data" , async () => {
return db . syncs .insertOne (data);
});
} ,
);
```

Each step execution relies on a communication with Inngest's [Durable Execution Engine](\docs\learn\how-functions-are-executed) which is responsible to:

- Invoking Functions with the correct steps state (current step + previous steps data)
- Gather each step result and schedule the next step to perform

This architecture powers the durability of Inngest Functions with retriable steps and waits from hours to months. Also, when used in a serverless environment, steps benefit from an extended max duration, enabling workflows that both span over months and run for more than 5 minutes!

Explore the following guide for a step-by-step overview of a complete workflow run:

## [How Functions are executed](\docs\learn\how-functions-are-executed)

[A deep dive into Inngest's Durable Execution Engine with a step-by-step workflow run example.](\docs\learn\how-functions-are-executed)

## [SDK References](\docs\features\inngest-functions\steps-workflows#sdk-references)

## [TypeScript SDK](\docs\reference\functions\step-run)

[Steps API reference](\docs\reference\functions\step-run)

## [Python SDK](\docs\reference\python\steps\invoke)

[Steps API reference](\docs\reference\python\steps\invoke)

## [Go SDK](https://pkg.go.dev/github.com/inngest/inngestgo@v0.9.0/step)

[Steps API reference](https://pkg.go.dev/github.com/inngest/inngestgo@v0.9.0/step)