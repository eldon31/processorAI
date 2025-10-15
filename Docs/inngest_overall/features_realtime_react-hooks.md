#### On this page

- [React hooks / Next.js](\docs\features\realtime\react-hooks#react-hooks-next-js)
- [useInngestSubscription() API Reference](\docs\features\realtime\react-hooks#use-inngest-subscription-api-reference)
- [Parameters](\docs\features\realtime\react-hooks#parameters)
- [Return value](\docs\features\realtime\react-hooks#return-value)
- [Examples](\docs\features\realtime\react-hooks#examples)

Features [Realtime](\docs\features\realtime)

# React hooks / Next.js TypeScript SDK v3.32.0+

Realtime provides a [`useInngestSubscription()`](\docs\features\realtime\react-hooks#use-inngest-subscription-api-reference) React hook, offering a fully typed experience for subscribing to channels.

`useInngestSubscription()` securely subscribes to channels using a subscription token fetched from the server.

In Next.js, this is implemented as a server action that returns a token, which is then used by the client to subscribe:

### src/actions.ts

Copy Copied

```
"use server" ;
// securely fetch an Inngest Realtime subscription token from the server as a server action
export async function fetchSubscriptionToken () : Promise < Realtime . Token < typeof helloChannel , [ "logs" ]>> {
const token = await getSubscriptionToken ( getInngestApp () , {
channel : helloChannel () ,
topics : [ "logs" ] ,
});

return token;
}
```

### src/App.tsx

Copy Copied

```
"use client" ;

import { useInngestSubscription } from "@inngest/realtime/hooks" ;
import { getSubscriptionToken , Realtime } from "@inngest/realtime" ;
import { getInngestApp } from "@/inngest" ;
import { helloChannel } from "@/inngest/functions/helloWorld" ;
// import the server action to securely fetch the Realtime subscription token
import { fetchRealtimeSubscriptionToken } from "./actions" ;

export default function Home () {
// subscribe to the hello-world channel via the subscription token
// `data` is fully typed based on the selected channel and topics!
const { data , error } = useInngestSubscription ({
refreshToken : fetchRealtimeSubscriptionToken ,
});

return (
< div >
< h1 >Realtime</ h1 >
{ data .map ((message , i) => (
< div key = {i}>{ message .data}</ div >
))}
</ div >
)
}
```

## [useInngestSubscription() API Reference](\docs\features\realtime\react-hooks#use-inngest-subscription-api-reference)

### [Parameters](\docs\features\realtime\react-hooks#parameters)

- `enabled?: boolean` - Whether or not the hook will subscribe.
- `bufferInterval?: number` - If set and above `0` , the outputs will only update every `n` milliseconds. This helps with very busy streams that could overwhelm a UI.
- `token?: Realtime.Subscribe.Token` - The token to be used for subscribing (see [Subscribe from the client](\docs\features\realtime#subscribe-from-the-client) ).
- `refreshToken?: () => Promise<Realtime.Subscribe.Token>` - A function that will be called if no `token` is available, or if the hook has been re- `enabled` and the previous `token` has expired.

A `token` or `refreshToken` parameter is required.

### [Return value](\docs\features\realtime\react-hooks#return-value)

- `data: Array<Realtime.Message>` - All messages received on the subscription in chronological order.
- `latestData: Realtime.Message` - A shortcut to the last message received on the subscription. Useful for streams where each message is the latest state of an entity.
- `freshData: Array<Realtime.Message>` - If `bufferInterval` is active, this will be the last batch of messages released from the buffer. If `bufferInterval` is inactive, this is always the latest message.
- `error: Error | null` - If truthy, this indicates an error with the subscription.
- `state: InngestSubscriptionState` - The current state of the subscription, one of `"closed"` , `"error"` , `"refresh_token"` , `"connecting"` , `"active"` , or `"closing"` .
- `clear: () => void` - A function to clear all accumulated message data from the internal state. This includes `data` , `freshData` , and `latestData` arrays. Does not affect the connection or error state.

## [Examples](\docs\features\realtime\react-hooks#examples)

## [useInngestSubscription() Next.js demo](https://github.com/inngest/inngest-js/tree/main/examples/realtime/next-realtime-hooks)

[Clone this demo to see an interactive example of the](https://github.com/inngest/inngest-js/tree/main/examples/realtime/next-realtime-hooks) [`useInngestSubscription()`](https://github.com/inngest/inngest-js/tree/main/examples/realtime/next-realtime-hooks) [hook in action.](https://github.com/inngest/inngest-js/tree/main/examples/realtime/next-realtime-hooks)

## [Explore patterns and examples](\docs\examples\realtime)

[Use Realtime to stream updates from one or multiple Inngest functions, or to implement a Human-in-the-Loop mechanism.](\docs\examples\realtime)