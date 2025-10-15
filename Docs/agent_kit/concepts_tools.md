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

- [Creating a Tool](#creating-a-tool)
- [Optional parameters](#optional-parameters)
- [Examples](#examples)

Concepts

# Tools

Extending the functionality of Agents for structured output or performing tasks.

Tools are functions that extend the capabilities of an [Agent](\concepts\agents) . Tools have two core uses:

- Calling code, enabling models to interact with systems like your own database or external APIs.
- Turning unstructured inputs into structured responses.

A list of all available Tools and their configuration is sent in [an Agent's inference calls](\concepts\agents#how-agents-work) and a model may decide that a certain tool or tools should be called to complete the task. Tools are included in an Agent's calls to language models through features like OpenAI's " [function calling](https://platform.openai.com/docs/guides/function-calling) " or Claude's " [tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) ."

## [ Creating a Tool](#creating-a-tool)

Each Tool's `name` , `description` , and `parameters` are part of the function definition that is used by model to learn about the tool's capabilities and decide when it should be called. The `handler` is the function that is executed by the Agent if the model decides that a particular Tool should be called.

Here is a simple tool that lists charges for a given user's account between a date range:

Copy Ask AI

```
import { createTool } from '@inngest/agent-kit' ;

const listChargesTool = createTool ({
name: 'list_charges' ,
description:
"Returns all of a user's charges. Call this whenever you need to find one or more charges between a date range." ,
parameters: z . object ({
userId: z . string (),
created: z . object ({
gte: z . string (). date (),
lte: z . string (). date (),
}),
}),
handler : async ({ userId , created }, { network , agent , step }) => {
// input is strongly typed to match the parameter type.
return [{ ... }]
},
});
```

Writing quality `name` and `description` parameters help the model determine when the particular Tool should be called.

### [ Optional parameters](#optional-parameters)

Optional parameters should be defined using `.nullable()` (not `.optional()` ):

Copy Ask AI

```
const listChargesTool = createTool ({
name: 'list_charges' ,
description:
"Returns all of a user's charges. Call this whenever you need to find one or more charges between a date range." ,
parameters: z . object ({
userId: z . string (),
created: z . object ({
gte: z . string (). date (),
lte: z . string (). date (),
}). nullable (),
}),
handler : async ({ userId , created }, { network , agent , step }) => {
// input is strongly typed to match the parameter type.
return [{ ... }]
},
});
```

## [ Examples](#examples)

You can find multiple examples of tools in the below GitHub projects:

## [Hacker News Agent with Render and Inngest](https://github.com/inngest/agentkit-render-tutorial)

[A tutorial showing how to create a Hacker News Agent using AgentKit Code-style routing and Agents with tools.](https://github.com/inngest/agentkit-render-tutorial)

## [AgentKit SWE-bench](https://github.com/inngest/agent-kit/tree/main/examples/swebench#readme)

[This AgentKit example uses the SWE-bench dataset to train an agent to solve coding problems. It uses advanced tools to interact with files and codebases.](https://github.com/inngest/agent-kit/tree/main/examples/swebench#readme)

[Agents Previous](\concepts\agents) [Networks Next](\concepts\networks)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.