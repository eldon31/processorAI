#### On this page

- [Failure handlers](\docs\features\inngest-functions\error-retries\failure-handlers#failure-handlers)
- [Examples](\docs\features\inngest-functions\error-retries\failure-handlers#examples)

Features [Inngest Functions](\docs\features\inngest-functions) [Errors &amp; Retries](\docs\guides\error-handling)

# Failure handlers TypeScript only

If your function exhausts all of its retries, it will be marked as "Failed." You can handle this circumstance by either providing an [`onFailure/on_failure`](\docs\reference\functions\handling-failures) handler when defining your function, or by listening for the [`inngest/function.failed`](\docs\reference\system-events\inngest-function-failed) system event.

The first approach is function-specific, while the second covers all function failures in a given Inngest environment.

# Examples

The example below checks if a user's subscription is valid a total of six times. If you can't check the subscription after all retries, you'll unsubscribe the user:

TypeScript Python Go

Copy Copied

```
/* Option 1: give the inngest function an `onFailure` handler. */
inngest .createFunction (
{
id : "update-subscription" ,
retries : 5 ,
onFailure : async ({ event , error }) => {
// if the subscription check fails after all retries, unsubscribe the user
await unsubscribeUser ( event . data .userId);
} ,
} ,
{ event : "user/subscription.check" } ,
async ({ event }) => { /* ... */ } ,
);
/* Option 2: Listens for the [`inngest/function.failed`](/docs/reference/functions/handling-failures#the-inngest-function-failed-event) system event to catch all failures in the inngest environment*/
inngest .createFunction (
{ id : "handle-any-fn-failure" } ,
{ event : "inngest/function.failed" } ,
async ({ event }) => { /* ... */ } ,
);
```

To handle cancelled function runs, checkout out [this example](\docs\examples\cleanup-after-function-cancellation) that uses the [`inngest/function.cancelled`](\docs\reference\system-events\inngest-function-cancelled) system event.