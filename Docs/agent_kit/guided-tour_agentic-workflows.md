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
- [Setup](#setup)
- [Implementing our Code Assistant v2](#implementing-our-code-assistant-v2)
- [Overview of the agentic workflow](#overview-of-the-agentic-workflow)
- [A Network of Agents](#a-network-of-agents)
- [Creating Agents with Tools](#creating-agents-with-tools)
- [Assembling the Network](#assembling-the-network)
- [Running the Code Assistant v2](#running-the-code-assistant-v2)
- [What we've learned so far](#what-we%E2%80%99ve-learned-so-far)
- [Next steps](#next-steps)

Guided Tour

# Code Assistant v2: Complex code analysis

Use AgentKit Tools and Custom Router to add agentic capabilities.

## [ Overview](#overview)

Our [Code Assistant v1](\ai-agents-in-practice\ai-workflows) , relying on a RAG workflow, had limited capabilities linked to its lack of reasoning.

The second version of our Code Assistant will introduce reasoning capabilities to adapt analysis based on the user's input:

Copy Ask AI

```
const {
state : { kv },
} = await network . run (
`Analyze the files/example.ts file by suggesting improvements and documentation.`
);
console . log ( "Analysis:" , kv . get ( "summary" ));

// Analysis: The code analysis suggests several key areas for improvement:

// 1. Type Safety and Structure:
// - Implement strict TypeScript configurations
// - Add explicit return types and interfaces
// - Break down complex functions
// - Follow Single Responsibility Principle
// - Implement proper error handling

// 2. Performance Optimization:
// - Review and optimize critical operations
// ...
```

These agentic (reasoning) capabilities are introduced by the following AgentKit concepts:

- [**Tools**](\concepts\tools) : Enables [Agents](\concepts\agents) to interact with their environment (ex: file system or shared State).
- [**Router**](\concepts\router) : Powers the flow of the conversation between Agents.
- [**Network**](\concepts\network) : Add a shared [State](\concepts\state) to share information between Agents.

Let's learn these concepts in practice.

## [ Setup](#setup)

Similarly to the [Code Assistant v1](\ai-agents-in-practice\ai-workflows) , perform the following steps to setup your project:

1. Initialize your project

npm pnpm yarn Copy Ask AI

```
npm init
```

2. Install the required dependencies

npm pnpm yarn Copy Ask AI

```
npm install @inngest/agent-kit inngest zod
```

3. Add TypeScript support

npm pnpm yarn Copy Ask AI

```
Install the following dev dependencies:
```

And add the following scripts to your `package.json` :

Copy Ask AI

```
"scripts" : {
"start" : "tsx ./index.ts"
}
```

4. Download the example code file

Copy Ask AI

```
mkdir files
cd files
wget https://raw.githubusercontent.com/inngest/agent-kit/main/examples/code-assistant-agentic/files/example.ts
cd -
```

You are now set up, let's implement the v2 of our Code Assistant.

## [ Implementing our Code Assistant v2](#implementing-our-code-assistant-v2)

### [ Overview of the agentic workflow](#overview-of-the-agentic-workflow)

Our Code Assistant v2 introduces reasoning to perform tailored recommendations based on a given code file: refactoring, documentation, etc.

To achieve this behavior, we will need to:

- Create a `code_assistant_agent` Agent that will load a given filename from disk and plan a workflow using the following available [Agents](\concepts\agents) :
    - `analysis_agent` that will analyze the code file and suggest improvements
    - `documentation_agent` that will generate documentation for the code file
- Finally, create a `summarization_agent` Agent that will generate a summary of the suggestions made by other agents

Compared to our [Code Assistant v1](\ai-agents-in-practice\ai-workflows) , this new version does not consist of simple retrieval and generations steps.

Instead, it introduces more flexibility by enabling LLM models to plan actions and select tools to use.

Let's see how to implement the Agents.

### [ A Network of Agents](#a-network-of-agents)

Our Code Assistant v2 is composed of 4 Agents collaborating together to analyze a given code file.

Such collaboration is made possible by using a

[Network](\concepts\network) to orchestrate the Agents and share [State](\concepts\state) between them.

Unlike the [Code Assistant v1](\ai-agents-in-practice\ai-workflows) , the user prompt will be passed to the network instead of an individual Agent:

Copy Ask AI

```
await network . run (
`Analyze the files/example.ts file by suggesting improvements and documentation.`
);
```

To successfully run, a `Network` relies on:

- A Router to **indicate which Agent should be run next**
- **A shared State** , updated by the Agents' LLM responses and **tool calls**

Let's start by implementing our Agents and registering them into the Network.

### [ Creating Agents with Tools](#creating-agents-with-tools)

Attaching Tools to an Agent helps to:

- Enrich dynamically the Agent context with dynamic data
- Store the Agent results in the shared State

Learn more about [Tools](\concepts\tools) .

**The Analysis and Documentation Agents**

Our first two analysis Agents are straightforward:

Copy Ask AI

```
import { createAgent } from "@inngest/agent-kit" ;

const documentationAgent = createAgent ({
name: "documentation_agent" ,
system: "You are an expert at generating documentation for code" ,
});

const analysisAgent = createAgent ({
name: "analysis_agent" ,
system: "You are an expert at analyzing code and suggesting improvements" ,
});
```

Defining task specific LLM calls (Agents) is a great way to make the LLM reasoning more efficient and avoid unnecessary generations.

Our `documentation_agent` and `analysis_agent` are currently stateless and need to be *connected* to the Network by saving their suggestions into the shared State.

For this, we will create our first Tool using [`createTool`](\reference\create-tool) :

Copy Ask AI

```
const saveSuggestions = createTool ({
name: "save_suggestions" ,
description: "Save the suggestions made by other agents into the state" ,
parameters: z . object ({
suggestions: z . array ( z . string ()),
}),
handler : async ( input , { network }) => {
const suggestions = network ?. state . kv . get ( "suggestions" ) || [];
network ?. state . kv . set ( "suggestions" , [
... suggestions ,
... input . suggestions ,
]);
return "Suggestions saved!" ;
},
});
```

A Tool is a function that can be called by an Agent. The `name` , `description` and `parameters` are used by the Agent to understand what the Tool does and what it expects as input. The `handler` is the function that will be called when the Tool is used. `save_suggestions` 's handler relies on the [Network's State](\reference\state#reading-and-modifying-state-state-kv) [`kv`](\reference\state#reading-and-modifying-state-state-kv) [(key-value store)](\reference\state#reading-and-modifying-state-state-kv) API to share information with other Agents. Learn more about the [createTool()](\reference\create-tool) API.

The `save_suggestions` Tool is used by both `documentation_agent` and `analysis_agent` to save their suggestions into the shared State:

Copy Ask AI

```
import { createAgent } from "@inngest/agent-kit" ;

// `save_suggestions` definition...

const documentationAgent = createAgent ({
name: "documentation_agent" ,
system: "You are an expert at generating documentation for code" ,
tools: [ saveSuggestions ],
});

const analysisAgent = createAgent ({
name: "analysis_agent" ,
system: "You are an expert at analyzing code and suggesting improvements" ,
tools: [ saveSuggestions ],
});
```

Our `documentation_agent` and `analysis_agent` are now connected to the Network and will save their suggestions into the shared State.

Let's now create our `code_assistant_agent` that will read the code file from disk and plan the workflow to run.

**The Code Assistant Agent**

Let's jump into the action by looking at the full implementation of our `code_assistant_agent` :

Copy Ask AI

```
const codeAssistantAgent = createAgent ({
name: "code_assistant_agent" ,
system : ({ network }) => {
const agents = Array . from ( network ?. agents . values () || [])
. filter (
( agent ) =>
! [ "code_assistant_agent" , "summarization_agent" ]. includes ( agent . name )
)
. map (( agent ) => ` ${ agent . name } ( ${ agent . system } )` );
return `From a given user request, ONLY perform the following tool calls:
- read the file content
- generate a plan of agents to run from the following list: ${ agents . join ( ", " ) }

Answer with "done" when you are finished.` ;
},
tools: [
createTool ({
name: "read_file" ,
description: "Read a file from the current directory" ,
parameters: z . object ({
filename: z . string (),
}),
handler : async ( input , { network }) => {
const filePath = join ( process . cwd (), `files/ ${ input . filename } ` );
const code = readFileSync ( filePath , "utf-8" );
network ?. state . kv . set ( "code" , code );
return "File read!" ;
},
}),
createTool ({
name: "generate_plan" ,
description: "Generate a plan of agents to run" ,
parameters: z . object ({
plan: z . array ( z . string ()),
}),
handler : async ( input , { network }) => {
network ?. state . kv . set ( "plan" , input . plan );
return "Plan generated!" ;
},
}),
],
});
```

The highlighted lines emphasize three important parts of the `code_assistant_agent` :

- The [`system`](\reference\create-agent#param-system) [property](\reference\create-agent#param-system) can take a function receiving the current Network state as argument, enabling more flexibility in the Agent's behavior
    - Here, the `system` function is used to generate a prompt for the LLM based on the available Agents in the Network, enabling the LLM to plan the workflow to run
- The `code_assistant_agent` relies on two Tools to achieve its goal:
    - `read_file` to read the code file from disk and save it into the shared State
    - `generate_plan` to generate a plan of agents to run and save it into the shared State

The pattern of dynamic `system` prompt and tools are also used by the `summarization_agent` to generate a summary of the suggestions made by other agents.

**The Summarization Agent**

Copy Ask AI

```
const summarizationAgent = createAgent ({
name: "summarization_agent" ,
system : ({ network }) => {
const suggestions = network ?. state . kv . get ( "suggestions" ) || [];
return `Save a summary of the following suggestions:
${ suggestions . join ( " \n " ) } ` ;
},
tools: [
createTool ({
name: "save_summary" ,
description:
"Save a summary of the suggestions made by other agents into the state" ,
parameters: z . object ({
summary: z . string (),
}),
handler : async ( input , { network }) => {
network ?. state . kv . set ( "summary" , input . summary );
return "Saved!" ;
},
}),
],
});
```

The `summarization_agent` is a good example on how the State can be used to

store intermediate results and pass them to the next Agent: - the

`suggestions` are stored in the State by the `documentation_agent` and `analysis_agent` - the `summarization_agent` will read the `suggestions` from

the State and generate a summary - the summary is then stored in the State as

the

`summary` key

Our four Agents are now propely defined and connected to the Network's State.

Let's now configure our Network to run the Agents with a Router.

### [ Assembling the Network](#assembling-the-network)

An AgentKit [Network](\concepts\network) is defined by a set of Agents and an optional `defaultModel` :

Copy Ask AI

```
import { createNetwork , anthropic } from "@inngest/agent-kit" ;

// Agent and Tools definitions...

const network = createNetwork ({
name: "code-assistant-v2" ,
agents: [
codeAssistantAgent ,
documentationAgent ,
analysisAgent ,
summarizationAgent ,
],
defaultModel: anthropic ({
model: "claude-3-5-sonnet-latest" ,
max_tokens: 4096 ,
}),
});
```

The `defaultModel` will be applied to all Agents part of the Network.

A model can also be set on an individual Agent by setting the

`model` property. Learn more about the [Network Model configuration](\concepts\networks#model-configuration) .

Our Code Assistant v2 is missing a final piece: the Router.

Without a Router, the Network will not know which Agent to run next.

**Implementing the Router**

As stated in the [workflow overview](#overview-of-the-agentic-workflow) , our Code Assistant v2 is an agentic worflow composed of the following steps:

1. The `code_assistant_agent` will read the code file from disk and generate a plan of agents to run
2. Depending on the plan, the Network will run the next Agent in the plan ( *ex:* *`analysis_agent`* *and* *`documentation_agent`* )
3. Finally, the `summarization_agent` will generate a summary of the suggestions made by other agents

AgentKit's Router enables us to implement such dynamic workflow with code by providing a `defaultRouter` function:

Copy Ask AI

```
const network = createNetwork ({
name: "code-assistant-v2" ,
agents: [
codeAssistantAgent ,
documentationAgent ,
analysisAgent ,
summarizationAgent ,
],
router : ({ network }) => {
if ( ! network ?. state . kv . has ( "code" ) || ! network ?. state . kv . has ( "plan" )) {
return codeAssistantAgent ;
} else {
const plan = ( network ?. state . kv . get ( "plan" ) || []) as string [];
const nextAgent = plan . pop ();
if ( nextAgent ) {
network ?. state . kv . set ( "plan" , plan );
return network ?. agents . get ( nextAgent );
} else if ( ! network ?. state . kv . has ( "summary" )) {
return summarizationAgent ;
} else {
return undefined ;
}
}
},
defaultModel: anthropic ({
model: "claude-3-5-sonnet-latest" ,
max_tokens: 4096 ,
}),
});
```

**How does a Router work?** The Router is a function called by the Network when starting a new run and between each Agent call. The provided Router function ( `defaultRouter` ) receives a `network` argument granting access to the Network's state and Agents. Learn more about the [Router](\concepts\router) .

Let's have a closer look at the Router implementation:

Copy Ask AI

```
const router = ({ network }) => {
// the first iteration of the network will have an empty state
//  also, the first run of `code_assistant_agent` will store the `code`,
//  requiring a second run to generate the plan
if ( ! network ?. state . kv . has ( "code" ) || ! network ?. state . kv . has ( "plan" )) {
return codeAssistantAgent ;
} else {
// once the `plan` available in the state, we iterate over the agents to execute
const plan = ( network ?. state . kv . get ( "plan" ) || []) as string [];
const nextAgent = plan . pop ();
if ( nextAgent ) {
network ?. state . kv . set ( "plan" , plan );
return network ?. agents . get ( nextAgent );
// we no agents are left to run, we generate a summary
} else if ( ! network ?. state . kv . has ( "summary" )) {
return summarizationAgent ;
// if no agent are left to run and a summary is available, we are done
} else {
return undefined ;
}
}
};
```

Our Code Assistant v2 iteration is now complete. Let's run it!

## [ Running the Code Assistant v2](#running-the-code-assistant-v2)

First, go to your Anthropic dashboard and create a new API key.

Then, run the following command to execute our Code Assistant:

npm pnpm yarn Copy Ask AI

```
ANTHROPIC_API_KEY =< your-api-key > npm run start
```

The following output should be displayed in your terminal:

Copy Ask AI

```
Analysis: The code analysis suggests several key areas for improvement:

1. Type Safety and Structure:
- Implement strict TypeScript configurations
- Add explicit return types and interfaces
- Break down complex functions
- Follow Single Responsibility Principle
- Implement proper error handling

2. Performance Optimization:
- Review and optimize critical operations
- Consider caching mechanisms
- Improve data processing efficiency

3. Documentation:
- Add comprehensive JSDoc comments
- Document complex logic and assumptions
- Create detailed README
- Include setup and usage instructions
- Add code examples
```

Updating the `files/example.ts` by applying the suggestions and running the Code Assistant again will yield a different planning with a different summary. Try it out!

## [ What we've learned so far](#what-we%E2%80%99ve-learned-so-far)

Let's recap what we've learned so far:

- **Agentic workflows** , compared to RAG workflows, **are more flexible** and can be used to perform more complex tasks
- **Combining multiple Agents improves the accuracy** of the LLM reasoning and can save tokens
- **AgentKit enables to combine multiple Agents** into a [Network](\concepts\networks) , connected by a common [State](\concepts\state)
- **AgentKit's Router enables to implement our workflow with code** , keeping control over our reasoning planning

## [ Next steps](#next-steps)

This Code Assistant v2 shines by its analysis capabilities, but cannot be qualified as an AI Agent.

In the next version of our Code Assistant, we will transform it into a semi-autonomous AI Agent that can solve bugs and improve code of a small project.

## [Code Assistant v3: Autonomous Code Assistant](\ai-agents-in-practice\ai-agents)

[The final version update of our Code Assistant will transform it into a](\ai-agents-in-practice\ai-agents)

[semi-autonomous AI Agent.](\ai-agents-in-practice\ai-agents)

[Code Assistant v1: Explaining a given code file Previous](\guided-tour\ai-workflows) [Code Assistant v3: Autonomous Bug Solver Next](\guided-tour\ai-agents)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.