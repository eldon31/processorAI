AgentKit is a TypeScript framework for creating and orchestrating AI agents and AI workflows. Built with orchestration at its core, AgentKit enables developers to build, test, and deploy reliable multi-agent AI applications at scale. The framework integrates seamlessly with Inngest for serverless orchestration, providing fault-tolerant execution and local development tools with built-in tracing.

## What is AgentKit?

AgentKit provides simple and composable primitives to build everything from basic support agents to complex multi-agent systems. It supports multiple AI model providers including OpenAI, Anthropic, Gemini, and Grok, while offering powerful tool-building APIs with support for the Model Context Protocol (MCP).

Key capabilities include:

- **Multi-agent orchestration** with deterministic routing and shared state
- **Inngest integration** for serverless orchestration and fault-tolerant execution  
- **Tool ecosystem** with MCP support and external service integrations
- **Local development** with live tracing and input/output logs via Inngest Dev Server
- **Flexible routing** from code-based to fully autonomous agent-based routing

This overview covers the framework's fundamental architecture and components. For detailed installation instructions, see [Installation and Setup](#1.1). For in-depth exploration of core concepts, see [Core Concepts](#2).

Sources: [packages/agent-kit/package.json:2-4](), [docs/overview.mdx:8-22](), [README.md:1-16]()

## Core Architecture

**AgentKit Framework Components**

AgentKit is built around several key components that work together to enable flexible AI agent applications:

```mermaid
graph TD
    subgraph "AgentKit Core (@inngest/agent-kit)"
        createAgent["createAgent()"]
        createNetwork["createNetwork()"]
        createTool["createTool()"]
        createServer["createServer()"]
    end
    
    subgraph "Runtime Components"
        Agent["Agent Instance"]
        Network["Network Instance"]
        Tool["Tool Handler"]
        State["State Object"]
        Router["Router Function"]
    end
    
    subgraph "External Integration"
        InngestPlatform["Inngest Platform"]
        MCPServers["MCP Servers"]
        AIModels["AI Model APIs"]
    end

    createAgent --> Agent
    createNetwork --> Network
    createTool --> Tool
    createServer --> InngestPlatform
    
    Network --> Agent
    Network --> Router
    Network --> State
    Agent --> Tool
    Agent --> AIModels
    Tool --> MCPServers
    Tool --> State
    Router --> Agent
```

Sources: [packages/agent-kit/package.json:36-52](), [README.md:15-24](), [docs/overview.mdx:53-65]()

### Key Components

Each component in the AgentKit framework serves a specific purpose:

| Component | Description |
|-----------|-------------|
| Agents | Core building blocks that use LLMs to perform tasks |
| Networks | Orchestrate multiple agents through defined workflows |
| State | Manages shared context and memory across agent interactions |
| Routers | Determine which agent to run next based on state and rules |
| Tools | Enable agents to perform actions and access external systems |
| Model Adapters | Connect to different LLM providers (OpenAI, Anthropic, etc.) |

Sources: [README.md:15-24](), [docs/overview.mdx:10-20]()

## AgentKit with Inngest Integration

**Network Execution Flow**

The following diagram illustrates how AgentKit components interact during execution, including Inngest integration:

```mermaid
sequenceDiagram
    participant Client
    participant createServer as "createServer()"
    participant InngestFunction as "Inngest Function"
    participant networkRun as "network.run()"
    participant Router as "router({ network })"
    participant Agent as "Agent.run()"
    participant ModelAdapter as "openai() / anthropic()"
    participant ToolHandler as "Tool.handler()"
    participant State as "network.state"

    Client->>createServer: HTTP Request
    createServer->>InngestFunction: Trigger event
    InngestFunction->>networkRun: Execute with input
    networkRun->>Router: Determine first agent
    Router-->>networkRun: Return agent instance
    
    loop Until router returns undefined
        networkRun->>Agent: Execute agent
        Agent->>ModelAdapter: LLM inference call
        ModelAdapter-->>Agent: Response with tool calls
        
        opt Tool Execution
            Agent->>ToolHandler: Execute tool
            ToolHandler->>State: Update shared state
            ToolHandler-->>Agent: Tool result
        end
        
        Agent->>State: Store conversation history
        Agent-->>networkRun: Return AgentResult
        networkRun->>Router: Determine next agent
        Router-->>networkRun: Return next agent (or undefined)
    end
    
    networkRun-->>InngestFunction: Final result
    InngestFunction-->>Client: Response
```

Sources: [README.md:96-105](), [examples/demo/inngest.ts:21-38](), [README.md:111-146]()

## AgentKit Ecosystem Integration

**Technology Stack and Service Integration**

This diagram shows how AgentKit integrates with external services and AI providers:

```mermaid
flowchart TB
    subgraph "Application Layer"
        ExpressApp["Express Server"]
        InngestFunction["inngest.createFunction()"]
        createServerAPI["createServer({ networks })"]
    end

    subgraph "AgentKit Framework"
        createAgent["createAgent({ mcpServers, tools })"]
        createNetwork["createNetwork({ agents, router })"]
        createTool["createTool({ handler })"]
        ModelAdapters["openai() / anthropic() / gemini() / grok()"]
        StateManagement["createState<T>() / network.state"]
    end

    subgraph "AI Model Providers"
        OpenAIAPI["OpenAI API"]
        AnthropicAPI["Anthropic API"]
        GeminiAPI["Google Gemini API"]
        GrokAPI["xAI Grok API"]
    end

    subgraph "External Integrations"
        MCPServers["MCP Servers\n(Model Context Protocol)"]
        InngestPlatform["Inngest Platform\n(Orchestration & Tracing)"]
        SmitheryRegistry["Smithery Tool Registry"]
    end

    ExpressApp --> createServerAPI
    createServerAPI --> InngestFunction
    InngestFunction --> createNetwork
    createNetwork --> createAgent
    createAgent --> createTool
    createAgent --> ModelAdapters
    createAgent --> MCPServers
    createNetwork --> StateManagement
    
    ModelAdapters --> OpenAIAPI
    ModelAdapters --> AnthropicAPI
    ModelAdapters --> GeminiAPI
    ModelAdapters --> GrokAPI
    
    createTool --> SmitheryRegistry
    InngestFunction --> InngestPlatform
```

Sources: [README.md:33-105](), [packages/agent-kit/package.json:54-63](), [README.md:96-105]()

## State-Based Routing Architecture

**Deterministic Routing with Shared State**

AgentKit provides deterministic routing through state-based coordination between network components:

```mermaid
flowchart TB
    subgraph "Network State Access"
        StateData["network.state.data<T>"]
        StateKV["network.state.kv"]
        StateResults["network.state.results"]
    end
    
    subgraph "State Consumers"
        RouterFunction["router({ network })"]
        AgentSystemPrompt["agent.system({ network })"]
        ToolHandler["tool.handler(input, { network })"]
        AgentLifecycle["agent.lifecycle.enabled({ network })"]
    end
    
    subgraph "State Updates"
        ToolMutation["tool.handler updates state"]
        ConversationHistory["Agent results stored"]
        TypedDataUpdate["Structured data mutations"]
    end

    StateData --> RouterFunction
    StateKV --> RouterFunction
    StateResults --> RouterFunction
    
    StateData --> AgentSystemPrompt
    StateKV --> AgentSystemPrompt
    
    StateData --> ToolHandler
    StateKV --> ToolHandler
    
    StateData --> AgentLifecycle
    StateKV --> AgentLifecycle
    
    ToolHandler --> ToolMutation
    AgentSystemPrompt --> ConversationHistory
    ToolMutation --> TypedDataUpdate
```

Sources: [README.md:111-146](), [docs/reference/state.mdx:1-113](), [README.md:147-298]()

## Multi-Agent Coordination Patterns

**Code-Based vs Agent-Based Routing**

AgentKit supports multiple coordination patterns for different use cases:

```mermaid
flowchart TD
    subgraph "Code-Based Routing"
        CodeRouter["router: ({ network }) => Agent"]
        StateLogic["if (!network.state.kv.has('plan'))"]
        DeterministicFlow["return planningAgent"]
        StateReactive["else return executionAgent"]
    end
    
    subgraph "Agent-Based Routing"
        RoutingAgent["createRoutingAgent({ onRoute })"]
        AgentDecision["LLM decides next agent"]
        OnRouteCallback["lifecycle.onRoute({ result })"]
        FlowControl["return [agentName] or undefined"]
    end
    
    subgraph "Shared State"
        NetworkState["network.state"]
        ConversationHistory["Message history"]
        TypedData["Typed application data"]
        KeyValue["Key-value storage"]
    end

    CodeRouter --> StateLogic
    StateLogic --> DeterministicFlow
    StateLogic --> StateReactive
    
    RoutingAgent --> AgentDecision
    AgentDecision --> OnRouteCallback
    OnRouteCallback --> FlowControl
    
    CodeRouter --> NetworkState
    RoutingAgent --> NetworkState
    NetworkState --> ConversationHistory
    NetworkState --> TypedData
    NetworkState --> KeyValue
```

Sources: [README.md:142-296](), [README.md:297-497]()

## Routing Mechanisms

AgentKit supports different routing strategies to control agent execution flow:

| Routing Type | Description | Use Case |
|--------------|-------------|----------|
| Code-based Routing | Uses programmatic logic to determine next agent | Precise control over agent flow |
| Agent-based Routing | Uses an AI agent to decide the next step | More autonomous, flexible workflows |
| State-based Routing | Routes based on the current state | Reactive workflows that adapt to context |

Sources: [README.md:111-146](), [README.md:147-497]()

## Basic Usage Example

Here's a simplified view of how the core components are used together:

```mermaid
flowchart LR
    subgraph "Basic AgentKit Usage"
        A["createAgent()"] --> B["Configure Tools"]
        A --> C["Set Model Adapter"]
        A --> D["Define System Prompt"]
        E["createNetwork()"] --> F["Add Agents"]
        E --> G["Define Router"]
        E --> H["Configure State"]
        I["network.run()"] --> J["Execute Workflow"]
    end
```

Sources: [README.md:80-105](), [docs/overview.mdx:78-118]()

## Supported Model Providers

AgentKit supports multiple LLM providers through its model adapter system:

| Provider | Models | Integration Method |
|----------|--------|-------------------|
| OpenAI | GPT-3.5, GPT-4o, etc. | `openai()` adapter |
| Anthropic | Claude 3 Opus, Sonnet, Haiku | `anthropic()` adapter |
| Google | Gemini | `gemini()` adapter |
| xAI | Grok | `grok()` adapter |

Sources: [README.md:80-105](), [packages/agent-kit/CHANGELOG.md:48-50]()

## Current Version and Status

AgentKit is currently at version 0.8.0, with recent updates including StreamableHttp support in MCP Client and improved concurrent server handling. The framework continues active development with focus on expanding model provider support, improving MCP integration, and enhancing the developer experience.

Recent additions include support for Gemini and Grok models, typed state management, and enhanced tool integration capabilities.

Sources: [packages/agent-kit/package.json:3](), [packages/agent-kit/CHANGELOG.md:3-12]()

For more information on how to get started with AgentKit, please see the [Quick Start Guide](#3.1). For detailed explanation of the core concepts, refer to the pages on [Agents](#2.1), [Networks](#2.2), [State Management](#2.3), [Routers](#2.4), [Tools](#2.5), and [Model Adapters](#2.6).