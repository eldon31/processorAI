#### On this page

- [Inngest Steps](\docs\learn\inngest-steps#inngest-steps)
- [Benefits of Using Steps](\docs\learn\inngest-steps#benefits-of-using-steps)
- [Anatomy of an Inngest Step](\docs\learn\inngest-steps#anatomy-of-an-inngest-step)
- [Available Step Methods](\docs\learn\inngest-steps#available-step-methods)
- [step.run()](\docs\learn\inngest-steps#step-run)
- [step.sleep()](\docs\learn\inngest-steps#step-sleep)
- [step.sleepUntil()](\docs\learn\inngest-steps#step-sleep-until)
- [step.waitForEvent()](\docs\learn\inngest-steps#step-wait-for-event)
- [step.invoke()](\docs\learn\inngest-steps#step-invoke)
- [step.sendEvent()](\docs\learn\inngest-steps#step-send-event)
- [Available Step Methods](\docs\learn\inngest-steps#available-step-methods-2)
- [step.Run()](\docs\learn\inngest-steps#step-run-2)
- [step.Sleep()](\docs\learn\inngest-steps#step-sleep-2)
- [step.WaitForEvent()](\docs\learn\inngest-steps#step-wait-for-event-2)
- [step.Invoke()](\docs\learn\inngest-steps#step-invoke-2)
- [Available Step Methods](\docs\learn\inngest-steps#available-step-methods-3)
- [step.run()](\docs\learn\inngest-steps#step-run-3)
- [step.sleep()](\docs\learn\inngest-steps#step-sleep-3)
- [step.sleep\_until()](\docs\learn\inngest-steps#step-sleep-until-2)
- [step.wait\_for\_event()](\docs\learn\inngest-steps#step-wait-for-event-3)
- [step.invoke()](\docs\learn\inngest-steps#step-invoke-3)
- [step.send\_event()](\docs\learn\inngest-steps#step-send-event-2)
- [Further reading](\docs\learn\inngest-steps#further-reading)

[Inngest tour](\docs\sdk\overview)

# Inngest Steps

Steps are fundamental building blocks in Inngest functions. Each step represents an individual task (or other unit of work) within a function that can be executed independently.

Steps are crucial because they allow functions to run specific tasks in a controlled and sequential (or parallel) manner. You can build complex workflows by chaining together simple, discrete operations.

On this page, you will learn about the benefits of using steps, and get an overview of the available step methods.

## [Benefits of Using Steps](\docs\learn\inngest-steps#benefits-of-using-steps)

- **Improved reliability** : structured steps enable precise control and handling of each task within a function.
- **Error handling** : capturing and managing errors at the step level means better error recovery.
- **Retry mechanism** : failing steps can be retried and recovered independently, without re-executing other successful steps.
- **Independent testing** : each step can be tested and debugged independently from others.
- **Improved code readability** : modular approach makes code easier to navigate and refactor.

If you'd like to learn more about how Inngest steps are executed, check the ["How Inngest functions are executed"](\docs\learn\how-functions-are-executed) page.

## [Anatomy of an Inngest Step](\docs\learn\inngest-steps#anatomy-of-an-inngest-step)

TypeScript Go Python

The first argument of every Inngest step method is an `id` . Each step is treated as a discrete task which can be individually retried, debugged, or recovered. Inngest uses the ID to memoize step state across function versions.

Copy Copied

```
export default inngest .createFunction (
{ id : "import-product-images" } ,
{ event : "shop/product.imported" } ,
async ({ event , step }) => {
const uploadedImageURLs = await step .run (
// step ID
"copy-images-to-s3" ,
// other arguments, in this case: a handler
async () => {
return copyAllImagesToS3 ( event . data .imageURLs);
});
}
);
```

The ID is also used to identify the function in the Inngest system.

Inngest's SDK also records a counter for each unique step ID.  The counter increases every time the same step is called.  This allows you to run the same step in a loop, without changing the ID.

Please note that each step is executed as **a separate HTTP request** . To ensure efficient and correct execution, place any non-deterministic logic (such as DB calls or API calls) within a `step.run()` call.

## [Available Step Methods](\docs\learn\inngest-steps#available-step-methods)

### [step.run()](\docs\reference\functions\step-run)

This method executes a defined piece of code.

Code within

`step.run()` is automatically retried if it throws an error. When `step.run()` finishes successfully, the response is saved in the function run state  and the step will not re-run.

Use it to run synchronous or asynchronous code as a retriable step in your function.

Copy Copied

```
export default inngest .createFunction (
{ id : "import-product-images" } ,
{ event : "shop/product.imported" } ,
async ({ event , step }) => {
// Here goes the business logic
// By wrapping code in steps, it will be retried automatically on failure
const uploadedImageURLs = await step .run ( "copy-images-to-s3" , async () => {
return copyAllImagesToS3 ( event . data .imageURLs);
});
}
);
```

`step.run()` acts as a code-level transaction.  The entire step must succeed to complete.

### [step.sleep()](\docs\reference\functions\step-sleep)

This method pauses execution for a specified duration. Even though it seems like a `setInterval` , your function does not run for that time (you don't use any compute). Inngest handles the scheduling for you. Use it to add delays or to wait for a specific amount of time before proceeding. At maximum, functions can sleep for a year (seven days for the [free tier plans](\pricing) ).

Copy Copied

```
export default inngest .createFunction (
{ id : "send-delayed-email" } ,
{ event : "app/user.signup" } ,
async ({ event , step }) => {
await step .sleep ( "wait-a-couple-of-days" , "2d" );
// Do something else
}
);
```

### [step.sleepUntil()](\docs\reference\functions\step-sleep-until)

This method pauses execution until a specific date time. Any date time string in the format accepted by the Date object, for example `YYYY-MM-DD` or `YYYY-MM-DDHH:mm:ss` . At maximum, functions can sleep for a year (seven days for the [free tier plans](\pricing) ).

Copy Copied

```
export default inngest .createFunction (
{ id : "send-scheduled-reminder" } ,
{ event : "app/reminder.scheduled" } ,
async ({ event , step }) => {
const date = new Date ( event . data .remind_at);
await step .sleepUntil ( "wait-for-the-date" , date);
// Do something else
}
);
```

### [step.waitForEvent()](\docs\reference\functions\step-wait-for-event)

This method pauses the execution until a specific event is received.

Copy Copied

```
export default inngest .createFunction (
{ id : "send-onboarding-nudge-email" } ,
{ event : "app/account.created" } ,
async ({ event , step }) => {
const onboardingCompleted = await step .waitForEvent (
"wait-for-onboarding-completion" ,
{ event : "app/onboarding.completed" , timeout : "3d" , if : "event.data.userId == async.data.userId" }
);
// Do something else
}
);
```

### [step.invoke()](\docs\reference\functions\step-invoke)

This method is used to asynchronously call another Inngest function ( [written in any language SDK](\blog\cross-language-support-with-new-sdks) ) and handle the result. Invoking other functions allows you to easily re-use functionality and compose them to create more complex workflows or map-reduce type jobs.

This method comes with its own configuration, which enables defining specific settings like concurrency limits.

Copy Copied

```
// A function we will call in another place in our app
const computeSquare = inngest .createFunction (
{ id : "compute-square" } ,
{ event : "calculate/square" } ,
async ({ event }) => {
return { result : event . data .number * event . data .number }; // Result typed as { result: number }
}
);

// In this function, we'll call `computeSquare`
const mainFunction = inngest .createFunction (
{ id : "main-function" } ,
{ event : "main/event" } ,
async ({ step }) => {
const square = await step .invoke ( "compute-square-value" , {
function : computeSquare ,
data : { number : 4 } , // input data is typed, requiring input if it's needed
});

return `Square of 4 is ${ square .result } .` ; // square.result is typed as number
}
);
```

### [step.sendEvent()](\docs\reference\functions\step-send-event)

This method sends events to Inngest to invoke functions with a matching event. Use `sendEvent()` when you want to trigger other functions, but you do not need to return the result. It is useful for example in [fan-out functions](\docs\guides\fan-out-jobs) .

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

## [Further reading](\docs\learn\inngest-steps#further-reading)

- [Quick Start](\docs\getting-started\nextjs-quick-start?ref=docs-inngest-steps) : learn how to build complex workflows.
- ["How Inngest functions are executed"](\docs\learn\how-functions-are-executed) : Learn more about Inngest's execution model, including how steps are handled.
- Docs guide: ["Multi-step functions"](\docs\guides\multi-step-functions) .