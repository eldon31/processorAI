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

- [Adding a Smithery MCP Server to your Agent](#adding-a-smithery-mcp-server-to-your-agent)

Integrations

# Smithery - MCP Registry

Provide your Agents with hundred of prebuilt tools to interact with

[Smithery](https://smithery.ai/) is an MCP ( [Model Context Protocol](https://modelcontextprotocol.io/introduction) ) servers registry, listing more than 2,000 MCP servers across multiple use cases:

- Code related tasks (ex: GitHub, [E2B](\integrations\e2b) )
- Web Search Integration (ex: Brave, [Browserbase](\integrations\browserbase) )
- Database Integration (ex: Neon, Supabase)
- Financial Market Data
- Data &amp; App Analysis
- And more...

## [ Adding a Smithery MCP Server to your Agent](#adding-a-smithery-mcp-server-to-your-agent)

1

Install AgentKit

Within an existing project, install AgentKit along with the Smithery SDK:

npm pnpm yarn Copy Ask AI

```
npm install @inngest/agent-kit inngest @smithery/sdk
```

Don't have an existing project?

To create a new project, create a new directory then initialize using your package manager:

npm pnpm yarn Copy Ask AI

```
mkdir my-agent-kit-project && npm init
```

2

2. Setup an AgentKit Newtork with an Agent

Create an Agent and its associated Network, for example a Neon Assistant Agent:

Copy Ask AI

```
import { z } from "zod" ;
import {
anthropic ,
createAgent ,
createNetwork ,
createTool ,
} from "@inngest/agent-kit" ;

const neonAgent = createAgent ({
name: "neon-agent" ,
system: `You are a helpful assistant that help manage a Neon account.
IMPORTANT: Call the 'done' tool when the question is answered.
` ,
tools: [
createTool ({
name: "done" ,
description: "Call this tool when you are finished with the task." ,
parameters: z . object ({
answer: z . string (). describe ( "Answer to the user's question." ),
}),
handler : async ({ answer }, { network }) => {
network ?. state . kv . set ( "answer" , answer );
},
}),
],
});

const neonAgentNetwork = createNetwork ({
name: "neon-agent" ,
agents: [ neonAgent ],
defaultModel: anthropic ({
model: "claude-3-5-sonnet-20240620" ,
defaultParameters: {
max_tokens: 1000 ,
},
}),
router : ({ network }) => {
if ( ! network ?. state . kv . get ( "answer" )) {
return neonAgent ;
}
return ;
},
});
```

3

Add the Neon MCP Smithery Server to your Agent

Add the [Neon MCP Smithery Server](https://smithery.ai/server/neon/) to your Agent by using `createSmitheryUrl()` from the `@smithery/sdk/config.js` module

and providing it to the Agent via the

`mcpServers` option:

Copy Ask AI

```
import {
anthropic ,
createAgent ,
createNetwork ,
createTool ,
} from "@inngest/agent-kit" ;
import { createSmitheryUrl } from "@smithery/sdk/config.js" ;
import { z } from "zod" ;

const smitheryUrl = createSmitheryUrl ( "https://server.smithery.ai/neon/ws" , {
neonApiKey: process . env . NEON_API_KEY ,
});

const neonAgent = createAgent ({
name: "neon-agent" ,
system: `You are a helpful assistant that help manage a Neon account.
IMPORTANT: Call the 'done' tool when the question is answered.
` ,
tools: [
createTool ({
name: "done" ,
description: "Call this tool when you are finished with the task." ,
parameters: z . object ({
answer: z . string (). describe ( "Answer to the user's question." ),
}),
handler : async ({ answer }, { network }) => {
network ?. state . kv . set ( "answer" , answer );
},
}),
],
mcpServers: [
{
name: "neon" ,
transport: {
type: "ws" ,
url: smitheryUrl . toString (),
},
},
],
});

const neonAgentNetwork = createNetwork ({
name: "neon-agent" ,
agents: [ neonAgent ],
defaultModel: anthropic ({
model: "claude-3-5-sonnet-20240620" ,
defaultParameters: {
max_tokens: 1000 ,
},
}),
router : ({ network }) => {
if ( ! network ?. state . kv . get ( "answer" )) {
return neonAgent ;
}
return ;
},
});
```

Integrating Smithery with AgentKit requires using the `createSmitheryUrl()` function to create a valid URL for the MCP server. Most Smithery servers instruct to use the `createTransport()` function which is not supported by AgentKit.

To use the

`createSmitheryUrl()` function, simply append `/ws` to the end of the Smithery server URL provided by Smithery.

You will find the complete example on GitHub:

## [Neon Assistant Agent (using MCP)](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme)

[This examples shows how to use the](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme) [Neon MCP Smithery Server](https://smithery.ai/server/neon/) [to build a Neon Assistant Agent that can help you manage your Neon databases. Agents Tools Network Integrations Code-based Router](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme)

[Using AgentKit with Browserbase Previous](\integrations\browserbase)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.