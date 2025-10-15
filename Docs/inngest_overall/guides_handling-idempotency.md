#### On this page

- [Handling idempotency](\docs\guides\handling-idempotency#handling-idempotency)
- [What is idempotency?](\docs\guides\handling-idempotency#what-is-idempotency)
- [How to handle idempotency with Inngest](\docs\guides\handling-idempotency#how-to-handle-idempotency-with-inngest)
- [At the event level (the producer)](\docs\guides\handling-idempotency#at-the-event-level-the-producer)
- [At the function level (the consumer)](\docs\guides\handling-idempotency#at-the-function-level-the-consumer)
- [Example](\docs\guides\handling-idempotency#example)
- [Writing CEL expressions](\docs\guides\handling-idempotency#writing-cel-expressions)
- [Idempotency keys and fan-out](\docs\guides\handling-idempotency#idempotency-keys-and-fan-out)

Features [Inngest Functions](\docs\features\inngest-functions) [Errors &amp; Retries](\docs\guides\error-handling)

# Handling idempotency

Ensuring that your code is idempotent is foundational to building reliable systems. Within Inngest, there are multiple ways to ensure that your functions are idempotent.

## [What is idempotency?](\docs\guides\handling-idempotency#what-is-idempotency)

Idempotency, by definition, describes an operation that can occur multiple times without changing the result beyond the initial execution. In the world of software, this means that a functions can be executed multiple times, but it will always have the same effect as being called once. An example of this is an "upsert."

## [How to handle idempotency with Inngest](\docs\guides\handling-idempotency#how-to-handle-idempotency-with-inngest)

It should always be the aim to write code that is idempotent itself within your system or your Inngest functions, but there are also some features within Inngest that can help you ensure idempotency.

As Inngest functions are triggered by events, there are two main ways to ensure idempotency:

- [at the event level (](\docs\guides\handling-idempotency#at-the-event-level-the-producer) [*the producer*](\docs\guides\handling-idempotency#at-the-event-level-the-producer) [)](\docs\guides\handling-idempotency#at-the-event-level-the-producer) and/or
- [at the function level (](\docs\guides\handling-idempotency#at-the-function-level-the-consumer) [*the consumer*](\docs\guides\handling-idempotency#at-the-function-level-the-consumer) [)](\docs\guides\handling-idempotency#at-the-function-level-the-consumer)

## [At the event level (the producer)](\docs\guides\handling-idempotency#at-the-event-level-the-producer)

Each event that is received by Inngest will trigger any functions with that matching trigger. If an event is sent twice, Inngest will trigger the function twice. This is the default behavior as Inngest does not know if the event is the same event or a new event.

**Example:** Using an e-commerce store as an example, a user can add the same t-shirt to their cart twice because they want to buy two ( *2 unique events* ). That same user may check out and pay for all items in their cart but click the "pay" button twice ( *2 duplicate events* ).

To prevent an event from being handled twice, you can set a unique event `id` when [sending the event](\docs\reference\events\send#inngest-send-event-payload-event-payload-promise) . This `id` acts as an idempotency key **over a 24 hour period** and Inngest will check to see if that event has already been received before triggering another function.

TypeScript Go Python

Copy Copied

```
const cartId = 'CGo5Q5ekAxilN92d27asEoDO' ;
await inngest .send ({
id : `checkout-completed- ${ cartId } ` , // <-- This is the idempotency key
name : 'cart/checkout.completed' ,
data : {
email : 'taylor@example.com' ,
cartId : cartId
}
})
```

| Event ID                                    | Timestamp    | Function                   |
|---------------------------------------------|--------------|----------------------------|
| checkout-completed-CGo5Q5ekAxilN92d27asEoDO | 08:00:00.000 | ✅ Functions are triggered |
| checkout-completed-CGo5Q5ekAxilN92d27asEoDO | 08:00:00.248 | ❌ Nothing is triggered    |

As you can see in the above example, setting the `id` allows you to prevent duplicate execution on the producer side, where the event originates.

Some other key points to note:

- Event IDs will only be used to prevent duplicate execution for a 24 hour period. After 24 hours, the event will be treated as a new event and will trigger any functions with that trigger.
- Inngest will store the second event and it will be visible in your event history, but it will *not* trigger any functions.
- Events that fan-out to multiple functions will trigger each function as they normally would.

**Tip** - If you are using Inngest's [webhook transforms](\docs\platform\webhooks#defining-a-transform-function) , you can set the `id` in the transform to ensure that the event is idempotent.

Event idempotency is ignored by some features:

- Debouncing
- Event batching
- Function pausing. While a function is paused, event idempotency is ignored. So if a replay is created after unpausing, it may have "skipped" runs that ignored event idempotency.

## [At the function level (the consumer)](\docs\guides\handling-idempotency#at-the-function-level-the-consumer)

You might prefer to ensure idempotency at the function level or you may not be able to control the event that is being sent (from a webhook). The [function's](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function) [`idempotency`](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function) [config option](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function) allows you to do this.

Each function's `idempotency` key is defined as a [CEL expression](\docs\guides\writing-expressions) that is evaluated with the event payload's data. The expression is used to generate a unique string key which idempotently prevents duplicate execution of the function.

Each unique expression will only trigger one function execution **per 24 hour period** . After 24 hours, a new event that generates the same unique expression will trigger another function execution.

### [Example](\docs\guides\handling-idempotency#example)

We'll use the same example of an e-commerce store to demonstrate how this works. We have an event here with no `id` set ( [see above](\docs\guides\handling-idempotency#at-the-event-level-the-producer) ), but we want to ensure that the `send-checkout-email` function is only triggered once for each `cartId` to prevent duplicate emails being sent.

### Event payload

Copy Copied

```
{
"name" : "cart/checkout.completed" ,
"data" : {
"email" : "blake@example.com" ,
"cartId" : "s6CIMNqIaxt503I1gVEICfwp"
} ,
"ts" : 1703275661157
}
```

### Function definition with idempotency key

Copy Copied

```
export const sendEmail = inngest .createFunction (
{
id : 'send-checkout-email' ,
// This is the idempotency key
idempotency : 'event.data.cartId' ,
// Evaluates to: "s6CIMNqIaxt503I1gVEICfwp"
// for the given event payload
} ,
{ trigger : 'cart/checkout.completed' } ,
async ({ event , step }) => { /* ... */ }
})
```

### [Writing CEL expressions](\docs\guides\handling-idempotency#writing-cel-expressions)

While CEL can do many things, we'll focus on how to use it to generate a unique string key for idempotency. The key things to know are:

- You can access any of the event payload's data using the `event` variable and dot-notation for nested properties.
- You can use the `+` operator to concatenate strings together.

Combining two or more properties together is a good way to ensure the level of uniqueness that you need. Here are couple of examples:

- **User signup:** You only want to send a welcome email once per user, so you'd set `idempotency` to `event.data.userId` in case there your API sends duplicate events.
- **Organization team invite:** A user may be part of multiple organizations in your app. You only want to send a team invite email once per user/organization combination, so you'd set `idempotency` to `event.data.userId + "-" + event.data.organizationId` .

For more information on writing CEL expressions, read [our guide](\docs\guides\writing-expressions) .

💡 If you want to control when a function is executed over a period of time you might prefer:

- [`rateLimit`](\docs\reference\functions\rate-limit) - Limit the number of function executions per period of time
- [`debounce`](\docs\reference\functions\debounce) - Delay function execution for duplicate events over a period of time

### [Idempotency keys and fan-out](\docs\guides\handling-idempotency#idempotency-keys-and-fan-out)

One reason why you might want to use `idempotency` at the function level is if you have an `event` that fans-out to multiple functions. Let's take the following fan-out example:

| Function       | Event trigger           | How often        |
|----------------|-------------------------|------------------|
| Track requests | ai/generation.requested | Every time       |
| Run generation | ai/generation.requested | Once per request |

In this case, you would want to set `idempotency` on the "Run generation" function to ensure that it runs once, for example, for every unique prompt that is sent. You may want to do this as you don't want to re-run the same exact prompt and waste compute resources/credits. However, you still might want to track the number of requests that each user submitted, so you would not want to set `idempotency` on the "Track requests" function. You can see the code for both functions below.

**View the function code**

Both functions use the same event trigger, `ai/generation.requested` which contains a `promptHash` and a `userId` in the event payload.

### Track requests function

Copy Copied

```
const trackRequests = inngest .createFunction (
{ id : 'track-requests' } ,
{ event : 'ai/generation.requested' } ,
async ({ event , step }) => {
// Track the request
}
)
```

### Run generation function

Copy Copied

```
const runGeneration = inngest .createFunction (
{
id : 'run-generation' ,
// Given the event payload sends a hash of the prompt,
// this will only run once per unique prompt per user
// every 24 hours:
idempotency : `event.data.promptHash + "-" + event.data.userId`
} ,
{ event : 'ai/generation.requested' } ,
async ({ event , step }) => {
// Track the request
}
)
```