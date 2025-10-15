#### On this page

- [Singleton Functions](\docs\guides\singleton#singleton-functions)
- [When to use Singleton Functions](\docs\guides\singleton#when-to-use-singleton-functions)
- [Singleton compared to concurrency:](\docs\guides\singleton#singleton-compared-to-concurrency)
- [Singleton compared to Rate Limiting:](\docs\guides\singleton#singleton-compared-to-rate-limiting)
- [How it works](\docs\guides\singleton#how-it-works)
- [Using a key](\docs\guides\singleton#using-a-key)
- [Two modes: Skip vs Cancel](\docs\guides\singleton#two-modes-skip-vs-cancel)
- [Compatibility with other flow control features](\docs\guides\singleton#compatibility-with-other-flow-control-features)
- [FAQ](\docs\guides\singleton#faq)
- [How does Singleton Functions work with retries?](\docs\guides\singleton#how-does-singleton-functions-work-with-retries)

Features [Inngest Functions](\docs\features\inngest-functions) [Flow Control](\docs\guides\flow-control)

# Singleton Functions TypeScript v3.39.0+ Go SDK v0.12.0+ Python v0.5+

Singleton Functions enable you to ensure that only a single run of your function ( *or a set of specific function runs, based on specific event properties* ) is happening at a time.

Singleton Functions only process one run at a time.

<!-- image -->

Singleton Functions only process one run at a time.

<!-- image -->

Singleton Functions are available in the TypeScript SDK starting from version 3.39.0.

## [When to use Singleton Functions](\docs\guides\singleton#when-to-use-singleton-functions)

Singleton Functions are useful when you want to ensure that only a single instance of a function is running at a time, for example:

- A third-party data synchronization workflow
- A compute- or time-intensive function that should not be run multiple times at the same time (ex: AI processing)

### [Singleton compared to concurrency:](\docs\guides\singleton#singleton-compared-to-concurrency)

While [Concurrency](\docs\guides\concurrency) set to `1` ensures that only a single step of a given function is running at a time, Singleton Functions ensure that only a single run of a given function is happening at a time.

### [Singleton compared to Rate Limiting:](\docs\guides\singleton#singleton-compared-to-rate-limiting)

[Rate Limiting](\docs\guides\rate-limiting) is similar to Singleton Functions, but it is designed to limit the number of runs started within a time period, whereas Singleton Functions are designed to ensure that only a single run of a function occurs over a given time window.

Rate Limiting is useful for controlling the rate of execution of a function, while Singleton Functions are useful for ensuring that only a single run of a function occurs over a given time window.

## [How it works](\docs\guides\singleton#how-it-works)

Singleton Functions are configured using the `singleton` property in the function definition.

The following `data-sync` function demonstrates singleton behavior scoped to individual users. Depending on the `mode` , new runs will either be skipped or will cancel the existing run:

Copy Copied

```
const dataSync = inngest .createFunction ({
id : "data-sync" ,
singleton : {
key : "event.data.user_id" ,
mode : "skip" ,
}
} ,
{ event : "data-sync.start" } ,
async ({ event }) => {
// ...
} ,
);
```

Refer to the [reference documentation](\docs\reference\functions\singleton) for more details.

### [Using a key](\docs\guides\singleton#using-a-key)

When a `key` is added, the unique runs rule is applied for each unique value of the `key` expression. For example, if your `key` is set to `event.data.user_id` ,

each user would have their individual singleton rule applied to functions runs, ensuring that only a single run of the function is happening at a time for each user. Read

[our guide to writing expressions](\docs\guides\writing-expressions) for more information.

### [Two modes: Skip vs Cancel](\docs\guides\singleton#two-modes-skip-vs-cancel)

Singleton Functions can be configured to either skip the new run or cancel the existing run and start a new one.

The `mode` property configures the behavior of the Singleton Function:

- `"skip"` - Skips the new run if another run is already executing.
- `"cancel"` - Cancels the existing run and starts the new one.

**Cancel mode behavior** : Triggering multiple function runs with the same key in very rapid succession may result in some runs being skipped rather than cancelled, similar to a debounce effect. This prevents excessive cancellation overhead when events are triggered in quick bursts.

### [When should I use "cancel" mode vs "skip" mode?](\docs\guides\singleton#when-should-i-use-cancel-mode-vs-skip-mode)

Use `"skip"` mode when you want to prevent duplicate work and preserve the currently running function. Use `"cancel"` mode when you want to ensure the most recent event is always processed, even if it means cancelling an in-progress run.

Skip mode Cancel mode

Copy Copied

```
const dataSync = inngest .createFunction ({
id : "data-sync" ,
singleton : {
key : "event.data.user_id" ,
mode : "skip" ,
}
} ,
{ event : "data-sync.start" } ,
async ({ event }) => {
const userId = event . data .user_id;

// This long-running sync process will not be interrupted
// If another sync is triggered for this user, it will be skipped
const data = await syncUserDataFromExternalAPI (userId);
const processed = await processLargeDataset (data);
await updateDatabase (processed);
} ,
);
```

## [Compatibility with other flow control features](\docs\guides\singleton#compatibility-with-other-flow-control-features)

Singleton Functions can be combined with other flow control features, with the following considerations:

| Flow control   | Compatibility   | Considerations                                                                                                            |
|----------------|-----------------|---------------------------------------------------------------------------------------------------------------------------|
| Debounce       | ✅              | Can be used together without issues.                                                                                      |
| Rate limiting  | ✅              | Similar functionality but rate limiting operates over a predefined time window rather than function execution duration.   |
| Throttling     | ✅              | Similar functionality but throttling enqueues events over time rather than discarding/canceling them.                     |
| Concurrency    | ❌              | Singleton functions implicitly have a concurrency of 1. A concurrency setting can be set but should be used with caution. |
| Batching       | ❌              | Singleton isn't compatible with batching; function registration will fail if both are set.                                |

## [FAQ](\docs\guides\singleton#faq)

### [How does Singleton Functions work with retries?](\docs\guides\singleton#how-does-singleton-functions-work-with-retries)

If a singleton function fails and is retrying, it should still skip new incoming runs.