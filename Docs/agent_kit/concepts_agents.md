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

- [Creating an Agent](#creating-an-agent)
- [Adding tools](#adding-tools)
- [How Agents work](#how-agents-work)
- [Lifecycle hooks](#lifecycle-hooks)
- [System prompts](#system-prompts)
- [Dynamic system prompts](#dynamic-system-prompts)
- [Static system prompts](#static-system-prompts)
- [Using Agents in Networks](#using-agents-in-networks)
- [Agent descriptions](#agent-descriptions)

Concepts

# Agents

Create agents to accomplish specific tasks with tools inside a network.

Agents are the core of AgentKit. Agents are *stateless* entities with a defined goal and an optional set of [Tools](\concepts\tools) that can be used to accomplish a goal.

Agents can be called individually or, more powerfully, composed into a [Network](\concepts\networks) with multiple agents that can work together with persisted [State](\concepts\state) .

At the most basic level, an Agent is a wrapper around a specific provider's [model](\concepts\models) , OpenAI gpt-4 for example, and a set of of [tools](\concepts\tools) .

## [ Creating an Agent](#creating-an-agent)

To create a simple Agent, all that you need is a `name` , `system` prompt and a `model` . All configuration options are detailed in the `createAgent` [reference](\reference\agent) .

Here is a simple agent created using the `createAgent` function:

Copy Ask AI

```
import { createAgent , openai } from '@inngest/agent-kit' ;

const codeWriterAgent = createAgent ({
name: 'Code writer' ,
system:
'You are an expert TypeScript programmer.  Given a set of asks, you think step-by-step to plan clean, ' +
'idiomatic TypeScript code, with comments and tests as necessary.' +
'Do not respond with anything else other than the following XML tags:' +
'- If you would like to write code, add all code within the following tags (replace $filename and $contents appropriately):' +
"  <file name='$filename.ts'>$contents</file>" ,
model: openai ( 'gpt-4o-mini' ),
});
```

While `system` prompts can be static strings, they are more powerful when they

are

[dynamic system prompts](#dynamic-system-prompts) defined as callbacks

that can add additional context at runtime.

Any Agent can be called using `run()` with a user prompt. This performs an inference call to the model with the system prompt as the first message and the input as the user message.

Copy Ask AI

```
const { output } = codeWriterAgent . run (
'Write a typescript function that removes unnecessary whitespace' ,
);
console . log ( output );
// [{ role: 'assistant', content: 'function removeUnecessaryWhitespace(...' }]
```

When including your Agent in a Network, a `description` is required. Learn

more about

[using Agents in Networks here](#using-agents-in-networks) .

## [ Adding tools](#adding-tools)

[Tools](\concepts\tools) are functions that extend the capabilities of an Agent. Along with the prompt (see `run()` ), Tools are included in calls to the language model through features like OpenAI's " [function calling](https://platform.openai.com/docs/guides/function-calling) " or Claude's " [tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) ."

Tools are defined using the `createTool` function and are passed to agents via the `tools` parameter:

Copy Ask AI

```
import { createAgent , createTool , openai } from '@inngest/agent-kit' ;

const listChargesTool = createTool ({
name: 'list_charges' ,
description:
"Returns all of a user's charges. Call this whenever you need to find one or more charges between a date range." ,
parameters: z . array (
z . object ({
userId: z . string (),
}),
),
handler : async ( output , { network , agent , step }) => {
// output is strongly typed to match the parameter type.
},
});

const supportAgent = createAgent ({
name: 'Customer support specialist' ,
system: 'You are an customer support specialist...' ,
model: openai ( 'gpt-3.5-turbo' ),
tools: [ listChargesTool ],
});
```

When `run()` is called, any step that the model decides to call is immediately executed before returning the output. Read the " [How agents work](#how-agents-work) " section for additional information.

Learn more about Tools in [this guide](\concepts\tools) .

## [ How Agents work](#how-agents-work)

Agents themselves are relatively simple. When you call `run()` , there are several steps that happen:

1

Preparing the prompts

The initial messages are created using the `system` prompt, the `run()` user

prompt, and

[Network State](\concepts\network-state) , if the agent is part

of a

[Network](\concepts\networks) . For added control, you can dynamically modify the Agent's prompts before the next step using the `onStart` [lifecycle hook](#lifecycle-hooks) .

2

Inference call

An inference call is made to the provided [`model`](\concepts\models) using Inngest's [`step.ai`](https://www.inngest.com/docs/features/inngest-functions/steps-workflows/step-ai-orchestration#step-tools-step-ai) . `step.ai` automatically retries on failure and caches the result for durability. The result is parsed into an `InferenceResult` object that contains all messages, tool calls and the raw API response from the model. To modify the result prior to calling tools, use the optional `onResponse` [lifecycle hook](#lifecycle-hooks) .

3

Tool calling

If the model decides to call one of the available `tools` , the Tool is automatically called. After tool calling is complete, the `onFinish` [lifecycle hook](#lifecycle-hooks) is called with the updated `InferenceResult` . This enables you to modify or inspect the output of the called tools.

4

Complete

The result is returned to the caller.

### [ Lifecycle hooks](#lifecycle-hooks)

Agent lifecycle hooks can be used to intercept and modify how an Agent works enabling dynamic control over the system:

Copy Ask AI

```
import { createAgent , openai } from '@inngest/agent-kit' ;

const agent = createAgent ({
name: 'Code writer' ,
description: 'An expert TypeScript programmer which can write and debug code.' ,
system: '...' ,
model: openai ( 'gpt-3.5-turbo' ),
lifecycle: {
onStart : async ({ prompt , network : { state }, history }) => {
// Dynamically alter prompts using Network state and history.

return { prompt , history }
},
},
});
```

As mentioned in the " [How Agents work](#how-agents-work) " section, there are a few lifecycle hooks that can be defined on the Agent's `lifecycle` options object.

- Dynamically alter prompts using Network [State](\concepts\state) or the Network's history.
- Parse output of model after an inference call.

Learn more about lifecycle hooks and how to define them in [this reference](\reference\create-agent#lifecycle) .

## [ System prompts](#system-prompts)

An Agent's system prompt can be defined as a string or an async callback. When Agents are part of a [Network](\concepts\networks) , the Network [State](\concepts\state) is passed as an argument to create dynamic prompts, or instructions, based on history or the outputs of other Agents.

### [ Dynamic system prompts](#dynamic-system-prompts)

Dynamic system prompts are very useful in agentic workflows, when multiple models are called in a loop, prompts can be adjusted based on network state from other call outputs.

Copy Ask AI

```
const agent = createAgent ({
name: 'Code writer' ,
description:
'An expert TypeScript programmer which can write and debug code.' ,

// The system prompt can be dynamically created at runtime using Network state:
system : async ({ network }) => {
// A default base prompt to build from:
const basePrompt =
'You are an expert TypeScript programmer. ' +
'Given a set of asks, think step-by-step to plan clean, ' +
'idiomatic TypeScript code, with comments and tests as necessary.' ;

// Inspect the Network state, checking for existing code saved as files:
const files : Record < string , string > | undefined = network . state . data . files ;
if ( ! files ) {
return basePrompt ;
}

// Add the files from Network state as additional context automatically
let additionalContext = 'The following code already exists:' ;
for ( const [ name , content ] of Object . entries ( files )) {
additionalContext += `<file name=' ${ name } '> ${ content } </file>` ;
}
return ` ${ basePrompt } ${ additionalContext } ` ;
},
});
```

### [ Static system prompts](#static-system-prompts)

Agents may also just have static system prompts which are more useful for simpler use cases.

Copy Ask AI

```
const codeWriterAgent = createAgent ({
name: 'Copy editor' ,
system:
`You are an expert copy editor. Given a draft article, you provide ` +
`actionable improvements for spelling, grammar, punctuation, and formatting.` ,
model: openai ( 'gpt-3.5-turbo' ),
});
```

## [ Using Agents in Networks](#using-agents-in-networks)

Agents are the most powerful when combined into [Networks](\concepts\networks) . Networks include [state](\concepts\state) and [routers](\concepts\routers) to create stateful workflows that can enable Agents to work together to accomplish larger goals.

### [ Agent descriptions](#agent-descriptions)

Similar to how [Tools](\concepts\tools) have a `description` that enables an LLM to decide when to call it, Agents also have an `description` parameter. This is *required* when using Agents within Networks. Here is an example of an Agent with a description:

Copy Ask AI

```
const codeWriterAgent = createAgent ({
name: 'Code writer' ,
description:
'An expert TypeScript programmer which can write and debug code. Call this when custom code is required to complete a task.' ,
system: `...` ,
model: openai ( 'gpt-3.5-turbo' ),
});
```

[Local development Previous](\getting-started\local-development) [Tools Next](\concepts\tools)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.