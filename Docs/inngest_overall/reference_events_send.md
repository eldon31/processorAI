#### On this page

- [Send events](\docs\reference\events\send#send-events)
- [inngest.send(eventPayload | eventPayload[], options): Promise&lt;{ ids: string[] }&gt;](\docs\reference\events\send#inngest-send-event-payload-event-payload-options-promise-ids-string)
- [Return values](\docs\reference\events\send#return-values)
- [User data encryption 🔐](\docs\reference\events\send#user-data-encryption)
- [Usage limits](\docs\reference\events\send#usage-limits)

References [TypeScript SDK](\docs\reference\typescript)

# Send events

Send events to Inngest. Functions with matching event triggers will be invoked.

Copy Copied

```
import { inngest } from "./client" ;

await inngest .send ({
name : "app/account.created" ,
data : {
accountId : "645e9f6794e10937e9bdc201" ,
billingPlan : "pro" ,
} ,
user : {
external_id : "645ea000129f1c40109ca7ad" ,
email : "taylor@example.com" ,
}
})
```

To send events from within of the context of a function, use [`step.sendEvent()`](\docs\reference\functions\step-send-event) .

## [inngest.send(eventPayload | eventPayload[], options): Promise&lt;{ ids: string[] }&gt;](\docs\reference\events\send#inngest-send-event-payload-event-payload-options-promise-ids-string)

- Name `eventPayload` Type object | object[] Required required Description An event payload object or an array of event payload objects. Properties
- Name `options` Type object Required optional Version v3.21.0+ Description Properties

Copy Copied

```
// Send a single event
await inngest .send ({
name : "app/post.created" ,
data : { postId : "01H08SEAXBJFJNGTTZ5TAWB0BD" }
});

// Send an array of events
await inngest .send ([
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e024befa68763f5b500" }
} ,
{
name : "app/invoice.created" ,
data : { invoiceId : "645e9e08f29fb563c972b1f7" }
} ,
]);

// Send user data that will be encrypted at rest
await inngest .send ({
name : "app/account.created" ,
data : { billingPlan : "pro" } ,
user : {
external_id : "6463da8211cdbbcb191dd7da" ,
email : "test@example.com"
}
});

// Specify the idempotency id, version, and timestamp
await inngest .send ({
// Use an id specific to the event type & payload
id : "cart-checkout-completed-ed12c8bde" ,
name : "storefront/cart.checkout.completed" ,
data : { cartId : "ed12c8bde" } ,
user : { external_id : "6463da8211cdbbcb191dd7da" } ,
ts : 1684274328198 ,
v : "2024-05-15.1"
});
```

### [Return values](\docs\reference\events\send#return-values)

The function returns a promise that resolves to an object with an array of Event IDs that were sent. These events can be used to look up the event in the Inngest dashboard or via [the REST API](https://api-docs.inngest.com/docs/inngest-api/pswkqb7u3obet-get-an-event) .

Copy Copied

```
const { ids } = await inngest .send ([
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

## [User data encryption 🔐](\docs\reference\events\send#user-data-encryption)

All data sent in the `user` object is fully encrypted at rest.

⚠️ When [replaying a function](\docs\platform\replay) , `event.user` will be empty. This will be fixed in the future, but for now assume that you cannot replay functions that rely on `event.user` data.

In the future, this object will be used to support programmatic deletion via API endpoint to support certain right-to-be-forgotten flows in your system. This will use the `user.external_id` property for lookup.

## [Usage limits](\docs\reference\events\send#usage-limits)

See [usage limits](\docs\usage-limits\inngest#events) for more details.