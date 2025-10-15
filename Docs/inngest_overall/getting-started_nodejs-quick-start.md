#### On this page

- [Node.js Quick Start](\docs\getting-started\nodejs-quick-start#node-js-quick-start)
- [Select your Node.js framework](\docs\getting-started\nodejs-quick-start#select-your-node-js-framework)
- [Optional: Use a starter project](\docs\getting-started\nodejs-quick-start#optional-use-a-starter-project)
- [Starting your project](\docs\getting-started\nodejs-quick-start#starting-your-project)
- [1. Install the Inngest SDK](\docs\getting-started\nodejs-quick-start#1-install-the-inngest-sdk)
- [2. Run the Inngest Dev Server](\docs\getting-started\nodejs-quick-start#2-run-the-inngest-dev-server)
- [3. Create an Inngest client](\docs\getting-started\nodejs-quick-start#3-create-an-inngest-client)
- [4. Set up the Inngest http endpoint](\docs\getting-started\nodejs-quick-start#4-set-up-the-inngest-http-endpoint)
- [5. Write your first Inngest function](\docs\getting-started\nodejs-quick-start#5-write-your-first-inngest-function)
- [5. Trigger your function from the Inngest Dev Server UI](\docs\getting-started\nodejs-quick-start#5-trigger-your-function-from-the-inngest-dev-server-ui)
- [6. Trigger from code](\docs\getting-started\nodejs-quick-start#6-trigger-from-code)
- [Next Steps](\docs\getting-started\nodejs-quick-start#next-steps)

[Quick start](\docs\getting-started\nextjs-quick-start)

# Node.js Quick Start

In this tutorial you will add Inngest to a Node.js app to easily run background tasks and build complex workflows.

Inngest makes it easy to build, manage, and execute durable functions. Some use cases include scheduling drip marketing campaigns, building payment flows, or chaining LLM interactions.

By the end of this ten-minute tutorial you will:

- Set up and run Inngest on your machine.
- Write your first Inngest function.
- Trigger your function from your app and through Inngest Dev Server.

Let's get started!

## [Select your Node.js framework](\docs\getting-started\nodejs-quick-start#select-your-node-js-framework)

Choose your preferred Node.js web framework to get started. This guide uses ESM (ECMAScript Modules), but it also works for Common.js with typical modifications.

Express.js Fastify

Inngest works with any Node, Bun or Deno backend framework,but this tutorial will focus on some of the most popular frameworks.

### [Optional: Use a starter project](\docs\getting-started\nodejs-quick-start#optional-use-a-starter-project)

If you don't have an existing project, you can clone the following starter project to run through the quick start tutorial:

## [Starting your project](\docs\getting-started\nodejs-quick-start#starting-your-project)

Start your server using your typical script. We recommend using something like [`tsx`](https://www.npmjs.com/package/tsx) or [`nodemon`](https://www.npmjs.com/package/nodemon) for automatically restarting on file save:

tsx nodemon

Copy Copied

```
npx tsx watch ./index.ts # replace with your own main entrypoint file
```

Now let's add Inngest to your project.

## [1. Install the Inngest SDK](\docs\getting-started\nodejs-quick-start#1-install-the-inngest-sdk)

In your project directory's root, run the following command to install Inngest SDK:

npm yarn pnpm bun

Copy Copied

```
npm install inngest
```

## [2. Run the Inngest Dev Server](\docs\getting-started\nodejs-quick-start#2-run-the-inngest-dev-server)

Next, start the [Inngest Dev Server](\docs\local-development#inngest-dev-server) , which is a fast, in-memory version of Inngest where you can quickly send and view events events and function runs. This tutorial assumes that your Express.js server will be running on port `3000` ; change this to match your port if you use another.

npm yarn pnpm bun

Copy Copied

```
npx inngest-cli@latest dev -u http://localhost: 3000 /api/inngest
```

**You should see a similar output to the following:**

Copy Copied

```
$ npx inngest-cli@latest dev -u http://localhost: 3000 /api/inngest

12 :33PM INF executor > service starting
12 :33PM INF runner > starting event stream backend = redis
12 :33PM INF executor > subscribing to function queue
12 :33PM INF runner > service starting
12 :33PM INF runner > subscribing to events topic = events
12 :33PM INF no shard finder;  skipping shard claiming
12 :33PM INF devserver > service starting
12 :33PM INF devserver > autodiscovering locally hosted SDKs
12 :33PM INF api > starting server addr = 0.0.0.0: 8288

Inngest dev server online at 0.0.0.0: 8288 , visible at the following URLs:

- http://127.0.0.1: 8288 (http://localhost:8288)

Scanning for available serve handlers.
To disable scanning run `inngest dev ` with flags: --no-discovery -u < your-serve-ur l >
```

In your browser open [`http://localhost:8288`](http://localhost:8288/) to see the development UI where later you will test the functions you write:

Inngest Dev Server's 'Runs' tab with no data

<!-- image -->

## [3. Create an Inngest client](\docs\getting-started\nodejs-quick-start#3-create-an-inngest-client)

Inngest invokes your functions securely via an [API endpoint](\docs\learn\serving-inngest-functions) at `/api/inngest` . To enable that, you will create an [Inngest client](\docs\reference\client\create) in your project, which you will use to send events and create functions.

Create a file in the directory of your preference. We recommend creating an `inngest` directory for your client and all functions.

### src/inngest/index.ts

Copy Copied

```
import { Inngest } from "inngest" ;

// Create a client to send and receive events
export const inngest = new Inngest ({ id : "my-app" });

// Create an empty array where we'll export future Inngest functions
export const functions = [];
```

## [4. Set up the Inngest http endpoint](\docs\getting-started\nodejs-quick-start#4-set-up-the-inngest-http-endpoint)

Using your existing Express.js server, we'll set up Inngest using the provided `serve` handler which will "serve" Inngest functions. Here we'll assume this file is your entrypoint at `inngest.ts` and all import paths will be relative to that:

### ./index.ts

Copy Copied

```
import express from "express" ;
import { serve } from "inngest/express" ;
import { inngest , functions } from "./src/inngest"

const app = express ();
// Important: ensure you add JSON middleware to process incoming JSON POST payloads.
app .use ( express .json ());
// Set up the "/api/inngest" (recommended) routes with the serve handler
app .use ( "/api/inngest" , serve ({ client : inngest , functions }));

app .listen ( 3000 , () => {
console .log ( 'Server running on http://localhost:3000' );
});
```

👉 Note that you can import a [`serve`](\docs\reference\serve) handler for other frameworks and the rest of the code remains the same. These adapters enable you to change your web framework without changing any Inngest function code (ex. instead of `inngest/express` it could be `inngest/next` or `inngest/hono` );

## [5. Write your first Inngest function](\docs\getting-started\nodejs-quick-start#5-write-your-first-inngest-function)

In this step, you will write your first durable function. This function will be triggered whenever a specific event occurs (in our case, it will be `test/hello.world` ). Then, it will sleep for a second and return a "Hello, World!".

To define the function, use the [`createFunction`](\docs\reference\functions\create) method on the Inngest client.

**Learn more: What is** **`createFunction`** **method?**

The `createFunction` method takes three objects as arguments:

- **Configuration** : A unique `id` is required and it is the default name that will be displayed on the Inngest dashboard to refer to your function. You can also specify [additional options](\docs\reference\functions\create#configuration) such as `concurrency` , `rateLimit` , `retries` , or `batchEvents` , and others.
- **Trigger** : `event` is the name of the event that triggers your function. Alternatively, you can use `cron` to specify a schedule to trigger this function. Learn more about triggers [here](\docs\features\events-triggers) .
- **Handler** : The function that is called when the `event` is received. The `event` payload is passed as an argument. Arguments include `step` to define durable steps within your handler and [additional arguments](\docs\reference\functions\create#handler) include logging helpers and other data.

Define a function in the same file where we defined our Inngest client:

### src/inngest/index.ts

Copy Copied

```
import { Inngest } from "inngest" ;

export const inngest = new Inngest ({ id : "my-app" });

// Your new function:
const helloWorld = inngest .createFunction (
{ id : "hello-world" } ,
{ event : "test/hello.world" } ,
async ({ event , step }) => {
await step .sleep ( "wait-a-moment" , "1s" );
return { message : `Hello ${ event . data .email } !` };
} ,
);

// Add the function to the exported array:
export const functions = [
helloWorld
];
```

In the previous step, we configured the exported `functions` array to be passed to our Inngest http endpoint. Each new function must be added to this array in order for Inngest to read it's configuration and invoke it.

Now, it's time to run your function!

## [5. Trigger your function from the Inngest Dev Server UI](\docs\getting-started\nodejs-quick-start#5-trigger-your-function-from-the-inngest-dev-server-ui)

You will trigger your function in two ways: first, by invoking it directly from the Inngest Dev Server UI, and then by sending events from code.

With your Express.js server and Inngest Dev Server running, open the Inngest Dev Server UI and select the "Functions" tab [`http://localhost:8288/functions`](http://localhost:8288/functions) . You should see your function. (Note: if you don't see any function, select the "Apps" tab to troubleshoot)

Inngest Dev Server web interface's functions tab with functions listed

<!-- image -->

To trigger your function, use the "Invoke" button for the associated function:

Inngest Dev Server web interface's functions tab with the invoke button highlighted

<!-- image -->

In the pop up editor, add your event payload data like the example below. This can be any JSON and you can use this data within your function's handler. Next, press the "Invoke Function" button:

Copy Copied

```
{
"data" : {
"email" : "test@example.com"
}
}
```

Inngest Dev Server web interface's invoke modal with payload editor and invoke submit button highlighted

<!-- image -->

The payload is sent to Inngest (which is running locally) which automatically executes your function in the background! You can see the new function run logged in the "Runs" tab:

Inngest Dev Server web interface's runs tab with a single completed run displayed

<!-- image -->

When you click on the run, you will see more information about the event, such as which function was triggered, its payload, output, and timeline:

Inngest Dev Server web interface's runs tab with a single completed run expanded

<!-- image -->

In this case, the payload triggered the `hello-world` function, which did sleep for a second and then returned `"Hello, World!"` . No surprises here, that's what we expected!

Inngest Dev Server web interface's runs tab with a single completed run expanded indicating that hello-world function ran, that it slept for 1s, and that the correct body was returned

<!-- image -->

To aid in debugging your functions, you can quickly "Rerun" or "Cancel" a function. Try clicking "Rerun" at the top of the "Run details" table:

Run details expanded with rerun and cancel buttons highlighted

<!-- image -->

After the function was replayed, you will see two runs in the UI:

Inngest Dev Server web interface's runs tab with two runs listed

<!-- image -->

Now you will trigger an event from inside your app.

## [6. Trigger from code](\docs\getting-started\nodejs-quick-start#6-trigger-from-code)

Inngest is powered by events.

**Learn more: events in Inngest.**

It is worth mentioning here that an event-driven approach allows you to:

- Trigger one *or* multiple functions from one event, aka [fan-out](\docs\guides\fan-out-jobs) .
- Store received events for a historical record of what happened in your application.
- Use stored events to [replay](\docs\platform\replay) functions when there are issues in production.
- Interact with long-running functions by sending new events including [waiting for input](\docs\features\inngest-functions\steps-workflows\wait-for-event) and [cancelling](\docs\features\inngest-functions\cancellation\cancel-on-events) .

To trigger Inngest functions to run in the background, you will need to send events from your application to Inngest. Once the event is received, it will automatically invoke all functions that are configured to be triggered by it.

To send an event from your code, you can use the `Inngest` client's `send()` method.

**Learn more:** **`send()`** **method.**

Note that with the `send` method used below you now can:

- Send one or more events within any API route.
- Include any data you need in your function within the `data` object.

In a real-world app, you might send events from API routes that perform an action, like registering users (for example, `app/user.signup` ) or creating something (for example, `app/report.created` ).

You will now send an event from within your server from a `/api/hello GET` endpoint. Create a new get handler on your server object:

### ./index.ts

Copy Copied

```
import express from "express" ;
import { serve } from "inngest/express" ;
import { inngest , functions } from "./src/inngest"

app .use ( express .json ());
app .use ( "/api/inngest" , serve ({ client : inngest , functions }));

// Create a new route
app .get ( "/api/hello" , async function (req , res , next) {
await inngest .send ({
name : "test/hello.world" ,
data : {
email : "testUser@example.com" ,
} ,
}) .catch (err => next (err));
res .json ({ message : 'Event sent!' });
});

app .listen ( 3000 , () => {
console .log ( 'Server running on http://localhost:3000' );
});
```

Every time this API route is requested, an event is sent to Inngest. To test it, open [`http://localhost:3000/api/hello`](http://localhost:3000/api/hello) (change your port if your Express.js app is running elsewhere). You should see the following output: `{"message":"Event sent!"}`

Web browser showing the JSON response of the /api/hello endpoint

<!-- image -->

If you go back to the Inngest Dev Server, you will see a new run is triggered by this event:

Inngest Dev Server web interface's runs tab with a third run triggered by the 'test/hello.world' event

<!-- image -->

And - that's it! You now have learned how to create Inngest functions and you have sent events to trigger those functions. Congratulations 🥳

## [Next Steps](\docs\getting-started\nodejs-quick-start#next-steps)

To continue your exploration, feel free to check out:

- [Examples](\docs\examples) of what other people built with Inngest.
- [Case studies](\customers) showcasing a variety of use cases.
- [Our blog](\blog) where we explain how Inngest works, publish guest blog posts, and share our learnings.

You can also read more:

- About [Inngest functions](\docs\functions) .
- About [Inngest steps](\docs\steps) .
- About [Durable Execution](\docs\learn\how-functions-are-executed)
- How to [use Inngest with other frameworks](\docs\learn\serving-inngest-functions) .
- How to [deploy your app to your platform](\docs\deploy) .