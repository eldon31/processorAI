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

Streaming

# Overview

Realtime event streaming with AgentKit + useAgent

With a useAgent hook you can seamlessly stream a network of agents, a single agent and durable steps within tools used by your agents. You can think of useAgent as the bridge between durable agents and your user interface.

Instead of stitching together events, workflow steps and token streams - your UI receives structured events that describe lifecycles, content parts, tool calls and completions. This hook consumes these events and maintains your UI state for a single conversation or many conversations in parallel.

Here's a simple example of how you would use the hook in your React component:

Copy Ask AI

```
import { useAgent } from "@inngest/use-agent" ;

export function MyAgentUI () {
const { messages , sendMessage , status } = useAgent ();

const onSubmit = ( e ) => {
e . preventDefault ();
const value = new FormData ( e . currentTarget ). get ( "input" );
sendMessage ( value );
};

return (
< div >
< ul >
{ messages . map (({ id , role , parts }) => (
< li key = { id } >
< div > { role } </ div >
{ parts . map (({ id , type , content }) =>
type === "text" ? < div key = { id } > { content } </ div > : null
) }
</ li >
)) }
</ ul >

< form onSubmit = { onSubmit } >
< input name = "input" />
< button type = "submit" disabled = { status !== "ready" } >
Send
</ button >
</ form >
</ div >
);
}
```

Let's take a closer look at what components, endpoints and other files we will need to wire this all up:

- **Inngest Client (** **`/api/inngest/client.ts`** **)** : Initializes Inngest with the `realtimeMiddleware` .
- **Realtime Channel (** **`/api/inngest/realtime.ts`** **)** : Defines a typed realtime channel and topic.
- **Chat Route:** **`/api/chat/route.ts`** : This is a standard Next.js API route. Its only job is to receive a request from the frontend and send an event to Inngest to trigger a function.
- **Token Route:** **`/api/realtime/token/route.ts`** : This secure endpoint generates a subscription token that the frontend needs to connect to Inngest realtime.
- **Inngest Route:** **`/api/inngest/route.ts`** : The standard handler that serves all your Inngest functions.

Once you've configured all the foundational endpoints needed for streaming, you'll want to create some agents, define types and integrate this into a UI:

1

Define server-side types

Define your server-side state type, import all your tools and pass them into `createToolManifest` to generate a type that you will use in your UI.

Copy Ask AI

```
import { createToolManifest , type StateData } from "@inngest/agent-kit" ;
import { selectEventsTool } from "./event-matcher" ;
import { generateSqlTool } from "./query-writer" ;

// server-side state used by networks, routers and agents
export type AgentState = StateData & {
userId ?: string ;
eventTypes ?: string [];
schemas ?: Record < string , unknown >;
selectedEvents ?: { event_name : string ; reason : string }[];
currentQuery ?: string ;
sql ?: string ;
};

// a typed manifest of all available tools
const manifest = createToolManifest ([
generateSqlTool ,
selectEventsTool ,
] as const );

export type ToolManifest = typeof manifest ;
```

2

Define client-side types

Create a `ClientState` type which will type state that your UI will send to your agent backend. This is a great place to pass along important context about the user or what they're doing in your app.

Copy Ask AI

```
import {
useAgent ,
type AgentKitEvent ,
type UseAgentsConfig ,
type UseAgentsReturn ,
} from "@inngest/use-agent" ;

import type { ToolManifest } from "@/app/api/inngest/functions/agents/types" ;

export type ClientState = {
sqlQuery : string ;
eventTypes : string [];
schemas : Record < string , unknown > | null ;
currentQuery : string ;
};

export type AgentConfig = { tools : ToolManifest ; state : ClientState };

export type AgentEvent = AgentKitEvent < ToolManifest >;

export function useInsightsAgent (
config : UseAgentsConfig < ToolManifest , ClientState >
) : UseAgentsReturn < ToolManifest , ClientState > {
return useAgent <{ tools : ToolManifest ; state : ClientState }>( config );
}
```

3

Create agents and an Inngest function to run them

4

Integrate a useAgent hook into your UI

For a deeper dive into streaming agents, check out our [Usage Guide](\streaming\usage-guide) .

[Deployment Previous](\concepts\deployment) [Usage Guide Next](\streaming\usage-guide)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.