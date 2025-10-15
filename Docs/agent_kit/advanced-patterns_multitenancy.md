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

- [Configuring Multi-tenancy](#configuring-multi-tenancy)
- [Transforming your AgentKit network into an Inngest function](#transforming-your-agentkit-network-into-an-inngest-function)
- [Configuring a concurrency per user](#configuring-a-concurrency-per-user)
- [Going further](#going-further)

Advanced Patterns

# Configuring Multi-tenancy

Configure capacity based on users or organizations.

As discussed in the [deployment guide](\concepts\deployment) , moving an AgentKit network into users' hands requires configuring usage limits.

To avoid having one user's usage affect another, you can configure multi-tenancy.

Multi-tenancy consists of configuring limits based on users or organizations ( *called "tenants"* ).

It can be easily configured on your AgentKit network using Inngest.

**Prerequisites** Your AgentKit network [must be configured with Inngest](\getting-started\local-development#1-install-the-inngest-package) .

## [ Configuring Multi-tenancy](#configuring-multi-tenancy)

Adding multi-tenancy to your AgentKit network is done by transforming your AgentKit network into an Inngest function.

### [ Transforming your AgentKit network into an Inngest function](#transforming-your-agentkit-network-into-an-inngest-function)

First, you'll need to create an Inngest Client:

src/inngest/client.ts Copy Ask AI

```
import { Inngest } from "inngest" ;

const inngest = new Inngest ({
id: "my-agentkit-network" ,
});
```

Then, transform your AgentKit network into an Inngest function as follows:

src/inngest/agent-network.ts Copy Ask AI

```
import { createAgent , createNetwork , openai } from "@inngest/agent-kit" ;
import { createServer } from "@inngest/agent-kit/server" ;

import { inngest } from "./inngest/client" ;

const deepResearchAgent = createAgent ({
name: "Deep Research Agent" ,
tools: [
/* ... */
],
});

const network = createNetwork ({
name: "My Network" ,
defaultModel: openai ({ model: "gpt-4o" }),
agents: [ deepResearchAgent ],
});

const deepResearchNetworkFunction = inngest . createFunction (
{
id: "deep-research-network" ,
},
{
event: "deep-research-network/run" ,
},
async ({ event , step }) => {
const { input } = event . data ;
return network . run ( input );
}
);

const server = createServer ({
functions: [ deepResearchNetworkFunction ],
});

server . listen ( 3010 , () => console . log ( "Agent kit running!" ));
```

The `network.run()` is now performed by the Inngest function.

Don't forget to register the function with `createServer` 's `functions` property.

### [ Configuring a concurrency per user](#configuring-a-concurrency-per-user)

We can now configure the capacity by user by adding concurrency and throttling configuration to our Inngest function:

src/inngest/agent-network.ts Copy Ask AI

```
import { createAgent , createNetwork , openai } from '@inngest/agent-kit' ;
import { createServer } from '@inngest/agent-kit/server' ;

import { inngest } from './inngest/client' ;

// network and agent definitions..

const deepResearchNetworkFunction = inngest . createFunction ({
id: 'deep-research-network' ,
concurrency: [
{
key: "event.data.user_id" ,
limit: 10 ,
},
],
}, {
event: "deep-research-network/run"
}, async ({ event , step }) => {
const { input } = event . data ;

return network . run ( input );
})

const server = createServer ({
functions: [ deepResearchNetworkFunction ],
});

server . listen ( 3010 , () => console . log ( "Agent kit running!" ));
```

Your AgentKit network will now be limited to 10 concurrent requests per user.

The same can be done to add [throttling](https://www.inngest.com/docs/guides/throttling?ref=agentkit-docs-multitenancy) , [rate limiting](https://www.inngest.com/docs/guides/rate-limiting?ref=agentkit-docs-multitenancy) or [priority](https://www.inngest.com/docs/guides/priority?ref=agentkit-docs-multitenancy) .

## [ Going further](#going-further)

## [Customizing the retries](\advanced-patterns\retries)

[Learn how to customize the retries of your multi-steps tools.](\advanced-patterns\retries)

[Configuring Retries Previous](\advanced-patterns\retries) [UI Streaming with useAgent Next](\advanced-patterns\legacy-ui-streaming)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.