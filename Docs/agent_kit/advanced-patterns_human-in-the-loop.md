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

- [Creating a "Human in the Loop" tool](#creating-a-%E2%80%9Chuman-in-the-loop%E2%80%9D-tool)
- [Example: Support Agent with Human in the Loop](#example%3A-support-agent-with-human-in-the-loop)
- [Transforming your AgentKit network into an Inngest function](#transforming-your-agentkit-network-into-an-inngest-function)
- [Add a ask\_developer tool to the network](#add-a-ask-developer-tool-to-the-network)
- [Try it out](#try-it-out)

Advanced Patterns

# Human in the Loop

Enable your Agents to wait for human input.

Agents such as Support Agents, Coding or Research Agents might require human oversight.

By combining AgentKit with Inngest, you can create [Tools](\concepts\tools) that can wait for human input.

## [ Creating a "Human in the Loop" tool](#creating-a-%E2%80%9Chuman-in-the-loop%E2%80%9D-tool)

"Human in the Loop" tools are implemented using Inngest's [`waitForEvent()`](https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-event) step method:

Copy Ask AI

```
import { createTool } from "@inngest/agent-kit" ;

createTool ({
name: "ask_developer" ,
description: "Ask a developer for input on a technical issue" ,
parameters: z . object ({
question: z . string (). describe ( "The technical question for the developer" ),
context: z . string (). describe ( "Additional context about the issue" ),
}),
handler : async ({ question , context }, { step }) => {
if ( ! step ) {
return { error: "This tool requires step context" };
}

// Example: Send a Slack message to the developer

// Wait for developer response event
const developerResponse = await step . waitForEvent ( "developer.response" , {
event: "app/support.ticket.developer-response" ,
timeout: "4h" ,
match: "data.ticketId" ,
});

if ( ! developerResponse ) {
return { error: "No developer response provided" };
}

return {
developerResponse: developerResponse . data . answer ,
responseTime: developerResponse . data . timestamp ,
};
},
});
```

The `ask_developer` tool will wait up to 4 hours for a `"developer.response"` event to be received, pausing the execution of the AgentKit network.

The incoming

`"developer.response"` event will be matched against the `data.ticketId` field of the event that trigger the AgentKit network.

For this reason, the AgentKit network will need to be wrapped in an Inngest function as demonstrated in the next section.

## [ Example: Support Agent with Human in the Loop](#example%3A-support-agent-with-human-in-the-loop)

Let's consider a Support Agent Network automously triaging and solving tickets:

Copy Ask AI

```
const customerSupportAgent = createAgent ({
name: "Customer Support" ,
description:
"I am a customer support agent that helps customers with their inquiries." ,
system: `You are a helpful customer support agent.
Your goal is to assist customers with their questions and concerns.
Be professional, courteous, and thorough in your responses.` ,
model: anthropic ({
model: "claude-3-5-haiku-latest" ,
max_tokens: 1000 ,
}),
tools: [
searchKnowledgeBase ,
// ...
],
});

const technicalSupportAgent = createAgent ({
name: "Technical Support" ,
description: "I am a technical support agent that helps critical tickets." ,
system: `You are a technical support specialist.
Your goal is to help resolve critical tickets.
Use your expertise to diagnose problems and suggest solutions.
If you need developer input, use the ask_developer tool.` ,
model: anthropic ({
model: "claude-3-5-haiku-latest" ,
max_tokens: 1000 ,
}),
tools: [
searchLatestReleaseNotes ,
// ...
],
});

const supervisorRoutingAgent = createRoutingAgent ({
// ...
});

// Create a network with the agents and default router
const supportNetwork = createNetwork ({
name: "Support Network" ,
agents: [ customerSupportAgent , technicalSupportAgent ],
defaultModel: anthropic ({
model: "claude-3-5-haiku-latest" ,
max_tokens: 1000 ,
}),
router: supervisorRoutingAgent ,
});
```

You can find the complete example code in the [examples/support-agent-human-in-the-loop](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop) directory.

To avoid the Support Agent to be stuck or classifying tickets incorrectly, we'll implement a "Human in the Loop" tool to enable a human to add some context.

To implement a "Human in the Loop" tool, we'll need to embed our AgentKit network into an Inngest function.

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

const customerSupportAgent = createAgent ({
name: "Customer Support" ,
// ..
});

const technicalSupportAgent = createAgent ({
name: "Technical Support" ,
// ..
});

// Create a network with the agents and default router
const supportNetwork = createNetwork ({
name: "Support Network" ,
agents: [ customerSupportAgent , technicalSupportAgent ],
// ..
});

const supportAgentWorkflow = inngest . createFunction (
{
id: "support-agent-workflow" ,
},
{
event: "app/support.ticket.created" ,
},
async ({ step , event }) => {
const ticket = await step . run ( "get_ticket_details" , async () => {
const ticket = await getTicketDetails ( event . data . ticketId );
return ticket ;
});

if ( ! ticket || "error" in ticket ) {
throw new NonRetriableError ( `Ticket not found: ${ ticket . error } ` );
}

const response = await supportNetwork . run ( ticket . title );

return {
response ,
ticket ,
};
}
);

// Create and start the server
const server = createServer ({
functions: [ supportAgentWorkflow as any ],
});

server . listen ( 3010 , () =>
console . log ( "Support Agent demo server is running on port 3010" )
);
```

The `network.run()` is now performed by the Inngest function.

Don't forget to register the function with `createServer` 's `functions` property.

### [ Add a ask\_developer tool to the network](#add-a-ask-developer-tool-to-the-network)

Our AgentKit network is now ran inside an Inngest function triggered by the `"app/support.ticket.created"` event which carries

the

`data.ticketId` field.

The `Technical Support` Agent will now use the `ask_developer` tool to ask a developer for input on a technical issue:

Copy Ask AI

```
import { createTool } from "@inngest/agent-kit" ;

createTool ({
name: "ask_developer" ,
description: "Ask a developer for input on a technical issue" ,
parameters: z . object ({
question: z . string (). describe ( "The technical question for the developer" ),
context: z . string (). describe ( "Additional context about the issue" ),
}),
handler : async ({ question , context }, { step }) => {
if ( ! step ) {
return { error: "This tool requires step context" };
}

// Example: Send a Slack message to the developer

// Wait for developer response event
const developerResponse = await step . waitForEvent ( "developer.response" , {
event: "app/support.ticket.developer-response" ,
timeout: "4h" ,
match: "data.ticketId" ,
});

if ( ! developerResponse ) {
return { error: "No developer response provided" };
}

return {
developerResponse: developerResponse . data . answer ,
responseTime: developerResponse . data . timestamp ,
};
},
});
```

Our `ask_developer` tool will now wait for a `"developer.response"` event to be received (ex: from a Slack message), and match it against the `data.ticketId` field.

The result of the `ask_developer` tool will be returned to the `Technical Support` Agent.

Look at the Inngest [`step.waitForEvent()`](https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-event) documentation for more details and examples.

### [ Try it out](#try-it-out)

## [Support Agent with "Human in the loop"](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[This Support AgentKit Network is composed of two Agents (Customer Support and](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[Technical Support) and a Supervisor Agent that routes the ticket to the](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[correct Agent. The Technical Support Agent can wait for a developer response](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[when facing complex technical issues.](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[MCP as tools Previous](\advanced-patterns\mcp) [Multi-steps tools Next](\advanced-patterns\multi-steps-tools)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.