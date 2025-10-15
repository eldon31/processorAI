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

- [Creating a single agent](#creating-a-single-agent)
- [Creating a multi-agent network](#creating-a-multi-agent-network)
- [Next steps](#next-steps)

Get Started

# Quick start

Learn the basics of AgentKit in a few minutes.

In this tutorial, you will create an [Agent](\concepts\agents) and run it within a [Network](\concepts\networks) using AgentKit.

Follow this guide by forking the [quick-start](https://github.com/inngest/agent-kit/tree/main/examples/quick-start) example locally by running:

Copy Ask AI

```
npx git-ripper https://github.com/inngest/agent-kit/tree/main/examples/quick-start
```

## [ Creating a single agent](#creating-a-single-agent)

1

Install AgentKit

Within an existing project, install AgentKit and Inngest from npm:

npm pnpm yarn Copy Ask AI

```
npm install @inngest/agent-kit inngest
```

**Important:** Starting with AgentKit v0.9.0, `inngest` is a required peer dependency. You must install both packages together to ensure proper runtime compatibility and prevent conflicts. You can always find the latest release version on [npm](https://www.npmjs.com/package/@inngest/agent-kit) .

Don't have an existing project?

To create a new project, create a new directory and initialize it using your package manager:

npm pnpm yarn Copy Ask AI

```
mkdir my-agent-kit-project && npm init
```

2

Create an agent

To start, we'll create our first " [Agent](\concepts\agents) ." An Agent is an entity that has a specific role to answer questions or perform tasks (see "tools" below). Let's create a new file, `index.ts` . Using the `createAgent` constructor, give your agent a `name` , a `description` , and its initial `system` prompt. The `name` and `description` properties are used to help the LLM determine which Agent to call. You'll also specify which `model` you want the agent to use. Here we'll use Anthropic's [Claude 3.5 Haiku](https://docs.anthropic.com/en/docs/about-claude/models) model. ( [Model reference](\concepts\models) ) Your agent can be whatever you want, but in this quick start, we'll create a PostgreSQL database administrator agent:

index.ts Copy Ask AI

```
import { createAgent , anthropic } from '@inngest/agent-kit' ;

const dbaAgent = createAgent ({
name: 'Database administrator' ,
description: 'Provides expert support for managing PostgreSQL databases' ,
system:
'You are a PostgreSQL expert database administrator. ' +
'You only provide answers to questions related to PostgreSQL database schema, indexes, and extensions.' ,
model: anthropic ({
model: 'claude-3-5-haiku-latest' ,
defaultParameters: {
max_tokens: 1000 ,
},
}),
});
```

You'll also need to set your provider API keys as environment variables:

terminal Copy Ask AI

```
export ANTHROPIC_API_KEY = sk-ant-api03-XXXXXX ....
```

3

Run the server

Next, we'll create an HTTP server to run our agent. In the same file as our Agent definition:

index.ts Copy Ask AI

```
import { createAgent , anthropic } from '@inngest/agent-kit' ;
import { createServer } from '@inngest/agent-kit/server' ;
// ...
const server = createServer ({
agents: [ dbaAgent ],
});
server . listen ( 3000 , () => console . log ( 'AgentKit server running!' ));
```

Now we can run our AgentKit server using [`npx`](https://docs.npmjs.com/cli/v8/commands/npx) and [`tsx`](https://tsx.is/) (for easy TypeScript execution):

terminal Copy Ask AI

```
npx tsx ./index.ts
```

4

Test our agent

To test our agent, we'll use the [Inngest dev server](https://www.inngest.com/docs/local-development) to visually debug our agents. Using `npx` , we'll start the server and point it to our AgentKit server:

terminal Copy Ask AI

```
npx inngest-cli@latest dev -u http://localhost:3000/api/inngest
```

Now, open the dev server and select the functions tab ( `http://localhost:8288/functions` ) and click the "Invoke" button: In the Invoke function modal, specify the input prompt for your agent and click the "Invoke function" button:

Invoke payload Copy Ask AI

```
{
"data" : {
"input" : "How do I aggregate an integer column across a date column by week?"
}
}
```

You'll be redirected to watch the agent run and view the output:

A key benefit of AgentKit is the ability to create a system of agents called a

"

[Network](\concepts\networks) ." Networks are used to create AI Agents by combining

multiple specialized

[Agents](\concepts\agents) to answer more complex questions.

Let's transform our single agent into a network of two agents, capable of helping with

both database administration and security questions.

## [ Creating a multi-agent network](#creating-a-multi-agent-network)

1

Adding a second Agent

Agents collaborate in a Network by sharing a common [State](\concepts\state) . Let's update our Database Administrator Agent to include a tool to save the answer to the question in the database:

Copy Ask AI

```
const dbaAgent = createAgent ({
name: "Database administrator" ,
description: "Provides expert support for managing PostgreSQL databases" ,
system:
"You are a PostgreSQL expert database administrator. " +
"You only provide answers to questions related to PostgreSQL database schema, indexes, and extensions." ,
model: anthropic ({
model: "claude-3-5-haiku-latest" ,
defaultParameters: {
max_tokens: 4096 ,
},
}),
tools: [
createTool ({
name: "save_answer" ,
description: "Save the answer to the questions" ,
parameters: z . object ({
answer: z . string (),
}),
handler : async ({ answer }, { network } : Tool . Options < NetworkState >) => {
network . state . data . dba_agent_answer = answer ;
},
}),
],
});
```

[Tools](\concepts\tools) are based on [Tool](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)

[Calling](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)

,

enabling your Agent to interact with the

[State](\concepts\state) of the

Network, store data in external databases, or dynamically fetch data from

third-party APIs. Let's now create a second

*Database Security* Agent:

Copy Ask AI

```
import { createAgent , anthropic } from "@inngest/agent-kit" ;

// ...

const securityAgent = createAgent ({
name: "Database Security Expert" ,
description:
"Provides expert guidance on PostgreSQL security, access control, audit logging, and compliance best practices" ,
system:
"You are a PostgreSQL security expert. " +
"You only provide answers to questions related to PostgreSQL security topics such as encryption, access control, audit logging, and compliance best practices." ,
model: anthropic ({
model: "claude-3-5-haiku-latest" ,
defaultParameters: {
max_tokens: 1000 ,
},
}),
tools: [
createTool ({
name: "save_answer" ,
description: "Save the answer to the questions" ,
parameters: z . object ({
answer: z . string (),
}),
handler : async ({ answer }, { network } : Tool . Options < NetworkState >) => {
network . state . data . security_agent_answer = answer ;
},
}),
],
});
```

Our second Security Expert Agent is similar to the first, but with a different system prompt specifically for security questions. We can now create a network combining our "Database Administrator" and "Database Security" Agents, which enables us to answer more complex questions.

2

Creating a Network

Create a network using the `createNetwork` constructor. Define a `name` and include our agents from the previous step in the `agents` array. You must also configure a `router` that the [*Router*](\concepts\routers) will use to determine which agent to call:

Copy Ask AI

```
import { /*...*/ createNetwork } from "@inngest/agent-kit" ;

export interface NetworkState {
// answer from the Database Administrator Agent
dba_agent_answer ?: string ;

// answer from the Security Expert Agent
security_agent_answer ?: string ;
}

// ...
const devOpsNetwork = createNetwork < NetworkState >({
name: "DevOps team" ,
agents: [ dbaAgent , securityAgent ],
router : async ({ network }) => {
if ( ! network . state . data . security_agent_answer ) {
return securityAgent ;
} else if (
network . state . data . security_agent_answer &&
network . state . data . dba_agent_answer
) {
return ;
}
return dbaAgent ;
},
});

const server = createServer ({
agents: [ dbaAgent , securityAgent ],
networks: [ devOpsNetwork ],
});
```

The highlighted lines are the key parts of our AI Agent behavior:

- The `agents` property defines the agents that are part of the network
- The `router` function defines the logic for which agent to call next. In this example, we call the Database Administrator Agent followed by the Security Expert Agent before ending the network (by returning `undefined` ).

3

Test our network

We'll use the same approach to test our network as we did above. With your Inngest dev server running, open the dev server and select the functions tab ( `http://localhost:8288/functions` ) and click the "Invoke" button of the *DevOps team* function with the following payload:

Invoke payload Copy Ask AI

```
{
"data" : {
"input" : "I am building a Finance application. Help me answer the following 2 questions: \n - How can I scale my application to millions of requests per second? \n - How should I design my schema to ensure the safety of each organization's data?"
}
}
```

The network will now run through the Agents to answer the questions: You can inspect the answers of each Agent by selecting the *Finalization* step and inspecting the JSON payload in the right panel:

## [ Next steps](#next-steps)

Congratulations! You've now created your first AI Agent with AgentKit.

In this guide, you've learned that:

- [**Agents**](\concepts\agents) are the building blocks of AgentKit. They are used to call a single model to answer specific questions or perform tasks.
- [**Networks**](\concepts\networks) are groups of agents that can work together to achieve more complex goals.
- [**Routers**](\concepts\routers) , combined with [**State**](\concepts\state) , enable you to control the flow of your Agents.

The following guides will help you build more advanced AI Agents:

## [Adding Tools to Agents](\concepts\tools)

[Let your Agent act and gather data with tools](\concepts\tools)

## [Implementing reasoning-based routing](\concepts\routers)

[Learn how to dynamically route between agents](\concepts\routers)

You can also explore the following examples to see how to use AgentKit in more complex scenarios:

## [Support Agent with "Human in the loop"](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[This AgentKit example shows how to build a Support Agent Network with a "Human](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

[in the loop" pattern.](https://github.com/inngest/agent-kit/tree/main/examples/support-agent-human-in-the-loop#readme)

## [AgentKit SWE-bench](https://github.com/inngest/agent-kit/tree/main/examples/swebench#readme)

[This AgentKit example uses the SWE-bench dataset to train an agent to solve coding problems. It uses advanced tools to interact with files and codebases.](https://github.com/inngest/agent-kit/tree/main/examples/swebench#readme)

[AgentKit Previous](\overview) [Installation Next](\getting-started\installation)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.