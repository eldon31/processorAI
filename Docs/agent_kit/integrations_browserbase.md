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

- [Building AgentKit tools using Browserbase](#building-agentkit-tools-using-browserbase)
- [Example: Reddit Search Agent using Browserbase](#example%3A-reddit-search-agent-using-browserbase)
- [Enable autonomous browsing with Stagehand](#enable-autonomous-browsing-with-stagehand)

Integrations

# Using AgentKit with Browserbase

Develop AI Agents that can browse the web

[Browserbase](https://www.browserbase.com/) provides managed [headless browsers](https://docs.browserbase.com/introduction/what-is-headless-browser) to

enable Agents to browse the web autonomously.

There are two ways to use Browserbase with AgentKit:

- **Create your own Browserbase tools** : useful if you want to build simple actions on webpages with manual browser control.
- **Use Browserbase's** [**Stagehand**](https://www.stagehand.dev/) **library as tools** : a better approach for autonomous browsing and resilient scraping.

## [ Building AgentKit tools using Browserbase](#building-agentkit-tools-using-browserbase)

Creating AgentKit [tools](\concepts\tools) using the Browserbase TypeScript SDK is straightforward.

1

Install AgentKit

Within an existing project, install AgentKit, Browserbase and Playwright core:

npm pnpm yarn Copy Ask AI

```
npm install @inngest/agent-kit inngest @browserbasehq/sdk playwright-core
```

Don't have an existing project?

To create a new project, create a new directory then initialize using your package manager:

npm pnpm yarn Copy Ask AI

```
mkdir my-agent-kit-project && npm init
```

2

2. Setup an AgentKit Newtork with an Agent

Create a Agent and its associated Network, for example a Reddit Search Agent:

Copy Ask AI

```
import {
anthropic ,
createAgent ,
createNetwork ,
} from "@inngest/agent-kit" ;

const searchAgent = createAgent ({
name: "reddit_searcher" ,
description: "An agent that searches Reddit for relevant information" ,
system:
"You are a helpful assistant that searches Reddit for relevant information." ,
});

// Create the network
const redditSearchNetwork = createNetwork ({
name: "reddit_search_network" ,
description: "A network that searches Reddit using Browserbase" ,
agents: [ searchAgent ],
maxIter: 2 ,
defaultModel: anthropic ({
model: "claude-3-5-sonnet-latest" ,
max_tokens: 4096 ,
});
```

3

Create a Browserbase tool

Let's configure the Browserbase SDK and create a tool that can search Reddit:

Copy Ask AI

```
import {
anthropic ,
createAgent ,
createNetwork ,
createTool ,
} from "@inngest/agent-kit" ;
import { z } from "zod" ;
import { chromium } from "playwright-core" ;
import Browserbase from "@browserbasehq/sdk" ;

const bb = new Browserbase ({
apiKey: process . env . BROWSERBASE_API_KEY as string ,
});

// Create a tool to search Reddit using Browserbase
const searchReddit = createTool ({
name: "search_reddit" ,
description: "Search Reddit posts and comments" ,
parameters: z . object ({
query: z . string (). describe ( "The search query for Reddit" ),
}),
handler : async ({ query }, { step }) => {
return await step ?. run ( "search-on-reddit" , async () => {
// Create a new session
const session = await bb . sessions . create ({
projectId: process . env . BROWSERBASE_PROJECT_ID as string ,
});

// Connect to the session
const browser = await chromium . connectOverCDP ( session . connectUrl );
try {
const page = await browser . newPage ();

// Construct the search URL
const searchUrl = `https://search-new.pullpush.io/?type=submission&q= ${ query } ` ;

console . log ( searchUrl );

await page . goto ( searchUrl );

// Wait for results to load
await page . waitForSelector ( "div.results" , { timeout: 10000 });

// Extract search results
const results = await page . evaluate (() => {
const posts = document . querySelectorAll ( "div.results div:has(h1)" );
return Array . from ( posts ). map (( post ) => ({
title: post . querySelector ( "h1" )?. textContent ?. trim (),
content: post . querySelector ( "div" )?. textContent ?. trim (),
}));
});

console . log ( "results" , JSON . stringify ( results , null , 2 ));

return results . slice ( 0 , 5 ); // Return top 5 results
} finally {
await browser . close ();
}
});
},
});
```

Configure your `BROWSERBASE_API_KEY` and `BROWSERBASE_PROJECT_ID` in the `.env` file. You can find your API key and project ID from the [Browserbase](https://docs.browserbase.com/introduction/getting-started#creating-your-account)

[dashboard](https://docs.browserbase.com/introduction/getting-started#creating-your-account)

. We recommend building tools using Browserbase using Inngest's `step.run()` function. This ensures that the tool will only run once across multiple runs. More information about using `step.run()` can be found in the [Multi steps tools](\advanced-patterns\multi-steps-tools) page.

### [ Example: Reddit Search Agent using Browserbase](#example%3A-reddit-search-agent-using-browserbase)

You will find a complete example of a Reddit search agent using Browserbase in the Reddit Search Agent using Browserbase example:

## [Reddit Search Agent using Browserbase](https://github.com/inngest/agent-kit/tree/main/examples/reddit-search-browserbase-tools#readme)

[This examples shows how to build tools using Browserbase to power a Reddit search agent. Agents Tools Network Integrations](https://github.com/inngest/agent-kit/tree/main/examples/reddit-search-browserbase-tools#readme)

## [ Enable autonomous browsing with Stagehand](#enable-autonomous-browsing-with-stagehand)

Building AgentKit tools using [Stagehand](https://www.stagehand.dev/) gives more autonomy to your agents.

Stagehand comes with 4 primary API that can be directly used as tools:

- `goto()` : navigate to a specific URL
- `observe()` : observe the current page
- `extract()` : extract data from the current page
- `act()` : take action on the current page

These methods can be easily directly be used as tools in AgentKit, enabling agents to browse the web autonomously.

Below is an example of a simple search agent that uses Stagehand to search the web:

Copy Ask AI

```
import { createAgent , createTool } from "@inngest/agent-kit" ;
import { z } from "zod" ;
import { getStagehand , stringToZodSchema } from "./utils.js" ;

const webSearchAgent = createAgent ({
name: "web_search_agent" ,
description: "I am a web search agent." ,
system: `You are a web search agent.
` ,
tools: [
createTool ({
name: "navigate" ,
description: "Navigate to a given URL" ,
parameters: z . object ({
url: z . string (). describe ( "the URL to navigate to" ),
}),
handler : async ({ url }, { step , network }) => {
return await step ?. run ( "navigate" , async () => {
const stagehand = await getStagehand (
network ?. state . kv . get ( "browserbaseSessionID" ) !
);
await stagehand . page . goto ( url );
return `Navigated to ${ url } .` ;
});
},
}),
createTool ({
name: "extract" ,
description: "Extract data from the page" ,
parameters: z . object ({
instruction: z
. string ()
. describe ( "Instructions for what data to extract from the page" ),
schema: z
. string ()
. describe (
"A string representing the properties and types of data to extract, for example: '{ name: string, age: number }'"
),
}),
handler : async ({ instruction , schema }, { step , network }) => {
return await step ?. run ( "extract" , async () => {
const stagehand = await getStagehand (
network ?. state . kv . get ( "browserbaseSessionID" ) !
);
const zodSchema = stringToZodSchema ( schema );
return await stagehand . page . extract ({
instruction ,
schema: zodSchema ,
});
});
},
}),
createTool ({
name: "act" ,
description: "Perform an action on the page" ,
parameters: z . object ({
action: z
. string ()
. describe ( "The action to perform (e.g. 'click the login button')" ),
}),
handler : async ({ action }, { step , network }) => {
return await step ?. run ( "act" , async () => {
const stagehand = await getStagehand (
network ?. state . kv . get ( "browserbaseSessionID" ) !
);
return await stagehand . page . act ({ action });
});
},
}),
createTool ({
name: "observe" ,
description: "Observe the page" ,
parameters: z . object ({
instruction: z
. string ()
. describe ( "Specific instruction for what to observe on the page" ),
}),
handler : async ({ instruction }, { step , network }) => {
return await step ?. run ( "observe" , async () => {
const stagehand = await getStagehand (
network ?. state . kv . get ( "browserbaseSessionID" ) !
);
return await stagehand . page . observe ({ instruction });
});
},
}),
],
});
```

These 4 AgentKit tools using Stagehand enables the Web Search Agent to browse the web autonomously. The `getStagehand()` helper function is used to retrieve the persisted instance created for the network execution ( *see full code below* ).

You will find the complete example on GitHub:

## [Simple Search Agent using Stagehand](https://github.com/inngest/agent-kit/tree/main/examples/simple-search-stagehand/#readme)

[This examples shows how to build tools using Stagehand to power a simple search agent. Agents Tools Network Integrations](https://github.com/inngest/agent-kit/tree/main/examples/simple-search-stagehand/#readme)

[Using AgentKit with E2B Previous](\integrations\e2b) [Smithery - MCP Registry Next](\integrations\smithery)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.