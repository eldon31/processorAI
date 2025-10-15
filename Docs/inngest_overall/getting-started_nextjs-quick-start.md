#### On this page

- [Next.js Quick Start](\docs\getting-started\nextjs-quick-start#next-js-quick-start)
- [Choose Next.js version](\docs\getting-started\nextjs-quick-start#choose-next-js-version)
- [Before you start: choose a project](\docs\getting-started\nextjs-quick-start#before-you-start-choose-a-project)
- [1. Install Inngest](\docs\getting-started\nextjs-quick-start#1-install-inngest)
- [2. Run the Inngest Dev Server](\docs\getting-started\nextjs-quick-start#2-run-the-inngest-dev-server)
- [3. Create an Inngest client](\docs\getting-started\nextjs-quick-start#3-create-an-inngest-client)
- [4. Write your first Inngest function](\docs\getting-started\nextjs-quick-start#4-write-your-first-inngest-function)
- [Define the function](\docs\getting-started\nextjs-quick-start#define-the-function)
- [Add the function to serve()](\docs\getting-started\nextjs-quick-start#add-the-function-to-serve)
- [5. Trigger your function from the Inngest Dev Server UI](\docs\getting-started\nextjs-quick-start#5-trigger-your-function-from-the-inngest-dev-server-ui)
- [6. Trigger from code](\docs\getting-started\nextjs-quick-start#6-trigger-from-code)
- [Next Steps](\docs\getting-started\nextjs-quick-start#next-steps)

[Quick start](\docs\getting-started\nextjs-quick-start)

# Next.js Quick Start

In this tutorial you will add Inngest to a Next.js app to see how easy it can be to build complex workflows.

Inngest makes it easy to build, manage, and execute reliable workflows. Some use cases include scheduling drip marketing campaigns, building payment flows, or chaining LLM interactions.

By the end of this ten-minute tutorial you will:

- Set up and run Inngest on your machine.
- Write your first Inngest function.
- Trigger your function from your app and through Inngest Dev Server.

Let's get started!

### [Choose Next.js version](\docs\getting-started\nextjs-quick-start#choose-next-js-version)

Choose your preferred Next.js version for this tutorial:

Next.js - App Router Next.js - Pages Router

## [Before you start: choose a project](\docs\getting-started\nextjs-quick-start#before-you-start-choose-a-project)

In this tutorial you can use any existing Next.js project, or you can create a new one.

**Instructions for creating a new Next.js project**

Run the following command in your terminal to create a new Next.js project:

Copy Copied

```
npx create-next-app@latest --ts --eslint --tailwind --src-dir --app --import-alias= '@/*' inngest-guide
```

Once you've chosen a project, open it in a code editor.

Next, start your Next.js app in development mode by running:

Copy Copied

```
npm run dev
```

Now you can add Inngest to your project!

## [1. Install Inngest](\docs\getting-started\nextjs-quick-start#1-install-inngest)

With the Next.js app now running running open a new tab in your terminal. In your project directory's root, run the following command to install Inngest SDK:

npm yarn pnpm bun

Copy Copied

```
npm install inngest
```

## [2. Run the Inngest Dev Server](\docs\getting-started\nextjs-quick-start#2-run-the-inngest-dev-server)

Next, start the [Inngest Dev Server](\docs\local-development#inngest-dev-server) , which is a fast, in-memory version of Inngest where you can quickly send and view events events and function runs:

npm yarn pnpm bun

Copy Copied

```
npx inngest-cli@latest dev
```

**You should see a similar output to the following:**

Copy Copied

```
$ npx inngest-cli@latest dev

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

## [3. Create an Inngest client](\docs\getting-started\nextjs-quick-start#3-create-an-inngest-client)

Inngest invokes your functions securely via an [API endpoint](\docs\learn\serving-inngest-functions) at `/api/inngest` . To enable that, you will create an [Inngest client](\docs\reference\client\create) in your Next.js project, which you will use to send events and create functions.

Make a new directory next to your `app` directory (for example, `src/inngest` ) where you'll define your Inngest functions and the client.

In the `/src/inngest` directory create an Inngest client:

### src/inngest/client.ts

Copy Copied

```
import { Inngest } from "inngest" ;

// Create a client to send and receive events
export const inngest = new Inngest ({ id : "my-app" });
```

Next, you will set up a route handler for the `/api/inngest` route. To do so, create a file inside your `app` directory (for example, at `src/app/api/inngest/route.ts` ) with the following code:

### src/app/api/inngest/route.ts

Copy Copied

```
import { serve } from "inngest/next" ;
import { inngest } from "../../../inngest/client" ;

// Create an API that serves zero functions
export const { GET , POST , PUT } = serve ({
client : inngest ,
functions : [
/* your functions will be passed here later! */
] ,
});
```

## [4. Write your first Inngest function](\docs\getting-started\nextjs-quick-start#4-write-your-first-inngest-function)

In this step, you will write your first reliable serverless function. This function will be triggered whenever a specific event occurs (in our case, it will be `test/hello.world` ). Then, it will sleep for a second and return a "Hello, World!".

### [Define the function](\docs\getting-started\nextjs-quick-start#define-the-function)

To define the function, use the [`createFunction`](\docs\reference\functions\create) method on the Inngest client.

**Learn more: What is** **`createFunction`** **method?**

The `createFunction` method takes three objects as arguments:

- **Configuration** : A unique `id` is required and it is the default name that will be displayed on the Inngest dashboard to refer to your function. You can also specify [additional options](\docs\reference\functions\create#configuration) such as `concurrency` , `rateLimit` , `retries` , or `batchEvents` , and others.
- **Trigger** : `event` is the name of the event that triggers your function. Alternatively, you can use `cron` to specify a schedule to trigger this function. Learn more about triggers [here](\docs\features\events-triggers) .
- **Handler** : The function that is called when the `event` is received. The `event` payload is passed as an argument. Arguments include `step` to define durable steps within your handler and [additional arguments](\docs\reference\functions\create#handler) include logging helpers and other data.

Inside your `src/inngest` directory create a new file called `functions.ts` where you will define Inngest functions. Add the following code:

### src/inngest/functions.ts

Copy Copied

```
import { inngest } from "./client" ;

export const helloWorld = inngest .createFunction (
{ id : "hello-world" } ,
{ event : "test/hello.world" } ,
async ({ event , step }) => {
await step .sleep ( "wait-a-moment" , "1s" );
return { message : `Hello ${ event . data .email } !` };
} ,
);
```

### [Add the function to serve()](\docs\getting-started\nextjs-quick-start#add-the-function-to-serve)

Next, import your Inngest function in the routes handler ( `src/app/api/inngest/route.ts` ) and add it to the `serve` handler so Inngest can invoke it via HTTP:

### src/app/api/inngest/route.ts

Copy Copied

```
import { serve } from "inngest/next" ;
import { inngest } from "../../../inngest/client" ;
import { helloWorld } from "../../../inngest/functions" ;

export const { GET , POST , PUT } = serve ({
client : inngest ,
functions : [
helloWorld , // <-- This is where you'll always add all your functions
] ,
});
```

👉 Note that you can import [`serve()`](\docs\reference\serve) for other frameworks and the rest of the code, in fact, remains the same - only the import statement changes (instead of `inngest/next` , it would be `inngest/astro` , `inngest/remix` , and so on).

Now, it's time to run your function!

## [5. Trigger your function from the Inngest Dev Server UI](\docs\getting-started\nextjs-quick-start#5-trigger-your-function-from-the-inngest-dev-server-ui)

Inngest is powered by events.You will trigger your function in two ways: first, by invoking it directly from the Inngest Dev Server UI, and then by sending events from code.

With your Next.js app and Inngest Dev Server running, open the Inngest Dev Server UI and select the "Functions" tab [`http://localhost:8288/functions`](http://localhost:8288/functions) . You should see your function. (Note: if you don't see any function, select the "Apps" tab to troubleshoot)

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

## [6. Trigger from code](\docs\getting-started\nextjs-quick-start#6-trigger-from-code)

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

You will now send an event from within your Next.js app: from the "hello" Next.js API function. To do so, create a new API handler in the `src/app/api/hello/route.ts` file:

### src/app/api/hello/route.ts

Copy Copied

```
import { NextResponse } from "next/server" ;
import { inngest } from "../../../inngest/client" ; // Import our client

// Opt out of caching; every request should send a new event
export const dynamic = "force-dynamic" ;

// Create a simple async Next.js API route handler
export async function GET () {
// Send your event payload to Inngest
await inngest .send ({
name : "test/hello.world" ,
data : {
email : "testUser@example.com" ,
} ,
});

return NextResponse .json ({ message : "Event sent!" });
}
```

👉 Note that we use [`"force-dynamic"`](https://nextjs.org/docs/app/building-your-application/caching) to ensure we always send a new event on every request. In most situations, you'll probably want to send an event during a `POST` request so that you don't need this config option.

Every time this API route is requested, an event is sent to Inngest. To test it, open [`http://localhost:3000/api/hello`](http://localhost:3000/api/hello) (change your port if your Next.js app is running elsewhere). You should see the following output: `{"message":"Event sent!"}`

Web browser showing the JSON response of the /api/hello endpoint

<!-- image -->

If you go back to the Inngest Dev Server, you will see a new run is triggered by this event:

Inngest Dev Server web interface's runs tab with a third run triggered by the 'test/hello.world' event

<!-- image -->

And - that's it! You now have learned how to create Inngest functions and you have sent events to trigger those functions. Congratulations 🥳

## [Next Steps](\docs\getting-started\nextjs-quick-start#next-steps)

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