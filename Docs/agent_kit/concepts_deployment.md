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

- [Deploying your AgentKit network with Inngest](#deploying-your-agentkit-network-with-inngest)
- [1. Install the Inngest SDK](#1-install-the-inngest-sdk)
- [2. Serve your AgentKit network over HTTP](#2-serve-your-agentkit-network-over-http)
- [3. Deploy your AgentKit network](#3-deploy-your-agentkit-network)
- [4. Sync your AgentKit network with the Inngest Platform](#4-sync-your-agentkit-network-with-the-inngest-platform)
- [Configuring Multitenancy and Retries](#configuring-multitenancy-and-retries)

Concepts

# Deployment

Deploy your AgentKit networks to production.

Deploying an AgentKit network to production is straightforward but there are a few things to consider:

- **Scalability** : Your Network Agents rely on tools which interact with external systems. You'll need to ensure that your deployment environment can scale to handle the requirements of your network.
- **Reliability** : You'll need to ensure that your AgentKit network can handle failures and recover gracefully.
- **Multitenancy** : You'll need to ensure that your AgentKit network can handle multiple users and requests concurrently without compromising on performance or security.

All the above can be easily achieved by using Inngest alongside AgentKit.

By installing the Inngest SDK, your AgentKit network will automatically benefit from:

- [**Multitenancy support**](\advanced-patterns\multitenancy) with fine grained concurrency and throttling configuration
- **Retrieable and** [**parallel tool calls**](\advanced-patterns\retries) for reliable and performant tool usage
- **LLM requests offloading** to improve performance and reliability for Serverless deployments
- **Live and detailed observability** with step-by-step traces including the Agents inputs/outputs and token usage

You will find below instructions to configure your AgentKit network deployment with Inngest.

## [ Deploying your AgentKit network with Inngest](#deploying-your-agentkit-network-with-inngest)

Deploying your AgentKit network with Inngest to benefit from automatic retries, LLM requests offloading and live observability only requires

a few steps:

### [ 1. Install the Inngest SDK](#1-install-the-inngest-sdk)

npm pnpm yarn Copy Ask AI

```
npm install inngest
```

### [ 2. Serve your AgentKit network over HTTP](#2-serve-your-agentkit-network-over-http)

Update your AgentKit network to serve over HTTP as follows:

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

### [ 3. Deploy your AgentKit network](#3-deploy-your-agentkit-network)

**Configuring environment variables**

[Create an Inngest account](https://www.inngest.com/?ref=agentkit-docs-deployment) and open the top right menu to access your Event Key and Signing Key:

Create and copy an Event Key, and copy your Signing Key

Then configure the following environment variables into your deployment environment ( *ex: AWS, Vercel, GCP* ):

- `INNGEST_API_KEY` : Your Event Key
- `INNGEST_SIGNING_KEY` : Your Signing Key

**Deploying your AgentKit network**

You can now deploy your AgentKit network to your preferred cloud provider.

Once deployed, copy the deployment URL for the final configuration step.

### [ 4. Sync your AgentKit network with the Inngest Platform](#4-sync-your-agentkit-network-with-the-inngest-platform)

On your Inngest dashboard, click on the "Sync new app" button at the top right of the screen.

Then, paste the deployment URL into the "App URL" by adding `/api/inngest` to the end of the URL:

Sync your AgentKit network deployment with the Inngest Platform

**You sync is failing?** Read our [troubleshooting guide](https://www.inngest.com/docs/apps/cloud?ref=agentkit-docs-deployment#troubleshooting) for more information.

Once the sync succeeds, you can navigate to the *Functions* tabs where you will find your AgentKit network:

Your AgentKit network is now live and ready to use

Your AgentKit network can now be triggered manually from the Inngest Dashboard or [from your app using](\concepts\networks) [`network.run()`](\concepts\networks) .

## [ Configuring Multitenancy and Retries](#configuring-multitenancy-and-retries)

## [Multitenancy](\advanced-patterns\multitenancy)

[Configure usage limits based on users or organizations.](\advanced-patterns\multitenancy)

## [Retries](\advanced-patterns\retries)

[Learn how to configure retries for your AgentKit Agents and Tools.](\advanced-patterns\retries)

[Models Previous](\concepts\models) [Overview Next](\streaming\overview)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.