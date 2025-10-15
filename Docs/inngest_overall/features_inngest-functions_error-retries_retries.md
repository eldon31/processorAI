#### On this page

- [Retries](\docs\features\inngest-functions\error-retries\retries#retries)
- [Steps and Retries](\docs\features\inngest-functions\error-retries\retries#steps-and-retries)
- [Preventing retries with Non-retriable errors](\docs\features\inngest-functions\error-retries\retries#preventing-retries-with-non-retriable-errors)
- [Customizing retry times](\docs\features\inngest-functions\error-retries\retries#customizing-retry-times)

Features [Inngest Functions](\docs\features\inngest-functions) [Errors &amp; Retries](\docs\guides\error-handling)

# Retries

By default, in *addition* to the **initial attempt** , Inngest will retry a function or a step up to 4 times until it succeeds. This means that for a function with a default configuration, it will be attempted 5 times in total.

For the function below, if the database write fails then it'll be retried up to 4 times until it succeeds:

TypeScript Go Python

Copy Copied

```
inngest .createFunction (
{ id : "click-recorder" } ,
{ event : "app/button.clicked" } ,
async ({ event , attempt }) => {
await db . clicks .insertOne ( event .data); // this code now retries!
} ,
);
```

You can configure the number of `retries` by specifying it in your function configuration. Setting the value to `0` will disable retries.

TypeScript Go Python

Copy Copied

```
inngest .createFunction (
{
id : "click-recorder" ,
retries : 10 , // choose how many retries you'd like
} ,
{ event : "app/button.clicked" } ,
async ({ event , step , attempt }) => { /* ... */ } ,
);
```

You can customize the behavior of your function based on the number of retries using the `attempt` argument. `attempt` is passed in the function handler's context and is zero-indexed, meaning the first attempt is `0` , the second is `1` , and so on. The `attempt` is incremented every time the function throws an error and is retried, and is reset when steps complete. This allows you to handle attempt numbers differently in each step.

Retries will be performed with backoff according to [the default schedule](https://github.com/inngest/inngest/blob/main/pkg/backoff/backoff.go#L10-L22) .

## [Steps and Retries](\docs\features\inngest-functions\error-retries\retries#steps-and-retries)

A function can be broken down into multiple steps, where each step is individually executed and retried.

Here, both the " *get-data* " and " *save-data* " steps have their own set of retries. If the " *save-data* " step has a failure, it's retried, alone, in a separate request.

TypeScript Go Python

Copy Copied

```
inngest .createFunction (
{ id : "sync-systems" } ,
{ event : "auto/sync.request" } ,
async ({ step }) => {
// Can be retried up to 4 times
const data = await step .run ( "get-data" , async () => {
return getDataFromExternalSource ();
});

// Can also be retried up to 4 times
await step .run ( "save-data" , async () => {
return db . syncs .insertOne (data);
});
} ,
);
```

You can configure the number of [`retries`](\docs\reference\functions\create#inngest-create-function-configuration-trigger-handler-inngest-function) for each function. This excludes the initial attempt.  A retry count of `4` means that each step will be attempted up to 5 times.

## [Preventing retries with Non-retriable errors](\docs\features\inngest-functions\error-retries\retries#preventing-retries-with-non-retriable-errors)

You can throw a [non-retriable error](\docs\reference\typescript\functions\errors#non-retriable-error) from a step or a function, which will bypass any remaining retries and fail the step or function it was thrown from.

This is useful for when you know an error is permanent and want to stop all execution. In this example, the user doesn't exist, so there's no need to continue to email them.

TypeScript Go Python

Copy Copied

```
import { NonRetriableError } from "inngest" ;

inngest .createFunction (
{ id : "user-weekly-digest" } ,
{ event : "user/weekly.digest.requested" } ,
async ({ event , step }) => {
const user = await step
.run ( "get-user-email" , () => {
return db . users .findOne ( event . data .userId);
})
.catch ((err) => {
if ( err .name === "UserNotFoundError" ) {
throw new NonRetriableError ( "User no longer exists; stopping" );
}

throw err;
});

await step .run ( "send-digest" , () => {
return sendDigest ( user .email);
});
} ,
);
```

## [Customizing retry times](\docs\features\inngest-functions\error-retries\retries#customizing-retry-times)

Retries are executed with exponential back-off with some jitter, but it's also possible to specify exactly when you'd like a step or function to be retried.

In this example, an external API provided `Retry-After` header with information on when requests can be made again, so you can tell Inngest to retry your function then.

TypeScript Go Python

Copy Copied

```
import { RetryAfterError } from 'inngest' ;

inngest .createFunction (
{ id : "send-welcome-notification" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {

const msg = await step .run ( 'send-message' , async () => {
const { success , retryAfter , message } = await twilio . messages .create ({
to : event . data . user .phoneNumber ,
body : "Welcome to our service!" ,
});

if ( ! success && retryAfter) {
throw new RetryAfterError ( "Hit Twilio rate limit" , retryAfter);
}

return { message };
});

} ,
);
```