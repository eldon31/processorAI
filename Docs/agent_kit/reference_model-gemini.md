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

# Gemini Model

Configure Google Gemini as your model provider

The `gemini` function configures Google's Gemini as your model provider.

Copy Ask AI

```
import { createAgent , gemini } from "@inngest/agent-kit" ;

const agent = createAgent ({
name: "Code writer" ,
system: "You are an expert TypeScript programmer." ,
model: gemini ({ model: "gemini-pro" }),
});
```

## [ Configuration](#configuration)

The `gemini` function accepts a model name string or a configuration object:

Copy Ask AI

```
const agent = createAgent ({
model: gemini ({
model: "gemini-pro" ,
apiKey: process . env . GOOGLE_API_KEY ,
baseUrl: "https://generativelanguage.googleapis.com/v1/" ,
defaultParameters: {
generationConfig: {
temperature: 1.5 ,
},
},
}),
});
```

### [ Options](#options)

[](#param-model) model string required ID of the model to use. See the [model endpoint](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)

[compatibility](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)

table for details on which models work with the Gemini API.

[](#param-api-key) apiKey string The Google API key to use for authenticating your request. By default we'll

search for and use the

`GOOGLE_API_KEY` environment variable.

[](#param-base-url) baseUrl string default: "https://generativelanguage.googleapis.com/v1/" The base URL for the Gemini API.

[](#param-default-parameters) defaultParameters object The default parameters to use for the model. See Gemini's [`models.generateContent`](https://ai.google.dev/api/generate-content#method:-models.generatecontent) [reference](https://ai.google.dev/api/generate-content#method:-models.generatecontent) .

### [ Available Models](#available-models)

Gemini Copy Ask AI

```
"gemini-1.5-flash"
"gemini-1.5-flash-8b"
"gemini-1.5-pro"
"gemini-1.0-pro"
"text-embedding-004"
"aqa"
```

For the latest list of available models, see [Google's Gemini model overview](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) .

## [ Limitations](#limitations)

Gemini models do not currently support function without parameters.

[Anthropic Model Previous](\reference\model-anthropic) [Grok Model Next](\reference\model-grok)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.