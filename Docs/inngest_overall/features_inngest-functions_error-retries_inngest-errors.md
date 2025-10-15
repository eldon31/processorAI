# Inngest Errors

Inngest automatically handles errors and retries for you. You can use standard errors or use included Inngest errors to control how Inngest handles errors.

TypeScript Go Python

## [Standard errors](\docs\features\inngest-functions\error-retries\inngest-errors#standard-errors)

All `Error` objects are handled by Inngest and [retried automatically](\docs\features\inngest-functions\error-retries\retries) . This includes all standard errors like `TypeError` and custom errors that extend the `Error` class. You can throw errors in the function handler or within a step.

Copy Copied

```
export default inngest .createFunction (
{ id : "import-item-data" } ,
{ event : "store/import.requested" } ,
async ({ event }) => {

// throwing a standard error
if ( ! event .itemId) {
throw new Error ( "Item ID is required" );
}

// throwing an error within a step
const item = await step .run ( 'fetch-item' , async () => {
const response = await fetch ( `https://api.ecommerce.com/items/ ${ event .itemId } ` );
if ( response .status === 500 ) {
throw new Error ( "Failed to fetch item from ecommerce API" );
}
// ...
});
}
);
```

## [Prevent any additional retries](\docs\features\inngest-functions\error-retries\inngest-errors#prevent-any-additional-retries)

Use `NonRetriableError` to prevent Inngest from retrying the function *or* step. This is useful when the type of error is not expected to be resolved by a retry, for example, when the error is caused by an invalid input or when the error is expected to occur again if retried.

Copy Copied

```
import { NonRetriableError } from "inngest" ;

export default inngest .createFunction (
{ id : "mark-store-imported" } ,
{ event : "store/import.completed" } ,
async ({ event }) => {
try {
const result = await database .updateStore (
{ id : event . data .storeId } ,
{ imported : true }
);
return result .ok === true ;
} catch (err) {
// Passing the original error via `cause` enables you to view the error in function logs
throw new NonRetriableError ( "Store not found" , { cause : err });
}
}
);
```

### [Parameters](\docs\features\inngest-functions\error-retries\inngest-errors#parameters)

Copy Copied

```
new NonRetriableError (message: string , options ?: { cause? : Error }): NonRetriableError
```

- Name `message` Type string Required required Description The error message.
- Name `options` Type object Required optional Description Show nested properties

## [Retry after a specific period of time](\docs\features\inngest-functions\error-retries\inngest-errors#retry-after-a-specific-period-of-time)

Use `RetryAfterError` to control when Inngest should retry the function or step. This is useful when you want to delay the next retry attempt for a specific period of time, for example, to more gracefully handle a race condition or backing off after hitting an API rate limit.

If `RetryAfterError` is not used, Inngest will use [the default retry backoff policy](https://github.com/inngest/inngest/blob/main/pkg/backoff/backoff.go#L10-L22) .

Copy Copied

```
inngest .createFunction (
{ id : "send-welcome-sms" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {
const { success , retryAfter } = await twilio . messages .create ({
to : event . data . user .phoneNumber ,
body : "Welcome to our service!" ,
});

if ( ! success && retryAfter) {
throw new RetryAfterError ( "Hit Twilio rate limit" , retryAfter);
}
}
);
```

### [Parameters](\docs\features\inngest-functions\error-retries\inngest-errors#parameters-2)

Copy Copied

```
new RetryAfterError (
message: string ,
retryAfter: number | string | date ,
options ?: { cause? : Error }
): RetryAfterError
```

- Name `message` Type string Required required Description The error message.
- Name `retryAfter` Type number | string | date Required required Description The specified time to delay the next retry attempt. The following formats are accepted:
- Name `options` Type object Required optional Description Show nested properties

## [Step errors v3.12.0+](\docs\features\inngest-functions\error-retries\inngest-errors#step-errors)

After a step exhausts all of its retries, it will throw a `StepError` which can be caught and handled in the function handler if desired.

try/catch Chaining with .catch() Ignoring and logging the error

Copy Copied

```
inngest .createFunction (
{ id : "send-weather-forecast" } ,
{ event : "weather/forecast.requested" } ,
async ({ event , step }) => {
let data;

try {
data = await step .run ( 'get-public-weather-data' , async () => {
return await fetch ( 'https://api.weather.com/data' );
});
} catch (err) {
// err will be an instance of StepError
// Handle the error by recovering with a different step
data = await step .run ( 'use-backup-weather-api' , async () => {
return await fetch ( 'https://api.stormwaters.com/data' );
});
}
// ...
}
);
```

Support for handling step errors is available in the Inngest TypeScript SDK starting from version **3.12.0** . Prior to this version, wrapping a step in try/catch will not work correctly.

## [Attempt counter](\docs\features\inngest-functions\error-retries\inngest-errors#attempt-counter)

The current attempt number is passed in as input to the function handler. `attempt` is a zero-index number that increments for each retry. The first attempt will be `0` , the second `1` , and so on. The number is reset after a successfully executed step.

Copy Copied

```
inngest .createFunction (
{ id : "generate-summary" } ,
{ event : "blog/post.created" } ,
async ({ attempt }) => {
// `attempt` is the zero-index attempt number

await step .run ( 'call-llm' , async () => {
if (attempt < 2 ) {
// Call OpenAI's API two times
} else {
// After two attempts to OpenAI, try a different LLM, for example, Mistral
}
});
}
);
```

## [Stack traces](\docs\features\inngest-functions\error-retries\inngest-errors#stack-traces)

When calling functions that return Promises, await the Promise to ensure that the stack trace is preserved. This applies to functions executing in different cycles of the event loop, for example, when calling a database or an external API. This is especially useful when debugging errors in production.

Returning Promise Awaiting Promise

Copy Copied

```
inngest .createFunction (
{ id : "update-recent-usage" } ,
{ event : "app/update-recent-usage" } ,
async ({ event , step }) => {
// ...
await step .run ( "update in db" , () => doSomeWork ( event .data));
// ...
}
);
```

Please note that immediately returning the Promise will not include a pointer to the calling function in the stack trace. Awaiting the Promise will ensure that the stack trace includes the calling function.