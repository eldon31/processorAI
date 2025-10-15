#### On this page

- [Serve](\docs\reference\serve#serve)
- [serve(options)](\docs\reference\serve#serve-options)
- [How the serve API handler works](\docs\reference\serve#how-the-serve-api-handler-works)

References [TypeScript SDK](\docs\reference\typescript) [Serve](\docs\reference\serve)

# Serve

The `serve()` API handler is used to serve your application's [functions](\docs\reference\functions\create) via HTTP. This handler enables Inngest to remotely and securely read your functions' configuration and invoke your function code. This enables you to host your function code on any platform.

v3 v2

Copy Copied

```
import { serve } from "inngest/next" ; // or your preferred framework
import { inngest } from "./client" ;
import {
importProductImages ,
sendSignupEmail ,
summarizeText ,
} from "./functions" ;

serve ({
client : inngest ,
functions : [sendSignupEmail , summarizeText , importProductImages] ,
});
```

`serve` handlers are imported from convenient framework-specific packages like `"inngest/next"` , `"inngest/express"` , or `"inngest/lambda"` . [Click here for a full list of officially supported frameworks](\docs\learn\serving-inngest-functions) . For any framework that is not support, you can [create a custom handler](\docs\reference\serve#custom-frameworks) .

## [serve(options)](\docs\reference\serve#serve-options)

- Name `client` Type Inngest client Required required Description An Inngest client ( [reference](\docs\reference\client\create) ).
- Name `functions` Type InngestFunctions[] Required required Description An array of Inngest functions defined using `inngest.createFunction()` ( [reference](\docs\reference\functions\create) ).
- Name `signingKey` Type string Required required Description The Inngest [Signing Key](\docs\platform\signing-keys) for your [selected environment](\docs\platform\environments) . We recommend setting the [`INNGEST_SIGNING_KEY`](\docs\sdk\environment-variables#inngest-signing-key) environment variable instead of passing the `signingKey` option. You can find this in [the Inngest dashboard](https://app.inngest.com/env/production/manage/signing-key) .
- Name `serveHost` Type string Required optional Description The domain host of your application, *including* protocol, e.g. `https://myapp.com` . The SDK attempts to infer this via HTTP headers at runtime, but this may be required when using platforms like AWS Lambda or when using a reverse proxy. See also [`INNGEST_SERVE_HOST`](\docs\sdk\environment-variables#inngest-serve-host) .
- Name `servePath` Type string Required optional Description The path where your `serve` handler is hosted. The SDK attempts to infer this via HTTP headers at runtime. We recommend `/api/inngest` . See also [`INNGEST_SERVE_PATH`](\docs\sdk\environment-variables#inngest-serve-path) .
- Name `streaming` Type "allow" | "force" | false Required optional Description Enables streaming responses back to Inngest which can enable maximum serverless function timeouts. See [reference](\docs\streaming) for more information on the configuration. See also [`INNGEST_SERVE_HOST`](\docs\sdk\environment-variables#inngest-serve-host) .
- Name `logLevel` Type "fatal" | "error" | "warn" | "info" | "debug" | "silent" Required optional Description The minimum level to log from the Inngest serve endpoint. Defaults to `"info"` . See also [`INNGEST_LOG_LEVEL`](\docs\sdk\environment-variables#inngest-log-level) .
- Name `baseUrl` Type string Required optional Description The URL used to communicate with Inngest. This can be useful in testing environments when using the Inngest Dev Server. Defaults to: `"https://api.inngest.com/"` . See also [`INNGEST_BASE_URL`](\docs\sdk\environment-variables#inngest-base-url) .
- Name `fetch` Type Fetch API compatible interface Required optional Description Override the default [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) implementation. Defaults to the runtime's native Fetch API.
- Name `id` Type string Required optional Description The ID to use to represent this application instead of the client's ID. Useful for creating many Inngest endpoints in a single application.

We always recommend setting the [`INNGEST_SIGNING_KEY`](\docs\sdk\environment-variables#inngest-signing-key) over using the `signingKey` option. As with any secret, it's not a good practice to hard-code the signing key in your codebase.

## [How the serve API handler works](\docs\reference\serve#how-the-serve-api-handler-works)

The API works by exposing a single endpoint at `/api/inngest` which handles different actions utilizing HTTP request methods:

- `GET` : Return function metadata and render a debug page in in **development only** . See [`landingPage`](\docs\reference\serve#landingPage) .
- `POST` : Invoke functions with the request body as incoming function state.
- `PUT` : Trigger the SDK to register all functions with Inngest using the signing key.