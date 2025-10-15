#### On this page

- [Send Event](\docs\reference\functions\step-send-event#send-event)
- [step.sendEvent(id, eventPayload | eventPayload[]): Promise&lt;{ ids: string[] }&gt;](\docs\reference\functions\step-send-event#step-send-event-id-event-payload-event-payload-promise-ids-string)
- [Return values](\docs\reference\functions\step-send-event#return-values)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Send Event

Use to send event(s) reliably within your function. Use this instead of [`inngest.send()`](\docs\reference\events\send) to ensure reliable event delivery from within functions. This is especially useful when [creating functions that fan-out](\docs\guides\fan-out-jobs) .

v3 v2

Copy Copied

```
export default inngest .createFunction (
{ id : "user-onboarding" } ,
{ event : "app/user.signup" } ,
async ({ event , step }) => {
// Do something
await step .sendEvent ( "send-activation-event" , {
name : "app/user.activated" ,
data : { userId : event . data .userId } ,
});
// Do something else
}
);
```

To send events from outside of the context of a function, use [`inngest.send()`](\docs\reference\events\send) .

## [step.sendEvent(id, eventPayload | eventPayload[]): Promise&lt;{ ids: string[] }&gt;](\docs\reference\functions\step-send-event#step-send-event-id-event-payload-event-payload-promise-ids-string)

- Name `id` Type string Required required Description The ID of the step. This will be what appears in your function's logs and is used to memoize step state across function versions.
- Name `eventPayload` Type object | object[] Required required Description An event payload object or an array of event payload objects. [See the documentation for](\docs\reference\events\send#inngest-send-event-payload-event-payload-promise) [`inngest.send()`](\docs\reference\events\send#inngest-send-event-payload-event-payload-promise) for the event payload format.

v3 v2

Copy Copied

```
// Send a single event
await step .sendEvent ( "send-activation-event" , {
name : "app/user.activated" ,
data : { userId : "01H08SEAXBJFJNGTTZ5TAWB0BD" } ,
});

// Send an array of events
await step .sendEvent ( "send-invoice-events" , [
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e024befa68763f5b500" } ,
} ,
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e08f29fb563c972b1f7" } ,
} ,
]);
```

`step.sendEvent()` must be called using `await` or some other Promise handler to ensure your function sleeps correctly.

### [Return values](\docs\reference\functions\step-send-event#return-values)

The function returns a promise that resolves to an object with an array of Event IDs that were sent. These events can be used to look up the event in the Inngest dashboard or via [the REST API](https://api-docs.inngest.com/docs/inngest-api/pswkqb7u3obet-get-an-event) .

Copy Copied

```
const { ids } = await step .sendEvent ([
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e024befa68763f5b500" }
} ,
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e08f29fb563c972b1f7" }
} ,
]);
/**
* ids = [
*   "01HQ8PTAESBZPBDS8JTRZZYY3S",
*   "01HQ8PTFYYKDH1CP3C6PSTBZN5"
* ]
*/
```