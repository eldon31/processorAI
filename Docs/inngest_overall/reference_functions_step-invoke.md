#### On this page

- [Invoke](\docs\reference\functions\step-invoke#invoke)
- [step.invoke(id, options): Promise](\docs\reference\functions\step-invoke#step-invoke-id-options-promise)
- [How to call step.invoke()](\docs\reference\functions\step-invoke#how-to-call-step-invoke)
- [Using function references](\docs\reference\functions\step-invoke#using-function-references)
- [When to use step.invoke()](\docs\reference\functions\step-invoke#when-to-use-step-invoke)
- [Internal behaviour](\docs\reference\functions\step-invoke#internal-behaviour)
- [Return values and serialization](\docs\reference\functions\step-invoke#return-values-and-serialization)
- [Retries](\docs\reference\functions\step-invoke#retries)
- [Error handling](\docs\reference\functions\step-invoke#error-handling)
- [Function not found](\docs\reference\functions\step-invoke#function-not-found)
- [Invoked function fails](\docs\reference\functions\step-invoke#invoked-function-fails)
- [Invoked function times out](\docs\reference\functions\step-invoke#invoked-function-times-out)
- [Invoked function is rate limited](\docs\reference\functions\step-invoke#invoked-function-is-rate-limited)
- [Usage limits](\docs\reference\functions\step-invoke#usage-limits)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Invoke v3.7.0+

Use `step.invoke()` to asynchronously call another function and handle the result. Invoking other functions allows you to easily re-use functionality and compose them to create more complex workflows or map-reduce type jobs. `step.invoke()` returns a `Promise` that resolves with the return value of the invoked function.

Copy Copied

```
// Some function we'll call
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

## [step.invoke(id, options): Promise](\docs\reference\functions\step-invoke#step-invoke-id-options-promise)

- Name `id` Type string Required required Description The ID of the invocation. This is used in logs and to keep track of the invocation's state across different versions.
- Name `options` Type object Required required Description Options for the invocation: Properties Throwing errors within the invoked function will be reflected in the invoking function.

### Invoke a function directly

Copy Copied

```
const resultFromDirectCall = await step .invoke ( "invoke-by-definition" , {
function : anotherFunction ,
data : { ... } ,
});
```

### Invoke a function using a function reference

Copy Copied

```
const resultFromReference = await step .invoke ( "invoke-by-reference" , {
function : referenceFunction ( ... ) ,
data : { ... } ,
});
```

### Invoke a function with a timeout

Copy Copied

```
const resultFromDirectCall = await step .invoke ( "invoke-with-timeout" , {
function : anotherFunction ,
data : { ... } ,
timeout : "1h" ,
});
```

## [How to call step.invoke()](\docs\reference\functions\step-invoke#how-to-call-step-invoke)

Handling `step.invoke()` is similar to handling any other Promise in JavaScript:

Copy Copied

```
// Using the "await" keyword
const result = await step .invoke ( "invoke-function" , {
function : someInngestFn ,
data : { ... } ,
});

// Using `then` for chaining
step
.invoke ( "invoke-function" , { function : someInngestFn , data : { ... } })
.then ((result) => {
// further processing
});

// Running multiple invocations in parallel
Promise .all ([
step .invoke ( "invoke-first-function" , {
function : firstFunctionReference ,
data : { ... } ,
}) ,
step .invoke ( "invoke-second-function" , {
function : secondFn ,
data : { ... } ,
}) ,
]);
```

## [Using function references](\docs\reference\functions\step-invoke#using-function-references)

Instead of directly importing a local function to invoke, [`referenceFunction()`](\docs\functions\references) can be used to call an Inngest function located in another app, or to avoid importing the dependencies of a function within the same app.

Copy Copied

```
import { referenceFunction } from "inngest" ;
import { type computePi } from "@/inngest/computePi" ;

// Create a local reference to a function without importing dependencies
const computePi = referenceFunction < typeof computePi>({
functionId : "compute-pi" ,
});

// Create a reference to a function in another application
const computeSquare = referenceFunction ({
appId : "my-python-app" ,
functionId : "compute-square" ,
});

// square.result is typed as a number
const square = await step .invoke ( "compute-square-value" , {
function : computePi ,
data : { number : 4 } , // input data is typed, requiring input if it's needed
});
```

See [Referencing functions](\docs\functions\references) for more information.

## [When to use step.invoke()](\docs\reference\functions\step-invoke#when-to-use-step-invoke)

Use of `step.invoke()` to call an Inngest function directly is more akin to traditional RPC than Inngest's usual event-driven flow. While this tool still uses events behind the scenes, you can use it to help break up your codebase into reusable workflows that can be called from anywhere.

Use `step.invoke()` in tasks that need specific settings like concurrency limits. Because it runs with its own configuration,

distinct from the invoker's, you can provide a tailored configuration for each function.

If you don't need to define granular configuration or if your function won't be reused across app boundaries, use `step.run()` for simplicity.

## [Internal behaviour](\docs\reference\functions\step-invoke#internal-behaviour)

When a function object is passed as an argument, internally, the SDK retrieves the function's ID automatically. Alternatively, if a function ID `string` is passed, the Inngest SDK will assert the ID is correct at runtime. See [Error handling](\docs\reference\functions\step-invoke#error-handling) for more information about this point.

When Inngest receives the request to invoke a function, it'll do so and wait for an `inngest/function.finished` event, which it will use to fulfil the data (or error) for the step.

## [Return values and serialization](\docs\reference\functions\step-invoke#return-values-and-serialization)

Similar to `step.run()` , all data returned from `step.invoke()` is serialized as JSON. This is done to enable the SDK to return a valid serialized response to the Inngest service.

## [Retries](\docs\reference\functions\step-invoke#retries)

The invoked function will be executed as a regular Inngest function: it will have its own set of retries and can be seen as a brand new run.

If a `step.invoke()` fails for any of the reasons below, it will throw a `NonRetriableError` . This is to combat compounding retries, such that chains of invoked functions can be executed many more times than expected. For example, if A invokes B which invokes C, which invokes D, on failure D would be run 27 times ( `retryCount^n` ).

This may change on the future - [let us know](https://roadmap.inngest.com/roadmap?ref=docs) if you'd like to change this.

## [Error handling](\docs\reference\functions\step-invoke#error-handling)

### [Function not found](\docs\reference\functions\step-invoke#function-not-found)

If Inngest could not find a function to invoke using the given ID (see [Internal behaviour](\docs\reference\functions\step-invoke#internal-behaviour) above), an `inngest/function.finished` event will be sent with an appropriate error and the step will fail with a `NonRetriableError` .

### [Invoked function fails](\docs\reference\functions\step-invoke#invoked-function-fails)

If the function exhausts all retries and fails, an `inngest/function.finished` event will be sent with an appropriate error and the step will fail with a `NonRetriableError` .

### [Invoked function times out](\docs\reference\functions\step-invoke#invoked-function-times-out)

If the `timeout` has been reached and the invoked function is still running, the

step will fail with a

`NonRetriableError` .

### [Invoked function is rate limited](\docs\reference\functions\step-invoke#invoked-function-is-rate-limited)

If the called function has a rate limit configuration and is skipped, the step will fail with a `NonRetriableError` .

It's recommended to wrap the

`step.invoke` with a `try catch` if the invoked function is expected to be executing occasionally.

## [Usage limits](\docs\reference\functions\step-invoke#usage-limits)

See [usage limits](\docs\usage-limits\inngest#functions) for more details.