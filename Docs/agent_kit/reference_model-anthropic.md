##### Introduction

- [Introduction](\reference\introduction)

##### Agent

- [createAgent](\reference\create-agent)
- [createTool](\reference\create-tool)

##### Network

- [createNetwork](\reference\create-network)
- [createState](\reference\state)
- [Router](\reference\network-router)

##### Models

- [OpenAI Model](\reference\model-openai)
- [Anthropic Model](\reference\model-anthropic)
- [Gemini Model](\reference\model-gemini)
- [Grok Model](\reference\model-grok)

##### Streaming

- [useAgent](\reference\use-agent)

close

On this page

- [Configuration](#configuration)
- [Options](#options)
- [Available Models](#available-models)

Models

# Anthropic Model

Configure Anthropic as your model provider

The `anthropic` function configures Anthropic's Claude as your model provider.

Copy Ask AI

```
import { createAgent , anthropic } from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Code writer" ,
system: "You are an expert TypeScript programmer." ,
model: anthropic ({
model: "claude-3-opus" ,
// Note: max_tokens is required for Anthropic models
defaultParameters: { max_tokens: 4096 },
}),
});
```

## [ Configuration](#configuration)

The `anthropic` function accepts a model name string or a configuration object:

Copy Ask AI

```
const agent = createAgent ({
model: anthropic ({
model: "claude-3-opus" ,
apiKey: process . env . ANTHROPIC_API_KEY ,
baseUrl: "https://api.anthropic.com/v1/" ,
betaHeaders: [ "computer-vision" ],
defaultParameters: { temperature: 0.5 , max_tokens: 4096 },
}),
});
```

**Note:** **`defaultParameters.max_tokens`** **is required.**

### [ Options](#options)

[](#param-model) model string required ID of the model to use. See the [model endpoint](https://docs.anthropic.com/en/docs/about-claude/models)

[compatibility](https://docs.anthropic.com/en/docs/about-claude/models)

table

for details on which models work with the Anthropic API.

[](#param-max-tokens) max\_tokens number deprecated **This option has been moved to the** **`defaultParameters`** **option.**

The maximum number of tokens to generate before stopping.

[](#param-api-key) apiKey string The Anthropic API key to use for authenticating your request. By default we'll

search for and use the

`ANTHROPIC_API_KEY` environment variable.

[](#param-beta-headers) betaHeaders string[] The beta headers to enable, eg. for computer use, prompt caching, and so on.

[](#param-base-url) baseUrl string default: "https://api.anthropic.com/v1/" The base URL for the Anthropic API.

[](#param-default-parameters) defaultParameters object required The default parameters to use for the model (ex: `temperature` , `max_tokens` ,

etc).

**Note:** **`defaultParameters.max_tokens`** **is required.**

### [ Available Models](#available-models)

Anthropic Copy Ask AI

```
"claude-3-5-haiku-latest"
"claude-3-5-haiku-20241022"
"claude-3-5-sonnet-latest"
"claude-3-5-sonnet-20241022"
"claude-3-5-sonnet-20240620"
"claude-3-opus-latest"
"claude-3-opus-20240229"
"claude-3-sonnet-20240229"
"claude-3-haiku-20240307"
"claude-2.1"
"claude-2.0"
"claude-instant-1.2"
```

[OpenAI Model Previous](\reference\model-openai) [Gemini Model Next](\reference\model-gemini)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.