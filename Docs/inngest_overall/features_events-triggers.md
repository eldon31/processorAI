#### On this page

- [Events &amp; Triggers](\docs\features\events-triggers#events-and-triggers)
- [Why events?](\docs\features\events-triggers#why-events)
- [Learn more about Events](\docs\features\events-triggers#learn-more-about-events)

Features

# Events &amp; Triggers

Inngest functions are triggered asynchronously by **events** coming from various sources, including:

## [Your application](\docs\events)

[Send an event from your application's backend with the Inngest SDK.](\docs\events)

## [Cron schedule](\docs\guides\scheduled-functions)

[Run an Inngest function periodically with a trigger using cron syntax.](\docs\guides\scheduled-functions)

## [Webhook events](\docs\platform\webhooks)

[Use Inngest as a webhook consumer for any service to trigger functions.](\docs\platform\webhooks)

## [Another Inngest function](\docs\guides\invoking-functions-directly)

[Directly invoke other functions to compose more powerful functions.](\docs\guides\invoking-functions-directly)

You can customize each of these triggers in multiple ways:

- [**Filtering event triggers**](\docs\guides\writing-expressions) - Trigger a function for a subset of matching events sent.
- [**Delaying execution**](\docs\guides\delayed-functions) - Trigger a function to run at a specific timestamp in the future.
- [**Batching events**](\docs\guides\batching) - Process multiple events in a single function for more efficient systems.
- [**Multiple triggers**](\docs\guides\multiple-triggers) - Use a single function to handle multiple event types.

## [Why events?](\docs\features\events-triggers#why-events)

Using Events to trigger Inngest Functions instead of direct invocations offers a lot of flexibility:

- Events can trigger multiple Inngest Functions.
- Events can be used to synchronize Inngest Function runs with [cancellation](\docs\features\inngest-functions\cancellation) and ["wait for event" step](\docs\reference\functions\step-wait-for-event) .
- Events can be leveraged to trigger Functions across multiple applications.
- Similar Events can be grouped together for faster processing.

Events act as a convenient mapping between your application actions (ex, `user.signup` ) and your application's code (ex, `sendWelcomeEmail()` and `importContacts()` ):

### [Learn more about Events](\docs\features\events-triggers#learn-more-about-events)

## [Blog post: How event Filtering works](https://www.inngest.com/blog/accidentally-quadratic-evaluating-trillions-of-event-matches-in-real-time)

[Accidentally Quadratic: Evaluating trillions of event matches in real-time](https://www.inngest.com/blog/accidentally-quadratic-evaluating-trillions-of-event-matches-in-real-time)

## [Blog post: Events in practice](https://www.inngest.com/blog/nextjs-trpc-inngest)

[Building an Event Driven Video Processing Workflow with Next.js, tRPC, and Inngest](https://www.inngest.com/blog/nextjs-trpc-inngest)