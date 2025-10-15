# Setting up your Inngest app

With Inngest, you define functions or workflows using the SDK and deploy them to whatever platform or cloud provider you want including including serverless and container runtimes.

For Inngest to remotely execute your functions, you will need to set up a connection between your app and Inngest. This can be done in one of two ways:

## [serve()](#serving-inngest-functions)

[Serve your Inngest functions by creating an HTTP endpoint in your application.](#serving-inngest-functions)

[**Ideal for**](#serving-inngest-functions) [:](#serving-inngest-functions)

- [Serverless platforms like Vercel, Lambda, etc.](#serving-inngest-functions)
- [Adding Inngest to an existing API.](#serving-inngest-functions)
- [Zero changes to your CI/CD pipeline](#serving-inngest-functions)

## [connect()](\docs\setup\connect)

[Connect to Inngest's servers using out-bound WebSocket connection.](\docs\setup\connect)

[**Ideal for**](\docs\setup\connect) [:](\docs\setup\connect)

- [Container runtimes (Kubernetes, Docker, etc.)](\docs\setup\connect)
- [Latency sensitive applications](\docs\setup\connect)
- [Horizontal scaling with workers](\docs\setup\connect)

Inngest functions are portable, so you can migrate between `serve()` and `connect()` as well as cloud providers.

## [Serving Inngest functions](\docs\learn\serving-inngest-functions#serving-inngest-functions)

TypeScript Go Python

Inngest provides a `serve()` handler which adds an API endpoint to your router. You expose your functions to Inngest through this HTTP endpoint. To make automated deploys much easier, **the endpoint needs to be defined at** **`/api/inngest`** (though you can [change the API path](\docs\reference\serve#serve-client-functions-options) ).

### ./api/inngest.ts

Copy Copied

```
// All serve handlers have the same arguments:
serve ({
client : inngest , // a client created with new Inngest()
functions : [fnA , fnB] , // an array of Inngest functions to serve, created with inngest.createFunction()
/* Optional extra configuration */
});
```

## [Supported frameworks and platforms](\docs\learn\serving-inngest-functions#supported-frameworks-and-platforms)

- [Astro](\docs\learn\serving-inngest-functions#framework-astro)
- [AWS Lambda](\docs\learn\serving-inngest-functions#framework-aws-lambda)
- [Bun](\docs\learn\serving-inngest-functions#bun-serve)
- [Cloudflare Pages](\docs\learn\serving-inngest-functions#framework-cloudflare-pages-functions)
- [Cloudflare Workers](\docs\learn\serving-inngest-functions#framework-cloudflare-workers)
- [DigitalOcean Functions](\docs\learn\serving-inngest-functions#framework-digital-ocean-functions)
- [ElysiaJS](\docs\learn\serving-inngest-functions#framework-elysia-js)
- [Express](\docs\learn\serving-inngest-functions#framework-express)

- [Fastify](\docs\learn\serving-inngest-functions#framework-fastify)
- [Fresh (Deno)](\docs\learn\serving-inngest-functions#framework-fresh-deno)
- [Google Cloud Run Functions](\docs\learn\serving-inngest-functions#framework-google-cloud-run-functions)
- [Firebase Cloud functions](\docs\learn\serving-inngest-functions#framework-firebase-cloud-functions)
- [H3](\docs\learn\serving-inngest-functions#framework-h3)
- [Hono](\docs\learn\serving-inngest-functions#framework-hono)
- [Koa](\docs\learn\serving-inngest-functions#framework-koa)
- [NestJS](\docs\learn\serving-inngest-functions#framework-nest-js)

- [Next.js](\docs\learn\serving-inngest-functions#framework-next-js)
- [Nitro](\docs\learn\serving-inngest-functions#framework-nitro)
- [Nuxt](\docs\learn\serving-inngest-functions#framework-nuxt)
- [Redwood](\docs\learn\serving-inngest-functions#framework-redwood)
- [Remix](\docs\learn\serving-inngest-functions#framework-remix)
- [SvelteKit](\docs\learn\serving-inngest-functions#framework-svelte-kit)
- [Tanstack Start](\docs\learn\serving-inngest-functions#framework-tanstack-start)

You can also create a custom serve handler for any framework or platform not listed here - [read more here](\docs\learn\serving-inngest-functions#custom-frameworks) .

Want us to add support for another framework? Open an issue on [GitHub](https://github.com/inngest/website) or tell us about it on our [Discord](\discord) .

### [Framework: Astro v3.8.0+](\docs\learn\serving-inngest-functions#framework-astro)

Add the following to `./src/pages/api/inngest.ts` :

Copy Copied

```
import { serve } from "inngest/astro" ;
import { functions , inngest } from "../../inngest" ;

export const { GET , POST , PUT } = serve ({
client : inngest ,
functions ,
});
```

See the [Astro example](https://github.com/inngest/inngest-js/tree/main/examples/framework-astro) for more information.

### [Framework: AWS Lambda v1.5.0+](\docs\learn\serving-inngest-functions#framework-aws-lambda)

We recommend using [Lambda function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html) to trigger your functions, as these require no other configuration or cost.

Alternatively, you can use an API Gateway to route requests to your Lambda. The handler supports [API Gateway V1](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html) and [API Gateway V2](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html) . If you are running API Gateway behind a proxy or have some other configuration, you may have to specify the `serveHost` and `servePath` options when calling `serve()` to ensure Inngest knows the URL where you are serving your functions. See [Configuring the API path](\docs\reference\serve#serve-client-functions-options) for more details.

v3 v2

Copy Copied

```
import { serve } from "inngest/lambda" ;
import { inngest } from "./client" ;
import fnA from "./fnA" ; // Your own function

export const handler = serve ({
client : inngest ,
functions : [fnA] ,
});
```

### [Bun.serve()](\docs\learn\serving-inngest-functions#bun-serve)

You can use the `inngest/bun` handler with `Bun.serve()` for a lightweight

Inngest server:

### index.ts

Copy Copied

```
import { serve } from "inngest/bun" ;
import { functions , inngest } from "./inngest" ;

Bun .serve ({
port : 3000 ,
routes : {
// ...other routes...
"/api/inngest" : (request : Request ) => {
return serve ({ client : inngest , functions })(request);
} ,
} ,
});
```

See the [Bun example](https://github.com/inngest/inngest-js/tree/main/examples/bun) for more information.

### [Framework: Cloudflare Pages Functions](\docs\learn\serving-inngest-functions#framework-cloudflare-pages-functions)

You can import the Inngest API server when using [Cloudflare pages functions](https://developers.cloudflare.com/pages/platform/functions/) within `/functions/api/inngest.js` :

v3 v2

Copy Copied

```
import { serve } from "inngest/cloudflare" ;
import { inngest } from "../../inngest/client" ;
import fnA from "../../inngest/fnA" ; // Your own function

export const onRequest = serve ({
client : inngest ,
functions : [fnA] ,
});
```

### [Framework: Cloudflare Workers v3.19.15+](\docs\learn\serving-inngest-functions#framework-cloudflare-workers)

You can export `"inngest/cloudflare"` 's `serve()` as your Cloudflare Worker:

Copy Copied

```
import { serve } from "inngest/cloudflare" ;
import { inngest } from "./client" ;
import fnA from "./fnA" ;

export default {
fetch : serve ({
client : inngest ,
functions : [fnA] ,
// We suggest explicitly defining the path to serve Inngest functions
servePath : "/api/inngest" ,
}) ,
};
```

To automatically pass environment variables defined with Wrangler to Inngest function handlers, use the [Cloudflare Workers bindings middleware](\docs\examples\middleware\cloudflare-workers-environment-variables) .

### [Local development with Wrangler](\docs\learn\serving-inngest-functions#local-development-with-wrangler)

When developing locally with Wrangler and the `--remote` flag, your code is

deployed and run remotely. To use this with a local Inngest Dev Server, you must

use a tool such as

[ngrok](https://ngrok.com/) or [localtunnel](https://theboroer.github.io/localtunnel-www/) to allow access to

the Dev Server from the internet.

Copy Copied

```
ngrok http 8288
```

### wrangler.toml

Copy Copied

```
[vars]
# The URL of your tunnel. This enables the "cloud" worker to access the local Dev Server
INNGEST_DEV = "https://YOUR_TUNNEL_URL.ngrok.app"
# This may be needed:
# The URL of your local server. This enables the Dev Server to access the app at this local URL
# You may have to change this URL to match your local server if running on a different port.
# Without this, the "cloud" worker may attempt to redirect Inngest to the wrong URL.
INNGEST_SERVE_HOST = "http://localhost:8787"
```

See an example of this in the [Hono framework example on GitHub](https://github.com/inngest/inngest-js/tree/main/examples/framework-hono) .

### [Framework: DigitalOcean Functions](\docs\learn\serving-inngest-functions#framework-digital-ocean-functions)

The DigitalOcean serve function allows you to deploy Inngest to DigitalOcean serverless functions.

Because DigitalOcean does not provide the request URL in its function arguments, you

**must** include

the function URL and path when configuring your handler:

v3 v2

Copy Copied

```
import { serve } from "inngest/digitalocean" ;
import { inngest } from "./src/inngest/client" ;
import fnA from "./src/inngest/fnA" ; // Your own function

const main = serve ({
client : inngest ,
functions : [fnA] ,
// Your digitalocean hostname.  This is required otherwise your functions won't work.
serveHost : "https://faas-sfo3-your-url.doserverless.co" ,
// And your DO path, also required.
servePath : "/api/v1/web/fn-your-uuid/inngest" ,
});

// IMPORTANT: Makes the function available as a module in the project.
// This is required for any functions that require external dependencies.
module . exports .main = main;
```

Inngest functions can also be deployed to [DigitalOcean's App Platform or Droplets](\docs\deploy\digital-ocean) .

### [Framework: ElysiaJS](\docs\learn\serving-inngest-functions#framework-elysia-js)

For [deployment options](https://elysiajs.com/patterns/deploy.html) , Elysia can compile to a binary or to JavaScript, or you can deploy with Docker or Railway.

### src/index.ts

Copy Copied

```
import { Elysia } from "elysia" ;
import { serve } from "inngest/bun" ;
import { functions , inngest } from "./inngest" ;

const handler = serve ({
client : inngest ,
functions ,
});

const inngestHandler = new Elysia () .all ( "/api/inngest" , ({ request }) =>
handler (request)
);

// register the handler with Elysia
const app = new Elysia ()
.use (inngestHandler)
```

Elysia's `use` function expects a single argument. We make use of the `all` method for the inngest api route to handle the expected

methods and then get the request off of the context object passed to elysia handlers.

See the [ElysiaJS](https://github.com/inngest/inngest-js/tree/main/examples/framework-elysiajs)

[example](https://github.com/inngest/inngest-js/tree/main/examples/framework-elysiajs)

for more information.

### [Framework: Express](\docs\learn\serving-inngest-functions#framework-express)

You can serve Inngest functions within your existing Express app, deployed to any hosting provider

like Render, Fly, AWS, K8S, and others:

v3 v2

Copy Copied

```
import { serve } from "inngest/express" ;
import { inngest } from "./src/inngest/client" ;
import fnA from "./src/inngest/fnA" ; // Your own function

// Important:  ensure you add JSON middleware to process incoming JSON POST payloads.
app .use ( express .json ());
app .use (
// Expose the middleware on our recommended path at `/api/inngest`.
"/api/inngest" ,
serve ({ client : inngest , functions : [fnA] })
);
```

You must ensure you're using the `express.json()` middleware otherwise your functions won't be

executed.

**Note** - You may need to set [`express.json()`](https://expressjs.com/en/5x/api.html#express.json) ['s](https://expressjs.com/en/5x/api.html#express.json) [`limit`](https://expressjs.com/en/5x/api.html#express.json) [option](https://expressjs.com/en/5x/api.html#express.json) to something higher than the default `100kb` to support larger event payloads and function state.

See the [Express](https://github.com/inngest/inngest-js/tree/main/examples/framework-express)

[example](https://github.com/inngest/inngest-js/tree/main/examples/framework-express)

for more information.

### [Streaming v3.39.2+](\docs\learn\serving-inngest-functions#streaming)

Express can also stream responses back to Inngest, potentially allowing much

longer timeouts.

To enable this, set add the `streaming: "force"` option to your serve handler:

Copy Copied

```
const handler = serve ({
client : inngest ,
functions : [ ... fns] ,
streaming : "force" ,
});
```

For more information, check out the [Streaming](\docs\streaming) page.

### [Framework: Fastify v2.6.0+](\docs\learn\serving-inngest-functions#framework-fastify)

You can serve Inngest functions within your existing Fastify app.

We recommend using the exported `inngestFastify` plugin, though we also expose a generic `serve()` function if you'd like to manually create a route.

Plugin Custom route (v3) Custom route (v2)

Copy Copied

```
import Fastify from "fastify" ;
import { fastifyPlugin } from "inngest/fastify" ;
import { inngest , fnA } from "./inngest" ;

const fastify = Fastify ();

fastify .register (fastifyPlugin , {
client : inngest ,
functions : [fnA] ,
options : {} ,
});

fastify .listen ({ port : 3000 } , function (err , address) {
if (err) {
fastify . log .error (err);
process .exit ( 1 );
}
});
```

See the [Fastify example](https://github.com/inngest/inngest-js/tree/main/examples/framework-fastify) for more information.

### [Framework: Fresh (Deno)](\docs\learn\serving-inngest-functions#framework-fresh-deno)

Inngest works with Deno's [Fresh](https://fresh.deno.dev/)

[framework](https://fresh.deno.dev/)

via the `esm.sh` CDN.  Add the serve handler to `./api/inngest.ts` as follows:

v3 v2

Copy Copied

```
import { serve } from "https://esm.sh/inngest/deno/fresh" ;
import { inngest } from "./src/inngest/client.ts" ;
import fnA from "./src/inngest/fnA" ; // Your own function

export const handler = serve ({
client : inngest ,
functions : [fnA] ,
});
```

### [Framework: Google Cloud Run Functions](\docs\learn\serving-inngest-functions#framework-google-cloud-run-functions)

Google's [Functions Framework](https://github.com/GoogleCloudPlatform/functions-framework-nodejs) has an Express-compatible API which enables you to use the Express serve handler to deploy your Inngest functions to Google Cloud Run. This is an example of a function:

v3 v2

Copy Copied

```
import * as ff from "@google-cloud/functions-framework" ;
import { serve } from "inngest/express" ;
import { inngest } from "./src/inngest/client" ;
import fnA from "./src/inngest/fnA" ; // Your own function

ff .http (
"inngest" ,
serve ({
client : inngest ,
functions : [fnA] ,
servePath : "/" ,
})
);
```

You can run this locally with `npx @google-cloud/functions-framework --target=inngest` which will serve your Inngest functions on port `8080` .

See the [Google Cloud Functions example](https://github.com/inngest/inngest-js/tree/main/examples/framework-google-functions-framework) for more information.

1st generation Cloud Run Functions are not officially supported. Using one may result in a signature verification error.

### [Framework: Firebase Cloud Functions](\docs\learn\serving-inngest-functions#framework-firebase-cloud-functions)

Based on the Google Cloud Function architecture, the Firebase Cloud Functions provide a different API to serve functions using `onRequest` :

Copy Copied

```
import { onRequest } from "firebase-functions/v2/https" ;

import { serve } from "inngest/express" ;
import { inngest as inngestClient } from "./inngest/client" ;

export const inngest = onRequest (
serve ({
client : inngestClient ,
functions : [ /* ...functions... */ ] ,
})
);
```

Firebase Cloud Functions require configuring `INNGEST_SERVE_PATH` with the custom function path.

For example, for a project named `inngest-firebase-functions` deployed on the `us-central1` region, the `INNGEST_SERVE_PATH` value will be as follows:

Copy Copied

```
/inngest-firebase-functions/us-central1/inngest/
```

To serve your Firebase Cloud Function locally, use the following command:

Copy Copied

```
firebase emulators:start
```

Please note that you'll need to start your Inngest Local Dev Server with the `-u` flag to match our Firebase Cloud Function's custom path  as follows:

Copy Copied

```
npx inngest-cli@latest dev -u http://127.0.0.1: 5001 /inngest-firebase-functions/us-central1/inngest
```

*The above command example features a project named* *`inngest-firebase-functions`* *deployed on the* *`us-central1`* *region* .

### [Framework: H3 v2.7.0+](\docs\learn\serving-inngest-functions#framework-h3)

Inngest supports [H3](https://github.com/unjs/h3) and frameworks built upon it. Here's a simple H3 server that hosts serves an Inngest function.

### index.js

v3 v2

Copy Copied

```
import { createApp , eventHandler , toNodeListener } from "h3" ;
import { serve } from "inngest/h3" ;
import { createServer } from "node:http" ;
import { inngest } from "./inngest/client" ;
import fnA from "./inngest/fnA" ;

const app = createApp ();
app .use (
"/api/inngest" ,
eventHandler (
serve ({
client : inngest ,
functions : [fnA] ,
})
)
);

createServer ( toNodeListener (app)) .listen ( process . env . PORT || 3000 );
```

See the [github.com/unjs/h3](https://github.com/unjs/h3) repository for more information about how to host an H3 endpoint.

### [Framework: Hono](\docs\learn\serving-inngest-functions#framework-hono)

Inngest supports the [Hono](https://hono.dev/) framework which is popularly deployed to Cloudflare Workers. Add the following to `./src/index.ts` :

Copy Copied

```
import { Hono } from "hono" ;
import { serve } from "inngest/hono" ;
import { functions , inngest } from "./inngest" ;

const app = new Hono ();

app .on (
[ "GET" , "PUT" , "POST" ] ,
"/api/inngest" ,
serve ({
client : inngest ,
functions ,
})
);

export default app;
```

To automatically pass environment variables defined with Wrangler to Inngest function handlers, use the [Hono bindings middleware](\docs\examples\middleware\cloudflare-workers-environment-variables) .

If you're using Hono with Cloudflare's Wrangler CLI in " *cloud* " mode, follow [the documentation above](\docs\learn\serving-inngest-functions#local-development-with-wrangler) for Cloudflare Workers.

See the [Hono example](https://github.com/inngest/inngest-js/blob/main/examples/framework-hono) for more information.

### [Framework: Koa v3.6.0+](\docs\learn\serving-inngest-functions#framework-koa)

Add the following to your routing file:

Copy Copied

```
import { serve } from "inngest/koa" ;
import Koa from "koa" ;
import bodyParser from "koa-bodyparser" ;
import { functions , inngest } from "./inngest" ;

const app = new Koa ();
app .use ( bodyParser ()); // make sure we're parsing incoming JSON

const handler = serve ({
client : inngest ,
functions ,
});

app .use ((ctx) => {
if ( ctx . request .path === "/api/inngest" ) {
return handler (ctx);
}
});
```

See the [Koa example](https://github.com/inngest/inngest-js/tree/main/examples/framework-koa) for more information.

### [Framework: NestJS](\docs\learn\serving-inngest-functions#framework-nest-js)

Add the following to `./src/main.ts` :

Copy Copied

```
import { Logger } from '@nestjs/common' ;
import { NestFactory } from '@nestjs/core' ;
import { NestExpressApplication } from '@nestjs/platform-express' ;
import { serve } from 'inngest/express' ;

import { inngest } from '@modules/common/inngest/client' ;
import { getInngestFunctions } from '@modules/common/inngest/functions' ;

import { AppModule } from './app.module' ;
import { AppService } from './app.service' ;

async function bootstrap () {
const app = await NestFactory .create < NestExpressApplication >(AppModule , {
bodyParser : true ,
});

// Setup inngest
app .useBodyParser ( 'json' , { limit : '10mb' });

// Inject Dependencies into inngest functions

const logger = app .get (Logger);
const appService = app .get (AppService);

// Pass dependencies into this function
const inngestFunctions = getInngestFunctions ({
appService ,
logger ,
});

// Register inngest endpoint
app .use (
'/api/inngest' ,
serve ({
client : inngest ,
functions : inngestFunctions ,
}) ,
);

// Start listening for http requests
await app .listen ( 3000 );
}

bootstrap ();
```

See the [NestJS example](https://github.com/inngest/inngest-js/tree/main/examples/framework-nestjs) for more information.

### [Framework: Next.js](\docs\learn\serving-inngest-functions#framework-next-js)

Inngest has first class support for Next.js API routes, allowing you to easily create the Inngest API. Both the App Router and the Pages Router are supported. For the App Router, Inngest requires `GET` , `POST` , and `PUT` methods.

App Router Pages Router

Copy Copied

```
// src/app/api/inngest/route.ts
import { serve } from "inngest/next" ;
import { inngest } from "../../../inngest/client" ;
import fnA from "../../../inngest/fnA" ; // Your own functions

export const { GET , POST , PUT } = serve ({
client : inngest ,
functions : [fnA] ,
});
```

### [Streaming v1.8.0+](\docs\learn\serving-inngest-functions#streaming-2)

Next.js Functions hosted on [Vercel](\docs\deploy\vercel) with Fluid compute can stream responses back to Inngest which can help you reach the maximum duration of 800s (13m20s) provided you are on a paid Vercel plan.

To enable this, add the `streaming: "force"` option to your serve handler:

**Next.js 13+ on Fluid compute**

Copy Copied

```
export const { GET , POST , PUT } = serve ({
client : inngest ,
functions : [ ... fns] ,
streaming : "force" ,
});
```

**Edge runtime**

If you are not using Vercel Fluid compute, you can also stream responses to Inngest by running on their [edge runtime](https://vercel.com/docs/functions/runtimes/edge) .

To enable this, set your runtime to `"edge"` and add the `streaming: "allow"` option to your serve handler:

**Next.js 13+**

Copy Copied

```
export const runtime = "edge" ;

export const { GET , POST , PUT } = serve ({
client : inngest ,
functions : [ ... fns] ,
streaming : "allow" ,
});
```

**Older versions (Next.js 12)**

v3 v2

Copy Copied

```
export const config = {
runtime : "edge" ,
};

const handler = serve ({
client : inngest ,
functions : [ ... fns] ,
streaming : "allow" ,
});
```

For more information, check out the [Streaming](\docs\streaming) page.

### [Framework: Nitro v3.24.0](\docs\learn\serving-inngest-functions#framework-nitro)

Add the following to `./server/routes/api/inngest.ts` :

Copy Copied

```
import { serve } from "inngest/nitro" ;
import { inngest } from "~~/inngest/client" ;
import fnA from "~~/inngest/fnA" ; // Your own function

export default eventHandler (
serve ({
client : inngest ,
functions : [fnA] ,
})
);
```

See the [Nitro example](https://github.com/inngest/inngest-js/tree/main/examples/framework-nitro) for more information.

### [Framework: Nuxt v0.9.2+](\docs\learn\serving-inngest-functions#framework-nuxt)

Inngest has first class support for [Nuxt server routes](https://nuxt.com/docs/guide/directory-structure/server#server-routes) , allowing you to easily create the Inngest API.

Add the following within `./server/api/inngest.ts` :

v3 v2

Copy Copied

```
import { serve } from "inngest/nuxt" ;
import { inngest } from "~~/inngest/client" ;
import fnA from "~~/inngest/fnA" ; // Your own function

export default defineEventHandler (
serve ({
client : inngest ,
functions : [fnA] ,
})
);
```

See the [Nuxt example](https://github.com/inngest/inngest-js/tree/main/examples/framework-nuxt) for more information.

### [Framework: Redwood](\docs\learn\serving-inngest-functions#framework-redwood)

Add the following to `api/src/functions/inngest.ts` :

v3 v2

Copy Copied

```
import { serve } from "inngest/redwood" ;
import { inngest } from "src/inngest/client" ;
import fnA from "src/inngest/fnA" ; // Your own function

export const handler = serve ({
client : inngest ,
functions : [fnA] ,
servePath : "/api/inngest" ,
});
```

You should also update your `redwood.toml` to add `apiUrl = "/api"` , ensuring your API is served

at the

`/api` root.

### [Framework: Remix](\docs\learn\serving-inngest-functions#framework-remix)

Add the following to `./app/routes/api.inngest.ts` :

v3 v2

Copy Copied

```
// app/routes/api.inngest.ts
import { serve } from "inngest/remix" ;
import { inngest } from "~/inngest/client" ;
import fnA from "~/inngest/fnA" ;

const handler = serve ({
client : inngest ,
functions : [fnA] ,
});

export { handler as action , handler as loader };
```

See the [Remix example](https://github.com/inngest/inngest-js/tree/main/examples/framework-remix) for more information.

### [Streaming v2.3.0+](\docs\learn\serving-inngest-functions#streaming-3)

Remix Edge Functions hosted on [Vercel](\docs\deploy\vercel) can also stream responses back to Inngest, giving you a much higher request timeout of 15 minutes (up from 10 seconds on the Vercel Hobby plan!).

To enable this, set your runtime to `"edge"` (see [Quickstart for Using Edge Functions | Vercel Docs](https://vercel.com/docs/concepts/functions/edge-functions/quickstart) ) and add the `streaming: "allow"` option to your serve handler:

v3 v2

Copy Copied

```
export const config = {
runtime : "edge" ,
};

const handler = serve ({
client : inngest ,
functions : [ ... fns] ,
streaming : "allow" ,
});
```

For more information, check out the [Streaming](\docs\streaming) page.

### [Framework: SvelteKit v3.5.0+](\docs\learn\serving-inngest-functions#framework-svelte-kit)

Add the following to `./src/routes/api/inngest/+server.ts` :

Copy Copied

```
import { functions , inngest } from '$lib/inngest' ;
import { serve } from 'inngest/sveltekit' ;

const inngestServe = serve ({ client : inngest , functions });
export const GET = inngestServe . GET ;
export const POST = inngestServe . POST ;
export const PUT = inngestServe . PUT ;
```

See the [SvelteKit example](https://github.com/inngest/inngest-js/tree/main/examples/framework-sveltekit) for more information.

### [Framework: Tanstack Start](\docs\learn\serving-inngest-functions#framework-tanstack-start)

Add the following to `./src/routes/api/inngest.ts` :

Copy Copied

```
import { createServerFileRoute } from '@tanstack/react-start/server'

import { serve } from "inngest/edge" ;
import { inngest , functions } from "../../inngest" ;

const handler = serve ({ client : inngest , functions });

export const ServerRoute = createServerFileRoute ( '/api/inngest' ) .methods ({
GET : async ({ request }) => handler (request) ,
POST : async ({ request }) => handler (request) ,
PUT : async ({ request }) => handler (request)
})
```

See the [Tanstack Start example](https://github.com/inngest/inngest-js/tree/main/examples/framework-tanstack-start) for more information.

### [Custom frameworks](\docs\learn\serving-inngest-functions#custom-frameworks)

If the framework that your application uses is not included in the above list of first-party supported frameworks, you can create a custom `serve` handler.

To create your own handler, check out the [example handler](https://github.com/inngest/inngest-js/blob/main/packages/inngest/src/test/functions/handler.ts) in our SDK's open source repository to understand how it works. Here's an example of a custom handler being created and used:

Copy Copied

```
import { Inngest , InngestCommHandler , type ServeHandlerOptions } from "inngest" ;

const serve = (options : ServeHandlerOptions ) => {
const handler = new InngestCommHandler ({
frameworkName : "edge" ,
fetch : fetch .bind (globalThis) ,
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

const inngest = new Inngest ({ id : "example-edge-app" });

const fn = inngest .createFunction (
{ id : "hello-world" } ,
{ event : "test/hello.world" } ,
() => "Hello, World!"
);

export default serve ({ client : inngest , functions : [fn] });
```

### [Signing key](\docs\learn\serving-inngest-functions#signing-key)

You'll need to assign your [signing key](\docs\platform\signing-keys) to an [`INNGEST_SIGNING_KEY`](\docs\sdk\environment-variables#inngest-signing-key) environment variable in your hosting

provider or

`.env` file locally, which lets the SDK securely communicate with Inngest. If you can't

provide this as a signing key, you can pass it in to

`serve` when setting up your framework. [Read](\docs\sdk\reference\serve#reference)

[the reference for more information](\docs\sdk\reference\serve#reference)

.

### [Other configuration](\docs\learn\serving-inngest-functions#other-configuration)

When using `serve` , allow requests up to 4 MB in size. This is the maximum request size that Inngest will send to your app. Configurating maximum request size is framework-specific, so check the documentation for your framework for more information.

## [Reference](\docs\learn\serving-inngest-functions#reference)

For more information about the `serve` handler, read the [the reference guide](\docs\reference\serve) , which includes:

- [`serve()`](\docs\reference\serve#serve-client-functions-options) [configuration options](\docs\reference\serve#serve-client-functions-options)
- [How the serve handler works](\docs\reference\serve#how-the-serve-api-handler-works)