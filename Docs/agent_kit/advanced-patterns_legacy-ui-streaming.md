##### Get Started

- [Overview](\overview)
- [Quick start](\getting-started\quick-start)
- [Installation](\getting-started\installation)
- [Local development](\getting-started\local-development)

##### Concepts

- [Agents](\concepts\agents)
- [Tools](\concepts\tools)
- [Networks](\concepts\networks)
- [State](\concepts\state)
- [Routers](\concepts\routers)
- [History](\concepts\history)
- [Memory](\concepts\memory)
- [Models](\concepts\models)
- [Deployment](\concepts\deployment)

##### Streaming

- [Overview](\streaming\overview)
- [Usage Guide](\streaming\usage-guide)
- [Events](\streaming\events)
- [Transport](\streaming\transport)
- [Provider](\streaming\provider)

##### Advanced Patterns

- [Deterministic state routing](\advanced-patterns\routing)
- [MCP as tools](\advanced-patterns\mcp)
- [Human in the Loop](\advanced-patterns\human-in-the-loop)
- [Multi-steps tools](\advanced-patterns\multi-steps-tools)
- [Configuring Retries](\advanced-patterns\retries)
- [Configuring Multi-tenancy](\advanced-patterns\multitenancy)
- [UI Streaming with useAgent](\advanced-patterns\legacy-ui-streaming)

##### Guided Tour

- [The three levels of AI apps](\guided-tour\overview)
- [1. Explaining a given code file](\guided-tour\ai-workflows)
- [2. Complex code analysis](\guided-tour\agentic-workflows)
- [3. Autonomous Bug Solver](\guided-tour\ai-agents)

##### Integrations

- [E2B - Sandboxes for AI Agents](\integrations\e2b)
- [Browserbase - AI Browsers](\integrations\browserbase)
- [Smithery - MCP Registry](\integrations\smithery)

close

On this page

- [How it Works](#how-it-works)
- [Sequence Diagram](#sequence-diagram)
- [Usage Guide](#usage-guide)
- [1. Backend Setup](#1-backend-setup)
- [Inngest Function](#inngest-function)
- [API Routes](#api-routes)
- [2. Frontend Setup](#2-frontend-setup)
- [API Reference](#api-reference)
- [State Properties](#state-properties)
- [Action Methods](#action-methods)
- [UI Data Models](#ui-data-models)
- [ConversationMessage](#conversationmessage)
- [MessagePart](#messagepart)
- [TextUIPart](#textuipart)
- [ToolCallUIPart](#toolcalluipart)
- [AgentStatus](#agentstatus)

Advanced Patterns

# UI Streaming with useAgent

Stream AgentKit events to your UI with the useAgent hook.

The `useAgent` hook is a powerful client-side hook for React that manages real-time, multi-threaded conversations with an AgentKit network. It encapsulates the entire lifecycle of agent interactions, including sending messages, receiving streaming events, handling out-of-order event sequences, and managing connection state.

While `useChat` is the recommended high-level hook for building chat interfaces, `useAgent` provides the low-level building blocks for more customized implementations where you need direct control over the event stream and state management.

## [use-agent Example](https://github.com/inngest/agent-kit/tree/main/examples/use-agent)

[Find the complete source code for a Next.js chat application using](https://github.com/inngest/agent-kit/tree/main/examples/use-agent) [`useAgent`](https://github.com/inngest/agent-kit/tree/main/examples/use-agent) [on GitHub.](https://github.com/inngest/agent-kit/tree/main/examples/use-agent)

## [ How it Works](#how-it-works)

`useAgent` builds upon Inngest's Realtime capabilities to create a persistent, unified stream of events for a user. Here's a step-by-step breakdown of the data flow:

1. **Client Initialization** : The `useAgent` hook is initialized in your React component. It uses the `useInngestSubscription` hook from `@inngest/realtime/hooks` to establish a WebSocket connection.
2. **Authentication** : To connect, it calls a backend API route (e.g., `/api/realtime/token` ) to get a short-lived subscription token. This token authorizes the client to listen to events on a specific user channel.
3. **Sending a Message** : The user types a message and the UI calls the `sendMessage` function returned by the hook.
4. **API Request** : `sendMessage` makes a `POST` request to a backend API route (e.g., `/api/chat` ). This request contains the message content, the current `threadId` , and the conversation history.
5. **Triggering Inngest** : The chat API route receives the request and sends an `agent/chat.requested` event to Inngest using `inngest.send()` .
6. **Agent Execution** : An Inngest function ( `run-agent-chat.ts` in our example) is triggered by the event. It sets up the AgentKit network, state, and history adapter.
7. **Running the Network** : The Inngest function calls `network.run(message, { streaming: ... })` .
8. **Streaming Events** : As the network and its agents execute, they generate streaming events (e.g., `run.started` , `part.created` , `text.delta` ). The `streaming.publish` function inside the Inngest function forwards these events back to the user's realtime channel.
9. **Realtime Push** : The events are pushed over the WebSocket connection to the client.
10. **State Update** : `useAgent` receives the raw events, processes them in the correct sequence, handles out-of-order events, and updates its internal state.
11. **UI Re-render** : The component using the hook re-renders with the new messages, agent status, and other UI parts.

### [ Sequence Diagram](#sequence-diagram)

## [ Usage Guide](#usage-guide)

### [ 1. Backend Setup](#1-backend-setup)

First, you need to set up the backend infrastructure to handle chat requests and realtime communication.

#### [ Inngest Function](#inngest-function)

This function is the core of your agent's execution. It listens for chat requests and runs your AgentKit network, streaming events back to the client.

inngest/functions/run-agent-chat.ts Copy Ask AI

```
import { inngest } from "../client" ;
import { createCustomerSupportNetwork } from "../networks/customer-support-network" ;
import { userChannel } from "../../lib/realtime" ;
import { createState } from "@inngest/agent-kit" ;
import type { CustomerSupportState } from "../types/state" ;
import { PostgresHistoryAdapter } from "../db" ;

const historyAdapter = new PostgresHistoryAdapter < CustomerSupportState >({});

export const runAgentChat = inngest . createFunction (
{ id: "run-agent-chat" },
{ event: "agent/chat.requested" },
async ({ event , step , publish }) => {
await step . run ( "initialize-db-tables" , () =>
historyAdapter . initializeTables ()
);

const { threadId , message , userId , history , messageId } = event . data ;

const network = createCustomerSupportNetwork (
threadId ,
createState < CustomerSupportState >(
{ customerId: userId },
{ messages: history , threadId }
),
historyAdapter
);

// Run the network and stream events back to the client
const result = await network . run ( message , {
streaming: {
publish : async ( chunk ) => {
const enrichedChunk = {
... chunk ,
data: { ... chunk . data , threadId , userId },
};
await publish ( userChannel ( userId ). agent_stream ( enrichedChunk ));
},
},
messageId ,
});

return { success: true , threadId , result };
}
);
```

#### [ API Routes](#api-routes)

You'll need a few API routes in your Next.js application.

app/api/chat/route.ts Copy Ask AI

```
import { NextRequest , NextResponse } from "next/server" ;
import { inngest } from "@/inngest/client" ;
import { randomUUID } from "crypto" ;

export async function POST ( req : NextRequest ) {
const {
message ,
threadId : providedThreadId ,
userId ,
history ,
messageId ,
} = await req . json ();
const threadId = providedThreadId || randomUUID ();

await inngest . send ({
name: "agent/chat.requested" ,
data: { threadId , message , messageId , history , userId },
});

return NextResponse . json ({ success: true , threadId });
}
```

app/api/realtime/token/route.ts Copy Ask AI

```
import { NextRequest , NextResponse } from "next/server" ;
import { getSubscriptionToken } from "@inngest/realtime" ;
import { inngest } from "@/inngest/client" ;
import { userChannel } from "@/lib/realtime" ;

export async function POST ( req : NextRequest ) {
const { userId } = await req . json ();
// TODO: Add authentication/authorization here
const token = await getSubscriptionToken ( inngest , {
channel: userChannel ( userId ),
topics: [ "agent_stream" ],
});
return NextResponse . json ( token );
}
```

### [ 2. Frontend Setup](#2-frontend-setup)

Now, let's wire up the `useAgent` hook in a React component.

components/ChatComponent.tsx Copy Ask AI

```
"use client" ;

import { useAgent , type ConversationMessage } from "@/hooks/use-agent" ;

const USER_ID = "test-user-123" ;

export function ChatComponent ({ threadId } : { threadId : string }) {
const { messages , status , sendMessage , isConnected , error , clearError } =
useAgent ({
threadId: threadId ,
userId: USER_ID ,
debug: true ,
onError : ( err ) => console . error ( "Agent error:" , err ),
});

const handleSubmit = ( e : React . FormEvent < HTMLFormElement >) => {
e . preventDefault ();
const formData = new FormData ( e . currentTarget );
const message = formData . get ( "message" ) as string ;
if ( message . trim ()) {
sendMessage ( message );
e . currentTarget . reset ();
}
};

return (
< div >
< div > Status: { status } </ div >
< div > Connected: { isConnected ? "Yes" : "No" } </ div >
{ error && (
< div >
Error: { error . message }
< button onClick = { clearError } > Clear </ button >
</ div >
) }

< div className = "message-list" >
{ messages . map (( msg ) => (
< Message key = { msg . id } message = { msg } />
)) }
</ div >

< form onSubmit = { handleSubmit } >
< input
name = "message"
placeholder = "Ask anything..."
disabled = { status !== "idle" }
/>
< button type = "submit" disabled = { status !== "idle" } >
Send
</ button >
</ form >
</ div >
);
}

// A simple component to render a message with all its parts
function Message ({ message } : { message : ConversationMessage }) {
return (
< div className = { `message ${ message . role } ` } >
< strong > { message . role } </ strong >
{ message . parts . map (( part , index ) => {
switch ( part . type ) {
case "text" :
return < p key = { index } > { part . content } </ p > ;
case "tool-call" :
return (
< div
key = { index }
className = "tool-call"
style = { {
border: "1px solid #ccc" ,
padding: "10px" ,
marginTop: "10px" ,
borderRadius: "5px" ,
} }
>
< div >
< strong > Tool Call: </ strong > { part . toolName }
</ div >
< pre style = { { whiteSpace: "pre-wrap" , wordBreak: "break-all" } } >
Status: { part . state }
< br />
Input: { JSON . stringify ( part . input , null , 2 ) }
{ part . output && (
<>
< br />
Output: { JSON . stringify ( part . output , null , 2 ) }
</>
) }
</ pre >
</ div >
);
// TODO: Add cases for other part types like 'data', 'reasoning', etc.
default :
return null ;
}
}) }
</ div >
);
}
```

## [ API Reference](#api-reference)

The `useAgent` hook returns an object with the following properties and methods.

### [ State Properties](#state-properties)

[](#param-messages) messages ConversationMessage[] The array of messages for the **current thread** . Each message contains an

array of

`parts` that are streamed in real-time.

[](#param-status) status AgentStatus The current status of the agent for the active thread. It can be one of: `"idle"` , `"thinking"` , `"calling-tool"` , `"responding"` , or `"error"` .

[](#param-error) error { message: string; ... } | undefined An object containing details about the last error that occurred in the active

thread.

`undefined` if there is no error.

[](#param-threads) threads Record&lt;string, ThreadState&gt; An object containing the full state for all active threads, indexed by `threadId` . This allows you to manage multiple conversations in the

background.

[](#param-current-thread-id) currentThreadId string The ID of the currently active/displayed thread.

[](#param-is-connected) isConnected boolean `true` if the client is currently connected to the Inngest Realtime server.

[](#param-connection-error) connectionError { message: string; ... } | undefined An object containing details about a connection-level error (e.g., failure to

get a subscription token).

### [ Action Methods](#action-methods)

[](#param-send-message) sendMessage (message: string) =&gt; Promise&lt;void&gt; Sends a message to the **current thread** . It handles optimistic UI updates

and formats the history for the backend.

[](#param-send-message-to-thread) sendMessageToThread (threadId: string, message: string) =&gt; Promise&lt;void&gt; Sends a message to a **specific thread** , which can be different from the

currently active one.

[](#param-set-current-thread) setCurrentThread (threadId: string) =&gt; void Switches the active thread. This updates which thread's state is exposed via

the top-level

`messages` , `status` , and `error` properties.

[](#param-create-thread) createThread (threadId: string) =&gt; void Creates a new, empty thread in the local state.

[](#param-clear-messages) clearMessages () =&gt; void Clears all messages from the **current thread's** local state.

[](#param-replace-messages) replaceMessages (messages: ConversationMessage[]) =&gt; void Replaces all messages in the **current thread's** local state. Useful for

loading historical messages.

[](#param-clear-error) clearError () =&gt; void Clears the error state for the **current thread** .

[](#param-clear-connection-error) clearConnectionError () =&gt; void Clears any connection-level error.

## [ UI Data Models](#ui-data-models)

The `useAgent` hook exposes a set of rich UI data models to make building chat interfaces easier. These types define the structure of messages and their constituent parts.

### [ ConversationMessage](#conversationmessage)

Represents a complete message in the conversation, containing one or more parts.

Copy Ask AI

```
export interface ConversationMessage {
/** Unique identifier for this message */
id : string ;
/** Whether this message is from the user or the assistant */
role : "user" | "assistant" ;
/** Array of message parts that make up the complete message */
parts : MessagePart [];
/** ID of the agent that created this message (for assistant messages) */
agentId ?: string ;
/** When this message was created */
timestamp : Date ;
/** The status of the message, particularly for optimistic user messages */
status ?: "sending" | "sent" | "failed" ;
}
```

### [ MessagePart](#messagepart)

A union type representing all possible parts of a message.

Copy Ask AI

```
export type MessagePart =
| TextUIPart
| ToolCallUIPart
| DataUIPart
| FileUIPart
| SourceUIPart
| ReasoningUIPart
| StatusUIPart
| ErrorUIPart
| HitlUIPart ;
```

### [ TextUIPart](#textuipart)

Represents a text message part that can be streamed character by character.

Copy Ask AI

```
export interface TextUIPart {
type : "text" ;
/** Unique identifier for this text part */
id : string ;
/** The text content, updated incrementally during streaming */
content : string ;
/** Whether the text is still being streamed or is complete */
status : "streaming" | "complete" ;
}
```

### [ ToolCallUIPart](#toolcalluipart)

Represents a tool call that the agent is making, with streaming input and output.

Copy Ask AI

```
export interface ToolCallUIPart {
type : "tool-call" ;
/** Unique identifier for this tool call */
toolCallId : string ;
/** Name of the tool being called */
toolName : string ;
/** Current state of the tool call execution */
state :
| "input-streaming"
| "input-available"
| "awaiting-approval"
| "executing"
| "output-available" ;
/** Tool input parameters, streamed incrementally */
input : any ;
/** Tool output result, if available */
output ?: any ;
/** Error information if the tool call failed */
error ?: any ;
}
```

*(For brevity, other part types like* *`DataUIPart`* *,* *`ReasoningUIPart`* *, etc., are omitted here but follow a similar structure. You can find their full definitions in the* *`use-agent.ts`* *file in the example.)*

### [ AgentStatus](#agentstatus)

Represents the current activity status of the agent.

Copy Ask AI

```
export type AgentStatus =
| "idle"
| "thinking"
| "calling-tool"
| "responding"
| "error" ;
```

[Configuring Multi-tenancy Previous](\advanced-patterns\multitenancy) [The three levels of AI apps Next](\guided-tour\overview)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.