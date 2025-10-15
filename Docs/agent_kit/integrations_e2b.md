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

- [Setup](#setup)
- [Examples](#examples)

Integrations

# Using AgentKit with E2B

Develop Coding Agents using E2B Sandboxes as tools

[E2B](https://e2b.dev/) is an open-source runtime for executing AI-generated code in secure cloud sandboxes. Made for agentic &amp; AI use cases.

E2B is a perfect fit to build Coding Agents that can write code, fix bugs, and more.

## [ Setup](#setup)

1

Install AgentKit and E2B

Within an existing project, Install AgentKit and E2B from npm:

npm pnpm yarn Copy Ask AI

```
npm install @inngest/agent-kit inngest @e2b/code-interpreter
```

Don't have an existing project?

To create a new project, create a new directory then initialize using your package manager:

npm pnpm yarn Copy Ask AI

```
mkdir my-agent-kit-project && npm init
```

2

Setup your Coding Agent

Create a Agent and its associated Network:

Copy Ask AI

```
import {
createAgent ,
createNetwork ,
anthropic
} from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Coding Agent" ,
description: "An expert coding agent" ,
system: `You are a coding agent help the user to achieve the described task.

Once the task completed, you should return the following information:
<task_summary>
</task_summary>

Think step-by-step before you start the task.
` ,
model: anthropic ({
model: "claude-3-5-sonnet-latest" ,
max_tokens: 4096 ,
}),
});

const network = createNetwork ({
name: "Coding Network" ,
agents: [ agent ],
defaultModel: anthropic ({
model: "claude-3-5-sonnet-20240620" ,
maxTokens: 1000 ,
})
});
```

3

Create the E2B Tools

To operate, our Coding Agent will need to create files and run commands. Below is an example of how to create the `createOrUpdateFiles` and `terminal` E2B tools:

Copy Ask AI

```
import {
createAgent ,
createNetwork ,
anthropic ,
createTool
} from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Coding Agent" ,
description: "An expert coding agent" ,
system: `You are a coding agent help the user to achieve the described task.

Once the task completed, you should return the following information:
<task_summary>
</task_summary>

Think step-by-step before you start the task.
` ,
model: anthropic ({
model: "claude-3-5-sonnet-latest" ,
max_tokens: 4096 ,
}),
tools: [
// terminal use
createTool ({
name: "terminal" ,
description: "Use the terminal to run commands" ,
parameters: z . object ({
command: z . string (),
}),
handler : async ({ command }, { network }) => {
const buffers = { stdout: "" , stderr: "" };

try {
const sandbox = await getSandbox ( network );
const result = await sandbox . commands . run ( command , {
onStdout : ( data : string ) => {
buffers . stdout += data ;
},
onStderr : ( data : string ) => {
buffers . stderr += data ;
},
});
return result . stdout ;
} catch ( e ) {
console . error (
`Command failed: ${ e } \n stdout: ${ buffers . stdout } \n stderr: ${ buffers . stderr } `
);
return `Command failed: ${ e } \n stdout: ${ buffers . stdout } \n stderr: ${ buffers . stderr } ` ;
}
},
}),
// create or update file
createTool ({
name: "createOrUpdateFiles" ,
description: "Create or update files in the sandbox" ,
parameters: z . object ({
files: z . array (
z . object ({
path: z . string (),
content: z . string (),
})
),
}),
handler : async ({ files }, { network }) => {
try {
const sandbox = await getSandbox ( network );
for ( const file of files ) {
await sandbox . files . write ( file . path , file . content );
}
return `Files created or updated: ${ files
. map (( f ) => f . path )
. join ( ", " ) } ` ;
} catch ( e ) {
return "Error: " + e ;
}
},
}),
]
});

const network = createNetwork ({
name: "Coding Network" ,
agents: [ agent ],
defaultModel: anthropic ({
model: "claude-3-5-sonnet-20240620" ,
maxTokens: 1000 ,
})
});
```

You will find the complete example in the [E2B Coding Agent example](https://github.com/inngest/agent-kit/tree/main/examples/e2b-coding-agent#readme) . **Designing useful tools** As covered in Anthropic's ["Tips for Building AI Agents"](https://www.youtube.com/watch?v=LP5OCa20Zpg) ,

the best Agents Tools are the ones that you will need to accomplish the task by yourself. Do not map tools directly to the underlying API, but rather design tools that are useful for the Agent to accomplish the task.

## [ Examples](#examples)

## [Replicate Cursor's Agent mode](https://github.com/inngest/agent-kit/tree/main/examples/e2b-coding-agent#readme)

[This examples shows how to use E2B sandboxes to build a coding agent that can write code and run commands to generate complete project, complete refactoring and fix bugs. Agents Tools Network Integrations Code-based Router](https://github.com/inngest/agent-kit/tree/main/examples/e2b-coding-agent#readme)

## [AI-powered CSV contacts importer](https://github.com/inngest/agent-kit/tree/main/examples/e2b-csv-contacts-importer#readme)

[Let's reinvent the CSV upload UX with an AgentKit network leveraging E2B sandboxes. Agents Tools Network Integrations Code-based Router](https://github.com/inngest/agent-kit/tree/main/examples/e2b-csv-contacts-importer#readme)

[Code Assistant v3: Autonomous Bug Solver Previous](\guided-tour\ai-agents) [Using AgentKit with Browserbase Next](\integrations\browserbase)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.