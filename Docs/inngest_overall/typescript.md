#### On this page

- [TypeScript](\docs\typescript#type-script)
- [Using types](\docs\typescript#using-types)
- [new Inngest() client](\docs\typescript#new-inngest-client)
- [Sending events](\docs\typescript#sending-events)
- [Using with waitForEvent](\docs\typescript#using-with-wait-for-event)
- [Helpers](\docs\typescript#helpers)
- [GetEvents](\docs\typescript#get-events)
- [GetFunctionInput](\docs\typescript#get-function-input)
- [GetStepTools](\docs\typescript#get-step-tools)
- [Inngest.Any / InngestFunction.Any](\docs\typescript#inngest-any-inngest-function-any)

References [TypeScript SDK](\docs\reference\typescript) [Using the SDK](\docs\sdk\environment-variables)

# TypeScript

The Inngest SDK leverages the full power of TypeScript, providing you with some awesome benefits when handling events:

- 📑 **Autocomplete** `Tab ↹` your way to victory with inferred types for every event.
- **Instant feedback** Understand exactly where your code might error before you even save the file.

All of this comes together to provide some awesome type inference based on your actual production data.

## [Using types](\docs\typescript#using-types)

Once your types are generated, there are a few ways we can use them to ensure our functions are protected.

### [new Inngest() client](\docs\typescript#new-inngest-client)

We can use these when creating a new Inngest client via `new Inngest()` .

This comes with powerful inference; we autocomplete your event names when selecting what to react to, without you having to dig for the name and data.

### inngest/client.ts

v3 v2

Copy Copied

```
import { EventSchemas , Inngest } from "inngest" ;

type UserSignup = {
data : {
email : string ;
name : string ;
};
};
type Events = {
"user/new.signup" : UserSignup ;
};

export const inngest = new Inngest ({
id : "my-app" ,
schemas : new EventSchemas () .fromRecord < Events >() ,
});
```

### inngest/sendWelcomeEmail.ts

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction (
{ id : "send-welcome-email" } ,
{ event : "user/new.signup" } ,
async ({ event }) => {
// "event" is fully typed to provide typesafety within this function
return await email .send ( "welcome" , event . data .email);
}
);
```

### [Sending events](\docs\typescript#sending-events)

TypeScript will also enforce your custom events being the right shape - see [Event Format](\docs\reference\events\send) for more details.

We recommend putting your `new Inngest()` client and types in a single file, i.e. `/inngest/client.ts` so you can use it anywhere that you send an event.

Here's an example of sending an event within a Next.js API handler:

### pages/api/signup.ts

Copy Copied

```
import type { NextApiRequest , NextApiResponse } from "next" ;
import { inngest } from "../../inngest/client" ;

export default function handler (req : NextApiRequest , res : NextApiResponse ) {
const user = createNewUser ( req . body .email , req . body .password , req . body .name);

// TypeScript will now warn you if types do not match for the event payload
// and the user object's properties:
await inngest .send ({
name : "user/new.signup" ,
data : {
email : user .email ,
name : user .name ,
}
});
res .status ( 200 ) .json ({ success : true });
}
```

### [Using with waitForEvent](\docs\typescript#using-with-wait-for-event)

When writing step functions, you can use `waitForEvent` to pause the current function until another event is received or the timeout expires - whichever happens first. When you declare your types using the `Inngest` constructor, `waitForEvent` leverages any types that you have:

### inngest/client.ts

v3 v2

Copy Copied

```
import { EventSchemas , Inngest } from "inngest" ;

type UserSignup = {
data : {
email : string ;
user_id : string ;
name : string ;
};
};
type UserAccountSetupCompleted = {
data : {
user_id : string ;
};
};
type Events = {
"user/new.signup" : UserSignup ;
"user/account.setup.completed" : UserAccountSetupCompleted ;
};

export const inngest = new Inngest ({
id : "my-app" ,
schemas : new EventSchemas () .fromRecord < Events >() ,
});
```

### inngest/onboardingDripCampaign.ts

v3 v2

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction (
{ id : "onboarding-drip-campaign" } ,
{ event : "user/new.signup" } ,
async ({ event , step }) => {
await step .run ( "send-welcome-email" , async () => {
// "event" will be fully typed provide typesafety within this function
return await email .send ( "welcome" , event . data .email);
});

// We wait up to 2 days for the user to set up their account
const accountSetupCompleted = await step .waitForEvent (
"wait-for-setup-complete" ,
{
event : "user/account.setup.completed" ,
timeout : "2d" ,
// ⬇️ This matches both events using the same property
// Since both events types are registered above, this is match is typesafe
match : "data.user_id" ,
}
);

if ( ! accountSetupCompleted) {
await step .run ( "send-setup-account-guide" , async () => {
return await email .send ( "account_setup_guide" , event . data .email);
});
}
}
);
```

## [Helpers](\docs\typescript#helpers)

The TS SDK exports some helper types to allow you to access the type of particular Inngest internals outside of an Inngest function.

### [GetEvents v2.0.0+](\docs\typescript#get-events)

Get a record of all available events given an Inngest client.

It's recommended to use this instead of directly reusing your own event types, as Inngest will add extra properties and internal events such as `ts` and `inngest/function.failed` .

Copy Copied

```
import { type GetEvents } from "inngest" ;
import { inngest } from "@/inngest" ;

type Events = GetEvents < typeof inngest>;
```

By default, the returned events do not include internal events prefixed with `inngest/` , such as `inngest/function.finished` .

To include these events in v3.13.1+ , pass a second `true` generic:

Copy Copied

```
type Events = GetEvents < typeof inngest , true >;
```

### [GetFunctionInput v3.3.0+](\docs\typescript#get-function-input)

Get the argument passed to Inngest functions given an Inngest client and, optionally, an event trigger.

Useful for building function factories or other such abstractions.

Copy Copied

```
import { type GetFunctionInput } from "inngest" ;
import { inngest } from "@/inngest" ;

type InputArg = GetFunctionInput < typeof inngest>;
type InputArgWithTrigger = GetFunctionInput < typeof inngest , "app/user.created" >;
```

### [GetStepTools v3.3.0+](\docs\typescript#get-step-tools)

Get the `step` object passed to an Inngest function given an Inngest client and, optionally, an event trigger.

Is a small shim over the top of `GetFunctionInput<...>["step"]` .

Copy Copied

```
import { type GetStepTools } from "inngest" ;
import { inngest } from "@/inngest" ;

type StepTools = GetStepTools < typeof inngest>;
type StepToolsWithTrigger = GetStepTools < typeof inngest , "app/user.created" >;
```

### [Inngest.Any / InngestFunction.Any v3.10.0+](\docs\typescript#inngest-any-inngest-function-any)

Some exported classes have an `Any` type within their namespace that represents any instance of that class without inference or generics.

This is useful for typing lists of functions or factories that create Inngest primitives.

Copy Copied

```
import { type InngestFunction } from "inngest" ;

const functionsToServe : InngestFunction . Any [] = [];
```