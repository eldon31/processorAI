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

- [Using MCP as tools](#using-mcp-as-tools)
- [mcpServers reference](#mcpservers-reference)
- [MCP.Server](#mcp-server)
- [TransportSSE](#transportsse)
- [TransportWebsocket](#transportwebsocket)
- [Examples](#examples)

Advanced Patterns

# MCP as tools

Provide your Agents with MCP Servers as tools

AgentKit supports using [Claude's Model Context Protocol](https://modelcontextprotocol.io/) as tools.

Using MCP as tools allows you to use any MCP server as a tool in your AgentKit network, enabling your Agent

to access thousands of pre-built tools to interact with. Our integration with

[Smithery](https://smithery.ai/) provides a registry of MCP servers for common use cases, with more than 2,000 servers across multiple use cases.

## [ Using MCP as tools](#using-mcp-as-tools)

AgentKit supports configuring MCP servers via `Streamable HTTP` , `SSE` or `WS` transports:

Self-hosted MCP server Smithery MCP server Copy Ask AI

```
import { createAgent } from "@inngest/agent-kit" ;

const neonAgent = createAgent ({
name: "neon-agent" ,
system: `You are a helpful assistant that help manage a Neon account.
` ,
mcpServers: [
{
name: "neon" ,
transport: {
type: "ws" ,
url: "ws://localhost:8080" ,
},
},
],
});
```

## [ mcpServers reference](#mcpservers-reference)

The `mcpServers` parameter allows you to configure Model Context Protocol servers that provide tools for your agent. AgentKit automatically fetches the list of available tools from these servers and makes them available to your agent.

[](#param-mcp-servers) mcpServers MCP.Server[] An array of MCP server configurations.

### [ MCP.Server](#mcp-server)

[](#param-name) name string required A short name for the MCP server (e.g., "github", "neon"). This name is used to

namespace tools for each MCP server. Tools from this server will be prefixed

with this name (e.g., "neon-createBranch").

[](#param-transport) transport TransportSSE | TransportWebsocket required The transport configuration for connecting to the MCP server.

### [ TransportSSE](#transportsse)

[](#param-type) type 'sse' required Specifies that the transport is Server-Sent Events.

[](#param-url) url string required The URL of the SSE endpoint.

[](#param-event-source-init) eventSourceInit EventSourceInit Optional configuration for the EventSource.

[](#param-request-init) requestInit RequestInit Optional request configuration.

### [ TransportWebsocket](#transportwebsocket)

[](#param-type-1) type 'ws' required Specifies that the transport is WebSocket.

[](#param-url-1) url string required The WebSocket URL of the MCP server.

## [ Examples](#examples)

## [Neon Assistant Agent (using MCP)](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme)

[This examples shows how to use the](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme) [Neon MCP Smithery Server](https://smithery.ai/server/neon/) [to build a Neon Assistant Agent that can help you manage your Neon databases. Agents Tools Network Integrations Code-based Router](https://github.com/inngest/agent-kit/tree/main/examples/mcp-neon-agent/#readme)

[Deterministic state routing Previous](\advanced-patterns\routing) [Human in the Loop Next](\advanced-patterns\human-in-the-loop)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.