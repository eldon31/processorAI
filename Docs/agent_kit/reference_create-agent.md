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

- [Options](#options)
- [lifecycle](#lifecycle)

Agent

# createAgent

Define an agent

Agents are defined using the `createAgent` function.

Copy Ask AI

```
import { createAgent , agenticOpenai as openai } from '@inngest/agent-kit' ;

const agent = createAgent ({
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

## [ Options](#options)

[](#param-name) name string required The name of the agent. Displayed in tracing.

[](#param-description) description string Optional description for the agent, used for LLM-based routing to help the

network pick which agent to run next.

[](#param-model) model string required The provider model to use for inference calls.

[](#param-system) system string | function required The system prompt, as a string or function. Functions let you change prompts

based off of state and memory.

[](#param-tools) tools array&lt;TypedTool&gt; Defined tools that an agent can call. Tools are created via [`createTool`](\reference\createTool) .

[](#param-lifecycle) lifecycle Lifecycle Lifecycle hooks that can intercept and modify inputs and outputs throughout the stages of execution of `run()` . Learn about each [lifecycle](#lifecycle) hook that can be defined below.

### [ lifecycle](#lifecycle)

[](#param-on-start) onStart function

Called after the initial prompt messages are created and before the inference call request. The `onStart` hook can be used to:

- Modify input prompt for the Agent.
- Prevent the agent from being called by throwing an error.

[](#param-on-response) onResponse function

Called after the inference call request is completed and before tool calling. The `onResponse` hook can be used to:

- Inspect the tools that the model decided to call.
- Modify the response prior to tool calling.

[](#param-on-finish) onFinish function

Called after tool calling has completed. The `onFinish` hook can be used to:

- Modify the `InferenceResult` including the outputs prior to the result being added to [Network state](\concepts\network-state) .

onStart onResponse Copy Ask AI

```
const agent = createAgent ({
name: 'Code writer' ,
lifecycles: {
onStart : ({
agent ,
network ,
input ,
system , // The system prompt for the agent
history , // An array of messages
}) => {
// Return the system prompt (the first message), and any history added to the
// model's conversation.
return { system , history };
},
},
});
```

[Introduction Previous](\reference\introduction) [createTool Next](\reference\create-tool)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.