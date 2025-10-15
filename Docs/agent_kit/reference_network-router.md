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

- [Function Router](#function-router)
- [Example](#example)
- [Parameters](#parameters)
- [Return Values](#return-values)
- [createRoutingAgent()](#createroutingagent)
- [Example](#example-2)
- [Parameters](#parameters-2)
- [Returns](#returns)
- [Related APIs](#related-apis)

Network

# Network Router

Controlling the flow of execution between agents in a Network.

The `defaultRouter` option in `createNetwork` defines how agents are coordinated within a Network. It can be either a [Function Router](#function-router) or a [Routing Agent](#routing-agent) .

## [ Function Router](#function-router)

A function router is provided to the `defaultRouter` option in `createNetwork` .

### [ Example](#example)

Copy Ask AI

```
const network = createNetwork ({
agents: [ classifier , writer ],
router : ({ lastResult , callCount , network , stack , input }) => {
// First call: use the classifier
if ( callCount === 0 ) {
return classifier ;
}

// Get the last message from the output
const lastMessage = lastResult ?. output [ lastResult ?. output . length - 1 ];
const content =
lastMessage ?. type === "text" ? ( lastMessage ?. content as string ) : "" ;

// Second call: if it's a question, use the writer
if ( callCount === 1 && content . includes ( "question" )) {
return writer ;
}

// Otherwise, we're done!
return undefined ;
},
});
```

### [ Parameters](#parameters)

[](#param-input) input string The original input provided to the network.

[](#param-network) network Network The network instance, including its state and history. See [`Network.State`](\reference\state) for more details.

[](#param-stack) stack Agent[] The list of future agents to be called. ( *internal read-only value* )

[](#param-call-count) callCount number The number of agent calls that have been made.

[](#param-last-result) lastResult InferenceResult The result from the previously called agent. See [`InferenceResult`](\reference\state#inferenceresult) for more details.

### [ Return Values](#return-values)

| Return Type   | Description                                        |
|---------------|----------------------------------------------------|
| Agent         | Single agent to execute next                       |
| Agent[]       | Multiple agents to execute in sequence             |
| RoutingAgent  | Delegate routing decision to another routing agent |
| undefined     | Stop network execution                             |

## [ createRoutingAgent()](#createroutingagent)

Creates a new routing agent that can be used as a `defaultRouter` in a network.

### [ Example](#example-2)

Copy Ask AI

```
import { createRoutingAgent , createNetwork } from "@inngest/agent-kit" ;

const routingAgent = createRoutingAgent ({
name: "Custom routing agent" ,
description: "Selects agents based on the current state and request" ,
lifecycle: {
onRoute : ({ result , network }) => {
// Get the agent names from the result
const agentNames = result . output
. filter (( m ) => m . type === "text" )
. map (( m ) => m . content as string );

// Validate that the agents exist
return agentNames . filter (( name ) => network . agents . has ( name ));
},
},
});

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router: routingAgent ,
});
```

### [ Parameters](#parameters-2)

[](#param-name) name string required The name of the routing agent.

[](#param-description) description string Optional description of the routing agent's purpose.

[](#param-lifecycle) lifecycle object required

Show properties

[](#param-on-route) onRoute function required

Called after each inference to determine the next agent(s) to call. **Arguments:**

Copy Ask AI

```
{
result : InferenceResult ; // The result from the routing agent's inference
agent : RoutingAgent ; // The routing agent instance
network : Network ; // The network instance
}
```

**Returns:** `string[]` - Array of agent names to call next, or `undefined` to stop execution

[](#param-model) model AiAdapter.Any Optional model to use for routing decisions. If not provided, uses the

network's

`defaultModel` .

### [ Returns](#returns)

Returns a `RoutingAgent` instance that can be used as a network's `defaultRouter` .

## [ Related APIs](#related-apis)

- [createNetwork](\reference\create-network)
- [Network.State](\reference\state)

[createState Previous](\reference\state) [OpenAI Model Next](\reference\model-openai)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.