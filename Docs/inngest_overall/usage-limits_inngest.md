#### On this page

- [Usage Limits](\docs\usage-limits\inngest#usage-limits)
- [Functions](\docs\usage-limits\inngest#functions)
- [Sleep duration](\docs\usage-limits\inngest#sleep-duration)
- [Timeout](\docs\usage-limits\inngest#timeout)
- [Concurrency Upgradable](\docs\usage-limits\inngest#concurrency-upgradable)
- [Payload Size](\docs\usage-limits\inngest#payload-size)
- [Function run state size](\docs\usage-limits\inngest#function-run-state-size)
- [Number of Steps per Function](\docs\usage-limits\inngest#number-of-steps-per-function)
- [Events](\docs\usage-limits\inngest#events)
- [Name length](\docs\usage-limits\inngest#name-length)
- [Request Body Size Upgradable](\docs\usage-limits\inngest#request-body-size-upgradable)
- [Number of events per request Customizable](\docs\usage-limits\inngest#number-of-events-per-request-customizable)
- [Batch size](\docs\usage-limits\inngest#batch-size)

Platform

# Usage Limits

We have put some limits on the service to make sure we provide you a good default to start with, while also keeping it a good experience for all other users using Inngest.

Some of these limits are customizable, so if you need more than what the current limits provide, please [contact us](\contact) and we can update the limits for you.

## [Functions](\docs\usage-limits\inngest#functions)

The following applies to `step` usage.

### [Sleep duration](\docs\usage-limits\inngest#sleep-duration)

Sleep (with `step.sleep()` and `step.sleepUntil()` ) up to a year, and for free plan up to seven days. Check the [pricing page](\pricing) for more information.

### [Timeout](\docs\usage-limits\inngest#timeout)

Each step has a timeout depending on the hosting provider of your choice ( [see more info](\docs\usage-limits\providers) ), but Inngest supports up to `2 hours` at the maximum.

### [Concurrency Upgradable](\docs\usage-limits\inngest#concurrency-upgradable)

Check your concurrency limits on the [billing page](https://app.inngest.com/billing) . See the [pricing page](https://www.inngest.com/pricing) for more info about the concurrency limits in all plans.

### [Payload Size](\docs\usage-limits\inngest#payload-size)

The limit for data returned by a step is `4MB` .

### [Function run state size](\docs\usage-limits\inngest#function-run-state-size)

Function run state cannot exceed `32MB` . Its state includes:

- Event data (multiple events if using batching)
- Step-returned data
- Function-returned data
- Internal metadata ( *small - around a few bytes* )

### [Number of Steps per Function](\docs\usage-limits\inngest#number-of-steps-per-function)

The maximum number of steps allowed per function is `1000` .

⚠️

This limit is easily reached if you're using

`step` on each item in a loop.

Instead we recommend one or both of the following:

- Process the loop within a `step` and return that data
- Utilize the [fan out](\docs\guides\fan-out-jobs) feature to process each item in a separate function

## [Events](\docs\usage-limits\inngest#events)

### [Name length](\docs\usage-limits\inngest#name-length)

The maximum length allowed for an event name is `256` characters.

### [Request Body Size Upgradable](\docs\usage-limits\inngest#request-body-size-upgradable)

The maximum event payload size is dependent on your billing plan. The default on the Free Tier is `256KB` and is upgradable to `3MB` . See [the pricing page](\pricing?ref=docs-usage-limits) for additional detail.

### [Number of events per request Customizable](\docs\usage-limits\inngest#number-of-events-per-request-customizable)

Maximum number of events you can send in one request is `5000` .

If you're doing fan out, you'll need to be aware of this limitation when you run

`step.sendEvent(events)` .

TypeScript Go Python

Copy Copied

```
// this `events` list will need to be <= 5000
const events = [{name : "<event-name>" , data : {}} , ... ];

await step .sendEvent ( "send-example-events" , events);
// or
await inngest .send (events);
```

### [Batch size](\docs\usage-limits\inngest#batch-size)

The hard limit of a batch size is 10 MiB regardless of the `timeout` or `maxSize` limit.

Meaning the batch will be started if that limit is crossed even if the batch is not full or has not reached the timeout duration configured.