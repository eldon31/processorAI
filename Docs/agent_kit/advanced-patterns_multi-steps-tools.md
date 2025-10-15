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

- [Creating a multi-steps tool](#creating-a-multi-steps-tool)
- [Using the multi-steps tool in your AgentKit network](#using-the-multi-steps-tool-in-your-agentkit-network)
- [Going further](#going-further)

Advanced Patterns

# Multi-steps tools

Use multi-steps tools to create more complex Agents.

In this guide, we'll learn how to create a multi-steps tool that can be used in your AgentKit [Tools](\concepts\tools) to reliably perform complex operations.

By combining your AgentKit network with Inngest, each step of your tool will be **retried automatically** and you'll be able to **configure concurrency and throttling** .

**Prerequisites** Your AgentKit network [must be configured with Inngest](\getting-started\local-development#1-install-the-inngest-package) .

## [ Creating a multi-steps tool](#creating-a-multi-steps-tool)

Creating a multi-steps tool is done by creating an Inngest Function that will be used as a tool in your AgentKit network.

To create an Inngest Function, you'll need to create an Inngest Client:

src/inngest/client.ts Copy Ask AI

```
import { Inngest } from 'inngest' ;

const inngest = new Inngest ({
id: 'my-agentkit-network' ,
});
```

Then, we will implement our AgentKit Tool as an Inngest Function with multiple steps.

For example, we'll create a tool that searches for perform a research by crawling the web:

src/inngest/tools/research-web.ts Copy Ask AI

```
import { inngest } from '../client' ;

export const researchWebTool = inngest . createFunction ({
id: 'research-web-tool' ,
}, {
event: "research-web-tool/run"
}, async ({ event , step }) => {
const { input } = event . data ;

const searchQueries = await step . ai . infer ( 'generate-search-queries' , {
model: step . ai . models . openai ({ model: "gpt-4o" }),
// body is the model request, which is strongly typed depending on the model
body: {
messages: [{
role: "user" ,
content: `From the given input, generate a list of search queries to perform. \n ${ input } ` ,
}],
},
});

const searchResults = await Promise . all (
searchQueries . map ( query => step . run ( 'crawl-web' , async ( query ) => {
// perform crawling...
})
));

const summary = await step . ai . infer ( 'summarize-search-results' , {
model: step . ai . models . openai ({ model: "gpt-4o" }),
body: {
messages: [{
role: "user" ,
content: `Summarize the following search results: \n ${ searchResults . join ( ' \n ' ) } ` ,
}],
},
});

return summary . choices [ 0 ]. message . content ;
});
```

Our `researchWebTool` Inngest defines 3 main steps.

- The `step.ai.infer()` call will offload the LLM requests to the Inngest infrastructe which will also handle retries.
- The `step.run()` call will run the `crawl-web` step in parallel.

All the above steps will be retried automatically in case of failure, resuming the AgentKit network upon completion of the tool.

## [ Using the multi-steps tool in your AgentKit network](#using-the-multi-steps-tool-in-your-agentkit-network)

We can now add our `researchWebTool` to our AgentKit network:

src/inngest/agent-network.ts Copy Ask AI

```
import { createAgent , createNetwork , openai } from '@inngest/agent-kit' ;
import { createServer } from '@inngest/agent-kit/server' ;

import { researchWebTool } from './inngest/tools/research-web' ;


const deepResearchAgent = createAgent ({
name: 'Deep Research Agent' ,
tools: [ researchWebTool ],
});

const network = createNetwork ({
name: 'My Network' ,
defaultModel: openai ({ model: "gpt-4o" }),
agents: [ deepResearchAgent ],
});

const server = createServer ({
networks: [ network ],
functions: [ researchWebTool ],
});

server . listen ( 3010 , () => console . log ( "Agent kit running!" ));
```

We first import our `researchWebTool` function and pass it to the `deepResearchAgent` [`tools`](\reference\create-agent#param-tools) [array](\reference\create-agent#param-tools) .

Finally, we also need to pass the `researchWebTool` function to the `createServer()` 's `functions` array.

## [ Going further](#going-further)

## [Configuring Multitenancy](\advanced-patterns\multitenancy)

[Learn how to configure user-based capacity for your AgentKit network.](\advanced-patterns\multitenancy)

## [Customizing the retries](\advanced-patterns\retries)

[Learn how to customize the retries of your multi-steps tools.](\advanced-patterns\retries)

[Human in the Loop Previous](\advanced-patterns\human-in-the-loop) [Configuring Retries Next](\advanced-patterns\retries)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.