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

Network

# createNetwork

Define a network

Networks are defined using the `createNetwork` function.

Copy Ask AI

```
import { createNetwork , openai } from '@inngest/agent-kit' ;

// Create a network with two agents
const network = createNetwork ({
agents: [ searchAgent , summaryAgent ],
defaultModel: openai ({ model: 'gpt-4o' , step }),
maxIter: 10 ,
});
```

## [ Options](#options)

[](#param-agents) agents array&lt;Agent&gt; required Agents that can be called from within the `Network` .

[](#param-default-model) defaultModel string The provider model to use for routing inference calls.

[](#param-system) system string required The system prompt, as a string or function. Functions let you change prompts

based off of state and memory

[](#param-tools) tools array&lt;TypedTool&gt; Defined tools that an agent can call. Tools are created via [`createTool`](\reference\createTool) .

[createTool Previous](\reference\create-tool) [createState Next](\reference\state)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.