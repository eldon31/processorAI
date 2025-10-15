#### On this page

- [Cloudflare Workers environment variables and context](\docs\examples\middleware\cloudflare-workers-environment-variables#cloudflare-workers-environment-variables-and-context)
- [Creating middleware](\docs\examples\middleware\cloudflare-workers-environment-variables#creating-middleware)

[Middleware](\docs\examples\middleware\cloudflare-workers-environment-variables)

# Cloudflare Workers environment variables and context

Cloudflare Workers does not set environment variables a global object like Node.js does with `process.env` . Workers [binds environment variables](https://developers.cloudflare.com/workers/configuration/environment-variables/) to the worker's special `fetch` event handler thought a specific `env` argument.

This means accessing environment variables within Inngest function handlers isn't possible without explicitly passing them through from the worker event handler to the Inngest function handler.

We can accomplish this by use the [middleware](\docs\features\middleware) feature for Workers or when using [Hono](\docs\learn\serving-inngest-functions#framework-hono) .

## [Creating middleware](\docs\examples\middleware\cloudflare-workers-environment-variables#creating-middleware)

You can create middleware which extracts the `env` argument from the Workers `fetch` event handler arguments for either Workers or Hono:

1. Use `onFunctionRun` 's `reqArgs` array to get the `env` object and, optionally, cast a type.
2. Return the `env` object within the special `ctx` object of `transformInput` lifecycle method.

Workers Hono

Copy Copied

```
import { Inngest , InngestMiddleware } from 'inngest' ;

const bindings = new InngestMiddleware ({
name : 'Cloudflare Workers bindings' ,
init ({ client , fn }) {
return {
onFunctionRun ({ ctx , fn , steps , reqArgs }) {
return {
transformInput ({ ctx , fn , steps }) {
// reqArgs is the array of arguments passed to the Worker's fetch event handler
// ex. fetch(request, env, ctx)
// We cast the argument to the global Env var that Wrangler generates:
const env = reqArgs[ 1 ] as Env ;
return {
ctx : {
// Return the env object to the function handler's input args
env ,
} ,
};
} ,
};
} ,
};
} ,
});

// Include the middleware when creating the Inngest client
export const inngest = new Inngest ({
id : 'my-workers-app' ,
middleware : [bindings] ,
});
```

Within your functions, you can now access the environment variables via the `env` object argument that you returned in `transformInput` above. Here's an example function:

Copy Copied

```
const myFn = inngest .createFunction (
{ id : 'my-fn' } ,
{ event : 'demo/event.sent' } ,
// The "env" argument returned in transformInput is passed through:
async ({ event , step , env }) => {

// The env object will be typed as well:
console .log ( env . MY_VAR );
}
);
```