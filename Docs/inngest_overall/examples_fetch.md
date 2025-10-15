#### On this page

- [Fetch: performing API requests or fetching data](\docs\examples\fetch#fetch-performing-api-requests-or-fetching-data)
- [Getting started with step.fetch()](\docs\examples\fetch#getting-started-with-step-fetch)
- [Parallelize HTTP requests with step.fetch()](\docs\examples\fetch#parallelize-http-requests-with-step-fetch)
- [Make 3rd party library HTTP requests durable with the fetch() utility](\docs\examples\fetch#make-3rd-party-library-http-requests-durable-with-the-fetch-utility)

[Examples](\docs\examples)

# Fetch: performing API requests or fetching data TypeScript only

The Inngest TypeScript SDK provides a `step.fetch()` API and a `fetch()` utility, enabling you to make requests to third-party APIs or fetch data in a durable way by offloading them to the Inngest Platform.

For more information on how Fetch works, see the [Fetch documentation](\docs\features\inngest-functions\steps-workflows\fetch) .

## [Getting started with step.fetch()](\docs\examples\fetch#getting-started-with-step-fetch)

The `step.fetch()` API enables you to make durable HTTP requests while offloading them to the Inngest Platform, saving you compute and improving reliability:

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

`step.fetch()` takes the same arguments as the [native](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) [API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) .

## [Clone this example on GitHub](https://github.com/inngest/inngest-js/tree/main/examples/node-step-fetch/)

[Check out this complete](https://github.com/inngest/inngest-js/tree/main/examples/node-step-fetch/) [`step.fetch()`](https://github.com/inngest/inngest-js/tree/main/examples/node-step-fetch/) [example on GitHub.](https://github.com/inngest/inngest-js/tree/main/examples/node-step-fetch/)

## [Parallelize HTTP requests with step.fetch()](\docs\examples\fetch#parallelize-http-requests-with-step-fetch)

`step.fetch()` shares all the benefits of `step.run()` , including the ability to parallelize requests using `Promise.all()` :

Copy Copied

```
const processFiles = inngest .createFunction (
{ id : "process-files" , concurrency : 10 } ,
{ event : "files/process" } ,
async ({ step , event }) => {
// All requests will be offloaded and processed in parallel while matching the concurrency limit
const responses = await Promise .all ( event . data . files .map ( async (file) => {
return step .fetch ( `https://api.example.com/files/ ${ file .id } ` )
}))

// Your Inngest function is resumed here with the responses
await step .run ( "process-file" , async (file) => {
const body = await response .json ()
// body.files
})
}
)
```

Note that `step.fetch()` , like all other `step` APIs, matches your function's configuration such as [concurrency](\docs\guides\concurrency) or [throttling](\docs\guides\throttling) .

## [Make 3rd party library HTTP requests durable with the fetch() utility](\docs\examples\fetch#make-3rd-party-library-http-requests-durable-with-the-fetch-utility)

Inngest's `fetch()` utility can be passed as a custom fetch handler to make all the requests made by a 3rd party library durable.

For example, you can pass the `fetch()` utility to the AI SDK or the OpenAI libraries:

AI SDK OpenAI SDK

Copy Copied

```
import { fetch as inngestFetch } from 'inngest' ;
import { generateText } from 'ai' ;
import { createAnthropic } from '@ai-sdk/anthropic' ;

// Pass the Inngest fetch utility to the AI SDK's model constructor:
const anthropic = createAnthropic ({
fetch : inngestFetch ,
});

const weatherFunction = inngest .createFunction (
{ id : "weather-function" } ,
{ event : "weather/get" } ,
async ({ step }) => {
// This request is offloaded to the Inngest platform
// and it also retries automatically if it fails!
const response = await generateText ({
model : anthropic ( 'claude-3-5-sonnet-20240620' ) ,
prompt : `What's the weather in London?` ,
});
}
)
```