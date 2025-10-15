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

- [How to use a model](#how-to-use-a-model)
- [Create a model instance](#create-a-model-instance)
- [Configure model hyper parameters (temperature, etc.)](#configure-model-hyper-parameters-temperature%2C-etc)
- [Providing a model instance to an Agent](#providing-a-model-instance-to-an-agent)
- [Providing a model instance to a Network](#providing-a-model-instance-to-a-network)
- [List of supported models](#list-of-supported-models)
- [Environment variable used for each model provider](#environment-variable-used-for-each-model-provider)
- [Contribution](#contribution)

Concepts

# Models

Leverage different provider's models across Agents.

Within AgentKit, models are adapters that wrap a given provider (ex. OpenAI, Anthropic)'s specific model version (ex. `gpt-3.5` ).

Each [Agent](\concepts\agents) can each select their own model to use and a [Network](\concepts\networks) can select a default model.

Copy Ask AI

```
import { openai , anthropic , gemini } from "@inngest/agent-kit" ;
```

## [ How to use a model](#how-to-use-a-model)

### [ Create a model instance](#create-a-model-instance)

Each model helper will first try to get the API Key from the environment

variable. The API Key can also be provided with the

`apiKey` option to the

model helper.

OpenAI Anthropic Gemini Copy Ask AI

```
import { openai , createAgent } from "@inngest/agent-kit" ;


const model = openai ({ model: "gpt-3.5-turbo" });
const modelWithApiKey = openai ({ model: "gpt-3.5-turbo" , apiKey: "sk-..." });
```

### [ Configure model hyper parameters (temperature, etc.)](#configure-model-hyper-parameters-temperature%2C-etc)

You can configure the model hyper parameters (temperature, etc.) by passing the `defaultParameters` option:

OpenAI Anthropic Gemini Copy Ask AI

```
import { openai , createAgent } from "@inngest/agent-kit" ;

const model = openai ({
model: "gpt-3.5-turbo" ,
defaultParameters: { temperature: 0.5 },
});
```

The full list of hyper parameters can be found in the [types definition of](https://github.com/inngest/inngest-js/tree/main/packages/ai/src/models)

[each](https://github.com/inngest/inngest-js/tree/main/packages/ai/src/models)

[model](https://github.com/inngest/inngest-js/tree/main/packages/ai/src/models)

.

### [ Providing a model instance to an Agent](#providing-a-model-instance-to-an-agent)

Copy Ask AI

```
import { createAgent } from "@inngest/agent-kit" ;

const supportAgent = createAgent ({
model: openai ({ model: "gpt-3.5-turbo" }),
name: "Customer support specialist" ,
system: "You are an customer support specialist..." ,
tools: [ listChargesTool ],
});
```

### [ Providing a model instance to a Network](#providing-a-model-instance-to-a-network)

The provided `defaultModel` will be used for all Agents without a model

specified. It will also be used by the "

[Default Routing](\concepts\routers#default-routing-agent-autonomous-routing)

[Agent](\concepts\routers#default-routing-agent-autonomous-routing)

" if

enabled.

Copy Ask AI

```
import { createNetwork } from "@inngest/agent-kit" ;

const network = createNetwork ({
agents: [ supportAgent ],
defaultModel: openai ({ model: "gpt-4o" }),
});
```

## [ List of supported models](#list-of-supported-models)

For a full list of supported models, you can always check [the models directory here](https://github.com/inngest/inngest-js/tree/main/packages/ai/src/models) .

OpenAI Anthropic Gemini Grok Copy Ask AI

```
"gpt-4.5-preview"
"gpt-4o"
"chatgpt-4o-latest"
"gpt-4o-mini"
"gpt-4"
"o1"
"o1-preview"
"o1-mini"
"o3-mini"
"gpt-4-turbo"
"gpt-3.5-turbo"
```

### [ Environment variable used for each model provider](#environment-variable-used-for-each-model-provider)

- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Gemini: `GEMINI_API_KEY`
- Grok: `XAI_API_KEY`

## [ Contribution](#contribution)

Is there a model that you'd like to see included in AgentKit? Open an issue, create a pull request, or chat with the team on [Discord in the #ai channel](https://www.inngest.com/community) .

## [Contribute on GitHub](https://github.com/inngest/agent-kit)

[Fork, clone, and open a pull request.](https://github.com/inngest/agent-kit)

[Memory Previous](\concepts\memory) [Deployment Next](\concepts\deployment)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.