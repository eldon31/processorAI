#### On this page

- [Subscribing](\docs\features\realtime\subscribe#subscribing)

### [Subscribing](\docs\features\realtime\subscribe#subscribing)

To subscribe to data on the client (browser), you'll need to create a subscription token and use the `subscribe()` function which also requires `channel` and `topic` to be specified.

Your application uses the Inngest SDK to create a token, which is then used by the subscribe function to connect to the Inngest WebSocket server.

1

Create a subscription token

Subscription tokens are required to securely establish a connection to the Inngest WebSocket server.

Your application must create tokens on the server and pass them to the client. You can create a new endpoint to generate a token, ensuring that the user is authorized to subscribe to a given channel and topics.

Here's an example of a server endpoint that creates a token, scoped to a user's channel and specific topics.

Next.js - Server action Express Python - Fast API

Copy Copied

```
// ex. /app/actions/get-subscribe-token.ts
"use server" ;

import { inngest } from "@/inngest/client" ;
// See the "Typed channels (recommended)" section above for more details:
import { userChannel } from "@/inngest/functions/helloWorld" ;
import { getSubscriptionToken , Realtime } from "@inngest/realtime" ;
import { getSession } from "@/app/lib/session" ; // this could be any auth provider

export type UserChannelToken = Realtime . Token < typeof userChannel , [ "ai" ]>;

export async function fetchRealtimeSubscriptionToken () : Promise < UserChannelToken > {
const { userId } = await getSession ();

// This creates a token using the Inngest API that is bound to the channel and topic:
const token = await getSubscriptionToken (inngest , {
channel : `user: ${ userId } ` ,
topics : [ "ai" ] ,
});

return token;
}
```

2

Subscribe to a channel

Once you have a token, you can subscribe to a channel by calling the `subscribe` function with the token. You can also subscribe using the `useInngestSubscription` React hook. Read more about the [React hook here](\docs\features\realtime\react-hooks) .

React hook - useInngestSubscription() Basic subscribe

Copy Copied

```
// ex: ./app/page.tsx
"use client" ;

// ℹ️ Import the hook from the hooks sub-package:
import { useInngestSubscription } from "@inngest/realtime/hooks" ;
import { useState } from "react" ;
import { fetchRealtimeSubscriptionToken } from "./actions" ;

export default function Home () {
// The hook automatically fetches the token from the server.
// The server checks that the user is authorized to subscribe to
// the channel and topic, then returns a token:
const { data , error , freshData , state , latestData } = useInngestSubscription ({
refreshToken : fetchRealtimeSubscriptionToken ,
});

return (
< div >
{data.map((message , i) => (
< div key = {i} > {message.data} </ div >
))}
</ div >
);
}
```

That's all you need to do to subscribe to a channel from the client!