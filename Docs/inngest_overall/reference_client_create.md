#### On this page

- [Create the Inngest Client](\docs\reference\client\create#create-the-inngest-client)
- [Configuration](\docs\reference\client\create#configuration)
- [Defining Event Payload Types](\docs\reference\client\create#defining-event-payload-types)
- [Reusing event types](\docs\reference\client\create#reusing-event-types)
- [Cloud Mode and Dev Mode](\docs\reference\client\create#cloud-mode-and-dev-mode)
- [Best Practices](\docs\reference\client\create#best-practices)
- [Share your client across your codebase](\docs\reference\client\create#share-your-client-across-your-codebase)
- [Handling multiple environments with middleware](\docs\reference\client\create#handling-multiple-environments-with-middleware)

References [TypeScript SDK](\docs\reference\typescript)

# Create the Inngest Client

The `Inngest` client object is used to configure your application, enabling you to create functions and send events.

v3 v2

Copy Copied

```
import { Inngest } from "inngest" ;

const inngest = new Inngest ({
id : "my-application" ,
});
```

## [Configuration](\docs\reference\client\create#configuration)

- Name `id` Type string Required required Description A unique identifier for your application. We recommend a hyphenated slug.
- Name `baseUrl` Type string Required optional Description Override the default ( `https://inn.gs/` ) base URL for sending events. See also the [`INNGEST_BASE_URL`](\docs\sdk\environment-variables#inngest-base-url) environment variable.
- Name `env` Type string Required optional Description The environment name. Required only when using [Branch Environments](\docs\platform\environments) .
- Name `eventKey` Type string Required optional Description An Inngest [Event Key](\docs\events\creating-an-event-key) . Alternatively, set the [`INNGEST_EVENT_KEY`](\docs\sdk\environment-variables#inngest-event-key) environment variable.
- Name `fetch` Type Fetch API compatible interface Required optional Description Override the default [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) implementation. Defaults to the runtime's native Fetch API. If you need to specify this, make sure that you preserve the function's [binding](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_objects/Function/bind) , either by using `.bind` or by wrapping it in an anonymous function.
- Name `isDev` Type boolean Required optional Version v3.15.0+ Description Set to `true` to force Dev mode, setting default local URLs and turning off signature verification, or force Cloud mode with `false` . Alternatively, set [`INNGEST_DEV`](\docs\sdk\environment-variables#inngest-dev) .
- Name `logger` Type Logger Required optional Version v2.0.0+ Description A logger object that provides the following interfaces ( `.info()` , `.warn()` , `.error()` , `.debug()` ). Defaults to using `console` if not provided. Overwrites [`INNGEST_LOG_LEVEL`](\docs\sdk\environment-variables#inngest-log-level) if set. See [logging guide](\docs\guides\logging) for more details.
- Name `middleware` Type array Required optional Version v2.0.0+ Description A stack of [middleware](\docs\reference\middleware\overview) to add to the client.
- Name `schemas` Type EventSchemas Required optional Version v2.0.0+ Description Event payload types. See [Defining Event Payload Types](\docs\reference\client\create#defining-event-payload-types) .

We recommend setting the [`INNGEST_EVENT_KEY`](\docs\sdk\environment-variables#inngest-event-key) as an environment variable over using the `eventKey` option. As with any secret, it's not a good practice to hard-code the event key in your codebase.

## [Defining Event Payload Types](\docs\reference\client\create#defining-event-payload-types)

You can leverage TypeScript, Zod, Valibot, or any schema library that

implements the

[Standard Schema interface](https://standardschema.dev/) to define

your event payload types.

When you pass types to the Inngest client,

events are fully typed when using them with

`inngest.send()` and `inngest.createFunction()` . This can more easily alert you to issues with your

code during compile time.

Click the toggles on the top left of the code block to see the different methods available!

Standard Schema Union Record Stacking

Copy Copied

```
import { EventSchemas , Inngest } from "inngest" ;
import { z } from "zod" ;

export const inngest = new Inngest ({
schemas : new EventSchemas () .fromSchema ({
"app/account.created" : z .object ({
userId : z .string () ,
}) ,
"app/subscription.started" : z .object ({
userId : z .string () ,
planId : z .string () ,
}) ,
}) ,
});
```

### [Reusing event types v2.0.0+](\docs\reference\client\create#reusing-event-types)

You can use the `GetEvents<>` generic to access the final event types from an Inngest client.

It's recommended to use this instead of directly reusing your event types, as Inngest will add extra properties and internal events such as `ts` and `inngest/function.failed` .

Copy Copied

```
import { EventSchemas , Inngest , type GetEvents } from "inngest" ;

export const inngest = new Inngest ({
schemas : new EventSchemas () .fromRecord <{
"app/user.created" : { data : { userId : string } };
}>() ,
});

type Events = GetEvents < typeof inngest>;
type AppUserCreated = Events [ "app/user.created" ];
```

For more information on this and other TypeScript helpers, see [TypeScript -](\docs\typescript#helpers)

[Helpers](\docs\typescript#helpers)

.

## [Cloud Mode and Dev Mode](\docs\reference\client\create#cloud-mode-and-dev-mode)

An SDK can run in two separate "modes:" **Cloud** or **Dev** .

- **Cloud Mode**
    - 🔒 Signature verification **ON**
    - Defaults to communicating with Inngest Cloud (e.g. `https://api.inngest.com` )
- **Dev Mode**
    - ❌ Signature verification **OFF**
    - Defaults to communicating with an Inngest Dev Server (e.g. `http://localhost:8288` )

You can force either Dev or Cloud Mode by setting [`INNGEST_DEV`](\docs\sdk\environment-variables#inngest-dev) or the [`isDev`](\docs\reference\client\create#configuration) option.

If neither is set, the SDK will attempt to infer which mode it should be in

based on environment variables such as

`NODE_ENV` . Most of the time, this inference is all you need and explicitly setting a mode

isn't required.

## [Best Practices](\docs\reference\client\create#best-practices)

### [Share your client across your codebase](\docs\reference\client\create#share-your-client-across-your-codebase)

Instantiating the `Inngest` client in a single file and sharing it across your codebase is ideal as you only need a single place to configure your client and define types which can be leveraged anywhere you send events or create functions.

### ./inngest/client.ts

v3 v2

Copy Copied

```
import { Inngest } from "inngest" ;

export const inngest = new Inngest ({ id : "my-app" });
```

### ./inngest/myFunction.ts

Copy Copied

```
import { inngest } from "./client" ;

export default inngest .createFunction ( ... );
```

### [Handling multiple environments with middleware](\docs\reference\client\create#handling-multiple-environments-with-middleware)

If your client uses middleware, that middleware may import dependencies that are not supported across multiple environments such as "Edge" and "Serverless" (commonly with either access to WebAPIs or Node).

In this case, we'd recommend creating a separate client for each environment, ensuring Node-compatible middleware is only used in Node-compatible environments and vice versa.

This need is common in places where function execution should declare more involved middleware, while sending events from the edge often requires much less.

### ./inngest/client.ts

v3 v2

Copy Copied

```
// inngest/client.ts
import { Inngest } from "inngest" ;
import { nodeMiddleware } from "some-node-middleware" ;

export const inngest = new Inngest ({
id : "my-app" ,
middleware : [nodeMiddleware] ,
});

// inngest/edgeClient.ts
import { Inngest } from "inngest" ;

export const inngest = new Inngest ({
id : "my-app-edge" ,
});
```

Also see [Referencing functions](\docs\functions\references) , which can help you invoke functions across these environments without pulling in any dependencies.