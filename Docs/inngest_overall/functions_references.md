#### On this page

- [Referencing functions](\docs\functions\references#referencing-functions)
- [How to use referenceFunction](\docs\functions\references#how-to-use-reference-function)
- [Configuration](\docs\functions\references#configuration)

References [TypeScript SDK](\docs\reference\typescript)

# Referencing functions

Using [`step.invoke()`](\docs\reference\functions\step-invoke) , you can directly call one Inngest function from another and handle the result. You can use this with `referenceFunction` to call Inngest functions located in other apps, or to avoid importing dependencies of functions within the same app.

Copy Copied

```
// @/inngest/compute.ts
import { referenceFunction } from "inngest" ;
import { z } from "zod" ;
import { type computePi } from "@/inngest/computePi" ;

// Create a local reference to a function without importing dependencies
export const computePi = referenceFunction < typeof computePi>({
functionId : "compute-pi" ,
});

// Create a reference to a function in another application
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
// @/inngest/someFn.ts
import { computeSquare } from "@/inngest/compute" ; // import the referenece

// square.result is typed as a number
const square = await step .invoke ( "compute-square-value" , {
function : computeSquare ,
data : { number : 4 } , // input data is typed, requiring input if it's needed
});
```

## [How to use referenceFunction](\docs\functions\references#how-to-use-reference-function)

The simplest reference just contains a `functionId` . When used, this will invoke the function with the given ID in the same app that is used to invoke it.

The input and output types are `unknown` .

Copy Copied

```
import { referenceFunction } from "inngest" ;

await step .invoke ( "start-process" , {
function : referenceFunction ({
functionId : "some-fn" ,
}) ,
});
```

If referencing a function in a different application, specify an `appId` too:

Copy Copied

```
import { referenceFunction } from "inngest" ;

await step .invoke ( "start-process" , {
function : referenceFunction ({
functionId : "some-fn" ,
appId : "some-app" ,
}) ,
});
```

You can optionally provide `schemas` , which are a collection of [Zod](https://zod.dev/) schemas used to provide typing to the input and output of the referenced function.

In the future, this will also *validate* the input and output.

Copy Copied

```
import { referenceFunction } from "inngest" ;
import { z } from "zod" ;

await step .invoke ( "start-process" , {
function : referenceFunction ({
functionId : "some-fn" ,
appId : "some-app" ,
schemas : {
data : z .object ({
foo : z .string () ,
}) ,
return : z .object ({
success : z .boolean () ,
}) ,
} ,
}) ,
});
```

Even if functions are within the same app, this can also be used to avoid importing the dependencies of one function into another, which is useful for frameworks like Next.js where edge and serverless logic can be colocated but require different dependencies.

Copy Copied

```
import { referenceFunction } from "inngest" ;
import { type someInngestFn } from "@/inngest/someFn" ; // import only the type

await step .invoke ( "start-process" , {
function : referenceFunction < typeof someInngestFn>({
functionId : "some-fn" ,
}) ,
});
```

## [Configuration](\docs\functions\references#configuration)

- Name `functionId` Type string Required required Description The ID of the function to reference. This can be either a local function ID or the ID of a function that exists in another app. If the latter, `appId` must also be provided. If `appId` is not provided, the function ID will be assumed to be a local function ID (the app ID of the calling app will be used).
- Name `appId` Type string Required optional Description The ID of the app that the function belongs to. This is only required if the function being refenced exists in another app.
- Name `schemas` Type object Required optional Description The schemas of the referenced function, providing typing to the input `data` and `return` of invoking the referenced function. If not provided and a local function type is not being passed as a generic into `referenceFunction()` , the schemas will be inferred as `unknown` . Properties