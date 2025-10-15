#### On this page

- [Creating middleware](\docs\features\middleware\create#creating-middleware)
- [Initialization](\docs\features\middleware\create#initialization)
- [Specifying lifecycles and hooks](\docs\features\middleware\create#specifying-lifecycles-and-hooks)
- [Adding configuration](\docs\features\middleware\create#adding-configuration)
- [Next steps](\docs\features\middleware\create#next-steps)

Features [Middleware](\docs\features\middleware)

# Creating middleware

Creating middleware means defining the lifecycles and subsequent hooks in those lifecycles to run code in. Lifecycles are actions such as a function run or sending events, and individual hooks within those are where we run code, usually with a *before* and *after* step.

TypeScript (v2.0.0+) Python (v0.3.0+)

A Middleware is created using the `InngestMiddleware` class.

**```
new InngestMiddleware(options): InngestMiddleware
```**

Copy Copied

```
// Create a new middleware
const myMiddleware = new InngestMiddleware ({
name : "My Middleware" ,
init : () => {
return {};
} ,
});

// Register it on the client
const inngest = new Inngest ({
id : "my-app" ,
middleware : [myMiddleware] ,
});
```

## [Initialization](\docs\features\middleware\create#initialization)

As you can see above, we start with the `init` function, which is called when the client is initialized.

Copy Copied

```
import { InngestMiddleware } from "inngest" ;

new InngestMiddleware ({
name : "Example Middleware" ,
init () {
// This runs when the client is initialized
// Use this to set up anything your middleware needs
return {};
} ,
});
```

Function registration, lifecycles, and hooks can all be with synchronous or `async` functions. This makes it easy for our initialization handler to do some async work, like setting up a database connection.

Copy Copied

```
new InngestMiddleware ({
name : "Example Middleware" ,
async init () {
const db = await connectToDatabase ();

return {};
} ,
});
```

All lifecycle and hook functions can be synchronous or `async` functions - the SDK will always wait until a middleware's function has resolved before continuing to the next one.

As it's possible for an application to use multiple Inngest clients, it's recommended to always initialize dependencies within the initializer function/method, instead of in the global scope.

## [Specifying lifecycles and hooks](\docs\features\middleware\create#specifying-lifecycles-and-hooks)

Notice we're returning an empty object `{}` . From here, we can instead return the lifecycles we want to use for this client. See the [Middleware - Lifecycle - Hook reference](\docs\reference\middleware\lifecycle#hook-reference) for a full list of available hooks.

Copy Copied

```
new InngestMiddleware ({
name : "Example Middleware" ,
async init () {
// 1. Use init to set up dependencies
// 2. Use return values to group hooks by lifecycle: - "onFunctionRun" "onSendEvent"
return {
onFunctionRun ({ ctx , fn , steps }) {
// 3. Use the lifecycle function to pass dependencies into hooks
// 4. Return any hooks that you want to define for this action
return {
// 5. Define the hook that runs at a specific stage for this lifecycle.
beforeExecution () {
// 6. Define your hook
} ,
};
} ,
};
} ,
});
```

Here we use the `beforeExecution()` hook within the `onFunctionRun()` lifecycle.

The use of [closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) here means that our `onFunctionRun()` lifecycle can access anything from the middleware's initialization, like our `db` connection.

`onFunctionRun()` here is also called for every function execution, meaning you can run code specific to this execution without maintaining any global state. We can even conditionally register hooks based on incoming arguments. For example, here we only register a hook for a specific event trigger:

Copy Copied

```
new InngestMiddleware ({
name : "Example Middleware" ,
async init () {
return {
onFunctionRun ({ ctx , fn , steps }) {
// Register a hook only if this event is the trigger
if ( ctx . event .name === "app/user.created" ) {
return {
beforeExecution () {
console .log ( "Function executing with user created event" );
} ,
};
}

// Register no hooks if the trigger was not `app/user.created`
return {};
} ,
};
} ,
});
```

Learn more about hooks with:

- [Lifecycle](\docs\reference\middleware\lifecycle) - middleware ordering and see all available hooks
- [TypeScript](\docs\reference\middleware\typescript) - how to affect input and output types and values

## [Adding configuration](\docs\features\middleware\create#adding-configuration)

It's common for middleware to require additional customization or options from developers. For this, we recommend creating a function that takes in some options and returns the middleware.

### inngest/middleware/myMiddleware.ts

Copy Copied

```
import { InngestMiddleware } from "inngest" ;

export const createMyMiddleware = (logEventOutput : string ) => {
return new InngestMiddleware ({
name : "My Middleware" ,
init () {
return {
onFunctionRun ({ ctx , fn , steps }) {
if ( ctx . event .name === logEventOutput) {
return {
transformOutput ({ result , step }) {
console .log (
` ${ logEventOutput } output: ${ JSON .stringify (result) } `
);
} ,
};
}

return {};
} ,
};
} ,
});
};
```

Copy Copied

```
import { createMyMiddleware } from "./middleware/myMiddleware" ;

export const inngest = new Inngest ({
id : "my-client" ,
middleware : [ createMyMiddleware ( "app/user.created" )] ,
});
```

Make sure to let TypeScript infer the output of the function instead of strictly typing it; this helps Inngest understand changes to input and output of arguments. See [Middleware - TypeScript](\docs\reference\middleware\typescript) for more information.

## [Next steps](\docs\features\middleware\create#next-steps)

Check out our pre-built middleware and examples:

## [Dependency Injection](\docs\features\middleware\dependency-injection)

[Provide shared client instances (ex, OpenAI) to your Inngest Functions.](\docs\features\middleware\dependency-injection)

## [Encryption Middleware](\docs\features\middleware\encryption-middleware)

[End-to-end encryption for events, step output, and function output.](\docs\features\middleware\encryption-middleware)

## [Sentry Middleware](\docs\features\middleware\sentry-middleware)

[Quickly setup Sentry for your Inngest Functions.](\docs\features\middleware\sentry-middleware)

## [Datadog middleware](\docs\examples\track-failures-in-datadog)

[Add tracing with Datadog under a few minutes.](\docs\examples\track-failures-in-datadog)

## [Cloudflare Workers &amp; Hono middleware](\docs\examples\middleware\cloudflare-workers-environment-variables)

[Access environment variables within Inngest functions.](\docs\examples\middleware\cloudflare-workers-environment-variables)