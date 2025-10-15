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

- [How Networks work](#how-networks-work)
- [Model configuration](#model-configuration)
- [Combination of multiple models](#combination-of-multiple-models)
- [Routing &amp; maximum iterations](#routing-%26-maximum-iterations)
- [Routing](#routing)
- [Maximum iterations](#maximum-iterations)
- [Combining maxIter and defaultRouter](#combining-maxiter-and-defaultrouter)
- [Providing a default State](#providing-a-default-state)

Concepts

# Networks

Combine one or more agents into a Network.

Networks are **Systems of** [**Agents**](\concepts\agents) . Use Networks to create powerful AI workflows by combining multiple Agents.

A network contains three components:

- The [Agents](\concepts\agents) that the network can use to achieve a goal
- A [State](\concepts\state) including past messages and a key value store, shared between Agents and the Router
- A [Router](\concepts\routers) , which chooses whether to stop or select the next agent to run in the loop

Here's a simple example:

Copy Ask AI

```
import { createNetwork , openai } from '@inngest/agent-kit' ;

// searchAgent and summaryAgent definitions...

// Create a network with two agents.
const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
});

// Run the network with a user prompt
await network . run ( 'What happened in the 2024 Super Bowl?' );
```

By calling `run()` , the network runs a core loop to call one or more agents to find a suitable answer.

## [ How Networks work](#how-networks-work)

Networks can be thought of as while loops with memory ( [State](\concepts\state) ) that call Agents and Tools until the Router determines that there is no more work to be done.

1

Create the Network of Agents

You create a network with a list of available [Agents](\concepts\agents) .

Each Agent can use a different

[model and inference](\concepts\models)

[provider](\concepts\models)

.

2

Provide the staring prompt

You give the network a user prompt by calling `run()` .

3

Core execution loop

The network runs its core loop:

1

Call the Network router

The [Router](\concepts\routers) decides the first Agent to run with your

input.

2

Run the Agent

Call the Agent with your input. This also runs the agent's [lifecycles](\concepts\agents#lifecycle-hooks) , and any [Tools](\concepts\tools) that the model decides to call.

3

Store the result

Stores the result in the network's [State](\concepts\state) . State can

be accessed by the Router or other Agent's Tools in future loops.

4

Call the the Router again ↩️

Return to the top of the loop and calls the Router with the new State.

The Router can decide to quit or run another Agent.

## [ Model configuration](#model-configuration)

A Network must provide a default model which is used for routing between Agents and for Agents that don't have one:

Copy Ask AI

```
import { createNetwork , openai } from '@inngest/agent-kit' ;

// searchAgent and summaryAgent definitions...

const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
defaultModel: openai ({ model: 'gpt-4o' }),
});
```

A Network not defining a `defaultModel` and composed of Agents without model will throw an error.

### [ Combination of multiple models](#combination-of-multiple-models)

Each Agent can specify it's own model to use so a Network may end up using multiple models. Here is an example of a Network that defaults to use an OpenAI model, but the `summaryAgent` is configured to use an Anthropic model:

Copy Ask AI

```
import { createNetwork , openai , anthropic } from '@inngest/agent-kit' ;

const searchAgent = createAgent ({
name: 'Search' ,
description: 'Search the web for information' ,
});

const summaryAgent = createAgent ({
name: 'Summary' ,
description: 'Summarize the information' ,
model: anthropic ({ model: 'claude-3-5-sonnet' }),
});

// The searchAgent will use gpt-4o, while the summaryAgent will use claude-3-5-sonnet.
const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
defaultModel: openai ({ model: 'gpt-4o' }),
});
```

## [ Routing &amp; maximum iterations](#routing-%26-maximum-iterations)

### [ Routing](#routing)

A Network can specify an optional `defaultRouter` function that will be used to determine the next Agent to run.

Copy Ask AI

```
import { createNetwork } from '@inngest/agent-kit' ;

// classifier and writer Agents definition...

const network = createNetwork ({
agents: [ classifier , writer ],
router : ({ lastResult , callCount }) => {
// retrieve the last message from the output
const lastMessage = lastResult ?. output [ lastResult ?. output . length - 1 ];
const content = lastMessage ?. type === 'text' ? lastMessage ?. content as string : '' ;
// First call: use the classifier
if ( callCount === 0 ) {
return classifier ;
}
// Second call: if it's a question, use the writer
if ( callCount === 1 && content . includes ( 'question' )) {
return writer ;
}
// Otherwise, we're done!
return undefined ;
},
});
```

Refer to the [Router](\concepts\routers) documentation for more information about how to create a custom Router.

### [ Maximum iterations](#maximum-iterations)

A Network can specify an optional `maxIter` setting to limit the number of iterations.

Copy Ask AI

```
import { createNetwork } from '@inngest/agent-kit' ;

// searchAgent and summaryAgent definitions...

const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
defaultModel: openai ({ model: 'gpt-4o' }),
maxIter: 10 ,
});
```

Specifying a `maxIter` option is useful when using a [Default Routing Agent](\concepts\routers#default-routing-agent-autonomous-routing) or a [Hybrid Router](\concepts\routers#hybrid-code-and-agent-routers-semi-supervised-routing) to avoid infinite loops. A Routing Agent or Hybrid Router rely on LLM calls to make decisions, which means that they can sometimes fail to identify a final condition.

### [ Combining maxIter and defaultRouter](#combining-maxiter-and-defaultrouter)

You can combine `maxIter` and `defaultRouter` to create a Network that will stop after a certain number of iterations or when a condition is met.

However, please note that the `maxIter` option can prevent the `defaultRouter` from being called (For example, if `maxIter` is set to 1, the `defaultRouter` will only be called once).

## [ Providing a default State](#providing-a-default-state)

A Network can specify an optional `defaultState` setting to provide a default [State](\concepts\state) .

Copy Ask AI

```
import { createNetwork } from '@inngest/agent-kit' ;

// searchAgent and summaryAgent definitions...

const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
defaultState: new State ({
foo: 'bar' ,
}),
});
```

Providing a `defaultState` can be useful to persist the state in database between runs or initialize your network with external data.

[Tools Previous](\concepts\tools) [State Next](\concepts\state)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.