#### On this page

- [Middleware lifecycle](\docs\reference\middleware\lifecycle#middleware-lifecycle)
- [Hook reference](\docs\reference\middleware\lifecycle#hook-reference)
- [onFunctionRun lifecycle](\docs\reference\middleware\lifecycle#on-function-run-lifecycle)
- [onSendEvent lifecycle](\docs\reference\middleware\lifecycle#on-send-event-lifecycle)

References [TypeScript SDK](\docs\reference\typescript) [Middleware](\docs\reference\middleware\lifecycle)

# Middleware lifecycle v2.0.0+

## [Hook reference](\docs\reference\middleware\lifecycle#hook-reference)

The `init()` function can return functions for two separate lifecycles to hook into.

💡 All lifecycle and hook functions can be synchronous or `async` functions - the SDK will always wait until a middleware's function has resolved before continuing to the next one.

### [onFunctionRun lifecycle](\docs\reference\middleware\lifecycle#on-function-run-lifecycle)

Triggered when a function is going to be executed.

Arguments

- Name `ctx` Type object Required optional Description The input data for the function. Only `event` and `runId` are available at this point.
- Name `steps` Type array Required optional Description An array of previously-completed step objects. Show nested properties
- Name `fn` Type InngestFunction Required optional Description The function that is about to be executed.
- Name `reqArgs` Type array Required optional Version v3.9.0+ Description Arguments passed to the framework's request handler, which are used by the SDK's `serve` handler.

Returns

- Name `transformInput` Type function Required optional Description Called once the input for the function has been set up. This is where you can modify the input before the function starts. Has the same input as the containing `onFunctionRun()` lifecycle function, but with a complete `ctx` object, including `step` tooling. Show nested returns
- Name `beforeMemoization` Type function Required optional Description Called before the function starts to memoize state (running over previously-seen code).
- Name `afterMemoization` Type function Required optional Description Called after the function has finished memoizing state (running over previously-seen code).
- Name `beforeExecution` Type function Required optional Description Called before any step or code executes.
- Name `afterExecution` Type function Required optional Description Called after any step or code has finished executing.
- Name `transformOutput` Type function Required optional Description Called after the function has finished executing and before the response is sent back to Inngest. This is where you can modify the output. Show nested arguments Show nested returns
- Name `finished` Type function Required optional Version v3.21.0+ Description Called when execution is complete and a final response is returned (success or an error), which will end the run. This function is not guaranteed to be called on every execution. It may be called multiple times if there are many parallel executions or during retries. Show nested arguments
- Name `beforeResponse` Type function Required optional Description Called after the output has been set and before the response has been sent back to Inngest. Use this to perform any final actions before the request closes.

Copy Copied

```
const myMiddleware = new InngestMiddleware ({
name : "My Middleware" ,
init ({ client , fn }) {
return {
onFunctionRun ({ ctx , fn , steps }) {
return {
transformInput ({ ctx , fn , steps }) {
// ...
return {
// All returns are optional
ctx : { /* extend fn input */ } ,
steps : steps .map (({ data }) => { /* transform step data */ })
}
} ,
beforeMemoization () {
// ...
} ,
afterMemoization () {
// ...
} ,
beforeExecution () {
// ...
} ,
afterExecution () {
// ...
} ,
transformOutput ({ result , step }) {
// ...
return {
// All returns are optional
result : {
// Transform data before it goes back to Inngest
data : transformData ( result .data)
}
}
} ,
finished ({ result }) {
// ...
} ,
beforeResponse () {
// ...
} ,
};
} ,
};
} ,
});
```

### [onSendEvent lifecycle](\docs\reference\middleware\lifecycle#on-send-event-lifecycle)

Triggered when an event is going to be sent via `inngest.send()` , `step.sendEvent()` , or `step.invoke()` .

Output

- Name `transformInput` Type function Required optional Description Called before the events are sent to Inngest. This is where you can modify the events before they're sent.
- Name `transformOutput` Type function Required optional Description Called after events are sent to Inngest. This is where you can perform any final actions and modify the output from `inngest.send()` .

Copy Copied

```
const myMiddleware = new InngestMiddleware ({
name : "My Middleware" ,
init : ({ client , fn }) => {
return {
onSendEvent () {
return {
transformInput ({ payloads }) {
// ...
} ,
transformOutput () {
// ...
} ,
};
} ,
};
} ,
});
```