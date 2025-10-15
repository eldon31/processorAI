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

- [Understanding the Event Lifecycle](#understanding-the-event-lifecycle)
- [Core Events Reference](#core-events-reference)
- [Run Lifecycle Events](#run-lifecycle-events)
- [run.started](#run-started)
- [run.completed](#run-completed)
- [stream.ended](#stream-ended)
- [Content Streaming Events](#content-streaming-events)
- [part.created](#part-created)
- [text.delta](#text-delta)
- [part.completed](#part-completed)
- [Tool Call Events](#tool-call-events)
- [tool\_call.arguments.delta](#tool-call-arguments-delta)
- [tool\_call.output.delta](#tool-call-output-delta)
- [Consuming Events in Your App](#consuming-events-in-your-app)
- [onEvent](#onevent)
- [onToolResult](#ontoolresult)
- [onStreamEnded](#onstreamended)

Streaming

# Events

The `use-agent` hook is built on an event-driven architecture. Real-time events are streamed from the server, processed by a state reducer, and used to build the conversation UI incrementally. This document details the events, their purpose, and how you can use them.

## [ Understanding the Event Lifecycle](#understanding-the-event-lifecycle)

1

Raw Event Streaming

A raw message is received from the Inngest realtime websocket connection

2

Mapping

The raw message is passed to an internal `mapToNetworkEvent` function, which transforms it into a standardized, strongly-typed `AgentKitEvent` . Invalid or unrecognized messages are discarded.

3

Dispatch

The valid `AgentKitEvent` is dispatched to the internal `StreamingEngine` .

4

Reduction

The `streaming-reducer` processes the event. It uses a sequencing and buffering mechanism to ensure events are applied in the correct order, even if they arrive out of order.

5

State Update

The reducer applies the event to the state, creating or updating messages and their parts.

6

UI Render

Your React UI re-renders with the new state.

7

Callbacks

If configured, `onEvent` , `onStreamEnded` , or `onToolResult` callbacks are fired, allowing you to react to specific events.

## [ Core Events Reference](#core-events-reference)

### [ Run Lifecycle Events](#run-lifecycle-events)

These events manage the overall state of an agent or network execution for a given turn.

#### [ run.started](#run-started)

- **Description** : Marks the beginning of an agent or network execution in response to a user message. This is often the first event in a sequence. It sets the agent's status to `submitted` .
- **Payload (** **`data`** **)** :
    - `threadId` : The ID of the thread this run belongs to.
    - `name` : The name of the agent or network that started.
    - `scope` : `"network"` or `"agent"` .
    - `runId` , `parentRunId` , `messageId` .
- **State Impact** : Sets `runActive: true` , `agentStatus: 'submitted'` , and may reset the event processing sequence if it's the start of a new "epoch".

#### [ run.completed](#run-completed)

- **Description** : Indicates that an agent or network run has finished its logic. This does *not* mean all streaming is complete. It primarily finalizes any in-flight tool outputs.
- **Payload (** **`data`** **)** : `threadId` , `scope` , `runId` , `messageId` , `name` .
- **State Impact** : Finalizes the state of any tools that were in the `executing` state, moving them to `output-available` . The overall agent status is not yet changed to `ready` .

#### [ stream.ended](#stream-ended)

- **Description** : The final event in a sequence. It indicates that all streaming for a turn is complete and the agent is now idle.
- **Payload (** **`data`** **)** : `threadId` , `scope` , `runId` , `messageId` , `name` .
- **State Impact** : Sets `runActive: false` and `agentStatus: 'ready'` . This signals that the system is ready for new user input.

### [ Content Streaming Events](#content-streaming-events)

These events are responsible for building the assistant's response message part by part.

#### [ part.created](#part-created)

- **Description** : Signals the creation of a new part within an assistant message.
- **Payload (** **`data`** **)** :
    - `messageId` : The ID of the message this part belongs to.
    - `partId` : The unique ID for this new part.
    - `type` : Either `"text"` or `"tool-call"` .
    - `metadata` : Optional data, often includes `toolName` for tool calls.
- **State Impact** : Adds a new, empty `TextUIPart` or `ToolCallUIPart` to the parts array of the corresponding message.

#### [ text.delta](#text-delta)

- **Description** : Streams a chunk of text for a `TextUIPart` .
- **Payload (** **`data`** **)** :
    - `messageId` , `partId` .
    - `delta` : The string of text to append.
- **State Impact** : Appends the `delta` content to the specified `TextUIPart` .

#### [ part.completed](#part-completed)

- **Description** : Marks a specific message part as complete. The payload varies based on the part type.
- **Payload (** **`data`** **)** :
    - `messageId` , `partId` .
    - `type` : Can be `"text"` , `"tool-call"` , or `"tool-output"` .
    - `finalContent` : The complete, final content for the part (e.g., the full text or final tool output).
- **State Impact** :
    - For `"text"` : Sets the part's `status` to `complete` .
    - For `"tool-call"` : Sets the tool's `state` to `input-available` and populates the final `input` .
    - For `"tool-output"` : Sets the tool's `state` to `output-available` and populates the final `output` .

### [ Tool Call Events](#tool-call-events)

These events are specific to the lifecycle of tool calls made by an agent.

#### [ tool\_call.arguments.delta](#tool-call-arguments-delta)

- **Description** : Streams a chunk of the JSON arguments for a tool call.
- **Payload (** **`data`** **)** :
    - `messageId` , `partId` .
    - `delta` : A string chunk of the JSON arguments object.
- **State Impact** : Appends the `delta` to the `input` field of the `ToolCallUIPart` . The reducer attempts to parse the accumulating string as JSON. Sets the tool's `state` to `input-streaming` .

#### [ tool\_call.output.delta](#tool-call-output-delta)

- **Description** : Streams a chunk of the output from a tool execution.
- **Payload (** **`data`** **)** :
    - `messageId` , `partId` .
    - `delta` : A string chunk of the tool's output.
- **State Impact** : Appends the `delta` to the `output` field of the `ToolCallUIPart` . Sets the tool's `state` to `executing` .

## [ Consuming Events in Your App](#consuming-events-in-your-app)

The `useAgent` hook provides callbacks to tap into this event stream.

### [ onEvent](#onevent)

This is the lowest-level callback. It fires for every single valid `AgentKitEvent` that the hook processes, giving you full visibility into the streaming process.

Copy Ask AI

```
useAgent ({
onEvent : ( evt , meta ) => {
console . log ( 'Event received:' , evt . event , 'for thread:' , meta . threadId );
if ( evt . event === 'run.started' ) {
// Show a global "thinking" indicator
}
}
})
```

### [ onToolResult](#ontoolresult)

A convenient, strongly-typed callback that fires only when a tool has finished executing and its final output is available ( `part.completed` with `type: "tool-output"` ).

Copy Ask AI

```
useAgent < MyAgentConfig >({
onToolResult : ( result ) => {
if ( result . toolName === 'getWeather' ) {
const weatherData = result . data ; // strongly typed!
// Display a custom weather component
}
}
})
```

### [ onStreamEnded](#onstreamended)

Fires when the entire sequence of events for a turn is complete ( `stream.ended` ). Useful for triggering actions after the assistant has fully responded.

Copy Ask AI

```
useAgent ({
onStreamEnded : ({ threadId }) => {
console . log ( `Agent has finished responding in thread ${ threadId } .` );
// Maybe run some analytics or enable the input field
}
})
```

[Usage Guide Previous](\streaming\usage-guide) [Transport Next](\streaming\transport)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.