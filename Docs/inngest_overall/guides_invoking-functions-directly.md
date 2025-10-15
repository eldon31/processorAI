#### On this page

- [Invoking functions directly](\docs\guides\invoking-functions-directly#invoking-functions-directly)
- [Invoking another function](\docs\guides\invoking-functions-directly#invoking-another-function)
- [When should I invoke?](\docs\guides\invoking-functions-directly#when-should-i-invoke)
- [Referencing another Inngest function](\docs\guides\invoking-functions-directly#referencing-another-inngest-function)
- [When should I invoke?](\docs\guides\invoking-functions-directly#when-should-i-invoke-2)
- [When should I invoke?](\docs\guides\invoking-functions-directly#when-should-i-invoke-3)
- [Creating a distributed system](\docs\guides\invoking-functions-directly#creating-a-distributed-system)
- [Similar pattern: Fan-Out](\docs\guides\invoking-functions-directly#similar-pattern-fan-out)

Features [Events &amp; Triggers](\docs\features\events-triggers)

# Invoking functions directly

Inngest's `step.invoke()` function provides a powerful tool for calling functions directly within your event-driven system. It differs from traditional event-driven triggers, offering a more direct, RPC-like approach. This encourages a few key benefits:

- Allows functions to call and receive the result of other functions
- Naturally separates your system into reusable functions that can spread across process boundaries
- Allows use of synchronous interaction between functions in an otherwise-asynchronous event-driven architecture, making it much easier to manage functions that require immediate outcomes

## [Invoking another function](\docs\guides\invoking-functions-directly#invoking-another-function)

TypeScript Go Python

### [When should I invoke?](\docs\guides\invoking-functions-directly#when-should-i-invoke)

Use `step.invoke()` in tasks that need specific settings like concurrency limits. Because it runs with its own configuration,

distinct from the invoker's, you can provide a tailored configuration for each function.

If you don't need to define granular configuration or if your function won't be reused across app boundaries, use `step.run()` for simplicity.

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

In the above example, our `mainFunction` calls `computeSquare` to retrieve the resulting value. `computeSquare` can now be called from here or any other process connected to Inngest.

## [Referencing another Inngest function](\docs\guides\invoking-functions-directly#referencing-another-inngest-function)

If a function exists in another app, you can create a reference that can be invoked in the same manner as the local `computeSquare` function above.

Copy Copied

```
// @/inngest/computeSquare.ts
import { referenceFunction } from "inngest" ;
import { z } from "zod" ;

// Create a reference to a function in another application.
export const computeSquare = referenceFunction ({
appId : "my-python-app" ,
functionId : "compute-square" ,
// Schemas are optional, but provide types for your call if specified
schemas : {
data : z .object ({
number : z .number () ,
}) ,
return : z .object ({
result : z .number () ,
}) ,
} ,
});
```

Copy Copied

```
import { computeSquare } from "@/inngest/computeSquare" ;

// square.result is typed as a number
const square = await step .invoke ( "compute-square-value" , {
function : computeSquare ,
data : { number : 4 } , // input data is typed, requiring input if it's needed
});
```

References can also be used to invoke local functions without needing to import them (and their dependencies) directly. This can be useful for frameworks like Next.js where edge and serverless handlers can be mixed together and require different sets of dependencies.

Copy Copied

```
import { inngest , referenceFunction } from "inngest" ;
import { type computeSquare } from "@/inngest/computeSquare" ; // Import only the type

const mainFunction = inngest .createFunction (
{ id : "main-function" } ,
{ event : "main/event" } ,
async ({ step }) => {
const square = await step .invoke ( "compute-square-value" , {
function : referenceFunction < typeof computeSquare>({
functionId : "compute-square" ,
}) ,
data : { number : 4 } , // input data is still typed
});

return `Square of 4 is ${ square .result } .` ; // square.result is typed as number
}
);
```

For more information on referencing functions, see [TypeScript -&gt; Referencing Functions](\docs\functions\references) .

## [Creating a distributed system](\docs\guides\invoking-functions-directly#creating-a-distributed-system)

You can invoke Inngest functions written in any language, hosted on different clouds.  For example, a TypeScript function on Vercel can invoke a Python function hosted in AWS.

By starting to define these blocks of functionality, you're creating a smart, distributed system with all of the benefits of event-driven architecture and without any of the hassle.

## [Similar pattern: Fan-Out](\docs\guides\invoking-functions-directly#similar-pattern-fan-out)

A similar pattern to invoking functions directly is that of fan-out - [check out the guide here](\docs\guides\fan-out-jobs) . Here are some key differences:

- Fan-out will trigger multiple functions simultaneously, whereas invocation will only trigger one
- Unlike invocation, fan-out will not receive the result of the invoked function
- Choose fan-out for parallel processing of independent tasks and invocation for coordinated, interdependent functions