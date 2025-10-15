##### Changelog

- [Changelog](\changelog\overview)

close

Changelog

# Changelog

Recent releases, new features, and fixes.

[](#2025-03-11) 2025-03-11 v0.5.0

- Introducing support for [Grok models](\reference\model-grok)
- Adding support for [Gemini latest models](\reference\model-gemini)

[](#2025-03-06) 2025-03-06 v0.4.0

- Add support for model hyper params (ex: temperature, top\_p, etc)
    - Breaking change: `anthropic() max_tokens` options has been moved in `defaultParameters`
- Add support OpenAI o3-mini, gpt-4.5, and more
- [Integration with Browserbase](\integrations\browserbase)

[](#2025-02-19) 2025-02-19 v0.3.0

- remove `server` export to allow non-Node runtimes
- allow tools with no parameters
- [Integration with E2B Code Interpreter](\integrations\e2b)

[](#2025-01-29) 2025-01-29 v0.2.2

- Allow specifying [Inngest functions as tools](\advanced-patterns\multi-steps-tools)
- Inngest is now an optional dependency

[](#2025-01-16) 2025-01-16 v0.2.1

- Fixed OpenAI adapter to safely parse non-string tool return values for Function calling
- Various documentation improvements

[](#2025-01-16-2) 2025-01-16 v0.2.0

- Added support for Model Context Protocol (MCP) tool calling
- Added basic development server
- Fixed Anthropic model to ensure proper message handling
- Improved code samples and concepts documentation
- Added comprehensive quick start guide
- Fixed bundling issues
- Improved model exports for better discovery
- Various cross-platform compatibility improvements

[](#2024-12-19) 2024-12-19 v0.1.2

- Fixed state reference handling in agents
- Updated SWEBench example configuration
- Various stability improvements

[](#2024-12-19-2) 2024-12-19 v0.1.1

- Fixed network to agent state propagation in run
- Improved git clone handling in SWEBench example
- Various minor improvements

[](#2024-12-19-3) 2024-12-19 v0.1.0

- Initial release of AgentKit
- Core framework implementation with lifecycle management
- Support for OpenAI and Anthropic models
- Network and Agent architecture with state management
- ReAct implementation for networks
- Tool calling support for agents
- Added SWEBench example
- Comprehensive documentation structure
- Stepless model/network/agent instantiations

⌘ I

Assistant Responses are generated using AI and may contain mistakes.