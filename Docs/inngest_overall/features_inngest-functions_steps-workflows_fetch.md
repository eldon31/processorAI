#### On this page

- [Fetch: performing API requests or fetching data](\docs\features\inngest-functions\steps-workflows\fetch#fetch-performing-api-requests-or-fetching-data)
- [Using step.fetch()](\docs\features\inngest-functions\steps-workflows\fetch#using-step-fetch)
- [step.fetch() observability](\docs\features\inngest-functions\steps-workflows\fetch#step-fetch-observability)
- [Using the fetch() utility](\docs\features\inngest-functions\steps-workflows\fetch#using-the-fetch-utility)
- [Within steps](\docs\features\inngest-functions\steps-workflows\fetch#within-steps)
- [Fallbacks](\docs\features\inngest-functions\steps-workflows\fetch#fallbacks)
- [How it works](\docs\features\inngest-functions\steps-workflows\fetch#how-it-works)

Features [Inngest Functions](\docs\features\inngest-functions) [Steps &amp; Workflows](\docs\features\inngest-functions\steps-workflows)

# Fetch: performing API requests or fetching data TypeScript only

The Inngest TypeScript SDK provides a `step.fetch()` API and a `fetch()` utility, enabling you to make requests to third-party APIs or fetch data in a durable way by offloading them to the Inngest Platform:

- `step.fetch()` is a shorthand for making HTTP requests from within an Inngest function, and it also makes it easier to start parallel HTTP requests.
- The `fetch()` utility can be passed to packages that accept a custom `fetch` implementation, such as `axios` .

Using Fetch offloads the HTTP request to the Inngest Platform

<!-- image -->

## [Using step.fetch()](\docs\features\inngest-functions\steps-workflows\fetch#using-step-fetch)

You can use `step.fetch()` to make HTTP requests within an Inngest function.

`step.fetch()` offloads the HTTP request to the Inngest Platform, so your service does not need to be active and waiting for the response.

### src/inngest/functions.ts

Copy Copied

```
import { inngest } from "./client" ;

export const retrieveTextFile = inngest .createFunction (
{ id : "retrieveTextFile" } ,
{ event : "textFile/retrieve" } ,
async ({ step }) => {
// The fetching of the text file is offloaded to the Inngest Platform
const response = await step .fetch (
"https://example-files.online-convert.com/document/txt/example.txt"
);

// The Inngest function run is resumed when the HTTP request is complete
await step .run ( "extract-text" , async () => {
const text = await response .text ();
const exampleOccurences = text .match ( /example/ g );
return exampleOccurences ?. length ;
});
}
);
```

## [step.fetch() example](\docs\examples\fetch)

[See the complete step.fetch() example including the source code and other use cases.](\docs\examples\fetch)

`step.fetch()` is useful:

- In serverless environments, to offload long-running HTTP requests that might trigger timeouts.
- As a shorthand for making HTTP requests within an Inngest function, making it easier to start parallel HTTP requests using `Promise.all()` .
- As a best practice to ensure that all HTTP requests are durable and can be inspected in the Inngest Platform or Dev Server.

### [step.fetch() observability](\docs\features\inngest-functions\steps-workflows\fetch#step-fetch-observability)

All `step.fetch()` calls are visible in your [Inngest Traces](\docs\platform\monitor\observability-metrics) , allowing you to monitor and debug your HTTP requests:

Inngest Traces showing a step.fetch() call

<!-- image -->

## [Using the fetch() utility](\docs\features\inngest-functions\steps-workflows\fetch#using-the-fetch-utility)

A Fetch API-compatible function is exported, allowing you to make any HTTP requests durable if they're called within an Inngest function.

For example, a `MyProductApi` class that relies on axios can take a `fetch` parameter:

### TypeScript

Copy Copied

```
import { fetch } from "inngest" ;

const api = new MyProductApi ({ fetch });

// A call outside an Inngest function will fall back to the global fetch
await api .getProduct ( 1 );

// A call from inside an Inngest function will be made durable and offloaded to the Inngest Platform
inngest .createFunction (
{ id : "my-fn" } ,
{ event : "product/activated" } ,
async () => {
await api .getProduct ( 1 );
} ,
);
```

⚠️ `fetch()` and `step.run()`

Inngest's `fetch()` calls should not be performed inside of `step.run()` blocks.

Doing so will result in

`fetch()` to fallback to the global `fetch` implementation.

Why? The `fetch()` utility transforms the `fetch` calls into `step.run()` calls, [which cannot be nested](\docs\sdk\eslint#inngest-no-nested-steps) .

### [Within steps](\docs\features\inngest-functions\steps-workflows\fetch#within-steps)

By default, using Inngest's `fetch` retains all the functionality of requests made outside of an endpoint, but ensures that those made from inside are durable.

Copy Copied

```
import { fetch as inngestFetch } from 'inngest' ;
import { generateText } from 'ai' ;
import { createAnthropic } from '@ai-sdk/anthropic' ;

// The AI SDK's createAnthropic objects can be passed a custom fetch implementation
const anthropic = createAnthropic ({
fetch : inngestFetch ,
});

// NOTE - Using this fetch outside of an Inngest function will fall back to the global fetch
const response = await generateText ({
model : anthropic ( 'claude-3-5-sonnet-20240620' ) ,
prompt : 'Hello, world!' ,
});

// A call from inside an Inngest function will be made durable
inngest .createFunction (
{ id : "generate-summary" } ,
{ event : "post.created" } ,
async ({ event }) => {
// This will use step.fetch automatically!
const response = await generateText ({
model : anthropic ( 'claude-3-5-sonnet-20240620' ) ,
prompt : `Summarize the following post: ${ event . data .content } ` ,
});
} ,
);
```

However, the same `fetch` is also exported as `step.fetch` , allowing you to create your APIs isolated within the function instead:

Copy Copied

```
inngest .createFunction (
{ id : "generate-summary" } ,
{ event : "post.created" } ,
async ({ step }) => {
const anthropic = createAnthropic ({
fetch : step .fetch ,
});

const response = await generateText ({
model : anthropic ( 'claude-3-5-sonnet-20240620' ) ,
prompt : `Summarize the following post: ${ event . data .content } ` ,
});
} ,
);
```

### [Fallbacks](\docs\features\inngest-functions\steps-workflows\fetch#fallbacks)

By default, it will gracefully fall back to the global `fetch` if called outside of an Inngest function, though you can also set a custom fallback using the `config` method:

Copy Copied

```
import { fetch } from "inngest" ;

const api = new MyProductApi ({
fetch : fetch .config ({ fallback : myCustomFetch }) ,
});
```

You can also disable the fallback entirely:

Copy Copied

```
import { fetch } from "inngest" ;

const api = new MyProductApi ({
fetch : fetch .config ({ fallback : undefined }) ,
});
```

### [How it works](\docs\features\inngest-functions\steps-workflows\fetch#how-it-works)

Inngest's `fetch` function uses some of the basic building blocks of Inngest to allow seamless creation of optionally durable code. When it's called, it will:

- Check the context in which it's running
- If not in an Inngest function, optionally use the fallback; otherwise,
- Report the request to Inngest
- Inngest makes the request
- Inngest continues the function with the `Response` received from your request

Critically, this means that your service does not have to be active for the duration of the call; we'll continue your function when we have a result, while also keeping it durable!