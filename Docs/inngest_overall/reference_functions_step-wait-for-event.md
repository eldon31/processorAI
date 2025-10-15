#### On this page

- [Wait for event](\docs\reference\functions\step-wait-for-event#wait-for-event)
- [step.waitForEvent(id, options): Promise&lt;null | EventPayload&gt;](\docs\reference\functions\step-wait-for-event#step-wait-for-event-id-options-promise-null-event-payload)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Wait for event

## [step.waitForEvent(id, options): Promise&lt;null | EventPayload&gt;](\docs\reference\functions\step-wait-for-event#step-wait-for-event-id-options-promise-null-event-payload)

- Name `id` Type string Required required Description The ID of the step. This will be what appears in your function's logs and is used to memoize step state across function versions.
- Name `options` Type object Required required Description Options for configuring how to wait for the event. Properties

v3 v2

Copy Copied

```
// Wait 7 days for an approval and match invoice IDs
const approval = await step .waitForEvent ( "wait-for-approval" , {
event : "app/invoice.approved" ,
timeout : "7d" ,
match : "data.invoiceId" ,
});

// Wait 30 days for a user to start a subscription
// on the pro plan
const subscription = await step .waitForEvent ( "wait-for-subscription" , {
event : "app/subscription.created" ,
timeout : "30d" ,
if : "event.data.userId == async.data.userId && async.data.billing_plan == 'pro'" ,
});
```

`step.waitForEvent()` must be called using `await` or some other Promise handler to ensure your function sleeps correctly.