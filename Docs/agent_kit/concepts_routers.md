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

- [What is a Router?](#what-is-a-router%3F)
- [Using a Router](#using-a-router)
- [Creating a custom Router](#creating-a-custom-router)
- [Routing Patterns](#routing-patterns)
- [Tips](#tips)
- [Code-based Routers (supervised routing)](#code-based-routers-supervised-routing)
- [Routing Agent (autonomous routing)](#routing-agent-autonomous-routing)
- [Hybrid code and agent Routers (semi-supervised routing)](#hybrid-code-and-agent-routers-semi-supervised-routing)
- [Using state in Routing](#using-state-in-routing)
- [Related Concepts](#related-concepts)

Concepts

# Routers

Customize how calls are routed between Agents in a Network.

The purpose of a Network's **Router** is to decide what [Agent](\concepts\agents) to call based off the current Network [State](\concepts\state) .

## [ What is a Router?](#what-is-a-router%3F)

A router is a function that gets called after each agent runs, which decides whether to:

1. Call another agent (by returning an `Agent` )
2. Stop the network's execution loop (by returning `undefined` )

The routing function gets access to everything it needs to make this decision:

- The [Network](\concepts\networks) object itself, including it's [State](\concepts\state) .
- The stack of [Agents](\concepts\agents) to be called.
- The number of times the Network has called Agents ( *the number of iterations* ).
- The result from the previously called Agent in the Network's execution loop.

For more information about the role of a Router in a Network, read about [how Networks work](\concepts\networks#how-networks-work) .

## [ Using a Router](#using-a-router)

Providing a custom Router to your Network is optional. If you don't provide

one, the Network will use the "Default Router" Routing Agent.

Providing a custom Router to your Network can be achieved using 3 different patterns:

- **Writing a custom** [**Code-based Router**](\concepts\routers#code-based-routers-supervised-routing) : Define a function that makes decisions based on the current [State](\concepts\state) .
- **Creating a** [**Routing Agent**](\concepts\routers#routing-agent-autonomous-routing) : Leverages LLM calls to decide which Agents should be called next based on the current [State](\concepts\state) .
- **Writing a custom** [**Hybrid Router**](\concepts\routers#hybrid-code-and-agent-routers-semi-supervised-routing) : Mix code and agent-based routing to get the best of both worlds.

## [ Creating a custom Router](#creating-a-custom-router)

Custom Routers can be provided by defining a `defaultRouter` function returning either an instance of an `Agent` object or `undefined` .

Copy Ask AI

```
import { createNetwork } from "@inngest/agent-kit" ;

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router : ({ lastResult , callCount }) => {
// retrieve the last message from the output
const lastMessage = lastResult ?. output [ lastResult ?. output . length - 1 ];
const content =
lastMessage ?. type === "text" ? ( lastMessage ?. content as string ) : "" ;
// First call: use the classifier
if ( callCount === 0 ) {
return classifier ;
}
// Second call: if it's a question, use the writer
if ( callCount === 1 && content . includes ( "question" )) {
return writer ;
}
// Otherwise, we're done!
return undefined ;
},
});
```

The `defaultRouter` function receives a number of arguments:

@inngest/agent-kit Copy Ask AI

```
interface RouterArgs {
network : Network ; // The entire network, including the state and history
stack : Agent []; // Future agents to be called
callCount : number ; // Number of times the Network has called agents
lastResult ?: InferenceResult ; // The the previously called Agent's result
}
```

The available arguments can be used to build the routing patterns described below.

## [ Routing Patterns](#routing-patterns)

### [ Tips](#tips)

- Start simple with code-based routing for predictable behavior, then add agent-based routing for flexibility.
- Remember that routers can access the network's [state](\concepts\state)
- You can return agents that weren't in the original network
- The router runs after each agent call
- Returning `undefined` stops the network's execution loop

That's it! Routing is what makes networks powerful - it lets you build workflows that can be as simple or complex as you need.

### [ Code-based Routers (supervised routing)](#code-based-routers-supervised-routing)

The simplest way to route is to write code that makes decisions. Here's an example that routes between a classifier and a writer:

Copy Ask AI

```
import { createNetwork } from "@inngest/agent-kit" ;

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router : ({ lastResult , callCount }) => {
// retrieve the last message from the output
const lastMessage = lastResult ?. output [ lastResult ?. output . length - 1 ];
const content =
lastMessage ?. type === "text" ? ( lastMessage ?. content as string ) : "" ;
// First call: use the classifier
if ( callCount === 0 ) {
return classifier ;
}
// Second call: if it's a question, use the writer
if ( callCount === 1 && content . includes ( "question" )) {
return writer ;
}
// Otherwise, we're done!
return undefined ;
},
});
```

Code-based routing is great when you want deterministic, predictable behavior. It's also the fastest option since there's no LLM calls involved.

### [ Routing Agent (autonomous routing)](#routing-agent-autonomous-routing)

Without a `defaultRouter` defined, the network will use the "Default Routing Agent" to decide which agent to call next.

The "Default Routing Agent" is a Routing Agent provided by Agent Kit to handle the default routing logic.

You can create your own Routing Agent by using the [`createRoutingAgent`](\reference\network-router#createroutingagent) helper function:

Copy Ask AI

```
import { createRoutingAgent } from "@inngest/agent-kit" ;

const routingAgent = createRoutingAgent ({
name: "Custom routing agent" ,
description: "Selects agents based on the current state and request" ,
lifecycle: {
onRoute : ({ result , network }) => {
// custom logic...
},
},
});

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router: routingAgent ,
});
```

Routing Agents look similar to Agents but are designed to make routing

decisions: - Routing Agents cannot have Tools. - Routing Agents provides a

single

`onRoute` lifecycle method.

### [ Hybrid code and agent Routers (semi-supervised routing)](#hybrid-code-and-agent-routers-semi-supervised-routing)

And, of course, you can mix code and agent-based routing. Here's an example that uses code for the first step, then lets an agent take over:

Copy Ask AI

```
import { createNetwork , getDefaultRoutingAgent } from "@inngest/agent-kit" ;

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router : ({ callCount }) => {
// Always start with the classifier
if ( callCount === 0 ) {
return classifier ;
}
// Then let the routing agent take over
return getDefaultRoutingAgent ();
},
});
```

This gives you the best of both worlds:

- Predictable first steps when you know what needs to happen
- Flexibility when the path forward isn't clear

### [ Using state in Routing](#using-state-in-routing)

The router is the brain of your network - it decides which agent to call next. You can use state to make smart routing decisions:

Copy Ask AI

```
import { createNetwork } from '@inngest/agent-kit' ;

// mathAgent and contextAgent Agents definition...

const network = createNetwork ({
agents: [ mathAgent , contextAgent ],
router : ({ network , lastResult }) : Agent | undefined => {
// Check if we've solved the problem
const solution = network . state . data . solution ;
if ( solution ) {
// We're done - return undefined to stop the network
return undefined ;
}

// retrieve the last message from the output
const lastMessage = lastResult ?. output [ lastResult ?. output . length - 1 ];
const content = lastMessage ?. type === 'text' ? lastMessage ?. content as string : '' ;

// Check the last result to decide what to do next
if ( content . includes ( 'need more context' )) {
return contextAgent ;
}

return mathAgent ;
};
});
```

## [ Related Concepts](#related-concepts)

## [Networks](\concepts\networks)

[Networks combines the State and Router to execute Agent workflows.](\concepts\networks)

## [State](\concepts\state)

[State is a key-value store that can be used to store data between Agents.](\concepts\state)

[State Previous](\concepts\state) [History Next](\concepts\history)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.