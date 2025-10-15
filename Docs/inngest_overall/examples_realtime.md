#### On this page

- [Realtime: Stream updates from Inngest functions](\docs\examples\realtime#realtime-stream-updates-from-inngest-functions)
- [Pattern: Stream updates from a single function run](\docs\examples\realtime#pattern-stream-updates-from-a-single-function-run)
- [Pattern: Stream updates from multiple function runs](\docs\examples\realtime#pattern-stream-updates-from-multiple-function-runs)
- [Human in the loop: Bi-directional workflows](\docs\examples\realtime#human-in-the-loop-bi-directional-workflows)
- [Learn more](\docs\examples\realtime#learn-more)

[Examples](\docs\examples)

# Realtime: Stream updates from Inngest functions

Inngest Realtime enables you to stream updates from your functions, power live UIs, and implement bi-directional workflows such as Human-in-the-Loop. Use channels and topics to broadcast updates, stream logs, or await user input.

## [Pattern: Stream updates from a single function run](\docs\examples\realtime#pattern-stream-updates-from-a-single-function-run)

Enable users to follow the progress of a long-running task by streaming updates from a dedicated channel. Here's how to trigger a function and subscribe to its updates:

Copy Copied

```
import crypto from "crypto" ;
import { inngest } from "@/inngest/client" ;
import { subscribe } from "@inngest/realtime" ;

export async function POST (req : Request ) {
const json = await req .json ();
const { prompt } = json;
const uuid = crypto .randomUUID ();

await inngest .send ({
name : "hello-world/hello" ,
data : { uuid } ,
});

const stream = await subscribe (inngest , {
channel : `hello-world. ${ uuid } ` ,
topics : [ "logs" ] ,
});

return new Response ( stream .getEncodedStream () , {
headers : {
"Content-Type" : "text/event-stream" ,
"Cache-Control" : "no-cache" ,
Connection : "keep-alive" ,
} ,
});
}
```

Your function can then publish updates to this channel:

Copy Copied

```
import { Inngest } from "inngest" ;
import { realtimeMiddleware , channel , topic } from "@inngest/realtime" ;

const inngest = new Inngest ({
id : "my-app" ,
middleware : [ realtimeMiddleware ()] ,
});

export const helloChannel = channel ((uuid : string ) => `hello-world. ${ uuid } ` ) .addTopic (
topic ( "logs" ) .type < string >()
);

export const someTask = inngest .createFunction (
{ id : "hello-world" } ,
{ event : "hello-world/hello" } ,
async ({ event , step , publish }) => {
const { uuid } = event .data;
await publish ( helloChannel (uuid) .logs ( "Hello, world!" ));
}
);
```

By creating a channel with a unique identifier, you can stream updates for a specific run to the end user.

## [Explore the full source code](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-single-run-subscription)

[Clone this example locally to run it and explore the full source code.](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-single-run-subscription)

## [Pattern: Stream updates from multiple function runs](\docs\examples\realtime#pattern-stream-updates-from-multiple-function-runs)

A Realtime channel can be used to stream updates from multiple function runs. Here, we'll define two channels: one global channel and one post-specific channel:

### src/inngest/channels.ts

Copy Copied

```
import {
channel ,
topic ,
} from "@inngest/realtime" ;
import { z } from "zod" ;

export const globalChannel = channel ( "global" ) .addTopic ( topic ( "logs" ) .type < string >());

export const postChannel = channel ((postId : string ) => `post: ${ postId } ` )
.addTopic (
topic ( "updated" ) .schema (
z .object ({
id : z .string () ,
likes : z .number () ,
})
)
)
.addTopic (
topic ( "deleted" ) .schema (
z .object ({
id : z .string () ,
reason : z .string () ,
})
)
);
```

Our `likePost` function will publish updates to both channels:

### src/inngest/functions/likePost.ts

Copy Copied

```
import {
channel ,
realtimeMiddleware ,
subscribe ,
topic ,
} from "@inngest/realtime" ;
import { EventSchemas , Inngest } from "inngest" ;
import { globalChannel , postChannel } from "../channels" ;

export const likePost = app .createFunction (
{
id : "post/like" ,
retries : 0 ,
} ,
{
event : "app/post.like" ,
} ,
async ({
event : {
data : { postId = "123" } ,
} ,
step ,
publish ,
}) => {
if ( ! postId) {
await publish (
globalChannel () .logs ( "Missing postId when trying to like post" )
);
throw new Error ( "Missing postId" );
}

await publish ( globalChannel () .logs ( `Liking post ${ postId } ` ));

// Fake a post update
const post = await step .run ( "Update likes" , async () => {
const fakePost = {
id : "123" ,
likes : Math .floor ( Math .random () * 10000 ) ,
};

return publish ( postChannel ( fakePost .id) .updated (fakePost));
});

return post;
}
);
```

The `globalChannel` will be used to stream updates for all posts, and the `postChannel` will be used to stream updates for specific posts.

## [Explore the full source code](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-across-multiple-channels)

[Clone this example locally to run it and explore the full source code.](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-across-multiple-channels)

## [Human in the loop: Bi-directional workflows](\docs\examples\realtime#human-in-the-loop-bi-directional-workflows)

Combine Realtime with `waitForEvent()` to enable workflows that require user input, such as review or approval steps. Here's how to send a message to the user and wait for their confirmation:

Copy Copied

```
import crypto from "crypto" ;
import { Inngest } from "inngest" ;
import { realtimeMiddleware , channel , topic } from "@inngest/realtime" ;

const inngest = new Inngest ({
id : "my-app" ,
middleware : [ realtimeMiddleware ()] ,
});

export const agenticWorkflowChannel = channel ( "agentic-workflow" ) .addTopic (
topic ( "messages" ) .schema (
z .object ({
message : z .string () ,
confirmationUUid : z .string () ,
})
)
);

export const agenticWorkflow = inngest .createFunction (
{ id : "agentic-workflow" } ,
{ event : "agentic-workflow/start" } ,
async ({ event , step , publish }) => {
await step .run ( /* ... */ );
const confirmationUUid = await step .run ( "get-confirmation-uuid" , async () => crypto .randomUUID ());
await publish ( agenticWorkflowChannel () .messages ({
message : "Confirm to proceed?" ,
confirmationUUid ,
}));
const confirmation = await step .waitForEvent ( "wait-for-confirmation" , {
event : "agentic-workflow/confirmation" ,
timeout : "15m" ,
if : `async.data.confirmationUUid == \" ${ confirmationUUid } \"` ,
});
if (confirmation) {
// continue workflow
}
}
);
```

The `confirmationUUid` links the published message to the reply event, ensuring the correct user response is handled.

## [Explore the full source code](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-human-in-the-loop)

[Clone this example locally to run it and explore the full source code.](https://github.com/inngest/inngest-js/tree/main/examples/realtime/nodejs/realtime-human-in-the-loop)

## [Learn more](\docs\examples\realtime#learn-more)

### [Realtime documentation](\docs\features\realtime)

[Learn more about streaming updates and real-time workflows with Inngest.](\docs\features\realtime)

### [Using Realtime with Next.js](\docs\features\realtime\react-hooks)

[Learn how to use Realtime with Next.js.](\docs\features\realtime\react-hooks)