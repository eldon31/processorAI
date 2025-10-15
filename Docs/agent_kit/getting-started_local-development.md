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

- [Using AgentKit with the Inngest Dev Server](#using-agentkit-with-the-inngest-dev-server)
- [1. Install the inngest package](#1-install-the-inngest-package)
- [2. Expose your AgentKit network over HTTP](#2-expose-your-agentkit-network-over-http)
- [3. Trigger your AgentKit network from the Inngest Dev Server](#3-trigger-your-agentkit-network-from-the-inngest-dev-server)
- [Features](#features)
- [Triggering your AgentKit network](#triggering-your-agentkit-network)
- [Inspect AgentKit Agents token usage, input and output](#inspect-agentkit-agents-token-usage%2C-input-and-output)
- [Rerun an AgentKit Agent with a different prompt](#rerun-an-agentkit-agent-with-a-different-prompt)

Get Started

# Local development

Run AgentKit locally with live traces and logs.

Developing AgentKit applications locally is a breeze when combined with the [Inngest Dev Server](https://www.inngest.com/docs/dev-server) .

The Inngest Dev Server is a local development tool that provides live traces and logs for your AgentKit applications, providing a

quicker feedback loop and full visibility into your AgentKit's state and Agent LLM calls:

## [ Using AgentKit with the Inngest Dev Server](#using-agentkit-with-the-inngest-dev-server)

### [ 1. Install the inngest package](#1-install-the-inngest-package)

To use AgentKit with the Inngest Dev Server, you need to install the `inngest` package.

npm pnpm yarn Copy Ask AI

```
npm install inngest
```

### [ 2. Expose your AgentKit network over HTTP](#2-expose-your-agentkit-network-over-http)

The Inngest Dev Server needs to be able to trigger your AgentKit network over HTTP.

If your AgentKit network runs as a CLI, a few lines changes will make it available over HTTP:

Copy Ask AI

```
import { createNetwork } from '@inngest/agent-kit' ;
import { createServer } from '@inngest/agent-kit/server' ;

const network = createNetwork ({
name: 'My Network' ,
agents: [ /* ... */ ],
});

const server = createServer ({
networks: [ network ],
});

server . listen ( 3010 , () => console . log ( "Agent kit running!" ));
```

Now, starting your AgentKit script will make it available over HTTP.

Let's now trigger our AgentKit network from the Inngest Dev Server.

### [ 3. Trigger your AgentKit network from the Inngest Dev Server](#3-trigger-your-agentkit-network-from-the-inngest-dev-server)

You can start the Inngest Dev Server with the following command:

Copy Ask AI

```
npx inngest-cli@latest dev
```

And navigate to the Inngest Dev Server by opening [http://127.0.0.1:8288](http://127.0.0.1:8288/) in your browser.

You can now explore the Inngest Dev Server features:

## [ Features](#features)

### [ Triggering your AgentKit network](#triggering-your-agentkit-network)

You can trigger your AgentKit network by clicking on the "Trigger" button in the Inngest Dev Server from the "Functions" tab.

In the opened, add an

`input` property with the input you want to pass to your AgentKit network:

Then, click on the "Run" button to trigger your AgentKit network"

### [ Inspect AgentKit Agents token usage, input and output](#inspect-agentkit-agents-token-usage%2C-input-and-output)

In the run view of your AgentKit network run, the Agents step will be highlighted with a ✨ green icon.

By expanding the step, you can inspect the Agents:

- The **model used** , ex: `gpt-4o`
- The **token usage** detailed as prompt tokens, completion tokens, and total tokens
- The **input** provided to the Agent
- The **output** provided by the Agent

**Tips** You can force line breaks to **make the input and output more readable** using the following button: You can **expand the input and output view to show its full content** using the following button: You can **update the input of an AgentKit Agent and trigger a rerun from this step** of the AgentKit network ( *see below* )

### [ Rerun an AgentKit Agent with a different prompt](#rerun-an-agentkit-agent-with-a-different-prompt)

On a given AgentKit Agent run, you can update the input of the Agent and trigger a rerun from this step of the AgentKit network.

First, click on the "Rerun with new prompt" button under the input area.

Then, the following modal will open:

[Installation Previous](\getting-started\installation) [Agents Next](\concepts\agents)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.