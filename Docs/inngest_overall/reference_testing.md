#### On this page

- [Testing](\docs\reference\testing#testing)
- [Installation](\docs\reference\testing#installation)
- [Unit tests](\docs\reference\testing#unit-tests)
- [Running an individual step](\docs\reference\testing#running-an-individual-step)
- [Assertions](\docs\reference\testing#assertions)
- [Mocking](\docs\reference\testing#mocking)

References [TypeScript SDK](\docs\reference\typescript)

# Testing

To test your Inngest functions programmatically, use the `@inngest/test` library, available on [npm](https://www.npmjs.com/package/@inngest/test) and [JSR](https://jsr.io/@inngest/test) .

This allows you to mock function state, step tooling, and inputs with a

Jest-compatible API supporting all major testing frameworks, runtimes, and

libraries:

- jest
- vitest
- `bun:test` (Bun)
- `@std/expect` (Deno)
- `chai` / `expect`

## [Installation](\docs\reference\testing#installation)

The `@inngest/test` package requires `inngest@>=3.22.12` .

npm Yarn pnpm Bun Deno

Copy Copied

```
npm install -D @inngest/test
```

## [Unit tests](\docs\reference\testing#unit-tests)

Use whichever supported testing framework; `@inngest/test` is unopinionated

about how your tests are run. We'll demonstrate here using

`jest` .

Import `InngestTestEngine` , our function to test, and create a new `InngestTestEngine` instance.

Copy Copied

```
import { InngestTestEngine } from "@inngest/test" ;
import { helloWorld } from "./helloWorld" ;

describe ( "helloWorld function" , () => {
const t = new InngestTestEngine ({
function : helloWorld ,
});
});
```

Now we can use the primary API for testing, `t.execute()` :

Copy Copied

```
test ( "returns a greeting" , async () => {
const { result } = await t .execute ();
expect (result) .toEqual ( "Hello World!" );
});
```

This will run the entire function (steps and all) to completion, then return the

response from the function, where we assert that it was the string

`"Hello World!"` .

A serialized `error` will be returned instead of `result` if the function threw:

Copy Copied

```
test ( "throws an error" , async () => {
const { error } = await t .execute ();
expect (error) .toContain ( "Some specific error" );
});
```

When using steps that delay execution, like `step.sleep` or `step.waitForEvent` , you will need to mock them. [Learn more about mocking steps](\docs\reference\testing#steps) .

### [Running an individual step](\docs\reference\testing#running-an-individual-step)

`t.executeStep()` can be used to run the function until a particular step has

been executed.

This is useful to test a single step within a function or to see that a

non-runnable step such as

`step.waitForEvent()` has been registered with the

correct options.

Copy Copied

```
test ( "runs the price calculations" , async () => {
const { result } = await t .executeStep ( "calculate-price" );
expect (result) .toEqual ( 123 );
});
```

Assertions can also be made on steps in any part of a run, regardless of if

that's the checkpoint we've waited for. See

[Assertions -&gt; State](\docs\reference\testing#assertions) .

### [Assertions](\docs\reference\testing#assertions)

`@inngest/test` adds Jest-compatible mocks by default that can help you assert

function and step input and output. You can assert:

- Function input
- Function output
- Step output
- Step tool usage

All of these values are returned from both `t.execute()` and `t.executeStep()` ;

we'll only show one for simplicity here.

The `result` is returned, which is the output of the run or step:

Copy Copied

```
const { result } = await t .execute ();
expect (result) .toEqual ( "Hello World!" );
```

`ctx` is the input used for the function run. This can be used to assert outputs

that are based on input data such as

`event` or `runId` , or to confirm that

middleware is working correctly and affecting input arguments.

Copy Copied

```
const { ctx , result } = await t .execute ();
expect (result) .toEqual ( `Run ID was: " ${ ctx .runId } "` );
```

The step tooling at `ctx.step` are all Jest-compatible spy functions, so you can

use them to assert that they've been called and used correctly:

Copy Copied

```
const { ctx } = await t .execute ();
expect ( ctx . step .run) .toHaveBeenCalledWith ( "my-step" , expect .any (Function));
```

`state` is also returned, which is a view into the outputs of all steps in the

run. This allows you to test each individual step output for any given input:

Copy Copied

```
const { state } = await t .execute ();
expect (state[ "my-step" ]). resolves .toEqual ( "some successful output" );
expect (state[ "dangerous-step" ]). rejects .toThrowError ( "something failed" );
```

### [Mocking](\docs\reference\testing#mocking)

Some mocking is done automatically by `@inngest/test` , but can be overwritten if

needed.

All mocks detailed below can be specified either when creating an `InngestTestEngine` instance or for each individual execution:

Copy Copied

```
// Set the events for every execution
const t = new InngestTestEngine ({
function : helloWorld ,
// mocks here
});

// Or for just one, which will overwrite any current event mocks
t .execute ({
// mocks here
});

t .executeStep ( "my-step" , {
// mocks here
})
```

You can also clone an existing `InngestTestEngine` instance to encourage re-use

of complex mocks:

Copy Copied

```
// Make a direct clone, which includes any mocks
const otherT = t .clone ();

// Provide some more mocks in addition to any existing ones
const anotherT = t .clone ({
// mocks here
});
```

For simplicity, the following examples will show usage of `t.execute()` , but the

mocks can be placed in any of these locations.

### [Events](\docs\reference\testing#events)

The incoming event data can be mocked. They are always specified as an array of

events to allow also mocking batches.

Copy Copied

```
t .execute ({
events : [{ name : "demo/event.sent" , data : { message : "Hi!" } }] ,
});
```

If no event mocks are given at all (or `events: undefined` is explicitly set),

an

`inngest/function.invoked` event will be mocked for you.

### [Steps](\docs\reference\testing#steps)

Mocking steps can help you model different paths and situations within your

function. To do so, any step can be mocked by providing the

`steps` option. You should always mock `sleep` and `waitForEvent` steps - [learn more here](\docs\reference\testing#sleep-and-wait-for-event) .

Here we mock two steps, one that will run successfully and another that will

model a failure and throw an error:

Copy Copied

```
t .execute ({
steps : [
{
id : "successful-step" ,
handler () {
return "We did it!" ;
} ,
} ,
{
id : "dangerous-step" ,
handler () {
throw new Error ( "Oh no!" );
} ,
} ,
] ,
});
```

These handlers will run lazily when they are found during a function's execution.

This means you can write complex mocks that respond to other information:

Copy Copied

```
let message = "" ;

t .execute ({
steps : [
{
id : "build-greeting" ,
handler () {
message = "Hello, " ;
return message;
} ,
} ,
{
id : "build-name" ,
handler () {
return message + " World!" ;
} ,
} ,
] ,
});
```

### [Sleep and waitForEvent](\docs\reference\testing#sleep-and-wait-for-event)

Steps that pause the function, `step.sleep` , `step.sleepUntil` , and `step.waitForEvent` should always be mocked.

step.sleep step.waitForEvent

Copy Copied

```
// Given the following function that sleeps
const myFunction = inngest .createFunction (
{ id : "my-function" } ,
{ event : "user.created" } ,
async ({ event , step }) => {
await step .sleep ( "one-day-delay" , "1d" );
return { message : "success" };
}
)
// Mock the step to execute a no-op handler to return immediately
t .execute ({
steps : [
{
id : "one-day-delay" ,
handler () {} , // no return value necessary
} ,
] ,
});
```

### [Modules and imports](\docs\reference\testing#modules-and-imports)

Any mocking of modules or imports outside of Inngest which your functions may

rely on should be done outside of Inngest with the testing framework you're

using.

Here are some links to the major supported frameworks and their guidance for

mocking imports:

- [jest](https://jestjs.io/docs/mock-functions#mocking-modules)
- [vitest](https://vitest.dev/guide/mocking#modules)
- [`bun:test`](https://bun.sh/docs/test/mocks#module-mocks-with-mock-module) [(Bun)](https://bun.sh/docs/test/mocks#module-mocks-with-mock-module)
- [`@std/testing`](https://jsr.io/@std/testing/doc/mock/~) [(Deno)](https://jsr.io/@std/testing/doc/mock/~)

### [Custom](\docs\reference\testing#custom)

You can also provide your own custom mocks for the function input.

When instantiating a new `InngestTestEngine` or starting an execution, provide a `transformCtx` function that will add these mocks every time the function is

run:

Copy Copied

```
const t = new InngestTestEngine ({
function : helloWorld ,
transformCtx : (ctx) => {
return {
... ctx ,
event : someCustomThing ,
};
} ,
});
```

If you wish to still add the automatic mocking from `@inngest/test` (such as the

spies on

`ctx.step.*` ), you can import and use the automatic transforms as part

of your own:

Copy Copied

```
import { InngestTestEngine , mockCtx } from "@inngest/test" ;

const t = new InngestTestEngine ({
function : helloWorld ,
transformCtx : (ctx) => {
return {
... mockCtx (ctx) ,
event : someCustomThing ,
};
} ,
});
```