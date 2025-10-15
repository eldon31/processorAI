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

Get Started

# AgentKit

A TypeScript library to create and orchestrate AI Agents.

AgentKit is a framework to build AI Agents, from single model inference calls to multi-agent systems that use tools. Designed with orchestration at its core, AgentKit enables developers to build, test, and deploy reliable AI applications at scale.

With AgentKit, you get:

✨ **Simple and composable primitives** to build from simple Support Agents to semi-autonomous Coding Agents.

🧠 **Support for** [**OpenAI, Anthropic, Gemini**](\concepts\models) and all OpenAI API compatible models.

🛠️ **Powerful tools building API** with support for [MCP as tools](\advanced-patterns\mcp) .

🔌 **Integrates** with your favorite AI libraries and products (ex: [E2B](\integrations\e2b) , [Browserbase](\integrations\browserbase) , [Smithery](\integrations\smithery) ).

⚡ **Stream live updates** to your UI with [UI Streaming](\advanced-patterns\ui-streaming) .

📊 [**Local Live traces**](\getting-started\local-development) **and input/output logs** when combined with the Inngest Dev Server.

New to AI Agents? Follow our [Guided Tour](\guided-tour\overview) to learn how to build your first AgentKit application.

All the above sounds familiar? Check our [**Getting started section**](#getting-started) or the [**"How AgentKit works" section**](#how-agentkit-works) to learn more about AgentKit's architecture.

## [ Getting started](#getting-started)

## [Quick start](\getting-started\quick-start)

[Jump into the action by building your first AgentKit application.](\getting-started\quick-start)

## [Examples](\examples\overview)

[Looking for inspiration? Check out our examples to see how AgentKit can be](\examples\overview)

[used.](\examples\overview)

## [Concepts](\concepts\agents)

[Learn the core concepts of AgentKit.](\concepts\agents)

## [SDK Reference](\reference\introduction)

[Ready to dive into the code? Browse the SDK reference to learn more about](\reference\introduction)

[AgentKit's primitives.](\reference\introduction)

## [ How AgentKit works](#how-agentkit-works)

AgentKit enables developers to compose simple single-agent systems or entire *systems of agents* in which multiple agents can work together. [**Agents**](\concepts\agents) are combined into [**Networks**](concepts\networks) which include a [**Router**](concepts\routers) to determine which Agent should be called.

Their system's memory is recorded as Network

[**State**](concepts\state) which

can be used by the Router, Agents or

[**Tools**](concepts\tools) to

collaborate on tasks.

The entire system is orchestration-aware and allows for customization at runtime for dynamic, powerful AI workflows and agentic systems. Here is what a simple Network looks like in code:

Copy Ask AI

```
import {
createNetwork ,
createAgent ,
openai ,
anthropic ,
} from "@inngest/agent-kit" ;
import { searchWebTool } from "./tools" ;

const navigator = createAgent ({
name: "Navigator" ,
system: "You are a navigator..." ,
tools: [ searchWebTool ],
});

const classifier = createAgent ({
name: "Classifier" ,
system: "You are a classifier..." ,
model: openai ( "gpt-3.5-turbo" ),
});

const summarizer = createAgent ({
model: anthropic ( "claude-3-5-haiku-latest" ),
name: "Summarizer" ,
system: "You are a summarizer..." ,
});

const network = createNetwork ({
agents: [ navigator , classifier , summarizer ],
defaultModel: openai ({ model: "gpt-4o" }),
});

const input = `Classify then summarize the latest 10 blog posts
on https://www.deeplearning.ai/blog/` ;

const result = await network . run ( input , ({ network }) => {
return defaultRoutingAgent ;
});
```

## [ llms.txt](#llms-txt)

You can access the entire AgentKit docs in markdown format at [agentkit.inngest.com/llms-full.txt](https://agentkit.inngest.com/llms-full.txt) . This is useful for passing the entire docs to an LLM, AI-enabled IDE, or similar tool to answer questions about AgentKit.

If your context window is too small to pass the entire docs, you can use the shorter [agentkit.inngest.com/llms.txt](https://agentkit.inngest.com/llms.txt) file which offers a table of contents for LLMs or other developer tools to index the docs more easily.

[Quick start Next](\getting-started\quick-start)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.