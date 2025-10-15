#### On this page

- [Rate limiting](\docs\guides\rate-limiting#rate-limiting)
- [How to configure rate limiting](\docs\guides\rate-limiting#how-to-configure-rate-limiting)
- [Configuration reference](\docs\guides\rate-limiting#configuration-reference)
- [How rate limiting works](\docs\guides\rate-limiting#how-rate-limiting-works)
- [Using a key](\docs\guides\rate-limiting#using-a-key)
- [Limitations](\docs\guides\rate-limiting#limitations)
- [Further reference](\docs\guides\rate-limiting#further-reference)

Features [Inngest Functions](\docs\features\inngest-functions) [Flow Control](\docs\guides\flow-control)

# Rate limiting

Rate limiting is a *hard limit* on how many function runs can start within a time period. Events that exceed the rate limit are *skipped* and do not trigger functions to start. This prevents excessive function runs over a given time period. Some use cases for rate limiting include:

- Preventing abuse of your system.
- Reducing frequency of data synchronization functions.
- Skipping noisy or duplicate [webhook](\docs\platform\webhooks) events.

## [How to configure rate limiting](\docs\guides\rate-limiting#how-to-configure-rate-limiting)

TypeScript Go Python

Copy Copied

```
export default inngest .createFunction (
{
id : "synchronize-data" ,
rateLimit : {
limit : 1 ,
period : "4h" ,
key : "event.data.company_id" ,
} ,
} ,
{ event : "intercom/company.updated" } ,
async ({ event , step }) => {
// This function will be rate limited
// It will only run once per 4 hours for a given event payload with matching company_id
}
);
```

### [Configuration reference](\docs\guides\rate-limiting#configuration-reference)

- `limit` - The maximum number of functions to run in the given time period.
- `period` - The time period of which to set the limit. The period begins when the first matching event is received.
- `key` - An optional [expression](\docs\guides\writing-expressions) using event data to apply each limit too. Each unique value of the `key` has its own limit, enabling you to rate limit function runs by any particular key, like a user ID.

Any events received in excess of your `limit` are ignored. This means this is not the right approach if you need to process every single event sent to Inngest. Consider using [throttle](\docs\guides\throttling) instead.

## [How rate limiting works](\docs\guides\rate-limiting#how-rate-limiting-works)

Each time an event is received that matches your function's trigger, it is evaluated prior to executing your function. If `rateLimit` is configured, Inngest uses the `limit` and `period` options to only execute a maximum number of functions during that period.

Inngest's rate limiting implementation uses the ["Generic Cell Rate Algorithm"](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm) (GCRA). To *overly simplify* how this works, Inngest will use the `limit` and `period` options to create "buckets" of time in which your function can execute *once* .

Copy Copied

```
limit / period = bucket time window
```

For example, this means that for a `limit: 10` and `period: '60m'` (60 minutes), the bucket time window will be 6 minutes. Any event triggering the function "fills up" the bucket for that time window and any additional events are ignored until the bucket's time window is reset. The algorithm (GCRA) is more sophisticated than this, but at the basic level - `rateLimit` ensures that you'll only run the max `limit` number of items over the `period` that you specify.

Events that are ignored by the function will continue to be stored by Inngest.

**How the rate limit is applied with a consistent rate of events received**

Visualization of how the rate limit is applied with a consistent rate of events received

<!-- image -->

**How the rate limit is applied with sporadic events received**

Visualization of how the rate limit is applied with sporadic events received

<!-- image -->

**How the rate limit is applied when limit is set to 1**

Visualization of how the rate limit is applied when limit is set to 1

<!-- image -->

### [Using a key](\docs\guides\rate-limiting#using-a-key)

When a `key` is added, a separate limit is applied for each unique value of the `key` expression. For example, if your `key` is set to `event.data.customer_id` , each customer would have their individual rate limit applied to functions run meaning different users might have the same function run in same bucket time window, but two runs will not happen for the same `event.data.customer_id` . Read [our guide to writing expressions](\docs\guides\writing-expressions) for more information.

**Note** - To prevent duplicate events from triggering your function more than once in a 24 hour period, use [the](\docs\guides\handling-idempotency#at-the-function-level-the-consumer) [`idempotency`](\docs\guides\handling-idempotency#at-the-function-level-the-consumer) [option](\docs\guides\handling-idempotency#at-the-function-level-the-consumer) which is the equivalent to setting `rateLimit` with a `key` , a `limit` of `1` and `period` of `24hr` .

## [Limitations](\docs\guides\rate-limiting#limitations)

- The maximum rate limit `period` is 24 hours.

## [Further reference](\docs\guides\rate-limiting#further-reference)

- [Rate limiting vs Throttling](\docs\guides\throttling#throttling-vs-rate-limiting)
- [TypeScript SDK Reference](\docs\reference\functions\rate-limit)
- [Python SDK Reference](\docs\reference\python\functions\create#configuration)