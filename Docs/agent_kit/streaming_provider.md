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

- [Why Use the Provider?](#why-use-the-provider%3F)
- [How It Works](#how-it-works)
- [Usage Patterns](#usage-patterns)
- [Basic Authenticated User](#basic-authenticated-user)
- [Anonymous Users](#anonymous-users)
- [Collaborative Sessions](#collaborative-sessions)
- [Custom Transport Configuration](#custom-transport-configuration)

Streaming

# Provider

A deep dive into the provider for streaming agents

The `AgentProvider` is a React component that creates a shared context for all `useAgent` hooks in your application. While it's optional, using it is highly recommended as it improves performance and ensures configuration consistency.

## [ Why Use the Provider?](#why-use-the-provider%3F)

By wrapping your agent-driven components in `AgentProvider` , you get several key benefits:

- **Performance** : A single WebSocket connection is established and shared across all components, reducing network overhead.
- **Consistency** : A shared transport configuration, user context, and channel key are used by all hooks, preventing inconsistencies.
- **Flexibility** : Individual hooks can still override the shared configuration if needed for specific cases.
- **Anonymous Users** : The provider automatically generates and persists a unique ID for anonymous users, allowing them to have a consistent experience across page loads.

## [ How It Works](#how-it-works)

`AgentProvider` creates a React Context that provides a shared transport instance, connection, and user information to any `useAgent` hook rendered within it. The hooks will automatically detect and use the context if it's available.

If you don't use the provider, each `useAgent` hook will create its own transport and connection, which is less efficient.

## [ Usage Patterns](#usage-patterns)

Here are some common ways to use the `AgentProvider` .

### [ Basic Authenticated User](#basic-authenticated-user)

For an application with logged-in users, pass the user's unique ID to the `userId` prop. This ensures that the agent's context is tied to the correct user.

Copy Ask AI

```
import { AgentProvider } from "@inngest/use-agent" ;
import { ChatPage } from "./ChatPage" ;
import { ThreadsSidebar } from "./ThreadsSidebar" ;

function App ({ userId }) {
return (
< AgentProvider userId = { userId } >
< ChatPage />
< ThreadsSidebar />
</ AgentProvider >
);
}
```

### [ Anonymous Users](#anonymous-users)

If your application supports guest users, you can omit the `userId` prop. The provider will automatically create a unique anonymous ID and store it in `sessionStorage` to maintain a consistent experience for the user during their session.

Copy Ask AI

```
import { AgentProvider } from "@inngest/use-agent" ;
import { GuestChatInterface } from "./GuestChatInterface" ;

function App () {
return (
< AgentProvider >
< GuestChatInterface />
</ AgentProvider >
);
}
```

### [ Collaborative Sessions](#collaborative-sessions)

To create shared, collaborative sessions (e.g., a chat where multiple users interact with the same agent in a shared context), you can use the `channelKey` prop. All users who connect with the same `channelKey` will be subscribed to the same real-time channel.

Copy Ask AI

```
import { AgentProvider } from "@inngest/use-agent" ;
import { CollaborativeChat } from "./CollaborativeChat" ;

function ProjectChat ({ projectId }) {
return (
< AgentProvider channelKey = { `project- ${ projectId } ` } >
< CollaborativeChat />
</ AgentProvider >
);
}
```

### [ Custom Transport Configuration](#custom-transport-configuration)

You can customize the HTTP endpoints and headers used by the transport layer by passing a configuration object to the `transport` prop. This is useful if your API routes don't follow the default conventions.

Copy Ask AI

```
import { AgentProvider } from "@inngest/use-agent" ;

function App ({ userId , getAuthToken }) {
return (
< AgentProvider
userId = { userId }
transport = { {
api: {
sendMessage: '/api/v2/chat' ,
fetchThreads: '/api/v2/threads'
},
headers : () => ({
'Authorization' : `Bearer ${ getAuthToken () } ` ,
})
} }
>
< ChatApp />
</ AgentProvider >
);
}
```

[Transport Previous](\streaming\transport) [Deterministic state routing Next](\advanced-patterns\routing)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.