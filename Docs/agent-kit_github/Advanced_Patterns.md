This document covers sophisticated patterns and architectural approaches for building complex multi-agent AI systems with AgentKit. These patterns enable advanced orchestration, external integrations, and human collaboration within agent workflows.

The patterns covered here include autonomous agent routing, external system integration via Model Context Protocol (MCP), human-in-the-loop workflows, and complex state management strategies. For specific implementation details on human workflow integration, see [Human-in-the-Loop](#5.1). For external tool server integration, see [MCP Integration](#5.2).

## Router Agent Patterns

Router Agents provide autonomous decision-making capabilities for agent orchestration. Unlike function-based routers that use predetermined logic, Router Agents leverage LLM reasoning to dynamically select the next agent based on current context.

### Autonomous Agent Orchestration

```mermaid
graph TB
    subgraph "Autonomous Routing System"
        UserInput["User Input"]
        RouterAgent["createRoutingAgent()"]
        SelectTool["select_agent Tool"]
        
        subgraph "Task Agents"
            PlannerAgent["plannerAgent"]
            EditorAgent["editorAgent"]
            AnalysisAgent["analysisAgent"]
        end
        
        subgraph "Router Logic"
            SystemPrompt["Dynamic System Prompt"]
            AgentSelection["Agent Selection Logic"]
            FinishedCheck["Finished Check"]
        end
        
        NetworkState["Network State"]
    end
    
    UserInput --> RouterAgent
    RouterAgent --> SystemPrompt
    SystemPrompt --> SelectTool
    SelectTool --> AgentSelection
    AgentSelection --> PlannerAgent
    AgentSelection --> EditorAgent
    AgentSelection --> AnalysisAgent
    AgentSelection --> FinishedCheck
    
    PlannerAgent --> NetworkState
    EditorAgent --> NetworkState
    AnalysisAgent --> NetworkState
    NetworkState --> RouterAgent
    
    FinishedCheck --> RouterAgent
```

Router Agents are created using `createRoutingAgent()` and implement the `onRoute` lifecycle hook to determine execution flow. The router evaluates network state and selects appropriate task agents until completion criteria are met.

**Sources:** [docs/reference/network-router.mdx:77-147](), [docs/guided-tour/ai-agents.mdx:275-361]()

### Router Agent Implementation Pattern

```mermaid
graph LR
    subgraph "Router Agent Components"
        SystemFunc["system: async function"]
        SelectAgentTool["select_agent Tool"]
        OnRouteHook["onRoute lifecycle"]
        ToolChoice["tool_choice: 'select_agent'"]
    end
    
    subgraph "Network Integration"
        AvailableAgents["network.availableAgents()"]
        AgentsMap["network.agents.get()"]
        NetworkState["network.state"]
    end
    
    subgraph "Execution Flow"
        ToolCall["Tool Call Result"]
        AgentName["Selected Agent Name"]
        Termination["undefined | Agent[]"]
    end
    
    SystemFunc --> AvailableAgents
    SelectAgentTool --> AgentsMap
    OnRouteHook --> ToolCall
    ToolCall --> AgentName
    AgentName --> Termination
    
    ToolChoice --> SelectAgentTool
```

The `createRoutingAgent()` function combines agent capabilities with routing logic through specific lifecycle hooks and tool definitions.

**Sources:** [docs/reference/network-router.mdx:79-147](), [docs/guided-tour/ai-agents.mdx:280-361]()

## Multi-Model Network Architecture

AgentKit supports heterogeneous model configurations within a single network, enabling specialized model selection for different agent roles.

### Model Provider Coordination

| Component | Model Configuration | Use Case |
|-----------|-------------------|----------|
| `defaultModel` | Network-wide fallback | Router agents, model-less agents |
| Agent `model` | Agent-specific override | Specialized capabilities |
| Router `model` | Routing decisions | Planning and orchestration |

```mermaid
graph TB
    subgraph "Multi-Model Network"
        DefaultModel["defaultModel: openai()"]
        
        subgraph "Specialized Agents"
            SearchAgent["searchAgent: defaultModel"]
            SummaryAgent["summaryAgent: anthropic()"]
            RouterAgent["routingAgent: model override"]
        end
        
        subgraph "Model Providers"
            OpenAI["OpenAI GPT-4"]
            Anthropic["Anthropic Claude"]
            Gemini["Google Gemini"]
        end
    end
    
    DefaultModel --> SearchAgent
    DefaultModel --> RouterAgent
    SummaryAgent --> Anthropic
    SearchAgent --> OpenAI
    RouterAgent --> OpenAI
```

Each agent can specify its own model configuration, allowing networks to leverage different model strengths for specific tasks.

**Sources:** [docs/concepts/networks.mdx:90-113]()

## State-Based Coordination Patterns

Advanced state management enables complex agent coordination through shared data structures and conversation history.

### State Management Architecture

```mermaid
graph TB
    subgraph "Network State System"
        ConversationHistory["conversation: Message[]"]
        KeyValueStore["kv: Map<string, any>"]
        TypedData["Typed State Schema"]
        
        subgraph "State Operations"
            StateRead["state.kv.get()"]
            StateWrite["state.kv.set()"]
            HistoryAccess["state.messages"]
        end
        
        subgraph "Agent Coordination"
            RouterDecision["Router State Check"]
            ToolStateUpdate["Tool State Mutation"]
            AgentContext["Agent Context Access"]
        end
    end
    
    ConversationHistory --> HistoryAccess
    KeyValueStore --> StateRead
    KeyValueStore --> StateWrite
    
    RouterDecision --> StateRead
    ToolStateUpdate --> StateWrite
    AgentContext --> HistoryAccess
```

State coordination enables deterministic routing decisions and persistent context across agent interactions.

**Sources:** [docs/concepts/networks.mdx:179-196](), [docs/advanced-patterns/human-in-the-loop.mdx:84-86]()

## External System Integration

AgentKit integrates with external systems through multiple patterns including MCP servers, Inngest orchestration, and custom tool implementations.

### Integration Architecture Overview

```mermaid
graph TB
    subgraph "AgentKit Core"
        CreateAgent["createAgent()"]
        CreateNetwork["createNetwork()"]
        CreateTool["createTool()"]
    end
    
    subgraph "External Integrations"
        MCPServers["MCP Servers"]
        SmitheryRegistry["Smithery Registry"]
        InngestPlatform["Inngest Platform"]
        CustomAPIs["Custom APIs"]
    end
    
    subgraph "Integration Methods"
        MCPConfig["mcpServers config"]
        StepContext["step context"]
        ToolHandlers["Tool handlers"]
        WaitForEvent["step.waitForEvent()"]
    end
    
    CreateAgent --> MCPConfig
    CreateNetwork --> InngestPlatform
    CreateTool --> ToolHandlers
    
    MCPConfig --> MCPServers
    MCPConfig --> SmitheryRegistry
    StepContext --> WaitForEvent
    WaitForEvent --> InngestPlatform
    ToolHandlers --> CustomAPIs
```

Integration patterns provide agents with extended capabilities through external tool servers and orchestration platforms.

**Sources:** [docs/integrations/smithery.mdx:146-154](), [docs/advanced-patterns/human-in-the-loop.mdx:24-47]()

## Event-Driven Workflow Patterns

Complex workflows can be implemented using Inngest's event-driven architecture combined with AgentKit's agent orchestration.

### Event-Driven Agent Execution

```mermaid
sequenceDiagram
    participant TriggerEvent as "Trigger Event"
    participant InngestFunction as "inngest.createFunction()"
    participant NetworkRun as "network.run()"
    participant WaitForEvent as "step.waitForEvent()"
    participant ResponseEvent as "Response Event"
    participant ToolHandler as "Tool Handler"
    
    TriggerEvent->>InngestFunction: "app/support.ticket.created"
    InngestFunction->>NetworkRun: Execute agent network
    NetworkRun->>WaitForEvent: Tool requires human input
    WaitForEvent-->>ResponseEvent: Wait for "developer.response"
    ResponseEvent->>ToolHandler: Process response
    ToolHandler->>NetworkRun: Continue execution
    NetworkRun->>InngestFunction: Return result
```

Event-driven patterns enable long-running workflows with human interaction points and external system coordination.

**Sources:** [docs/advanced-patterns/human-in-the-loop.mdx:154-178](), [docs/advanced-patterns/human-in-the-loop.mdx:32-36]()

## Tool Integration Patterns

Advanced tool patterns enable sophisticated agent capabilities through external system integration and custom implementations.

### Tool Architecture Components

```mermaid
graph TB
    subgraph "Tool System"
        CreateTool["createTool()"]
        ToolHandler["handler function"]
        ToolParams["parameters: z.object()"]
        
        subgraph "Context Access"
            StepContext["{ step }"]
            NetworkContext["{ network }"]
            AgentContext["{ agent }"]
        end
        
        subgraph "Tool Categories"
            FileSystemTools["File System Tools"]
            MCPTools["MCP Tools"]
            APITools["API Integration Tools"]
            HumanLoopTools["Human-in-Loop Tools"]
        end
    end
    
    CreateTool --> ToolHandler
    CreateTool --> ToolParams
    ToolHandler --> StepContext
    ToolHandler --> NetworkContext
    
    StepContext --> HumanLoopTools
    NetworkContext --> FileSystemTools
    NetworkContext --> APITools
    MCPTools --> CreateTool
```

Tool patterns provide structured interfaces for agent-environment interaction with proper context management and error handling.

**Sources:** [docs/advanced-patterns/human-in-the-loop.mdx:15-47](), [docs/guided-tour/ai-agents.mdx:143-216]()

## Lifecycle Management Patterns

Advanced agent lifecycle management enables sophisticated coordination and monitoring capabilities.

### Agent Lifecycle Hooks

| Hook | Purpose | Use Cases |
|------|---------|-----------|
| `onRoute` | Router agent decisions | Agent selection logic |
| `beforeInference` | Pre-execution setup | Context preparation |
| `afterInference` | Post-execution handling | Result processing |
| `onToolCall` | Tool execution control | Validation, logging |

```mermaid
graph LR
    subgraph "Lifecycle Flow"
        BeforeInference["beforeInference"]
        Inference["Model Inference"]
        ToolCalls["Tool Execution"]
        AfterInference["afterInference"]
        OnRoute["onRoute (Router)"]
    end
    
    subgraph "Hook Capabilities"
        ContextPrep["Context Preparation"]
        ResultProcessing["Result Processing"]
        ToolValidation["Tool Validation"]
        RouteDecision["Route Decision"]
    end
    
    BeforeInference --> ContextPrep
    Inference --> ToolCalls
    ToolCalls --> ToolValidation
    AfterInference --> ResultProcessing
    OnRoute --> RouteDecision
```

Lifecycle hooks enable fine-grained control over agent execution flow and provide extension points for custom logic.

**Sources:** [docs/reference/network-router.mdx:120-137](), [docs/guided-tour/ai-agents.mdx:347-361]()