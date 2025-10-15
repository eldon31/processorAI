#### On this page

- [Throttling](\docs\guides\throttling#throttling)
- [How to configure throttling](\docs\guides\throttling#how-to-configure-throttling)
- [Configuration reference](\docs\guides\throttling#configuration-reference)
- [How throttling works](\docs\guides\throttling#how-throttling-works)
- [Throttling vs Concurrency](\docs\guides\throttling#throttling-vs-concurrency)
- [Throttling vs Rate Limiting](\docs\guides\throttling#throttling-vs-rate-limiting)
- [Tips](\docs\guides\throttling#tips)
- [Further reference](\docs\guides\throttling#further-reference)

Features [Inngest Functions](\docs\features\inngest-functions) [Flow Control](\docs\guides\flow-control)

# Throttling

Throttling allows you to specify how many function runs can start within a time period. When the limit is reached, new function runs over the throttling limit will be *enqueued for the future* . Throttling is FIFO (first in first out). Some use cases for priority include:

- Evenly distributing function execution over time to reduce spikes.
- Working around third-party API rate limits.

## [How to configure throttling](\docs\guides\throttling#how-to-configure-throttling)

TypeScript Go Python

Copy Copied

```
inngest .createFunction (
{
id : "unique-function-id" ,
throttle : {
limit : 1 ,
period : "5s" ,
burst : 2 ,
key : "event.data.user_id" ,
} ,
}
{ event : "ai/summary.requested" } ,
async ({ event , step }) => {
}
);
```

You can configure throttling on each function using the optional `throttle` parameter.  The options directly control the generic cell rate algorithm parameters used within the queue.

### [Configuration reference](\docs\guides\throttling#configuration-reference)

- `limit` : The total number of runs allowed to start within the given `period` .
- `period` : The period within the limit will be applied.
- `burst` : The number of runs allowed to start in the given window in a single burst. This defaults to 1, which ensures that requests are smoothed amongst the given `period` .
- `key` : An optional expression which returns a throttling key using event data. This allows you to apply unique throttle limits specific to a user.

**Configuration information**

- The rate limit smooths requests in the given period, allowing `limit/period` requests a second.
- Period must be between `1s` and `7d` , or between 1 second and 7 days. The minimum granularity is one second.
- Throttling is currently applied per function. Two functions with the same key have two separate limits.
- Every request is evenly weighted and counts as a single unit in the rate limiter.

## [How throttling works](\docs\guides\throttling#how-throttling-works)

Throttling uses the [generic cell rate algorithm (GCRA)](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm) to limit function run *starts* directly in the queue. When you send an event or invoke a function that specifies throttling configuration, Inngest checks the function's throttle limit to see if there's capacity:

- If there's capacity, the function run starts as usual.
- If there is no capacity, the function run will begin when there's capacity in the future.

Note that throttling only applies to function run starts.  It does not apply to steps within a function.  This allows you to regulate how often functions begin work, *without* worrying about how many steps are in a function, or if steps run in parallel.  To limit how many steps can execute at once, use [concurrency controls](\docs\guides\concurrency) .

Throttling is [FIFO (first in first out)](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)) , so the first function run to be enqueued will be the first to start when there's capacity.

## [Throttling vs Concurrency](\docs\guides\throttling#throttling-vs-concurrency)

**Concurrency** limits the *number of executing steps across your function runs* .  This allows you to manage the total capacity of your functions.

**Throttling** limits the number of *new function runs* being started.  It does not limit the number of executing steps.  For example, with a throttling limit of 1 per minute, only one run will start in a single minute.  However, that run may execute hundreds of steps, as throttling does not limit steps.

## [Throttling vs Rate Limiting](\docs\guides\throttling#throttling-vs-rate-limiting)

Rate limiting also specifies how many functions can start within a time period.  However, in Inngest rate limiting ignores function runs over the limit and does not enqueue them for future work. Throttling will enqueue runs over the limit for the future.

Rate limiting is *lossy* and provides hard limits on function runs, while throttling delays function runs over the limit until there's capacity, smoothing spikes.

## [Tips](\docs\guides\throttling#tips)

- Configure [start timeouts](\docs\features\inngest-functions\cancellation\cancel-on-timeouts) to prevent large backlogs with throttling

## [Further reference](\docs\guides\throttling#further-reference)

- [TypeScript SDK Reference](\docs\reference\functions\create#throttle)
- [Python SDK Reference](\docs\reference\python\functions\create#configuration)