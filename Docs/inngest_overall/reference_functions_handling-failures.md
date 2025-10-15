#### On this page

- [Handling Failures](\docs\reference\functions\handling-failures#handling-failures)
- [How onFailure works](\docs\reference\functions\handling-failures#how-on-failure-works)
- [onFailure({ error, event, step, runId })](\docs\reference\functions\handling-failures#on-failure-error-event-step-run-id)
- [error](\docs\reference\functions\handling-failures#error)
- [event](\docs\reference\functions\handling-failures#event)
- [step](\docs\reference\functions\handling-failures#step)
- [runId](\docs\reference\functions\handling-failures#run-id)
- [Examples](\docs\reference\functions\handling-failures#examples)
- [Send a Slack notification when a function fails](\docs\reference\functions\handling-failures#send-a-slack-notification-when-a-function-fails)
- [Capture all failure errors with Sentry](\docs\reference\functions\handling-failures#capture-all-failure-errors-with-sentry)
- [Additional examples](\docs\reference\functions\handling-failures#additional-examples)

References [TypeScript SDK](\docs\reference\typescript)

# Handling Failures

Define any failure handlers for your function with the [`onFailure`](\docs\reference\functions\create#configuration) option. This function will be automatically called when your function fails after it's maximum number of retries. Alternatively, you can use the [`"inngest/function.failed"`](\docs\reference\functions\handling-failures#the-inngest-function-failed-event) system event to handle failures across all functions.

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction (
{
id : "import-product-images" ,
onFailure : async ({ error , event , step }) => {
// This is the failure handler which can be used to
// send an alert, notification, or whatever you need to do
} ,
} ,
{ event : "shop/product.imported" } ,
async ({ event , step , runId }) => {
// This is the main function handler's code
}
);
```

The failure handler is very useful for:

- Sending alerts to your team
- Sending metrics to a third party monitoring tool (e.g. Datadog)
- Send a notification to your team or user that the job has failed
- Perform a rollback of the transaction (i.e. undo work partially completed by the main handler)

*Failures* should not be confused with *Errors* which will be retried. Read the [error handling &amp; retries documentation](\docs\functions\retries) for more context.

## [How onFailure works](\docs\reference\functions\handling-failures#how-on-failure-works)

The `onFailure` handler is a helper that actually creates a separate Inngest function used specifically for handling failures for your main function handler.

The separate Inngest function utilizes an [`"inngest/function.failed"`](\docs\reference\functions\handling-failures#the-inngest-function-failed-event) system event that gets sent to your account any time a function fails. The function created with `onFailure` will appear as a separate function in your dashboard with the name format: `"<Your function name> (failure)"` .

## [onFailure({ error, event, step, runId })](\docs\reference\functions\handling-failures#on-failure-error-event-step-run-id)

The `onFailure` handler function has the same arguments as [the main function handler](\docs\reference\functions\create#handler) when creating a function, but also receives an `error` argument.

### [error](\docs\reference\functions\handling-failures#error)

The JavaScript [`Error`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/Error) object as thrown from the last retry in your main function handler.

The Inngest SDK attempts to serialize and deserialize the `Error` object to the best of its ability and any custom error classes (e.g. `Prisma.PrismaClientKnownRequestError` or `MyCustomErrorType` ) that may be thrown will be deserialized as the default `Error` object. This means you *cannot* use `instance` of within `onFailure` to infer the type of error.

### [event](\docs\reference\functions\handling-failures#event)

The [`"inngest/function.failed"`](\docs\reference\system-events\inngest-function-failed) system event payload object. This object is similar to any event payload, but it contains data specific to the failed function's final retry attempt. [See the complete reference for this event payload here](\docs\reference\system-events\inngest-function-failed) .

### [step](\docs\reference\functions\handling-failures#step)

[See the](\docs\reference\functions\create#step) [`step`](\docs\reference\functions\create#step) [reference in the create function documentation](\docs\reference\functions\create#step) .

### [runId](\docs\reference\functions\handling-failures#run-id)

This will be the function run ID for the error handling function, *not the function that failed* . To get the failed function's run ID, use `event.data.run_id` . [Learn more about](\docs\reference\functions\create#run-id) [`runId`](\docs\reference\functions\create#run-id) [here](\docs\reference\functions\create#run-id) .

## [Examples](\docs\reference\functions\handling-failures#examples)

### [Send a Slack notification when a function fails](\docs\reference\functions\handling-failures#send-a-slack-notification-when-a-function-fails)

In this example, the function attempts to sync all products from a Shopify store, and if it fails, it sends a message to the team's *#eng-alerts* Slack channel using the Slack Web Api's `chat.postMessage` ( [docs](https://api.slack.com/methods/chat.postMessage) ) API.

Copy Copied

```
import { client } from "@slack/web-api" ;
import { inngest } from "./client" ;

export default inngest .createFunction (
{
id : "sync-shopify-products" ,
// Your handler should be an async function:
onFailure : async ({ error , event }) => {
const originalEvent = event . data .event;

// Post a message to the Engineering team's alerts channel in Slack:
const result = await client . chat .postMessage ({
token : process . env . SLACK_TOKEN ,
channel : "C12345" ,
blocks : [
{
type : "section" ,
text : {
type : "mrkdwn" ,
text : `Sync Shopify function failed for Store ${
originalEvent .storeId
} : ${ error .toString () } ` ,
} ,
} ,
] ,
});

return result;
} ,
} ,
{ event : "shop/product_sync.requested" } ,
async ({ event , step , runId }) => {
// This is the main function handler's code
const products = await step .run ( "fetch-products" , async () => {
const storeId = event . data .storeId;
// The function might fail here or...
});
await step .run ( "save-products" , async () => {
// The function might fail here after the maximum number of retries
});
}
);
```

### [Capture all failure errors with Sentry](\docs\reference\functions\handling-failures#capture-all-failure-errors-with-sentry)

Similar to the above example, you can capture and all failed functions' errors and send them to a singular place. Here's an example using [Sentry's node.js library](https://docs.datadoghq.com/api/latest/events/) to capture and send all failure errors to Sentry.

Copy Copied

```
import * as Sentry from "@sentry/node" ;
import { inngest } from "./client" ;

Sentry .init ({
dsn : "https://examplePublicKey@o0.ingest.sentry.io/0" ,
});

export default inngest .createFunction (
{
name : "Send failures to Sentry" ,
id : "send-failed-function-errors-to-sentry"
} ,
{ event : "inngest/function.failed" } ,
async ({ event , step }) => {

// The error is serialized as JSON, so we must re-construct it for Sentry's error handling:
const error = event . data .error;
const reconstructedEvent = new Error ( error .message);
// Set the name in the newly created event:
// You can even customize the name here if you'd like,
// e.g. `Function Failure: ${event.} - ${error.name}`
reconstructedEvent .name = error .name;

// Add the stack trace to the error:
reconstructedEvent .stack = error .stack;

// Capture the error with Sentry and append any additional tags or metadata:
Sentry .captureException (reconstructedEvent , {
extra : {
function_id ,
} ,
});

// Flush the Sentry queue to ensure the error is sent:
return await Sentry .flush ();
}
);
```

### [Additional examples](\docs\reference\functions\handling-failures#additional-examples)

### [Track all function failures in Datadog](\docs\examples\track-failures-in-datadog)

[Send all function failures to Datadog (or similar) for monitoring.](\docs\examples\track-failures-in-datadog)