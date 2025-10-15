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

- [Overview](#overview)
- [HistoryConfig Interface](#historyconfig-interface)
- [createThread](#createthread)
- [get](#get)
- [appendUserMessage](#appendusermessage)
- [appendResults](#appendresults)
- [Usage](#usage)
- [Persistence Patterns](#persistence-patterns)
- [Server-Authoritative](#server-authoritative)
- [Client-Authoritative (Performance Optimized)](#client-authoritative-performance-optimized)
- [Server/Client Hybrid Pattern](#server%2Fclient-hybrid-pattern)
- [How Thread IDs Are Managed](#how-thread-ids-are-managed)
- [Thread Initialization Flow](#thread-initialization-flow)
- [Best Practices](#best-practices)
- [Future Enhancements](#future-enhancements)
- [Complete Example](#complete-example)

Concepts

# History

Learn how to persist conversations for your agents and networks

## [ Overview](#overview)

AgentKit enables persistent conversations that maintain context across multiple runs. By implementing a **History Adapter** , you can connect your agents and networks to any database or storage solution, allowing conversations to resume exactly where they left off.

A History Adapter is a configuration object that bridges AgentKit's execution lifecycle with your database. It tells AgentKit how to:

1. **Create** new conversation threads
2. **Load** existing conversation history
3. **Save** new messages and results

AgentKit is database-agnostic. You can use PostgreSQL, MongoDB, Redis, or any

storage solution by implementing the

`HistoryConfig` interface.

The adapter is passed to `createAgent()` or `createNetwork()` and AgentKit automatically calls your adapter's methods at the appropriate times during execution.

### [ HistoryConfig Interface](#historyconfig-interface)

The `HistoryConfig` interface has four optional methods. Below is an expanded view of the interface showing the context and parameters passed to each method.

Copy Ask AI

```
import type {
State ,
NetworkRun ,
AgentResult ,
GetStepTools ,
StateData ,
} from "@inngest/agent-kit" ;

interface HistoryConfig < T extends StateData > {
/**
* Creates a new conversation thread or ensures it exists.
* Invoked at the start of a run to initialize the thread.
*/
createThread ?: ( ctx : {
state : State < T >; // The current state, including your custom data
input : string ; // The user's input string
network ?: NetworkRun < T >; // The network instance (if applicable)
step ?: GetStepTools ; // Inngest step tools for durable execution
}) => Promise <{ threadId : string }>;

/**
* Retrieves conversation history from your database.
* Invoked after thread initialization if no history is provided by the client.
*/
get ?: ( ctx : {
threadId ?: string ; // The ID of the conversation thread
state : State < T >;
input : string ;
network : NetworkRun < T >;
step ?: GetStepTools ;
}) => Promise < AgentResult []>;

/**
* Saves the user's message at the beginning of a run.
* Invoked immediately after thread initialization, before any agents run.
*/
appendUserMessage ?: ( ctx : {
threadId ?: string ;
userMessage : {
id : string ; // Canonical, client-generated message ID
content : string ;
role : "user" ;
timestamp : Date ;
};
state : State < T >;
input : string ;
network : NetworkRun < T >;
step ?: GetStepTools ;
}) => Promise < void >;

/**
* Saves new agent results to your database after a run.
* Invoked at the end of a successful agent or network run.
*/
appendResults ?: ( ctx : {
threadId ?: string ;
newResults : AgentResult []; // The new results generated during this run
state : State < T >;
input : string ;
network : NetworkRun < T >;
step ?: GetStepTools ;
}) => Promise < void >;
}
```

#### [ createThread](#createthread)

- Creates a new conversation thread in your database or ensures an existing thread is present
- Invoked at the start of a run to initialize the thread
- **Important** : If a `threadId` already exists in the state, your adapter should upsert (insert or update) to ensure the thread exists in storage
- Returns an object with the `threadId`

#### [ get](#get)

- Retrieves conversation history from your database
- Invoked after thread initialization, but **only if** :
    - A `threadId` is present in the state
    - The client didn't provide `results` or `messages`
    - The thread was not just created in this run (client provided the threadId)
- Returns an array of `AgentResult[]` representing the conversation history
- **Recommended** : Include both user messages and agent results by converting user messages to `AgentResult` objects with `agentName: "user"` to preserve conversation order

#### [ appendUserMessage](#appendusermessage)

- Saves the user's message immediately at the beginning of a run
- Invoked after thread initialization but before any agents execute
- Ensures user intent is captured even if the agent run fails (enables "regenerate" workflows)
- Receives the user's message with a canonical, client-generated ID for idempotency

#### [ appendResults](#appendresults)

- Saves new agent results to your database after a network or agent run
- Invoked at the end of a successful agent or network run
- Receives only the *new* results generated during this run (AgentKit automatically filters out historical results to prevent duplicates)

## [ Usage](#usage)

Here's a complete example of creating a network with history persistence:

Copy Ask AI

```
import {
createNetwork ,
createAgent ,
createState ,
openai ,
} from "@inngest/agent-kit" ;
import { db } from "./db" ; // Your database client

// Define your history adapter with all four methods
const conversationHistoryAdapter : HistoryConfig < any > = {
// 1. Create new conversation threads (or ensure they exist)
createThread : async ({ state , input }) => {
// If a threadId already exists, upsert to ensure it's in the database
if ( state . threadId ) {
await db . thread . upsert ({
where: { id: state . threadId },
update: { updatedAt: new Date () },
create: {
id: state . threadId ,
userId: state . data . userId ,
title: input . slice ( 0 , 50 ),
createdAt: new Date (),
},
});
return { threadId: state . threadId };
}

// Otherwise, create a new thread
const thread = await db . thread . create ({
data: {
userId: state . data . userId ,
title: input . slice ( 0 , 50 ), // First 50 chars as title
createdAt: new Date (),
},
});
return { threadId: thread . id };
},

// 2. Load conversation history (including user messages)
get : async ({ threadId }) => {
if ( ! threadId ) return [];

const messages = await db . message . findMany ({
where: { threadId },
orderBy: { createdAt: "asc" },
});

// Transform ALL messages (user + agent) to AgentResult format
// This preserves the complete conversation order
return messages . map (( msg ) => {
if ( msg . role === "user" ) {
// Convert user messages to AgentResult with agentName: "user"
return new AgentResult (
"user" ,
[
{
type: "text" as const ,
role: "user" as const ,
content: msg . content ,
stop_reason: "stop" ,
},
],
[],
new Date ( msg . createdAt )
);
} else {
// Return agent results
return new AgentResult (
msg . agentName ,
[
{
type: "text" as const ,
role: "assistant" as const ,
content: msg . content ,
},
],
[],
new Date ( msg . createdAt )
);
}
});
},

// 3. Save user message immediately (before agents run)
appendUserMessage : async ({ threadId , userMessage }) => {
if ( ! threadId ) return ;

await db . message . create ({
data: {
messageId: userMessage . id , // Use canonical client-generated ID
threadId ,
role: "user" ,
content: userMessage . content ,
createdAt: userMessage . timestamp ,
},
});
},

// 4. Save agent results after the run
appendResults : async ({ threadId , newResults }) => {
if ( ! threadId ) return ;

// Save only agent responses (user message already saved)
for ( const result of newResults ) {
const content = result . output
. filter (( msg ) => msg . type === "text" )
. map (( msg ) => msg . content )
. join ( " \n " );

await db . message . create ({
data: {
messageId: result . id || crypto . randomUUID (), // Use result.id if available
threadId ,
role: "assistant" ,
agentName: result . agentName ,
content ,
checksum: result . checksum , // For idempotency
createdAt: result . createdAt ,
},
});
}
},
};
```

Once you've created your adapter, pass it to the `history` property when creating an agent or network:

Agent Network Copy Ask AI

```
import { createAgent } from "@inngest/agent-kit" ;
import { postgresHistoryAdapter } from "./my-postgres-adapter" ;

const chatAgent = createAgent ({
name: "chat-agent" ,
system: "You are a helpful assistant." ,
history: postgresHistoryAdapter , // Add your adapter here
});

// Now the agent will automatically persist conversations
await chatAgent . run ( "Hello!" , {
state: createState ({ userId: "user123" }, { threadId: "thread-456" }),
});
```

## [ Persistence Patterns](#persistence-patterns)

AgentKit supports two distint patterns for managing conversation history.

### [ Server-Authoritative](#server-authoritative)

The client sends a message with a `threadId` . AgentKit automatically loads the full conversation context from your database before the network runs.

Copy Ask AI

```
// Client sends just the threadId
const state = createState (
{ userId: "user123" },
{ threadId: "existing-thread-id" }
);

await chatNetwork . run ( "Continue our conversation" , { state });
// AgentKit calls history.get() to load full context for all agents
```

**Use case** : Perfect for restoring conversations after page refresh or when opening the app on a new device.

### [ Client-Authoritative (Performance Optimized)](#client-authoritative-performance-optimized)

The client maintains conversation state locally and sends the complete history with each request. AgentKit detects this and skips the database read for better performance.

Copy Ask AI

```
// Client sends the full conversation history
const state = createState (
{ userId: "user123" },
{
threadId: "thread-id" ,
results: previousConversationResults , // Full history from client
}
);

await chatNetwork . run ( "New message" , { state });
// AgentKit skips history.get() call - faster performance!
// Still calls appendUserMessage() and appendResults() to save new messages
```

**Use case** : Ideal for interactive chat applications where the frontend maintains conversation state and fetches messages from an existing/separate API

**Note** : Providing either `results` or `messages` to `createState` will disable the `history.get()` call, enabling this client-authoritative pattern.

### [ Server/Client Hybrid Pattern](#server%2Fclient-hybrid-pattern)

You can combine the Server-Authoritative and Client-Authoritative patterns for an optimal user experience. This hybrid approach allows for fast initial conversation loading and high-performance interactive chat.

1. **Initial Load (Server-Authoritative):** When a user opens a conversation thread, the client sends only the `threadId` . AgentKit fetches the history from your database using `history.get()` . The application then hydrates the client-side state with this history.
2. **Interactive Session (Client-Authoritative):** For all subsequent requests within the session, the client sends the full, up-to-date history ( `results` or `messages` ) along with the `threadId` . AgentKit detects the client-provided history and skips the database read, resulting in a faster response.

**Use case** : Ideal for interactive chat applications where the frontend maintains conversation state but lets AgentKit fetch messages via their history adapter

## [ How Thread IDs Are Managed](#how-thread-ids-are-managed)

AgentKit offers a flexible system for managing conversation thread IDs, ensuring that history is handled correctly whether you're starting a new conversation or continuing an existing one. Here's how AgentKit determines which `threadId` to use:

### [ Thread Initialization Flow](#thread-initialization-flow)

| Scenario                    | ``` threadId ```  provided?   | ``` createThread ```  exists?   | Behavior                                                                   |
|-----------------------------|-------------------------------|---------------------------------|----------------------------------------------------------------------------|
| Resume existing thread      | ✅ Yes                        | ✅ Yes                          | ``` createThread ```  Calls to upsert/ensure thread exists in DB           |
| Resume existing thread      | ✅ Yes                        | ❌ No                           | ``` threadId ```  Uses provided directly                                   |
| New conversation            | ❌ No                         | ✅ Yes                          | ``` createThread ```  ``` threadId ```  Calls to create new thread and get |
| New conversation (fallback) | ❌ No                         | ``` get ```  ❌ No (but exists) | ``` threadId ```  Auto-generates UUID as                                   |

1. **Explicit** **`threadId`** **with** **`createThread`** **:** When you provide a `threadId` and your adapter has a `createThread` method, AgentKit calls `createThread` to ensure the thread exists in your database. Your adapter should implement an **upsert** pattern (insert if new, update if exists) to handle both new and existing threads gracefully. Copy Ask AI `// Continue a specific, existing conversation const state = createState ( { userId: "user-123" }, { threadId: "existing-thread-id-123" } ); await network . run ( "Let's pick up where we left off." , { state }); // createThread is called to ensure thread exists in DB // Then history.get() loads the conversation history`
2. **Automatic Creation via** **`createThread`** **:** If you don't provide a `threadId` , AgentKit checks if your history adapter has a `createThread` method. If so, AgentKit calls it to create a new conversation thread in your database. Your `createThread` function is responsible for generating and returning the new unique `threadId` . This is the recommended approach for starting new conversations, as it ensures a record is created in your backend from the very beginning. Copy Ask AI `// Start a new conversation const state = createState ({ userId: "user-123" }); await network . run ( "Hello!" , { state }); // createThread is called to create a new thread // state.threadId is set to the new thread ID`
3. **Automatic Generation (Fallback):** In cases where you don't provide a `threadId` and your history adapter does *not* have a `createThread` method but *does* have a `get` method, AgentKit provides a fallback. It will automatically generate a standard UUID and assign it as the `threadId` for the current run. This convenience ensures the conversation can proceed with a unique identifier for saving and loading history, even without an explicit creation step. Copy Ask AI `// Fallback: UUID is generated automatically const state = createState ({ userId: "user-123" }); await network . run ( "Hello!" , { state }); // state.threadId is set to a new UUID // appendUserMessage and appendResults can use this ID`

## [ Best Practices](#best-practices)

Implement Idempotency with Message IDs and Checksums

Use unique constraints on `message_id` and `checksum` to prevent duplicate messages during retries or streaming scenarios.

Copy Ask AI

```
CREATE TABLE messages (
id SERIAL PRIMARY KEY ,
message_id UUID NOT NULL ,
thread_id UUID NOT NULL ,
message_type TEXT NOT NULL , -- 'user' or 'agent'
content TEXT ,
checksum TEXT NOT NULL ,
created_at TIMESTAMP DEFAULT NOW (),
UNIQUE (thread_id, message_id), -- Prevent duplicate message IDs
UNIQUE (thread_id, checksum ) -- Prevent duplicate content
);
```

Copy Ask AI

```
appendUserMessage : async ({ threadId , userMessage }) => {
await db . message . create ({
data: {
messageId: userMessage . id , // Use canonical client ID
threadId ,
content: userMessage . content ,
checksum: generateChecksum ( userMessage ),
},
});
},

appendResults : async ({ threadId , newResults }) => {
for ( const result of newResults ) {
await db . message . create ({
data: {
messageId: result . id || crypto . randomUUID (),
threadId ,
checksum: result . checksum , // Built-in checksum
// ... other fields
},
});
}
}
```

Leverage Inngest's Durable Steps

Wrap database operations in `step.run()` for automatic retries and durability.

Copy Ask AI

```
appendUserMessage : async ({ threadId , userMessage , step }) => {
if ( step ) {
return await step . run ( "save-user-message" , async () => {
return await db . saveMessage ( threadId , userMessage );
});
}
return await db . saveMessage ( threadId , userMessage );
}
```

Handle Missing Threads Gracefully

If a thread doesn't exist, return an empty array rather than throwing an error.

Copy Ask AI

```
get : async ({ threadId }) => {
if ( ! threadId ) return [];

const messages = await db . getMessages ( threadId );
return messages || []; // Handle null/undefined gracefully
}
```

Index Your Database Properly

Ensure you have indexes on key columns for fast queries.

Copy Ask AI

```
CREATE INDEX idx_messages_thread_id ON messages(thread_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_type ON messages(message_type);
CREATE INDEX idx_messages_message_id ON messages(message_id);
```

Return Complete Conversation History

Include both user messages and agent results in your `get()` method to preserve conversation order.

Copy Ask AI

```
get : async ({ threadId }) => {
const messages = await db . message . findMany ({
where: { threadId },
orderBy: { createdAt: "asc" },
});

// Convert ALL messages (user + agent) to AgentResult format
return messages . map (( msg ) => {
if ( msg . role === "user" ) {
return new AgentResult ( "user" , [
{ type: "text" , role: "user" , content: msg . content }
], [], new Date ( msg . createdAt ));
} else {
return new AgentResult ( msg . agentName , [
{ type: "text" , role: "assistant" , content: msg . content }
], [], new Date ( msg . createdAt ));
}
});
}
```

Implement Upsert in createThread

Handle both new and existing threads gracefully by implementing an upsert pattern.

Copy Ask AI

```
createThread : async ({ state }) => {
if ( state . threadId ) {
// Upsert: ensure existing thread is in DB
await db . thread . upsert ({
where: { id: state . threadId },
update: { updatedAt: new Date () },
create: { id: state . threadId , userId: state . data . userId },
});
return { threadId: state . threadId };
}

// Create new thread
const thread = await db . thread . create ({
data: { userId: state . data . userId },
});
return { threadId: thread . id };
}
```

## [ Future Enhancements](#future-enhancements)

The history system provides a foundation for advanced features to be released in the coming future including:

- **Database Adapters** : Pre-built adapters for popular databases (coming soon)
- **Progressive Summarization** : Automatic conversation compression for long threads
- **Search &amp; Retrieval** : Semantic search across conversation history

## [ Complete Example](#complete-example)

Check out the [AgentKit Starter](https://github.com/inngest/agent-kit/tree/main/examples/agentkit-starter) for a complete implementation featuring:

- PostgreSQL history adapter
- ChatGPT-style UI with thread management
- Real-time streaming responses
- Both server and client-authoritative patterns

The starter includes everything you need to build a conversational AI application with persistent history.

[Routers Previous](\concepts\routers) [Memory Next](\concepts\memory)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.