#### On this page

- [Batching events](\docs\guides\batching#batching-events)
- [How to configure batching](\docs\guides\batching#how-to-configure-batching)
- [Configuration reference](\docs\guides\batching#configuration-reference)
- [How batching works](\docs\guides\batching#how-batching-works)
- [Conditional Batching](\docs\guides\batching#conditional-batching)
- [Combining with other flow control methods](\docs\guides\batching#combining-with-other-flow-control-methods)
- [Limitations](\docs\guides\batching#limitations)
- [Further reference](\docs\guides\batching#further-reference)

Features [Events &amp; Triggers](\docs\features\events-triggers)

# Batching events

Batching allows a function to process multiple events in a single run. This is useful for high load systems where it's more efficient to handle a batch of events together rather than handling each event individually. Some use cases for batching include:

- Reducing the number of requests to an external API that supports batch operations.
- Creating a batch of database writes to reduce the number of transactions.
- Reducing the number of requests to your [Inngest app](\docs\apps) to improve performance or serverless costs.

## [How to configure batching](\docs\guides\batching#how-to-configure-batching)

TypeScript Code Go Python

Copy Copied

```
inngest .createFunction (
{
id : "record-api-calls" ,
batchEvents : {
maxSize : 100 ,
timeout : "5s" ,
key : "event.data.user_id" , // Optional: batch events by user ID
if : "event.data.account_type == \"free\"" , // Optional: Only batch events from free accounts
} ,
} ,
{ event : "log/api.call" } ,
async ({ events , step }) => {
// NOTE: Use the `events` argument, which is an array of event payloads
const attrs = events .map ((evt) => {
return {
user_id : evt . data .user_id ,
endpoint : evt . data .endpoint ,
timestamp : toDateTime ( evt .ts) ,
account_type : evt . data .account_type ,
};
});

const result = await step .run ( "record-data-to-db" , async () => {
return db .bulkWrite (attrs);
});

return { success : true , recorded : result . length };
}
);
```

### [Configuration reference](\docs\guides\batching#configuration-reference)

- `maxSize` - The maximum number of events to add to a single batch.
- `timeout` - The duration of time to wait to add events to a batch. If the batch is not full after this time, the function will be invoked with whatever events are in the current batch, regardless of size.
- `key` - An optional [expression](\docs\guides\writing-expressions) using event data to batch events by. Each unique value of the `key` will receive its own batch, enabling you to batch events by any particular key, like a user ID.
- `if` - An optional [boolean expression](\docs\guides\writing-expressions) using event data to conditionally batch events that evaluate to true on this expression.

It is recommended to consider the overall batch size that you will need to process including the typical event payload size. Processing large batches can lead to memory or performance issues in your application.

For system safety purposes, We also enforce a 10 MiB size limit for a batch, meaning if the size of the total number of events exceeds 10 MiB, the batch will start execution even if it's not full or has reached a timeout.

This limit cannot be changed at the moment.

## [How batching works](\docs\guides\batching#how-batching-works)

When batching is enabled, Inngest creates a new batch when the first event is received. The batch is filled with events until the `maxSize` is reached *or* the `timeout` is up. The function is then invoked with the full list of events in the batch. When `key` is set, Inngest will maintain a batch for each unique key, which allows you to batch events belonging to a single entity, for example a customer.

Depending on your SDK, the `events` argument will contain the full list of events within a batch. This allows you to operate on all of them within a single function.

### [Conditional Batching](\docs\guides\batching#conditional-batching)

Conditional Batching can be enabled by providing a boolean expression in `if` .  If the expression cannot be evaluated to a boolean value or if the expression evaluates to `false` , batching will be skipped for this event and the event will be scheduled for execution immediately.

## [Combining with other flow control methods](\docs\guides\batching#combining-with-other-flow-control-methods)

Batching does not work with all other flow control features.

You *can* combine batching with simple [concurrency](\docs\guides\concurrency) limits, but will not work correctly with the `key` configuration option.

You *cannot* use batching with [idempotency](\docs\guides\handling-idempotency) , [rate limiting](\docs\guides\rate-limiting) , [cancellation events](\docs\guides\cancel-running-functions#cancel-with-events) , or [priority](\docs\guides\priority) .

## [Limitations](\docs\guides\batching#limitations)

- Check our [pricing page](https://www.inngest.com/pricing) to verify the batch size limits for each plan.

## [Further reference](\docs\guides\batching#further-reference)

- [TypeScript SDK Reference](\docs\reference\functions\create#batchEvents)
- [Python SDK Reference](\docs\reference\python\functions\create#batch_events)