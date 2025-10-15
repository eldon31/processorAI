yarn add @inngest/agent-kit
```

Sources: [packages/agent-kit/package.json:1-77](), [docs/getting-started/quick-start.mdx:9-49]()

## Environment Setup

AgentKit requires API keys for the LLM providers you intend to use. These should be set as environment variables.

### Setting Environment Variables

For development, you can set these directly in your terminal:

```bash
# For Anthropic models
export ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXX

# For OpenAI models
export OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
```

For production, set these environment variables according to your deployment platform's specifications.

### Using .env Files

For local development, you can use a `.env` file with a package like `dotenv`:

1. Install dotenv:
   ```bash
   npm install dotenv
   ```

2. Create a `.env` file in your project root:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXX
   OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
   ```

3. Import dotenv at the top of your entry file:
   ```javascript
   import 'dotenv/config';
   ```

Sources: [docs/getting-started/quick-start.mdx:79-84](), [examples/quick-start/index.ts:1]()

## Setup Flow

```mermaid
flowchart TD
    subgraph "Installation Process"
        A["Install @inngest/agent-kit"] --> B["Set Environment Variables"]
        B --> C["Import Dependencies"]
        C --> D["Create Agents"]
        D --> E["Create Network (Optional)"]
        E --> F["Create Server"]
        F --> G["Start Server"]
    end
```

## Basic Configuration

After installation, you need to configure your agents, networks, and server. Here's a basic configuration example:

### Creating Agents

Import the necessary components and create an agent:

```javascript
import { createAgent, anthropic } from '@inngest/agent-kit';

const agent = createAgent({
  name: 'Database administrator',
  description: 'Provides expert support for managing PostgreSQL databases',
  system: 'You are a PostgreSQL expert database administrator...',
  model: anthropic({
    model: 'claude-3-5-haiku-latest',
    defaultParameters: {
      max_tokens: 1000,
    },
  }),
});
```

Sources: [docs/getting-started/quick-start.mdx:52-77](), [examples/quick-start/index.ts:2-17]()

### Creating a Network (Optional)

If you need multiple agents to work together, you can create a network:

```javascript
import { createNetwork } from '@inngest/agent-kit';

const network = createNetwork({
  name: 'DevOps team',
  agents: [agentOne, agentTwo],
  defaultModel: anthropic({
    model: 'claude-3-5-haiku-latest',
    defaultParameters: {
      max_tokens: 1000,
    },
  }),
});
```

Sources: [docs/getting-started/quick-start.mdx:137-185](), [examples/quick-start/index.ts:34-44]()

### Setting Up the Server

Create and start the HTTP server:

```javascript
import { createServer } from '@inngest/agent-kit/server';

const server = createServer({
  agents: [agent], // Add individual agents
  networks: [network], // Add networks (if any)
});

server.listen(3000, () => console.log('Agent kit running!'));
```

Sources: [docs/getting-started/quick-start.mdx:86-98](), [examples/quick-start/index.ts:46-51]()

## AgentKit Architecture After Setup

```mermaid
graph TD
    subgraph "AgentKit Application"
        User["User/Client"] -->|HTTP Request| Server["Express Server (createServer)"]
        Server -->|Process Request| Network["Network (createNetwork)"]
        Network -->|Route to| AgentA["Agent A (createAgent)"]
        Network -->|Route to| AgentB["Agent B (createAgent)"]
        
        AgentA -->|API Call| ModelA["LLM Provider API (e.g. Anthropic)"]
        AgentB -->|API Call| ModelB["LLM Provider API (e.g. OpenAI)"]
        
        ModelA -->|Response| AgentA
        ModelB -->|Response| AgentB
        
        AgentA -->|Result| Network
        AgentB -->|Result| Network
        Network -->|Final Response| Server
        Server -->|HTTP Response| User
    end
```

## Testing Your Installation

AgentKit integrates with the Inngest dev server for testing and debugging. To test your installation:

1. Start your AgentKit server:
   ```bash
   npx tsx ./index.ts
   ```

2. In a separate terminal, start the Inngest dev server:
   ```bash
   npx inngest-cli@latest dev -u http://localhost:3000/api/inngest
   ```

3. Open the Inngest dev server UI at `http://localhost:8288/functions`

4. Invoke a function with a test prompt:
   ```json
   {
     "data": {
       "input": "Your test prompt here"
     }
   }
   ```

5. View the agent execution and results in the UI

Sources: [docs/getting-started/quick-start.mdx:108-134]()

## Development Environment Structure

```mermaid
graph TD
    subgraph "Development Environment"
        App["Your Application"] -->|Imports| AK["@inngest/agent-kit"]
        App -->|Runs on| AppServer["Application Server (Port 3000)"]
        
        AK -->|Uses| CA["createAgent()"]
        AK -->|Uses| CN["createNetwork()"]
        AK -->|Uses| CS["createServer()"]
        
        AppServer -->|API Endpoint| InngestDev["Inngest Dev Server (Port 8288)"]
        InngestDev -->|Testing UI| Developer["Developer"]
        
        ENV["Environment Variables"] -->|API Keys| AK
    end
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure you've set the required environment variables for your LLM providers.
   ```
   Error: Missing API key for Anthropic
   ```
   Solution: Set the `ANTHROPIC_API_KEY` environment variable.

2. **Incompatible Node Version**: AgentKit requires Node.js 16 or higher.
   Solution: Upgrade your Node.js version.

3. **Server Connection Issues**: If you can't connect to the server, ensure:
   - The server is running on the correct port
   - There are no port conflicts
   - Your firewall isn't blocking the connection

4. **Inngest Dev Server Connection**: If the Inngest dev server can't connect to your AgentKit server:
   - Ensure both servers are running
   - Verify the URL for the `-u` parameter is correct (e.g., `http://localhost:3000/api/inngest`)

Sources: [docs/getting-started/quick-start.mdx:108-134]()

## Next Steps

After successful installation and setup:

- Learn about the [Core Concepts](#2) of AgentKit
- Understand how to create and configure [Agents](#2.1)
- Explore [Networks](#2.2) for multi-agent applications
- Add [Tools](#2.5) to enhance your agents' capabilities

For a complete hands-on example, follow the [Quick Start Guide](#3.1).

# Project Structure




This document describes the organization and structure of the AgentKit repository, including its directory layout, main components, and how they relate to each other. For information about installing and setting up AgentKit, see [Installation and Setup](#1.1).

## Repository Overview

AgentKit is organized as a monorepo using pnpm as the package manager with version `pnpm@9.14.2`. The repository structure follows a standard monorepo pattern with the core framework in `packages/agent-kit` and example applications in the `examples/` directory.

### Monorepo Configuration

The root `package.json` defines the workspace structure and shared development scripts:

| Script | Purpose |
|--------|---------|
| `lint` | Run ESLint across all packages |
| `test` | Run tests in all packages with test scripts |
| `build` | Build all packages recursively |
| `release` | Build and publish packages using Changesets |
| `version` | Update package versions and lockfile |

### High-Level Repository Organization

```mermaid
graph TD
    Root["/"]
    PackagesDir["packages/"]
    ExamplesDir["examples/"]
    ConfigFiles["Configuration Files"]
    
    Root --> PackagesDir
    Root --> ExamplesDir
    Root --> ConfigFiles
    
    PackagesDir --> AgentKit["agent-kit/"]
    
    AgentKit --> AgentKitSrc["src/"]
    AgentKit --> AgentKitDist["dist/"]
    AgentKit --> AgentKitPkg["package.json"]
    
    ExamplesDir --> QuickStart["quick-start/"]
    ExamplesDir --> SWEBench["swebench/"]
    ExamplesDir --> CodeAssistant["code-assistant/"]
    ExamplesDir --> Demo["demo/"]
    ExamplesDir --> Support["support/"]
    
    ConfigFiles --> PackageJson["package.json"]
    ConfigFiles --> ESLintConfig["eslint.config.mjs"]
    ConfigFiles --> GitIgnore[".gitignore"]
    ConfigFiles --> GitHubWorkflows[".github/workflows/"]
```

Sources: [package.json:1-32](), [eslint.config.mjs:1-33](), [.gitignore:1-13](), [.github/workflows/pr.yml:1-33]()

## Core Package Structure

The main AgentKit package (`packages/agent-kit`) contains the framework implementation. The source code is organized into logical modules that correspond to the core abstractions.

### Source Code Structure

```mermaid
graph TD
    Src["src/"]
    
    Src --> IndexTS["index.ts"]
    Src --> ServerTS["server.ts"]
    
    Src --> AgentTS["agent.ts"]
    Src --> ModelTS["model.ts"]
    Src --> ModelsDir["models/"]
    Src --> NetworkTS["network.ts"]
    Src --> StateTS["state.ts"]
    Src --> ToolTS["tool.ts"]
    Src --> UtilTS["util.ts"]
    Src --> TypesTS["types.ts"]
    
    ModelsDir --> OpenAITS["openai.ts"]
    ModelsDir --> AnthropicTS["anthropic.ts"]
    ModelsDir --> GeminiTS["gemini.ts"]
    ModelsDir --> GrokTS["grok.ts"]
```

### Core Exports Structure

The main entry point `index.ts` exports all framework components:

| Export Module | Purpose |
|---------------|---------|
| `./agent` | `createAgent` function and agent types |
| `./model` | Model adapter interfaces and base classes |
| `./models` | Specific AI model implementations |
| `./network` | `createNetwork` function and network types |
| `./state` | State management system |
| `./tool` | `createTool` function and tool interfaces |
| `./util` | Utility functions and helpers |
| `./types` | Core TypeScript type definitions |

The framework also provides a separate server entry point at `server.ts` for serving agents as Inngest functions.

Sources: [packages/agent-kit/src/index.ts:1-9]()

## Package Configuration

AgentKit is published as `@inngest/agent-kit` on npm. Its package configuration includes:

| Property | Value |
|----------|-------|
| Name | @inngest/agent-kit |
| Description | A framework for creating and orchestrating AI agents and AI workflows |
| Version | 0.7.3 (as of the provided CHANGELOG.md) |
| License | Apache-2.0 |
| Module Type | ESM (with CommonJS compatibility) |

The package exports both ESM and CommonJS modules to support different environments:

```
"exports": {
  ".": {
    "import": "./dist/index.js",
    "require": "./dist/index.cjs",
    "types": {
      "import": "./dist/index.d.ts",
      "require": "./dist/index.d.cts"
    }
  },
  "./server": {
    "import": "./dist/server.js",
    "require": "./dist/server.cjs",
    "types": {
      "import": "./dist/server.d.ts",
      "require": "./dist/server.d.cts"
    }
  }
}
```

Sources: [packages/agent-kit/package.json:36-53]()

## Core Dependencies

AgentKit relies on the following key dependencies:

| Dependency | Purpose |
|------------|---------|
| @inngest/ai | Integration with Inngest's AI functionality |
| @modelcontextprotocol/sdk | Implementation of Model Context Protocol (MCP) |
| express | Web server functionality |
| inngest | Workflow orchestration and function execution |
| zod | Schema validation and type inference |
| zod-to-json-schema | Convert Zod schemas to JSON schema for LLM tools |
| @dmitryrechkin/json-schema-to-zod | Convert JSON schema to Zod |
| eventsource | Server-sent events client |
| xxhashjs | Fast hashing library |

Sources: [packages/agent-kit/package.json:54-63]()

## Core Components and Code Entity Mapping

The AgentKit framework exports specific functions and classes that correspond to the core abstractions:

### Core Exports and Their Source Files

```mermaid
graph TD
    subgraph "Main Exports (index.ts)"
        CreateAgent["createAgent()"]
        CreateNetwork["createNetwork()"]
        CreateTool["createTool()"]
        CreateServer["createServer()"]
    end
    
    subgraph "Source Files"
        AgentTS["agent.ts"]
        NetworkTS["network.ts"]
        ToolTS["tool.ts"]
        ServerTS["server.ts"]
        StateTS["state.ts"]
        ModelTS["model.ts"]
        ModelsDir["models/"]
    end
    
    subgraph "Model Implementations"
        ModelsDir --> OpenAITS["openai.ts"]
        ModelsDir --> AnthropicTS["anthropic.ts"]
        ModelsDir --> GeminiTS["gemini.ts"]
        ModelsDir --> GrokTS["grok.ts"]
    end
    
    CreateAgent -.->|"Defined in"| AgentTS
    CreateNetwork -.->|"Defined in"| NetworkTS
    CreateTool -.->|"Defined in"| ToolTS
    CreateServer -.->|"Defined in"| ServerTS
    
    AgentTS -->|"Uses"| StateTS
    AgentTS -->|"Uses"| ModelTS
    NetworkTS -->|"Uses"| StateTS
    ToolTS -->|"Uses"| StateTS
    
    ModelTS -.->|"Implemented by"| ModelsDir
```

### Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant CreateNetwork["createNetwork()"]
    participant CreateAgent["createAgent()"]
    participant State["State System"]
    participant Router["Router"]
    participant ModelAdapter["Model Adapter"]
    
    User->>CreateNetwork: Initialize network
    CreateNetwork->>State: Initialize shared state
    CreateNetwork->>Router: Setup routing logic
    
    User->>CreateAgent: Create agents
    CreateAgent->>ModelAdapter: Configure AI model
    CreateAgent->>State: Register with state
    
    CreateNetwork->>Router: Execute routing
    Router->>CreateAgent: Select and run agent
    CreateAgent->>ModelAdapter: Generate response
    ModelAdapter-->>CreateAgent: AI response
    CreateAgent->>State: Update state
```

Sources: [packages/agent-kit/src/index.ts:1-9]()

## Framework Architecture

AgentKit provides a layered architecture for building AI agent applications:

### System Architecture

```mermaid
graph TB
    subgraph "User Applications"
        UserApps["Custom Agent Applications"]
    end
    
    subgraph "AgentKit Framework"
        CoreAPIs["createAgent, createNetwork"]
        State["State Management"]
        Tools["Tool System"]
        Router["Router System"]
        ModelAdapters["Model Adapters"]
    end
    
    subgraph "AI Models"
        OpenAI["OpenAI"]
        Anthropic["Anthropic"]
        Gemini["Gemini"]
        Grok["Grok"]
    end
    
    subgraph "External Tools"
        FSTools["File System Tools"]
        APITools["API Integration Tools"]
        MCP["Model Context Protocol"]
        InngestFn["Inngest Functions"]
    end
    
    UserApps -->|"Uses"| CoreAPIs
    CoreAPIs -->|"Uses"| State
    CoreAPIs -->|"Uses"| Tools
    CoreAPIs -->|"Uses"| Router
    CoreAPIs -->|"Uses"| ModelAdapters
    
    ModelAdapters -->|"Connects to"| OpenAI
    ModelAdapters -->|"Connects to"| Anthropic
    ModelAdapters -->|"Connects to"| Gemini
    ModelAdapters -->|"Connects to"| Grok
    
    Tools -->|"Integrates with"| FSTools
    Tools -->|"Integrates with"| APITools
    Tools -->|"Integrates with"| MCP
    Tools -->|"Integrates with"| InngestFn
```

This layered design allows flexibility in both the AI models used and the external tools integrated.

Sources: Component Relationships and Dependencies diagram in the provided background material

## Execution Flow

The following sequence diagram illustrates the typical execution flow when using AgentKit:

### Execution Flow Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Server as "Express Server"
    participant Agent
    participant Router
    participant Model as "LLM Model"
    participant Tools

    Client->>Server: Send request
    Server->>Agent: Process request
    
    loop Network Execution
        Agent->>Model: Generate response
        Model-->>Agent: Response with tool calls
        
        opt Tool Execution
            Agent->>Tools: Execute tools
            Tools-->>Agent: Tool results
        end
        
        Agent->>Router: Determine next agent
        Router-->>Agent: Next agent to run (or done)
    end
    
    Agent->>Server: Final result
    Server->>Client: Response
```

Sources: Deployment and Execution Flow diagram in the provided background material

## Example Applications

The repository includes several example applications that demonstrate different use cases:

### Examples Overview

| Example | Description | Key Components Used |
|---------|-------------|---------------------|
| quick-start | Basic examples for getting started | createAgent, createNetwork |
| swebench | Software Engineering Benchmark with code editing | createAgent, createNetwork, Tools, State |
| code-assistant | Code assistance applications | createAgent, createNetwork, Tools |
| search-stagehand | Search functionality with browser integration | createAgent, BrowserBase |

### Example Application Structure

The `examples/` directory contains practical demonstrations of AgentKit patterns:

```mermaid
graph TD
    ExamplesDir["examples/"]
    
    ExamplesDir --> QuickStart["quick-start/"]
    ExamplesDir --> SWEBench["swebench/"]
    ExamplesDir --> CodeAssistant["code-assistant/"]
    ExamplesDir --> Demo["demo/"]
    ExamplesDir --> Support["support/"]
    
    subgraph "SWE-bench Components"
        SWEBench --> SWEMakefile["Makefile"]
        SWEBench --> SWEData["opt/dev.parquet"]
        SWEMakefile --> DataDownload["Data Download Scripts"]
    end
    
    subgraph "AgentKit Core Usage"
        QuickStart --> CreateAgent["createAgent()"]
        QuickStart --> CreateNetwork["createNetwork()"]
        
        SWEBench --> CreateAgentSWE["createAgent()"]
        SWEBench --> CreateNetworkSWE["createNetwork()"]
        SWEBench --> CreateToolSWE["createTool()"]
        
        CodeAssistant --> CreateAgentCode["createAgent()"]
        CodeAssistant --> CreateNetworkCode["createNetwork()"]
    end
```

The SWE-bench example includes data management infrastructure with a `Makefile` for downloading benchmark datasets from Hugging Face.

Sources: [examples/swebench/Makefile:1-8]()

## Version History

AgentKit uses a semantic versioning approach. Recent notable changes (from the CHANGELOG):

| Version | Key Changes |
|---------|-------------|
| 0.7.3 | Export types improvements |
| 0.7.0 | Refactored AgentResult, added conversational history support |
| 0.6.0 | Implemented typed state management |
| 0.5.0 | Added Gemini and Grok support |
| 0.4.0 | Added model hyper parameters support |
| 0.3.0 | Restructured exports to allow non-Node runtimes |
| 0.2.0 | Added AgentKit server for serving agents and networks as Inngest functions |

Sources: [packages/agent-kit/CHANGELOG.md:1-152]()

## Development Tooling

The repository uses a comprehensive development toolchain for code quality, testing, and release management.

### Core Development Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| pnpm | Package management | `pnpm@9.14.2` with workspace support |
| TypeScript | Programming language | TypeScript ESLint integration |
| ESLint | Code linting | `eslint.config.mjs` with Prettier integration |
| Prettier | Code formatting | Integrated via `eslint-plugin-prettier` |
| Changesets | Release management | `@changesets/cli` for version management |
| Husky | Git hooks | Pre-commit hooks with `lint-staged` |

### ESLint Configuration

The ESLint setup uses a modern flat configuration approach:

```mermaid
graph TD
    ESLintConfig["eslint.config.mjs"]
    
    ESLintConfig --> ESLintJS["@eslint/js"]
    ESLintConfig --> TypeScriptESLint["typescript-eslint"]
    ESLintConfig --> PrettierPlugin["eslint-plugin-prettier"]
    
    ESLintConfig --> IgnorePatterns["Ignore Patterns"]
    IgnorePatterns --> DistDirs['"**/dist"']
    IgnorePatterns --> ConfigFile['"eslint.config.mjs"']
    IgnorePatterns --> Examples['"examples/**"']
    
    ESLintConfig --> TypeChecking["Type Checking"]
    TypeChecking --> ProjectService["projectService: true"]
    TypeChecking --> TSConfigRoot["tsconfigRootDir"]
```

### CI/CD Pipeline

The repository includes GitHub Actions workflows for continuous integration:

| Job | Purpose | Commands |
|-----|---------|----------|
| `build` | Build verification | `pnpm install`, `pnpm run build` |
| `lint` | Code quality | `pnpm run build`, `pnpm run lint` |
| `test` | Test execution | `pnpm install`, `pnpm run test` |

### Git Hooks Configuration

Pre-commit hooks ensure code quality:

```
"lint-staged": {
  "*.{j,t}s": "eslint --cache --fix"
}
```

Sources: [package.json:2-31](), [eslint.config.mjs:1-33](), [.github/workflows/pr.yml:1-33]()

This document provides an overview of the project structure of the AgentKit repository. For more details on core concepts and how to use specific components, refer to the [Core Concepts](#2) documentation.

# Core Concepts




This page provides an overview of the fundamental architectural components of AgentKit. These core concepts form the building blocks for creating both simple single-agent systems and complex multi-agent networks. For specific implementation details of each concept, refer to their dedicated pages: [Agents](#2.1), [Networks](#2.2), [State Management](#2.3), [Routers](#2.4), [Tools](#2.5), and [Model Adapters](#2.6).

## Overview of AgentKit Architecture

AgentKit is designed around a modular architecture that enables composable AI agent systems. The framework consists of six key components that work together to create flexible agent-based applications.

```mermaid
graph TD
    subgraph "AgentKit Core Functions"
        createAgent["createAgent()"]
        createNetwork["createNetwork()"]
        createTool["createTool()"]
        createServer["createServer()"]
    end

    subgraph "Runtime Components"
        Agent["Agent"]
        Network["Network"]
        NetworkState["network.state"]
        RouterFunction["router()"]
        ToolHandler["tool.handler()"]
        ModelAdapter["openai() | anthropic() | gemini()"]
    end

    createAgent --> Agent
    createNetwork --> Network
    createTool --> ToolHandler
    Network --> Agent
    Network --> RouterFunction
    Network --> NetworkState
    Agent --> ToolHandler
    Agent --> ModelAdapter
    Agent --> NetworkState
    RouterFunction --> Agent
    RouterFunction --> NetworkState
    ToolHandler --> NetworkState
```

*Diagram: Primary Components and Relationships in AgentKit*

Sources: [packages/agent-kit/README.md:17-24](), [packages/agent-kit/README.md:38-44]()

The diagram shows how these components interact:
- **Agents** use Tools and Model Adapters to interact with AI models
- **Networks** orchestrate multiple Agents and maintain shared State
- **Routers** determine which Agent to execute next
- **State** provides context and memory shared across components
- **Tools** extend Agent capabilities
- **Model Adapters** connect to different LLM providers

## Agent Component

Agents are the primary workhorses in AgentKit. An agent represents an encapsulated LLM interaction with a specific role and capability set.

```mermaid
classDiagram
    class createAgent {
        name: string
        system: string | function
        description?: string
        tools?: Tool[]
        model?: ModelAdapter
        mcpServers?: MCPServer[]
        lifecycle?: AgentLifecycle
    }
    
    class AgentInstance {
        run(input: string) InferenceResult
        name: string
        system: string | function
    }
    
    class createTool {
        name: string
        description: string
        parameters: ZodSchema
        handler: function
        strict?: boolean
    }
    
    class ModelAdapter {
        "openai()": GPTModels
        "anthropic()": ClaudeModels  
        "gemini()": GeminiModels
        "grok()": GrokModels
    }
    
    createAgent --> AgentInstance
    AgentInstance --> createTool
    AgentInstance --> ModelAdapter
```

*Diagram: Agent Component Structure*

Sources: [packages/agent-kit/README.md:52-78](), [docs/concepts/agents.mdx:14-33](), [docs/reference/create-tool.mdx:8-33]()

Each Agent includes:
- A **name** identifying the agent
- A **system prompt** defining its role and behavior
- Optional **tools** providing capability extensions
- A **model adapter** specifying which LLM to use
- Optional **MCP servers** providing additional tools

Agents are created using the `createAgent()` function, as seen in examples throughout the codebase.

## Network Component

Networks combine multiple agents into a collaborative system with shared state and orchestrated execution flow.

```mermaid
graph TD
    subgraph "createNetwork() Parameters"
        networkName["name: string"]
        networkAgents["agents: Agent[]"]
        networkRouter["router?: RouterFunction | RoutingAgent"]
        networkDefaultModel["defaultModel?: ModelAdapter"]
        networkMaxIter["maxIter?: number"]
    end
    
    subgraph "NetworkInstance Runtime"
        networkRun["network.run()"]
        networkState["network.state.kv"]
        networkStateData["network.state.data"]
        networkResults["network.state.results"]
        networkAgentsMap["network.agents: Map<string, Agent>"]
    end
    
    networkName --> networkRun
    networkAgents --> networkAgentsMap
    networkRouter --> networkRun
    networkDefaultModel --> networkAgentsMap
    networkRun --> networkState
    networkRun --> networkStateData
    networkRun --> networkResults
```

*Diagram: Network Component Structure*

Sources: [packages/agent-kit/README.md:80-95](), [packages/agent-kit/README.md:259-292]()

Networks include:
- A collection of **agents** that can be called
- A **router** that determines execution flow
- **State** that's shared between all agents
- **Message history** tracking all interactions
- A `run()` method to initiate execution

Networks are created using the `createNetwork()` function with a list of agents and a router.

## State Management

The State system provides shared memory and context across the network's agents, tools, and router.

```mermaid
flowchart LR
    subgraph "network.state API"
        stateKv["network.state.kv.get()"]
        stateKvSet["network.state.kv.set()"]
        stateData["network.state.data"]
        stateResults["network.state.results"]
    end
    
    subgraph "Access Points"
        systemPrompt["system: ({ network }) => string"]
        toolHandler["handler: (input, { network }) => any"]
        routerFunction["router: ({ network }) => Agent"]
        onStartHook["onStart: ({ network }) => void"]
    end
    
    stateKv --> routerFunction
    stateKvSet <--> toolHandler
    stateData --> systemPrompt
    stateResults --> routerFunction
    stateKv --> onStartHook
```

*Diagram: State Management System*

Sources: [packages/agent-kit/README.md:169-175](), [packages/agent-kit/README.md:270-284](), [docs/concepts/state.mdx:67-93]()

State in AgentKit consists of:
- **Typed data** - A typed object holding structured data
- **Key-value store** - For dynamic property storage
- **Message history** - Complete record of all agent interactions
- **Agent results** - Output from agent executions

The state can be accessed and modified by different components, enabling coordination between agents.

## Router Component

Routers determine which agent to execute next in a network, providing the orchestration logic for multi-agent systems.

```mermaid
flowchart TD
    subgraph "Router Function Signature"
        routerArgs["RouterArgs"]
        routerNetwork["{ network }"]
        routerStack["{ stack }"]
        routerCallCount["{ callCount }"]
        routerLastResult["{ lastResult }"]
    end
    
    subgraph "Router Implementation Types"
        codeBased["router: ({ network }) => Agent | undefined"]
        agentBased["createRoutingAgent({ name, onRoute })"]
        defaultRouter["getDefaultRoutingAgent()"]
    end
    
    subgraph "Router Decision Logic"
        stateCheck["network.state.kv.has('plan')"]
        agentSelection["return network.agents.get('agent-name')"]
        termination["return undefined"]
    end
    
    routerArgs --> codeBased
    routerArgs --> agentBased
    routerNetwork --> stateCheck
    stateCheck --> agentSelection
    stateCheck --> termination
```

*Diagram: Router Types and Decision Flow*

Sources: [packages/agent-kit/README.md:267-284](), [packages/agent-kit/README.md:415-476](), [docs/concepts/routers.mdx:70-79]()

AgentKit supports two primary routing approaches:
1. **Code-based routing** - A function with complete control over execution flow
2. **Agent-based routing** - An LLM agent that makes routing decisions

Routers use the network state to determine:
- Which agent to execute next
- When the network execution should terminate

## Tool System

Tools extend agent capabilities by allowing them to perform actions and interact with external systems.

```mermaid
classDiagram
    class createTool {
        name: string
        description: string
        parameters: ZodSchema
        handler: function
        strict?: boolean
        lifecycle?: ToolLifecycle
    }
    
    class ToolHandler {
        input: ParsedParameters
        context: ToolContext
        network: NetworkInstance
        agent: AgentInstance
        step?: InngestStep
    }
    
    class MCPServer {
        name: string
        transport: TransportConfig
        type: "sse" | "ws" | "streamable-http"
        url: string
    }
    
    class AgentTools {
        tools: Tool[]
        mcpServers: MCPServer[]
    }
    
    createTool --> ToolHandler
    MCPServer --> AgentTools
    createTool --> AgentTools
```

*Diagram: Tool System Component*

Sources: [packages/agent-kit/README.md:57-67](), [docs/reference/create-tool.mdx:61-90](), [docs/advanced-patterns/mcp.mdx:63-81]()

The tool system consists of:
- **Tool definition** - Created with `createTool()`, including name, description, parameters schema (using Zod), and handler function
- **MCP integration** - Support for Model Context Protocol for rich tool discovery
- **Tool handlers** - Functions that execute when the tool is called, with access to network state

## Model Adapters

Model adapters provide a uniform interface to different LLM providers, allowing agents to use various models interchangeably.

```mermaid
flowchart LR
    subgraph "Model Adapter Functions"
        openaiAdapter["openai({ model, defaultParameters })"]
        anthropicAdapter["anthropic({ model, defaultParameters })"]
        geminiAdapter["gemini({ model, defaultParameters })"]
        grokAdapter["grok({ model, defaultParameters })"]
    end
    
    subgraph "Usage in AgentKit"
        agentModel["createAgent({ model: openai() })"]
        networkDefaultModel["createNetwork({ defaultModel: anthropic() })"]
    end
    
    subgraph "Model Examples"
        gpt4o["'gpt-4o-mini'"]
        claude35["'claude-3-5-sonnet-latest'"]
        gemini15["'gemini-1.5-pro'"]
        grokBeta["'grok-beta'"]
    end
    
    openaiAdapter --> agentModel
    anthropicAdapter --> networkDefaultModel
    openaiAdapter --> gpt4o
    anthropicAdapter --> claude35
    geminiAdapter --> gemini15
    grokAdapter --> grokBeta
```

*Diagram: Model Adapter System*

Sources: [packages/agent-kit/README.md:83-89](), [packages/agent-kit/README.md:286-291]()

Model adapters:
- Provide consistent interfaces to different LLM providers
- Handle provider-specific request formatting
- Normalize response parsing
- Can be specified at the agent level or network level

## Execution Flow

To understand how all these components work together, let's examine the execution flow in an AgentKit application.

```mermaid
sequenceDiagram
    participant Client
    participant networkRun as "network.run()"
    participant router as "router({ network })"
    participant codeAssistantAgent as "codeAssistantAgent"
    participant documentationAgent as "documentationAgent"
    participant createTool as "tool.handler()"
    participant networkState as "network.state.kv"

    Client->>networkRun: "Analyze this file"
    networkRun->>router: "{ network, callCount: 0 }"
    router->>networkRun: "return codeAssistantAgent"
    networkRun->>codeAssistantAgent: "agent.run(input)"
    codeAssistantAgent->>createTool: "generate_plan tool call"
    createTool->>networkState: "set('plan', ['documentation_agent'])"
    createTool-->>codeAssistantAgent: "Plan generated!"
    codeAssistantAgent-->>networkRun: "InferenceResult"
    networkRun->>router: "{ network, callCount: 1 }"
    router->>networkState: "get('plan')"
    networkState-->>router: "['documentation_agent']"
    router->>networkRun: "return documentationAgent"
    networkRun->>documentationAgent: "agent.run()"
    documentationAgent->>createTool: "save_suggestions tool call"
    createTool->>networkState: "set('suggestions', [...])"
    createTool-->>documentationAgent: "Suggestions saved!"
    documentationAgent-->>networkRun: "InferenceResult"
    networkRun->>router: "{ network, callCount: 2 }"
    router->>networkRun: "return undefined"
    networkRun-->>Client: "Final NetworkResult"
```

*Diagram: AgentKit Execution Flow*

Sources: [packages/agent-kit/README.md:216-284](), [packages/agent-kit/README.md:259-292]()

The execution flow demonstrates:
1. The network starts with an input and determines the first agent via the router
2. Each agent interacts with an LLM and may call tools
3. Tool execution can update the shared state
4. After each agent execution, the router determines the next agent
5. When the router returns undefined, the network execution terminates

## Creating Simple vs. Complex Agent Systems

AgentKit supports both simple single-agent setups and complex multi-agent networks, with different patterns for different use cases.

| System Type | Components | Router Pattern | Example Code Reference |
|-------------|------------|----------------|------------------------|
| Single Agent | `createAgent()` with tools | N/A | [packages/agent-kit/README.md:52-78]() |
| Code-based Network | `createNetwork()` with function router | `router: ({ network }) => Agent` | [packages/agent-kit/README.md:259-284]() |
| Agent-based Network | `createRoutingAgent()` as router | `createRoutingAgent({ onRoute })` | [packages/agent-kit/README.md:415-476]() |
| MCP-enabled Agent | `mcpServers` configuration | Optional routing | [packages/agent-kit/README.md:48-78]() |

Sources: [packages/agent-kit/README.md:142-147](), [packages/agent-kit/README.md:298-302](), [packages/agent-kit/README.md:415-491]()

This table illustrates the flexibility of AgentKit in supporting various agent architectures, from simple to complex.

## Summary

AgentKit's core concepts work together to create a flexible framework for building AI agent systems:

- **Agents** encapsulate LLM interactions with specific roles
- **Networks** orchestrate multiple agents through a shared workflow
- **State** provides shared memory and context
- **Routers** determine the execution flow between agents
- **Tools** extend agent capabilities
- **Model Adapters** connect to different LLM providers

These components can be composed to build everything from simple task-specific agents to complex, autonomous multi-agent systems with sophisticated routing logic.

Sources: [docs/overview.mdx:57-64](), [packages/agent-kit/README.md:17-24]()

# Agents




Agents are the core execution units in AgentKit that encapsulate AI model interactions, system prompts, tools, and execution logic. This document covers agent creation, configuration, lifecycle management, and integration within networks. For information about agent orchestration and collaboration, see [Networks](#2.2). For details about agent tool integration, see [Tools](#2.5).

## Agent Architecture

Agents in AgentKit are stateless entities that wrap AI model adapters with specific capabilities and behaviors. Each agent represents a specialized role or function within a multi-agent system.

### Agent Component Structure

```mermaid
graph TB
    subgraph "Agent Core"
        Agent["Agent&lt;T&gt;"]
        Agent --> name["name: string"]
        Agent --> description["description: string"]
        Agent --> system["system: string | function"]
        Agent --> assistant["assistant: string"]
    end
    
    subgraph "Agent Capabilities"
        tools["tools: Map&lt;string, Tool.Any&gt;"]
        model["model: AiAdapter.Any"]
        mcpServers["mcpServers: MCP.Server[]"]
        tool_choice["tool_choice: Tool.Choice"]
    end
    
    subgraph "Agent Lifecycle"
        lifecycles["lifecycles: Agent.Lifecycle&lt;T&gt;"]
        onStart["onStart()"]
        onResponse["onResponse()"]
        onFinish["onFinish()"]
    end
    
    subgraph "Execution Methods"
        run["run()"]
        performInference["performInference()"]
        invokeTools["invokeTools()"]
        agentPrompt["agentPrompt()"]
    end
    
    Agent --> tools
    Agent --> model
    Agent --> mcpServers
    Agent --> tool_choice
    Agent --> lifecycles
    
    lifecycles --> onStart
    lifecycles --> onResponse
    lifecycles --> onFinish
    
    Agent --> run
    run --> performInference
    run --> invokeTools
    run --> agentPrompt
```

Sources: [packages/agent-kit/src/agent.ts:43-112](), [docs/concepts/agents.mdx:7-13]()

## Creating Agents

### Basic Agent Creation

The `createAgent` function is the primary method for instantiating agents. It accepts a configuration object and returns an `Agent` instance.

```typescript
const agent = createAgent({
  name: "code-writer",
  description: "Expert TypeScript programmer",
  system: "You are an expert TypeScript programmer...",
  model: openai({ model: "gpt-4" })
});
```

Sources: [packages/agent-kit/src/agent.ts:33-34](), [docs/concepts/agents.mdx:14-33]()

### Agent Configuration Options

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | Unique identifier for the agent |
| `description` | `string` | No* | Human-readable description (* Required for networks) |
| `system` | `string \| function` | Yes | Static prompt or dynamic prompt function |
| `assistant` | `string` | No | Pre-filled assistant message |
| `tools` | `Tool.Any[] \| InngestFunction.Any[]` | No | Available tools and functions |
| `model` | `AiAdapter.Any` | No | Model adapter (can inherit from network) |
| `tool_choice` | `Tool.Choice` | No | Tool selection strategy |
| `lifecycle` | `Agent.Lifecycle<T>` | No | Execution hooks |
| `mcpServers` | `MCP.Server[]` | No | Model Context Protocol servers |

Sources: [packages/agent-kit/src/agent.ts:534-546]()

### Dynamic System Prompts

System prompts can be functions that receive network context, enabling state-dependent behavior:

```typescript
const agent = createAgent({
  name: "context-aware-agent",
  system: ({ network }) => {
    const files = network?.state.kv.get("files") || {};
    return `Base prompt. Current files: ${Object.keys(files).join(", ")}`;
  }
});
```

Sources: [packages/agent-kit/src/agent.ts:57](), [docs/concepts/agents.mdx:164-198]()

## Agent Execution Lifecycle

### Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Model as "AgenticModel"
    participant Tools
    participant State
    
    User->>Agent: "run(input, options)"
    Agent->>Agent: "initMCP()"
    Agent->>Agent: "agentPrompt(input)"
    
    loop "Until no more tool calls (maxIter)"
        opt "onStart lifecycle"
            Agent->>Agent: "lifecycles.onStart()"
        end
        
        Agent->>Model: "performInference(prompt, history)"
        Model-->>Agent: "AgentResult with messages/tool_calls"
        
        opt "onResponse lifecycle"
            Agent->>Agent: "lifecycles.onResponse()"
        end
        
        Agent->>Tools: "invokeTools(messages)"
        Tools->>State: "Update network state"
        Tools-->>Agent: "ToolResultMessage[]"
    end
    
    opt "onFinish lifecycle"
        Agent->>Agent: "lifecycles.onFinish()"
    end
    
    Agent-->>User: "AgentResult"
```

Sources: [packages/agent-kit/src/agent.ts:165-245]()

### Lifecycle Hooks

The agent execution process provides three main intervention points:

#### `onStart` Hook
Called before model inference, allowing prompt and history modification:

```typescript
lifecycle: {
  onStart: async ({ prompt, history, network }) => {
    // Modify prompts based on current state
    return { prompt, history, stop: false };
  }
}
```

#### `onResponse` Hook  
Called after model inference but before tool execution:

```typescript
lifecycle: {
  onResponse: async ({ result, network }) => {
    // Modify or validate model response
    return result;
  }
}
```

#### `onFinish` Hook
Called after all tool executions complete:

```typescript
lifecycle: {
  onFinish: async ({ result, network }) => {
    // Final result processing
    return result;
  }
}
```

Sources: [packages/agent-kit/src/agent.ts:575-618](), [docs/concepts/agents.mdx:133-161]()

## Agent Types

### Standard Agents

The base `Agent<T>` class handles most use cases, providing model inference and tool execution capabilities.

```typescript
export class Agent<T extends StateData> {
  name: string;
  description: string;
  system: string | ((ctx: { network?: NetworkRun<T> }) => MaybePromise<string>);
  tools: Map<string, Tool.Any>;
  // ... other properties
}
```

### Routing Agents

`RoutingAgent<T>` extends the base agent class for network routing decisions:

```typescript
export class RoutingAgent<T extends StateData> extends Agent<T> {
  type = "routing";
  override lifecycles: Agent.RoutingLifecycle<T>;
}
```

Routing agents include an `onRoute` lifecycle method that determines which agents to execute next:

```typescript
const routingAgent = createRoutingAgent({
  name: "supervisor",
  system: "You coordinate other agents...",
  lifecycle: {
    onRoute: ({ result, network }) => {
      // Return array of agent names to execute
      return ["agent1", "agent2"];
    }
  }
});
```

Sources: [packages/agent-kit/src/agent.ts:512-531](), [docs/concepts/routers.mdx:127-158]()

## Tool Integration

### Tool Management

Agents maintain tools in a `Map<string, Tool.Any>` structure, supporting both AgentKit tools and Inngest functions:

```typescript
private setTools(tools: Agent.Constructor<T>["tools"]): void {
  for (const tool of tools || []) {
    if (isInngestFn(tool)) {
      // Handle Inngest function tools
      this.tools.set(tool["absoluteId"], { /* converted tool */ });
    } else {
      // Handle standard tools
      this.tools.set(tool.name, tool);
    }
  }
}
```

### Tool Execution

During inference, agents automatically invoke tools when the model requests them:

```typescript
private async invokeTools(
  msgs: Message[],
  network: NetworkRun<T>
): Promise<ToolResultMessage[]> {
  // Process tool_call messages
  // Execute tool handlers
  // Return tool results
}
```

Sources: [packages/agent-kit/src/agent.ts:114-147](), [packages/agent-kit/src/agent.ts:292-359]()

## MCP Integration

### MCP Server Configuration

Agents can integrate with Model Context Protocol servers to access external tools:

```typescript
const agent = createAgent({
  name: "mcp-enabled-agent",
  mcpServers: [
    {
      name: "github",
      transport: {
        type: "streamable-http",
        url: "https://mcp-server.example.com"
      }
    }
  ]
});
```

### MCP Tool Discovery

The agent automatically discovers and registers MCP tools during initialization:

```typescript
private async listMCPTools(server: MCP.Server) {
  const client = await this.mcpClient(server);
  const results = await client.request({ method: "tools/list" }, ListToolsResultSchema);
  
  results.tools.forEach((t) => {
    const name = `${server.name}-${t.name}`;
    this.tools.set(name, { /* converted MCP tool */ });
  });
}
```

Sources: [packages/agent-kit/src/agent.ts:95](), [packages/agent-kit/src/agent.ts:413-459](), [docs/advanced-patterns/mcp.mdx:12-61]()

## Agent-Network Integration

### Network Context Access

When agents run within networks, they receive network context through the `NetworkRun<T>` parameter:

```typescript
interface NetworkRun<T extends StateData> {
  network: Network<T>;
  state: State<T>;
}
```

### State Interaction

Agents access and modify shared network state through tools and lifecycle hooks:

```typescript
// In tool handler
handler: async (input, { network }) => {
  const currentValue = network.state.kv.get("key");
  network.state.kv.set("key", newValue);
}

// In system prompt
system: ({ network }) => {
  const context = network?.state.kv.get("context");
  return `Base prompt with context: ${context}`;
}
```

Sources: [packages/agent-kit/src/agent.ts:181-184](), [docs/concepts/state.mdx:67-93]()

## Model Adapter Integration

### Model Assignment

Agents can use specific models or inherit from network defaults:

```typescript
// Agent with specific model
const agent = createAgent({
  model: anthropic({ model: "claude-3-sonnet" })
});

// Agent inheriting network model
const rawModel = model || this.model || network?.defaultModel;
```

### Model Adapter Creation

The agent creates an `AgenticModel` wrapper around the raw model adapter:

```typescript
const p = createAgenticModelFromAiAdapter(rawModel);
const { output, raw } = await p.infer(
  this.name,
  prompt.concat(history),
  Array.from(this.tools.values()),
  this.tool_choice || "auto"
);
```

Sources: [packages/agent-kit/src/agent.ts:172-177](), [packages/agent-kit/src/agent.ts:253-258]()

# Networks




Networks orchestrate multiple [Agents](#2.1) to work together on complex tasks through shared [State](#2.3) and intelligent [Routers](#2.4). A Network defines a collection of agents, coordinates their execution through routing logic, and maintains conversation history and typed data that agents can read and modify.

For information about individual agent behavior, see [Agents](#2.1). For details on how routers control agent selection, see [Routers](#2.4). For state persistence across agent calls, see [State Management](#2.3).

## Core Architecture

Networks combine three fundamental components: agents, routers, and state. The `Network` class manages the execution loop, calling agents based on router decisions and maintaining shared state throughout the workflow.

```mermaid
graph TB
    subgraph "Network Class"
        Network["Network&lt;T&gt;"]
        NetworkRun["NetworkRun&lt;T&gt;"]
    end
    
    subgraph "Core Components"
        Agents["agents: Map&lt;string, Agent&lt;T&gt;&gt;"]
        Router["router: Network.Router&lt;T&gt;"]
        State["state: State&lt;T&gt;"]
    end
    
    subgraph "Execution Flow"
        Execute["execute()"]
        GetNextAgents["getNextAgents()"]
        Schedule["schedule()"]
        AgentRun["agent.run()"]
    end
    
    Network --> Agents
    Network --> Router
    Network --> State
    NetworkRun --> Execute
    Execute --> GetNextAgents
    GetNextAgents --> Router
    Execute --> Schedule
    Execute --> AgentRun
    AgentRun --> State
```

Sources: [packages/agent-kit/src/network.ts:19-139]()

## Network Creation

Networks are created using the `createNetwork` function, which requires a name, list of agents, and optional configuration including routers, models, and initial state.

### Basic Network Structure

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Network identifier |
| `agents` | `Agent<T>[]` | Array of available agents |
| `defaultModel` | `AiAdapter.Any` | Model used when agents don't specify one |
| `router` | `Network.Router<T>` | Custom routing logic |
| `maxIter` | `number` | Maximum agent execution iterations |
| `defaultState` | `State<T>` | Initial state configuration |

```mermaid
graph LR
    CreateNetwork["createNetwork&lt;AgentState&gt;()"]
    Constructor["Network.Constructor&lt;T&gt;"]
    NetworkInstance["Network&lt;AgentState&gt;"]
    
    CreateNetwork --> Constructor
    Constructor --> NetworkInstance
    
    subgraph "Constructor Properties"
        Name["name: string"]
        Agents["agents: Agent&lt;T&gt;[]"]
        DefaultModel["defaultModel?: AiAdapter.Any"]
        RouterProp["router?: Network.Router&lt;T&gt;"]
        MaxIter["maxIter?: number"]
        DefaultStateProp["defaultState?: State&lt;T&gt;"]
    end
    
    Constructor --> Name
    Constructor --> Agents
    Constructor --> DefaultModel
    Constructor --> RouterProp
    Constructor --> MaxIter
    Constructor --> DefaultStateProp
```

Sources: [packages/agent-kit/src/network.ts:12-14](), [packages/agent-kit/src/network.ts:251-262]()

## Execution Flow

The network execution follows a deterministic loop where routers select agents, agents execute with shared state, and the process continues until the router returns `undefined`.

### Network Execution Loop

```mermaid
sequenceDiagram
    participant Client
    participant NetworkRun
    participant Router
    participant Agent
    participant State
    
    Client->>NetworkRun: "run(input, overrides)"
    NetworkRun->>NetworkRun: "execute()"
    
    loop "Until router returns undefined or maxIter reached"
        NetworkRun->>Router: "getNextAgents()"
        Router-->>NetworkRun: "Agent[] | undefined"
        
        opt "If agents returned"
            NetworkRun->>NetworkRun: "schedule(agent.name)"
            NetworkRun->>Agent: "agent.run(input, {network, maxIter: 0})"
            Agent-->>NetworkRun: "AgentResult"
            NetworkRun->>State: "state.appendResult(call)"
        end
    end
    
    NetworkRun-->>Client: "NetworkRun&lt;T&gt;"
```

Sources: [packages/agent-kit/src/network.ts:362-432]()

### Stack-Based Agent Scheduling

The network maintains an internal stack (`_stack`) of agent names to execute. The `schedule` method adds agents to this stack, and the execution loop processes them sequentially.

```mermaid
graph TD
    Router["Router Function"]
    GetNextAgents["getNextAgents()"]
    Schedule["schedule(agentName)"]
    Stack["_stack: string[]"]
    ExecuteLoop["Execution Loop"]
    AgentRun["agent.run()"]
    
    Router --> GetNextAgents
    GetNextAgents --> Schedule
    Schedule --> Stack
    Stack --> ExecuteLoop
    ExecuteLoop --> AgentRun
    AgentRun --> Router
```

Sources: [packages/agent-kit/src/network.ts:358-360](), [packages/agent-kit/src/network.ts:387-429]()

## Router Types

Networks support two primary router patterns: function-based routers and agent-based routers. Function routers use deterministic code logic, while agent routers use LLM inference to make routing decisions.

### Function Router Implementation

Function routers implement the `Network.Router.FnRouter<T>` type, receiving router arguments and returning agents or `undefined`.

```mermaid
graph TB
    FnRouter["Network.Router.FnRouter&lt;T&gt;"]
    RouterArgs["Router.Args&lt;T&gt;"]
    
    subgraph "Router Arguments"
        Input["input: string"]
        NetworkArg["network: NetworkRun&lt;T&gt;"]
        StackArg["stack: Agent&lt;T&gt;[]"]
        CallCount["callCount: number"]
        LastResult["lastResult?: AgentResult"]
    end
    
    subgraph "Return Types"
        AgentReturn["Agent&lt;T&gt;"]
        AgentArray["Agent&lt;T&gt;[]"]
        RoutingAgent["RoutingAgent&lt;T&gt;"]
        Undefined["undefined"]
    end
    
    FnRouter --> RouterArgs
    RouterArgs --> Input
    RouterArgs --> NetworkArg
    RouterArgs --> StackArg
    RouterArgs --> CallCount
    RouterArgs --> LastResult
    
    FnRouter --> AgentReturn
    FnRouter --> AgentArray
    FnRouter --> RoutingAgent
    FnRouter --> Undefined
```

Sources: [packages/agent-kit/src/network.ts:296-329]()

### Default Routing Agent

When no custom router is provided, networks use the `getDefaultRoutingAgent()` which creates a `RoutingAgent` that selects agents based on their descriptions and available tools.

```mermaid
graph LR
    GetDefaultRoutingAgent["getDefaultRoutingAgent()"]
    CreateRoutingAgent["createRoutingAgent()"]
    SelectAgentTool["select_agent tool"]
    OnRoute["lifecycle.onRoute"]
    
    GetDefaultRoutingAgent --> CreateRoutingAgent
    CreateRoutingAgent --> SelectAgentTool
    CreateRoutingAgent --> OnRoute
    
    subgraph "Tool Handler Logic"
        ToolHandler["handler: ({name}, {network})"]
        AgentLookup["network.agents.get(name)"]
        AgentValidation["agent validation"]
    end
    
    SelectAgentTool --> ToolHandler
    ToolHandler --> AgentLookup
    AgentLookup --> AgentValidation
```

Sources: [packages/agent-kit/src/network.ts:150-248]()

## State Management in Networks

Networks maintain state through the `State<T>` class, which provides both conversation history and typed data storage. The state is accessible to agents and routers throughout the execution flow.

### State Integration Points

```mermaid
graph TB
    NetworkState["Network.state: State&lt;T&gt;"]
    
    subgraph "State Access Points"
        RouterAccess["router({network})"]
        AgentAccess["agent.run({network})"]
        ToolAccess["tool.handler(input, {network})"]
    end
    
    subgraph "State Operations"
        ReadData["network.state.data"]
        WriteData["network.state.data.property = value"]
        AppendResult["network.state.appendResult(call)"]
        FormatHistory["network.state.formatHistory()"]
    end
    
    NetworkState --> RouterAccess
    NetworkState --> AgentAccess
    NetworkState --> ToolAccess
    
    RouterAccess --> ReadData
    AgentAccess --> ReadData
    ToolAccess --> WriteData
    NetworkState --> AppendResult
    NetworkState --> FormatHistory
```

Sources: [packages/agent-kit/src/network.ts:35](), [packages/agent-kit/src/state.ts:36-96]()

## Example Implementation

The SWE-bench example demonstrates a practical network implementation with state-based routing between planning and editing agents.

### SWE-bench Network Structure

```mermaid
graph TB
    CodeWritingNetwork["codeWritingNetwork"]
    AgentStateInterface["AgentState interface"]
    
    subgraph "Network Configuration"
        Name["name: 'Code writing network'"]
        NetworkAgents["agents: [planningAgent, editingAgent]"]
        DefaultModelConfig["defaultModel: anthropic('claude-3-5-haiku-latest')"]
        DefaultRouterConfig["defaultRouter: ({network}) => Agent | undefined"]
    end
    
    subgraph "State Properties"
        Repo["repo: string"]
        Done["done: boolean"]
        Files["files?: string[]"]
        Plan["plan?: PlanObject"]
    end
    
    subgraph "Router Logic"
        CheckDone["if (network.state.data.done)"]
        CheckPlan["if (network.state.data.plan === undefined)"]
        ReturnPlanning["return planningAgent"]
        ReturnEditing["return editingAgent"]
        ReturnUndefined["return undefined"]
    end
    
    CodeWritingNetwork --> AgentStateInterface
    CodeWritingNetwork --> Name
    CodeWritingNetwork --> NetworkAgents
    CodeWritingNetwork --> DefaultModelConfig
    CodeWritingNetwork --> DefaultRouterConfig
    
    AgentStateInterface --> Repo
    AgentStateInterface --> Done
    AgentStateInterface --> Files
    AgentStateInterface --> Plan
    
    DefaultRouterConfig --> CheckDone
    CheckDone --> ReturnUndefined
    DefaultRouterConfig --> CheckPlan
    CheckPlan --> ReturnPlanning
    CheckPlan --> ReturnEditing
```

Sources: [examples/swebench/networks/codeWritingNetwork.ts:6-67]()

### Agent State Management

The network maintains typed state that agents modify through tools, enabling deterministic routing decisions based on workflow progress.

| State Property | Type | Purpose |
|----------------|------|---------|
| `repo` | `string` | Repository name being modified |
| `done` | `boolean` | Workflow completion flag |
| `files` | `string[]` | Available repository files |
| `plan` | `PlanObject` | Generated modification plan |

Sources: [examples/swebench/networks/codeWritingNetwork.ts:6-30]()

## Network Lifecycle Management

Networks support iteration limits and agent availability checks to prevent infinite loops and ensure proper workflow termination.

### Iteration Control

```mermaid
graph LR
    MaxIter["maxIter: number"]
    Counter["_counter: number"]
    ExecutionLoop["while (_stack.length > 0 && (_counter < maxIter))"]
    AgentCall["agent.run()"]
    IncrementCounter["_counter += 1"]
    
    MaxIter --> ExecutionLoop
    Counter --> ExecutionLoop
    ExecutionLoop --> AgentCall
    AgentCall --> IncrementCounter
    IncrementCounter --> ExecutionLoop
```

Sources: [packages/agent-kit/src/network.ts:50](), [packages/agent-kit/src/network.ts:387-409]()