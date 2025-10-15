#### On this page

- [Upgrading from Inngest SDK v2 to v3](\docs\sdk\migration#upgrading-from-inngest-sdk-v2-to-v3)
- [Breaking changes in v3](\docs\sdk\migration#breaking-changes-in-v3)
- [Removing the guard rails](\docs\sdk\migration#removing-the-guard-rails)
- [A simple example](\docs\sdk\migration#a-simple-example)
- [Clients and functions require IDs](\docs\sdk\migration#clients-and-functions-require-ids)
- [All steps require IDs](\docs\sdk\migration#all-steps-require-ids)
- [Serve handlers refactored](\docs\sdk\migration#serve-handlers-refactored)
- [Shorthand function creation removed](\docs\sdk\migration#shorthand-function-creation-removed)
- [Environment variables and configuration](\docs\sdk\migration#environment-variables-and-configuration)
- [Handling in-progress runs triggered from v2](\docs\sdk\migration#handling-in-progress-runs-triggered-from-v2)
- [Advanced: Updating custom framework serve handlers](\docs\sdk\migration#advanced-updating-custom-framework-serve-handlers)
- [Function fns option removed](\docs\sdk\migration#function-fns-option-removed)
- [Upgrading from Inngest SDK v1 to v2](\docs\sdk\migration#upgrading-from-inngest-sdk-v1-to-v2)
- [Breaking changes in v2](\docs\sdk\migration#breaking-changes-in-v2)
- [New features in v2](\docs\sdk\migration#new-features-in-v2)
- [Better event schemas](\docs\sdk\migration#better-event-schemas)
- [Clearer event sending](\docs\sdk\migration#clearer-event-sending)
- [Removed tools parameter](\docs\sdk\migration#removed-tools-parameter)
- [Removed ability to serve() without a client](\docs\sdk\migration#removed-ability-to-serve-without-a-client)
- [Renamed throttle to rateLimit](\docs\sdk\migration#renamed-throttle-to-rate-limit)
- [Migrating from Inngest SDK v0 to v1](\docs\sdk\migration#migrating-from-inngest-sdk-v0-to-v1)
- [What's new in v1](\docs\sdk\migration#what-s-new-in-v1)
- [Replacing function creation helpers](\docs\sdk\migration#replacing-function-creation-helpers)
- [Updating to async step functions](\docs\sdk\migration#updating-to-async-step-functions)
- [Advanced: Updating custom framework serve handlers](\docs\sdk\migration#advanced-updating-custom-framework-serve-handlers-2)

References [TypeScript SDK](\docs\reference\typescript) [Using the SDK](\docs\sdk\environment-variables)

# Upgrading from Inngest SDK v2 to v3

This guide walks through migrating your code from v2 to v3 of the Inngest TS SDK.

Upgrading from an earlier version? See further down the page:

- [Upgrading from v1 to v2](\docs\sdk\migration#breaking-changes-in-v2)
- [Upgrading from v0 to v1](\docs\sdk\migration#migrating-from-inngest-sdk-v0-to-v1)

## [Breaking changes in v3](\docs\sdk\migration#breaking-changes-in-v3)

Listed below are all breaking changes made in v3, potentially requiring code changes for you to upgrade.

- [Clients and functions now require IDs](\docs\sdk\migration#clients-and-functions-require-ids)
- [Steps now require IDs](\docs\sdk\migration#all-steps-require-ids)
- [Refactored serve handlers](\docs\sdk\migration#serve-handlers-refactored)
- [Removed shorthand function creation](\docs\sdk\migration#shorthand-function-creation-removed)
- [Refactored environment variables and config](\docs\sdk\migration#environment-variables-and-configuration)
- [Advanced: Updating custom framework serve handlers](\docs\sdk\migration#advanced-updating-custom-framework-serve-handlers)
- [Removed](\docs\sdk\migration#fns-removed) [`fns`](\docs\sdk\migration#fns-removed) [option](\docs\sdk\migration#fns-removed)

## [Removing the guard rails](\docs\sdk\migration#removing-the-guard-rails)

Aside from some of the breaking changes above, this version also some new features.

- **Versioning and state recovery** - Functions can change over time and even mid-run; our new engine will recover and adapt, even for functions running across huge timespans.
- **Allow mixing step and async logic** - Top-level `await` alongside steps is now supported within Inngest functions, allowing easier reuse of logic and complex use cases like dynamic imports.
- **Sending events returns IDs** - Sending an event now returns the event ID that has created.

See [Introducing Inngest TypeScript SDK v3.0](\blog\releasing-ts-sdk-3?ref=migration) to see what these features unlock for the future of the TS SDK.

## [A simple example](\docs\sdk\migration#a-simple-example)

The surface-level changes for v3 and mostly small syntactical changes, which TypeScript should be able to guide you through.

Here's a quick view of transitioning a client, function, and serve handler to v3.

When migrating, you'll want your ID to stay the same to ensure that in-progress runs switch over smoothly. We export a `slugify()` function you can use to generate an ID from your existing name as we used to do internally.

Copy Copied

```
import { slugify } from "inngest" ;

const fn = inngest .createFunction (
{ id : slugify ( "Onboarding Example" ) , name : "Onboarding Example" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {
// ...
}
);
```

This is only needed to ensure function runs started on v2 will transition to v3; new functions can specify any ID.

⚠️ `slugify()` **should only be applied to function IDs, not application IDs** . Changing the application ID will result new app, archiving the existing one.

### ✅ v3

Copy Copied

```
import { Inngest , slugify } from "inngest" ;
import { serve } from "inngest/next" ;

const inngest = new Inngest ({
id : "My App" ,
});

const fn = inngest .createFunction (
// NOTE: You can manually slug IDs or import slugify to convert names to IDs automatically.
// { id: "onboarding-example", name: "Onboarding example" },
{ id : slugify ( "Onboarding example" ) , name : "Onboarding example" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {
await step .run ( "send-welcome-email" , () =>
sendEmail ( event . user .email , "Welcome!" )
);

const profileCompleted = await step .waitForEvent (
"wait-for-profile-completion" ,
{
event : "app/user.profile.completed" ,
timeout : "1d" ,
match : "data.userId" ,
}
);

await step .sleep ( "wait-a-moment" , "5m" );

if ( ! profileCompleted) {
await step .run ( "send-profile-reminder" , () =>
sendEmail ( event . user .email , "Complete your profile!" )
);
}
}
);

export default serve ({
client : inngest ,
functions : [fn] ,
});
```

### 🛑 v2

Copy Copied

```
import { Inngest } from "inngest" ;
import { serve } from "inngest/next" ;

// Clients only previously required a `name`, but we want to be
// explicit that this is used to identify your application and manage
// concepts such as deployments.
const inngest = new Inngest ({ name : "My App" });

const fn = inngest .createFunction (
// Similarly, functions now require an `id` and `name` is optional.
{ name : "Onboarding Example" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {
// `step.run()` stays the same.
await step .run ( "send-welcome-email" , () =>
sendEmail ( event . user .email , "Welcome!" )
);

// The shape of `waitForEvent` has changed; all steps now require
// an ID.
const profileCompleted = await step .waitForEvent (
"app/user.profile.completed" ,
{
timeout : "1d" ,
match : "data.userId" ,
}
);

// All steps, even sleeps, require IDs.
await step .sleep ( "5m" );

if ( ! profileCompleted) {
await step .run ( "send-profile-reminder" , () =>
sendEmail ( event . user .email , "Complete your profile!" )
);
}
}
);

// Serving now uses a single object parameter for better readability.
export default serve (inngest , [fn]);
```

If during migration your function ID is not the same, you'll see duplicated functions in your function list. In that case, the recommended approach is to archive the old function using the dashboard.

## [Clients and functions require IDs](\docs\sdk\migration#clients-and-functions-require-ids)

When instantiating a client using `new Inngest()` or creating a function via `inngest.createFunction()` , it's now required to pass an `id` instead of a `name` . We recommend changing the property name and wrapping the value in `slugify()` to ensure you don't redeploy any functions.

### [Creating a client](\docs\sdk\migration#creating-a-client)

### ✅ v3

Copy Copied

```
import { Inngest } from "inngest" ;

export const inngest = new Inngest ({
id : "My App" ,
});
```

### 🛑 v2

Copy Copied

```
import { Inngest } from "inngest" ;

export const inngest = new Inngest ({
name : "My App" ,
});
```

### [Creating a function](\docs\sdk\migration#creating-a-function)

### ✅ v3

Copy Copied

```
inngest .createFunction (
{ id : "send-welcome-email" , name : "Send welcome email" } ,
{ event : "app/user.created" } ,
async ({ event }) => {
// ...
}
);
```

### 🛑 v2

Copy Copied

```
inngest .createFunction (
{ name : "Send welcome email" } ,
{ event : "app/user.created" } ,
async ({ event }) => {
// ...
}
);
```

Previously, only `name` was required, but this implied that the value was safe to change. Internally, we used this name to produce an ID which was used during deployments and executions.

## [All steps require IDs](\docs\sdk\migration#all-steps-require-ids)

When using any `step.*` tool, an ID is now required to ensure that determinism across changes to a function is easier to reason about for the user and the underlying engine.

The addition of these IDs allows you to deploy hotfixes and logic changes to long-running functions without fear of errors, failures, or panics. Beforehand, any changes to a function resulted in an irrecoverable error if step definitions changed. With this, changes to a function are smartly applied by default.

Every step tool now takes a new option, `StepOptionsOrId` , as its first argument. Either a `string` , indicating the ID for that step, or an object that can also include a friendly `name` .

Copy Copied

```
type StepOptionsOrId =
| string
| {
id : string ;
name ?: string ;
};
```

### [step.run()](\docs\sdk\migration#step-run)

This tool shouldn't require any changes. We'd still recommend changing the ID to something that's more obviously an identifier, like `send-welcome-email` , but you should wait for all existing v2 runs to complete before doing so.

See [Handling in-progress runs triggered from v2](\docs\sdk\migration#handling-in-progress-runs-triggered-from-v2) for more information.

### [step.sendEvent()](\docs\sdk\migration#step-send-event)

### ✅ v3

Copy Copied

```
step .sendEvent ( "broadcast-user-creation" , {
name : "app/user.created" ,
data : {
/* ... */
} ,
});
```

### 🛑 v2

Copy Copied

```
step .sendEvent ({
name : "app/user.created" ,
data : {
/* ... */
} ,
});
```

### [step.sleep()](\docs\sdk\migration#step-sleep)

### ✅ v3

Copy Copied

```
step .sleep ( "wait-before-poll" , "1m" );
```

### 🛑 v2

Copy Copied

```
step .sleep ( "1m" );
```

### [step.sleepUntil()](\docs\sdk\migration#step-sleep-until)

### ✅ v3

Copy Copied

```
step .sleepUntil ( "wait-for-user-birthday" , specialDate);
```

### 🛑 v2

Copy Copied

```
step .sleepUntil (specialDate);
```

### [step.waitForEvent()](\docs\sdk\migration#step-wait-for-event)

### ✅ v3

Copy Copied

```
step .waitForEvent ( "wait-for-user-login" , {
event : " app/user.login" ,
timeout : "1h " ,
});
```

### 🛑 v2

Copy Copied

```
step .waitForEvent ( "app/user.login" , {
timeout : "1h " ,
});
```

## [Serve handlers refactored](\docs\sdk\migration#serve-handlers-refactored)

Serving functions could become a bit unwieldy with the format we had, so we've slightly altered how you serve your functions to ensure proper discoverability of options and aid in readability when revisiting the code.

In v2, `serve()` would always return `any` , to ensure compatibility with any version of any framework. If you're experiencing issues, you can return to this - though we don't recommend it - by using a type assertion such as `serve() as any` .

Also see the [Environment variables and config](\docs\sdk\migration#environment-variables-and-configuration) section.

### ✅ v3

Copy Copied

```
import { serve } from "inngest/next" ;
import { inngest , functions } from "~/inngest" ;

export default serve ({
client : inngest ,
functions ,
// ...options
});
```

### 🛑 v2

Copy Copied

```
import { serve } from "inngest/next" ;
import { inngest , functions } from "~/inngest" ;

export default serve (inngest , functions , {
// ...options
});
```

## [Shorthand function creation removed](\docs\sdk\migration#shorthand-function-creation-removed)

`inngest.createFunction()` can no longer take a `string` as the first or second arguments; an object is now required to aid in the discoverability of options and configuration.

### ✅ v3

Copy Copied

```
inngest .createFunction (
{ id : "send-welcome-email" , name : "Send welcome email" } ,
{ event : "app/user.created" } ,
async () => {
// ...
}
);
```

### 🛑 v2

Copy Copied

```
inngest .createFunction (
"Send welcome email" ,
"app/user.created" ,
async () => {
// ...
}
);
```

## [Environment variables and configuration](\docs\sdk\migration#environment-variables-and-configuration)

The arrangement of environment variables available has shifted a lot over the course of v2, so in v3 we've streamlined what's available and how they're used.

We've refactored some environment variables for setting URLs for communicating with Inngest.

- **✅ Added** **`INNGEST_BASE_URL`** - Sets the URL to communicate with Inngest in one place, e.g. `http://localhost:8288` .
- **🛑 Removed** **`INNGEST_API_BASE_URL`** - Set `INNGEST_BASE_URL` instead.
- **🛑 Removed** **`INNGEST_DEVSERVER_URL`** - Set `INNGEST_BASE_URL` instead.

If you were using `INNGEST_DEVSERVER_URL` to test a production build against a local dev server, set `INNGEST_BASE_URL` to your dev server's address instead.

We've also added some new environment variables based on config options available when serving Inngest functions.

- **✅ Added** **`INNGEST_SERVE_HOST`** - Sets the `serveHost` serve option, e.g. `https://www.example.com` .
- **✅ Added** **`INNGEST_SERVE_PATH`** - Sets the `servePath` serve option, e.g. `/api/inngest` .
- **✅ Added** **`INNGEST_LOG_LEVEL`** - One of `"fatal" | "error" | "warn" | "info" | "debug" | "silent"` . Setting to `"debug"` will also set `DEBUG=inngest:*` .
- **✅ Added** **`INNGEST_STREAMING`** - One of `"allow" | "force" | "false"` .

Check out the [Environment variables](\docs\sdk\environment-variables?ref=migration) page for information on all current environment variables.

In this same vein, we've also refactored some configuration options when creating an Inngest client and serving functions.

- new Inngest()
    - **✅ Added** **`baseUrl`** - Sets the URL to communicate with Inngest in one place, e.g. `"http://localhost:8288"` . Synonymous with setting the `INNGEST_BASE_URL` environment variable above.
    - **🛑 Removed** **`inngestBaseUrl`** - Set `baseUrl` instead.
- serve()
    - **✅ Added** **`baseUrl`** - Sets the URL to communicate with Inngest in one place, e.g. `"http://localhost:8288"` . Synonymous with setting the `INNGEST_BASE_URL` environment variable above or using `baseUrl` when creating the client.
    - **🛑 Removed** **`inngestBaseUrl`** - Set `baseUrl` instead.
    - **🛑 Removed** **`landingPage`** - The landing page for the SDK was deprecated in v2. Use the Inngest Dev Server instead via `npx inngest-cli@latest dev` .

## [Handling in-progress runs triggered from v2](\docs\sdk\migration#handling-in-progress-runs-triggered-from-v2)

When upgrading to v3, there may be function runs in progress that were started using v2. For this reason, v3's engine changes are backwards compatible with v2 runs.

`step.run()` should require no changes from v2 to v3. To ensure runs are backwards-compatible, make sure to keep the ID the same while in-progress v2 runs complete.

## [Advanced: Updating custom framework serve handlers](\docs\sdk\migration#advanced-updating-custom-framework-serve-handlers)

We found that writing custom serve handlers could be a confusing experience, focusing heavily on Inngest concepts. With v3, we've changed these handlers to now focus almost exclusively on shared concepts around how to parse requests and send responses.

A handler is now defined by telling Inngest how to access certain pieces of the request and how to send a response. Handlers are also now correctly typed, meaning the output of `serve()` will be a function signature compatible with your framework.

See the simple handler below that uses the native `Request` and `Response` objects to see the comparison between v2 and v3.

As with custom handlers previously, check out our [custom framework handlers](\docs\learn\serving-inngest-functions#custom-frameworks?ref=migration) section to see how to define your own.

### ✅ v3

Copy Copied

```
export const serve = (options : ServeHandlerOptions ) => {
const handler = new InngestCommHandler ({
frameworkName ,
... options ,
handler : (req : Request ) => {
return {
body : () => req .json () ,
headers : (key) => req . headers .get (key) ,
method : () => req .method ,
url : () => new URL ( req .url , `https:// ${ req . headers .get ( "host" ) || "" } ` ) ,
transformResponse : ({ body , status , headers }) => {
return new Response (body , { status , headers });
} ,
};
} ,
});

return handler .createHandler ();
};
```

### 🛑 v2

Copy Copied

```
export const serve : ServeHandler = (inngest , fns , opts) => {
const handler = new InngestCommHandler (
name ,
inngest ,
fns ,
{
fetch : fetch .bind (globalThis) ,
... opts ,
} ,
(req : Request ) => {
const url = new URL ( req .url , `https:// ${ req . headers .get ( "host" ) || "" } ` );

return {
url ,
register : () => {
if ( req .method === "PUT" ) {
return {
deployId : url . searchParams .get ( queryKeys .DeployId) as string ,
};
}
} ,
run : async () => {
if ( req .method === "POST" ) {
return {
data : ( await req .json ()) as Record < string , unknown > ,
fnId : url . searchParams .get ( queryKeys .FnId) as string ,
stepId : url . searchParams .get ( queryKeys .StepId) as string ,
signature : req . headers .get ( headerKeys .Signature) as string ,
};
}
} ,
view : () => {
if ( req .method === "GET" ) {
return {
isIntrospection : url . searchParams .has ( queryKeys .Introspect) ,
};
}
} ,
};
} ,
({ body , status , headers }) : Response => {
return new Response (body , { status , headers });
}
);

return handler .createHandler ();
};
```

## [Function fns option removed](\docs\sdk\migration#function-fns-option-removed)

In v2, providing a `fns` option when creating a function -- an object of functions -- would wrap those passed functions in `step.run()` , meaning you can run code inside your function without the `step.run()` boilerplate.

This wasn't a very well advertised feature and had some drawbacks, so we're instead replacing it with some optional middleware.

Check out the [Common Actions Middleware Example](\docs\reference\middleware\examples#common-actions-for-every-function?ref=migration) for the code.

### ✅ v3

Copy Copied

```
import * as actions from "./actions" ;
import { createActionsMiddleware } from "./middleware" ;

const inngest = new Inngest ({
id : "my-app" ,
name : "My App" ,
middleware : [ createActionsMiddleware (actions)] ,
});

inngest .createFunction (
{ name : "Send welcome email" } ,
{ event : "app/user.created" } ,
async ({ event , action }) => {
const user = await action .getUserFromDb ( event . data .userId);
await action .sendWelcomeEmail ( user .email);
}
);
```

### 🛑 v2

Copy Copied

```
import * as actions from "./actions" ;

const inngest = new Inngest ({ name : "My App" });

inngest .createFunction (
{
name : "Send welcome email" ,
fns : actions ,
} ,
{ event : "app/user.created" } ,
async ({ event , fns }) => {
const user = await fns .getUserFromDb ( event . data .userId);
await fns .sendWelcomeEmail ( user .email);
}
);
```

# Upgrading from Inngest SDK v1 to v2

This guide walks through migrating your code from v1 to v2 of the Inngest TS SDK.

## [Breaking changes in v2](\docs\sdk\migration#breaking-changes-in-v2)

Listed below are all breaking changes made in v2, potentially requiring code changes for you to upgrade.

- New [Better event schemas](\docs\sdk\migration#better-event-schemas) - create and maintain your event types with a variety of native tools and third-party libraries
- [Clearer event sending](\docs\sdk\migration#clearer-event-sending) - we removed some alternate methods of sending events to settle on a common standard
- [Removed](\docs\sdk\migration#removed-tools-parameter) [`tools`](\docs\sdk\migration#removed-tools-parameter) [parameter](\docs\sdk\migration#removed-tools-parameter) - use `step` instead of `tools` for step functions
- [Removed ability to](\docs\sdk\migration#removed-ability-to-serve-without-a-client) [`serve()`](\docs\sdk\migration#removed-ability-to-serve-without-a-client) [without a client](\docs\sdk\migration#removed-ability-to-serve-without-a-client) - everything is specified with a client, so it makes sense for this to be the same
- [Renamed](\docs\sdk\migration#renamed-throttle-to-ratelimit) [`throttle`](\docs\sdk\migration#renamed-throttle-to-ratelimit) [to](\docs\sdk\migration#renamed-throttle-to-ratelimit) [`rateLimit`](\docs\sdk\migration#renamed-throttle-to-ratelimit) - the concept didn't quite match the naming

## [New features in v2](\docs\sdk\migration#new-features-in-v2)

Aside from some of the breaking features above, this version also adds some new features that aren't breaking changes.

- [Middleware](\docs\reference\middleware\overview?ref=migration) - specify functions to run at various points in an Inngest client's lifecycle
- **Logging** - use a default console logger or specify your own to log during your workflows

## [Better event schemas](\docs\sdk\migration#better-event-schemas)

Typing events is now done using a new `EventSchemas` class to create a guided, consistent, and extensible experience for declaring an event's data. This helps us achieve a few goals:

- Reduced duplication (no more `name` !)
- Allow many different methods of defining payloads to suit your codebase
- Easy to add support for third-party libraries like Zod and TypeBox
- Much clearer messaging when an event type doesn't satisfy what's required
- Allows the library to infer more data itself, which allows us to add even more powerful type inference

Copy Copied

```
// ❌ Invalid in v2
type Events = {
"app/user.created" : {
name : "app/user.created" ;
data : { id : string };
};
"app/user.deleted" : {
name : "app/user.deleted" ;
data : { id : string };
};
};

new Inngest < Events >();
```

Instead, in v2, we use a new `EventSchemas` class and its methods to show current event typing support clearly. All we have to do is create a `new EventSchemas()` instance and pass it into our `new Inngest()` instance.

Copy Copied

```
import { Inngest , EventSchemas } from "inngest" ;
//                ⬆️ New "EventSchemas" class

// ✅ Valid in v2 - `fromRecord()`
type Events = {
"app/user.created" : {
data : { id : string };
};
"app/user.deleted" : {
data : { id : string };
};
};

new Inngest ({
schemas : new EventSchemas () .fromRecord < Events >() ,
});
```

Notice we've reduced the duplication of `name` slightly too; a common annoyance we've been seeing for a while!

We use `fromRecord()` above to match the current event typing quite closely, but we now have some more options to define events without having to shim, like `fromUnion()` :

Copy Copied

```
// ✅ Valid in v2 - `fromUnion()`
type AppUserCreated = {
name : "app/user.created" ;
data : { id : string };
};

type AppUserDeleted = {
name : "app/user.deleted" ;
data : { id : string };
};

new EventSchemas () .fromUnion < AppUserCreated | AppUserDeleted >();
```

This approach also gives us scope to add explicit support for third-party libraries, like Zod:

Copy Copied

```
// ✅ Valid in v2 - `fromZod()`
const userDataSchema = z .object ({
id : z .string () ,
});

new EventSchemas () .fromZod ({
"app/user.created" : { data : userDataSchema } ,
"app/user.deleted" : { data : userDataSchema } ,
});
```

Stacking multiple event sources was technically supported in v1, but was a bit shaky. In v2, providing multiple event sources and optionally overriding previous ones is built in:

Copy Copied

```
// ✅ Valid in v2 - stacking
new EventSchemas ()
.fromRecord < Events >()
.fromUnion < Custom1 | Custom2 >()
.fromZod (zodEventSchemas);
```

Finally, we've added the ability to pull these built types out of Inngest for creating reusable logic without having to create an Inngest function. Inngest will append relevant fields and context to the events you input, so this is a great type to use for quickly understanding the resulting shape of data.

Copy Copied

```
import { Inngest , type GetEvents } from "inngest" ;

const inngest = new Inngest ({ name : "My App" });
type Events = GetEvents < typeof inngest>;
```

For more information, see [Defining Event Payload Types](\docs\reference\client\create#defining-event-payload-types?ref=migration) .

## [Clearer event sending](\docs\sdk\migration#clearer-event-sending)

v1 had two different methods of sending events that shared the same function. This "overload" resulted in autocomplete typing for TypeScript users appear more complex than it needed to be.

In addition, using a particular signature meant that you're locked in to sending a particular named event, meaning sending two different events in a batch required refactoring your call.

For these reasons, we've removed a couple of the event-sending signatures and settled on a single standard.

Copy Copied

```
// ❌ Invalid in v2
inngest .send ( "app/user.created" , { data : { userId : "123" } });
inngest .send ( "app/user.created" , [
{ data : { userId : "123" } } ,
{ data : { userId : "456" } } ,
]);

// ✅ Valid in v1 and v2
inngest .send ({ name : "app/user.created" , data : { userId : "123" } });
inngest .send ([
{ name : "app/user.created" , data : { userId : "123" } } ,
{ name : "app/user.created" , data : { userId : "456" } } ,
]);
```

## [Removed tools parameter](\docs\sdk\migration#removed-tools-parameter)

The `tools` parameter in a function was marked as deprecated in v1 and is now being fully removed in v2.

You can swap out `tools` with `step` in every case.

Copy Copied

```
inngest .createFunction (
{ name : "Example" } ,
{ event : "app/user.created" } ,
async ({ tools , step }) => {
// ❌ Invalid in v2
await tools .run ( "Foo" , () => {});

// ✅ Valid in v1 and v2
await step .run ( "Foo" , () => {});
}
);
```

## [Removed ability to serve() without a client](\docs\sdk\migration#removed-ability-to-serve-without-a-client)

In v1, serving Inngest functions could be done without a client via `serve("My App Name", ...)` . This limits our ability to do some clever TypeScript inference in places as we don't have access to the client that the functions have been created with.

We're shifting to ensure the client is the place where everything is defined and created, so we're removing the ability to `serve()` with a string name.

Copy Copied

```
// ❌ Invalid in v2
serve ( "My App" , [ ... fns]);

// ✅ Valid in v1 and v2
import { inngest } from "./client" ;
serve (inngest , [ ... fns]);
```

As is the case already in v1, the app's name will be the name of the client passed to serve. To preserve the ability to explicitly name a serve handler, you can now pass a `name` option when serving to use the passed string instead of the client's name.

Copy Copied

```
serve (inngest , [ ... fns] , {
name : "My Custom App Name" ,
});
```

## [Renamed throttle to rateLimit](\docs\sdk\migration#renamed-throttle-to-rate-limit)

Specifying a rate limit for a function in v1 meant specifying a `throttle` option when creating the function. The term "throttle" was confusing here, as the definition of throttling can change depending on the context, but usually implies that "throttled" events are still eventually used to trigger an event, which was not the case.

To be clearer about the functionality of this option, we're renaming it to `rateLimit` instead.

Copy Copied

```
inngest .createFunction (
{
name : "Example" ,
throttle : { count : 5 } , // ❌ Invalid in v2
rateLimit : { limit : 5 } , // ✅ Valid in v2
} ,
{ event : "app/user.created" } ,
async ({ tools , step }) => {
// ...
}
);
```

## [Migrating from Inngest SDK v0 to v1](\docs\sdk\migration#migrating-from-inngest-sdk-v0-to-v1)

This guide walks through migrating to the Inngest TS SDK v1 from previous versions.

## [What's new in v1](\docs\sdk\migration#what-s-new-in-v1)

- **Step functions and tools are now async** - create your flow however you'd express yourself with JavaScript Promises.
- **`inngest.createFunction`** **for everything** - all functions are now step functions; just use step tools within any function.
- **Unified client instantiation and handling of schemas via** **`new Inngest()`** - removed legacy helpers that required manual types.
- **A foundation for continuous improvement:**
    - Better type inference and schemas
    - Better error handling
    - Clearer patterns and tooling
    - Advanced function configuration

## [Replacing function creation helpers](\docs\sdk\migration#replacing-function-creation-helpers)

Creating any Inngest function now uses `inngest.createFunction()` to create a consistent experience.

- All helpers have been removed
- `inngest.createScheduledFunction()` has been removed
- `inngest.createStepFunction()` has been removed

Copy Copied

```
// ❌ Removed in v1
import {
createFunction ,
createScheduledFunction ,
createStepFunction ,
} from "inngest" ;

// ❌ Removed in v1
inngest .createScheduledFunction ( ... );
inngest .createStepFunction ( ... );
```

The following is how we would always create functions without the v0 helpers.

Copy Copied

```
// ✅ Valid in v1
import { Inngest } from "inngest" ;

// We recommend exporting this from ./src/inngest/client.ts, giving you a
// singleton across your entire app.
export const inngest = new Inngest ({ name : "My App" });

const singleStepFn = inngest .createFunction (
{ name : "Single step" } ,
{ event : "example/single.step" } ,
async ({ event , step }) => "..."
);

const scheduledFn = inngest .createFunction (
{ name : "Scheduled" } ,
{ cron : "0 9 * * MON" } ,
async ({ event , step }) => "..."
);

const stepFn = inngest .createFunction (
{ name : "Step function" } ,
{ event : "example/step.function" } ,
async ({ event , step }) => "..."
);
```

This helps ensure that important pieces such as type inference of events has a central place to reside.

As such, each of the following examples requries an Inngest Client ( `new Inngest()` ) is used to create the function.

Copy Copied

```
import { Inngest } from "inngest" ;

// We recommend exporting your client from a separate file so that it can be
// reused across the codebase.
export const inngest = new Inngest ({ name : "My App" });
```

See the specific examples below of how to transition from a helper to the new signatures.

```
createFunction()
```

Copy Copied

```
// ❌ Removed in v1
const singleStepFn = createFunction (
"Single step" ,
"example/single.step" ,
async ({ event }) => "..."
);
```

Copy Copied

```
// ✅ Valid in v1
const inngest = new Inngest ({ name : "My App" });

const singleStepFn = inngest .createFunction (
{ name : "Single step" } ,
{ event : "example/single.step" } ,
async ({ event , step }) => "..."
);
```

`createScheduledFunction()` or `inngest.createScheduledFunction()`

Copy Copied

```
// ❌ Removed in v1
const scheduledFn = createScheduledFunction ( // or inngest.createScheduledFunction
"Scheduled" ,
"0 9 * * MON" ,
async ({ event }) => "..."
);
```

Copy Copied

```
// ✅ Valid in v1
const inngest = new Inngest ({ name : "My App" });

const scheduledFn = inngest .createFunction (
{ name : "Scheduled" } ,
{ cron : "0 9 * * MON" } ,
async ({ event , step }) => "..."
);
```

`createStepFunction` or `inngest.createStepFunction`

Copy Copied

```
// ❌ Removed in v1
const stepFn = createStepFunction (
"Step function" ,
"example/step.function" ,
({ event , tools }) => "..."
);
```

Copy Copied

```
// ✅ Valid in v1
const inngest = new Inngest ({ name : "My App" });

const stepFn = inngest .createFunction (
{ name : "Step function" } ,
{ event : "example/step.function" } ,
async ({ event , step }) => "..."
);
```

## [Updating to async step functions](\docs\sdk\migration#updating-to-async-step-functions)

The signature of a step function is changing.

- **`tools`** **is now** **`step`** - We renamed this to be easier to reason about billing and make the code more readable.
- **Always** **`async`** - Every Inngest function is now an async function with access to async `step` tooling.
- **Steps now return promises** - To align with the async patterns that developers are used to and to enable more flexibility, make sure to `await` steps.

Step functions in v0 were synchronous, meaning steps had to run sequentially, one after the other.

v1 brings the full power of asynchronous JavaScript to those functions, meaning you can use any and all async tooling at your disposal; `Promise.all()` , `Promise.race()` , loops, etc.

Copy Copied

```
await Promise .all ([
step .run ( "Send email" , () => sendEmail ( user .email , "Welcome!" )) ,
step .run ( "Send alert to staff" , () => sendAlert ( "New user created!" )) ,
]);
```

Here we look at an example of a step function in v0 and compare it with the new v1.

Copy Copied

```
// ⚠️ v0 step function
import { createStepFunction } from "inngest" ;
import { getUser } from "./db" ;
import { sendAlert , sendEmail } from "./email" ;

export default createStepFunction (
"Example" ,
"app/user.created" ,
({ event , tools }) => {
const user = tools .run ( "Get user email" , () => getUser ( event .userId));

tools .run ( "Send email" , () => sendEmail ( user .email , "Welcome!" ));
tools .run ( "Send alert to staff" , () => sendAlert ( "New user created!" ));
}
);
```

Copy Copied

```
// ✅ v1 step function
import { inngest } from "./client" ;
import { getUser } from "./db" ;
import { sendAlert , sendEmail } from "./email" ;

export default inngest .createFunction (
{ name : "Example" } ,
{ event : "app/user.created" } ,
async ({ event , step }) => {
// The step must now be awaited!
const user = await step .run ( "Get user email" , () => getUser ( event .userId));

await step .run ( "Send email" , () => sendEmail ( user .email , "Welcome!" ));
await step .run ( "Send alert to staff" , () => sendAlert ( "New user created!" ));
}
);
```

These two examples have the exact same functionality. As above, there are a few key changes that were required.

- Using `createFunction()` on the client to create the step function
- Awaiting step tooling to ensure they run in order
- Using `step` instead of `tools`

When translating code to v1, be aware that not awaiting a step tool will mean it happens in the background, in parallel to the tools that follow. Just like a regular JavaScript async function, `await` halts progress, which is sometimes just what you want!

Async step functions with v1 of the Inngest TS SDK unlocks a huge `Array<Possibility>` . To explore these further, check out the [multi-step functions](\docs\guides\multi-step-functions?ref=migration) docs.

## [Advanced: Updating custom framework serve handlers](\docs\sdk\migration#advanced-updating-custom-framework-serve-handlers-2)

If you're using a custom serve handler and are creating your own `InngestCommHandler` instance, a `stepId` must be provided when returning arguments for the `run` command.

This can be accessed via the query string using the exported `queryKeys.StepId` enum.

Copy Copied

```
run : async () => {
if ( req .method === "POST" ) {
return {
fnId : url . searchParams .get ( queryKeys .FnId) as string ,
// 🆕 stepId is now required
stepId : url . searchParams .get ( queryKeys .StepId) as string ,
```