##### Introduction

- [Introduction](\reference\introduction)

##### Agent

- [createAgent](\reference\create-agent)
- [createTool](\reference\create-tool)

##### Network

- [createNetwork](\reference\create-network)
- [createState](\reference\state)
- [Router](\reference\network-router)

##### Models

- [OpenAI Model](\reference\model-openai)
- [Anthropic Model](\reference\model-anthropic)
- [Gemini Model](\reference\model-gemini)
- [Grok Model](\reference\model-grok)

##### Streaming

- [useAgent](\reference\use-agent)

close

On this page

- [Creating State](#creating-state)
- [Reading and Modifying State's data (state.data)](#reading-and-modifying-state%E2%80%99s-data-state-data)
- [State History](#state-history)
- [InferenceResult](#inferenceresult)
- [Message Types](#message-types)

Network

# createState

Leverage a Network's State across Routers and Agents.

The `State` class provides a way to manage state and history across a network of agents. It includes key-value storage and maintains a stack of all agent interactions.

The `State` is accessible to all Agents, Tools and Routers as a `state` or `network.state` property.

## [ Creating State](#creating-state)

Copy Ask AI

```
import { createState } from '@inngest/agent-kit' ;

export interface NetworkState {
// username is undefined until extracted and set by a tool
username ?: string ;
}

const state = createState < NetworkState >({
username: 'bar' ,
});

console . log ( state . data . username ); // 'bar'


const network = createNetwork ({
// ...
});

// Pass in state to each run
network . run ( "<query>" , { state })
```

## [ Reading and Modifying State's data ( state.data )](#reading-and-modifying-state%E2%80%99s-data-state-data)

The `State` class provides typed data accesible via the `data` property.

Learn more about the State use cases in the [State](\docs\concepts\state) concept guide.

[](#param-data) data object&lt;T&gt; A standard, mutable object which can be updated and modified within tools.

## [ State History](#state-history)

The State history is passed as a `history` to the lifecycle hooks and via the `network` argument to the Tools handlers to the Router function.

The State history can be retrieved *- as a copy -* using the `state.results` property composed of `InferenceResult` objects:

## [ InferenceResult](#inferenceresult)

The `InferenceResult` class represents a single agent call as part of the network state. It stores all inputs and outputs for a call.

[](#param-agent) agent Agent The agent responsible for this inference call.

[](#param-input) input string The input passed into the agent's run method.

[](#param-prompt) prompt Message[] The input instructions without additional history, including the system prompt, user input, and initial agent assistant message.

[](#param-history) history Message[] The history sent to the inference call, appended to the prompt to form a complete conversation log.

[](#param-output) output Message[] The parsed output from the inference call.

[](#param-tool-calls) toolCalls ToolResultMessage[] Output from any tools called by the agent.

[](#param-raw) raw string The raw API response from the call in JSON format.

## [ Message Types](#message-types)

The state system uses several message types to represent different kinds of interactions:

Copy Ask AI

```
type Message = TextMessage | ToolCallMessage | ToolResultMessage ;

interface TextMessage {
type : "text" ;
role : "system" | "user" | "assistant" ;
content : string | Array < TextContent >;
stop_reason ?: "tool" | "stop" ;
}

interface ToolCallMessage {
type : "tool_call" ;
role : "user" | "assistant" ;
tools : ToolMessage [];
stop_reason : "tool" ;
}

interface ToolResultMessage {
type : "tool_result" ;
role : "tool_result" ;
tool : ToolMessage ;
content : unknown ;
stop_reason : "tool" ;
}
```

[createNetwork Previous](\reference\create-network) [Network Router Next](\reference\network-router)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.