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

- [Configuring Retries](#configuring-retries)
- [Transforming your AgentKit network into an Inngest function](#transforming-your-agentkit-network-into-an-inngest-function)
- [Configuring a custom retry policy](#configuring-a-custom-retry-policy)
- [Going further](#going-further)

Advanced Patterns

# Configuring Retries

Configure retries for your AgentKit network Agents and Tool calls.

Using AgentKit alongside Inngest enables automatic retries for your AgentKit network Agents and Tools calls.

The default retry policy is to retry 4 times with exponential backoff and can be configured by following the steps below.

**Prerequisites** Your AgentKit network [must be configured with Inngest](\getting-started\local-development#1-install-the-inngest-package) .

## [ Configuring Retries](#configuring-retries)

Configuring a custom retry policy is done by transforming your AgentKit network into an Inngest function.

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

### [ Configuring a custom retry policy](#configuring-a-custom-retry-policy)

We can now configure the capacity by user by adding concurrency and throttling configuration to our Inngest function:

src/inngest/agent-network.ts Copy Ask AI

```
import { createAgent , createNetwork , openai } from '@inngest/agent-kit' ;
import { createServer } from '@inngest/agent-kit/server' ;

import { inngest } from './inngest/client' ;

// network and agent definitions..

const deepResearchNetworkFunction = inngest . createFunction ({
id: 'deep-research-network' ,
retries: 1
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

Your AgentKit network will now retry once on any failure happening during a single execution cycle of your network.

## [ Going further](#going-further)

## [Configuring Multitenancy](\advanced-patterns\multitenancy)

[Learn how to configure user-based capacity for your AgentKit network.](\advanced-patterns\multitenancy)

[Multi-steps tools Previous](\advanced-patterns\multi-steps-tools) [Configuring Multi-tenancy Next](\advanced-patterns\multitenancy)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.