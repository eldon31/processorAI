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

- [History](#history)
- [Typed state](#typed-state)
- [Using state in tools](#using-state-in-tools)

Concepts

# State

Shared memory, history, and key-value state for Agents and Networks.

State is shared memory, or context, that is be passed between different [Agents](\concepts\agents) in a [Networks](\concepts\networks) . State is used to store message history and build up structured data from tools.

State enables agent workflows to execute in a loop and contextually make decisions. Agents continuously build upon and leverage this context to complete complex tasks.

AgentKit's State stores data in two ways:

- **History of messages** - A list of prompts, responses, and tool calls.
- **Fully typed state data** - Typed state that allows you to build up structured data from agent calls, then implement [deterministic state-based routing](\advanced-patterns\routing) to easily model complex agent workflows.

Both history and state data are used automatically by the Network to store and provide context to the next Agent.

## [ History](#history)

The history system maintains a chronological record of all Agent interactions in your Network.

Each interaction is stored as an `InferenceResult` . Refer to the [InferenceResult reference](\reference\state#inferenceresult) for more information.

## [ Typed state](#typed-state)

State contains typed data that can be used to store information between Agent calls, update agent prompts, and manage routing.  Networks, agents,

and tools use this type in order to set data:

Copy Ask AI

```
export interface NetworkState {
// username is undefined until extracted and set by a tool
username ?: string ;
}

// You can construct typed state with optional defaults, eg. from memory.
const state = createState < NetworkState >({
username: "default-username" ,
});

console . log ( state . data . username ); // 'default-username'
state . data . username = "Alice" ;
console . log ( state . data . username ); // 'Alice'
```

Common uses for data include:

- Storing intermediate results that other Agents might need within lifecycles
- Storing user preferences or context
- Passing data between Tools and Agents
- State based routing

The `State` 's data is only retained for a single `Network` 's run.

This means that it is only short-term memory and is not persisted across

different Network

`run()` calls. You can implement memory by inspecting a network's state after it has

finished running.

State, which is required by [Networks](\concepts\networks) , has many uses across various AgentKit components.

Refer to the [State reference](\reference\state#reading-and-modifying-state-states-data) for more information.

## [ Using state in tools](#using-state-in-tools)

State can be leveraged in a Tool's `handler` method to get or set data. Here is an example of a Tool that uses `kv` as a temporary store for files and their contents that are being written by the Agent.

Copy Ask AI

```
const writeFiles = createTool ({
name: "write_files" ,
description: "Write code with the given filenames" ,
parameters: z . object ({
files: z . array (
z . object ({
filename: z . string (),
content: z . string (),
})
),
}),
handler : ( output , { network }) => {
// files is the output from the model's response in the format above.
// Here, we store OpenAI's generated files in the response.
const files = network . state . data . files || {};
for ( const file of output . files ) {
files [ file . filename ] = file . content ;
}
network . state . data . files = files ;
},
});
```

[Networks Previous](\concepts\networks) [Routers Next](\concepts\routers)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.