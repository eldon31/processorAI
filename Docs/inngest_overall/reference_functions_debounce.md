#### On this page

- [Debounce functions](\docs\reference\functions\debounce#debounce-functions)

References [TypeScript SDK](\docs\reference\typescript)

# Debounce functions v3.1.0+

Debounce delays a function run for the given `period` , and reschedules functions for the given `period` any time new events are received while the debounce is active.  The function run starts after the specified `period` passes and no new events have been received.  Functions use the last event as their input data.

See the [Debounce guide](\docs\guides\debounce) for more information about how this feature works.

Copy Copied

```
export default inngest .createFunction (
{
id : "handle-webhook" ,
debounce : {
key : "event.data.account_id" ,
period : "5m" ,
} ,
} ,
{ event : "intercom/company.updated" } ,
async ({ event , step }) => {
// This function will only be scheduled 5m after events have stopped being received with the same
// `event.data.account_id` field.
//
// `event` will be the last event in the series received.
}
);
```

- Name `debounce` Type object Required optional Description Options to configure how to debounce function execution Properties

Functions will run using the last event received as the input data.

Debounce cannot be combined with [batching](\docs\guides\batching) .