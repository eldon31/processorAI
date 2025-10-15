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
- [Limitations](#limitations)

Models

# Grok Model

Configure Grok as your model provider

The `grok` function configures Grok as your model provider.

Copy Ask AI

```
import { createAgent , grok } from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Code writer" ,
system: "You are an expert TypeScript programmer." ,
model: grok ({ model: "grok-4-latest" }),
});
```

## [ Configuration](#configuration)

The `grok` function accepts a model name string or a configuration object:

Copy Ask AI

```
const agent = createAgent ({
model: grok ({
model: "grok-4-latest" ,
apiKey: process . env . XAI_API_KEY ,
baseUrl: "https://api.x.ai/v1" ,
defaultParameters: { temperature: 0.5 },
}),
});
```

### [ Options](#options)

[](#param-model) model string required ID of the model to use. See the [xAI models list](https://docs.x.ai/docs/models) .

[](#param-api-key) apiKey string The xAI API key to use for authenticating your request. By default we'll

search for and use the

`XAI_API_KEY` environment variable.

[](#param-base-url) baseUrl string default: "https://api.x.ai/v1" The base URL for the xAI API.

[](#param-default-parameters) defaultParameters object The default parameters to use for the model (ex: `temperature` , `max_tokens` ,

etc).

### [ Available Models](#available-models)

Gemini Copy Ask AI

```
"grok-2-1212"
"grok-2"
"grok-2-latest"
"grok-3"
"grok-3-latest"
"grok-4"
"grok-4-latest";
```

For the latest list of available models, see [xAI's Grok model overview](https://docs.x.ai/docs/models) .

## [ Limitations](#limitations)

Grok models do not currently support strict function parameters.

[Gemini Model Previous](\reference\model-gemini) [useAgent Next](\reference\use-agent)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.