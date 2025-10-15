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

# OpenAI Model

Configure OpenAI as your model provider

The `openai` function configures OpenAI as your model provider.

Copy Ask AI

```
import { createAgent , openai } from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Code writer" ,
system: "You are an expert TypeScript programmer." ,
model: openai ({ model: "gpt-4" }),
});
```

## [ Configuration](#configuration)

The `openai` function accepts a model name string or a configuration object:

Copy Ask AI

```
const agent = createAgent ({
model: openai ({
model: "gpt-4" ,
apiKey: process . env . OPENAI_API_KEY ,
baseUrl: "https://api.openai.com/v1/" ,
defaultParameters: { temperature: 0.5 },
}),
});
```

### [ Options](#options)

[](#param-model) model string required ID of the model to use. See the [model endpoint](https://platform.openai.com/docs/models#model-endpoint-compatibility)

[compatibility](https://platform.openai.com/docs/models#model-endpoint-compatibility)

table for details on which models work with the Chat API.

[](#param-api-key) apiKey string The OpenAI API key to use for authenticating your request. By default we'll

search for and use the

`OPENAI_API_KEY` environment variable.

[](#param-base-url) baseUrl string default: "https://api.openai.com/v1/" The base URL for the OpenAI API.

[](#param-default-parameters) defaultParameters object The default parameters to use for the model (ex: `temperature` , `max_tokens` ,

etc).

### [ Available Models](#available-models)

OpenAI Copy Ask AI

```
"gpt-4o"
"chatgpt-4o-latest"
"gpt-4o-mini"
"gpt-4"
"o1-preview"
"o1-mini"
"gpt-3.5-turbo"
```

[Network Router Previous](\reference\network-router) [Anthropic Model Next](\reference\model-anthropic)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.