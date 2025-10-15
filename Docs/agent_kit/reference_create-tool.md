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

- [Options](#options)
- [Handler Function](#handler-function)
- [lifecycle](#lifecycle)

Agent

# createTool

Provide tools to an agent

Tools are defined using the `createTool` function.

Copy Ask AI

```
import { createTool } from '@inngest/agent-kit' ;

const tool = createTool ({
name: 'write-file' ,
description: 'Write a file to disk with the given contents' ,
parameters: {
type: 'object' ,
properties: {
path: {
type: 'string' ,
description: 'The path to write the file to' ,
},
contents: {
type: 'string' ,
description: 'The contents to write to the file' ,
},
},
required: [ 'path' , 'contents' ],
},
handler : async ({ path , contents }, { agent , network }) => {
await fs . writeFile ( path , contents );
return { success: true };
},
});
```

## [ Options](#options)

[](#param-name) name string required The name of the tool. Used by the model to identify which tool to call.

[](#param-description) description string required A clear description of what the tool does. This helps the model understand when and how to use the tool.

[](#param-parameters) parameters JSONSchema | ZodType required A JSON Schema object or Zod type that defines the parameters the tool accepts. This is used to validate the model's inputs and provide type safety.

[](#param-handler) handler function required The function that executes when the tool is called. It receives the validated parameters as its first argument and a context object as its second argument.

[](#param-strict) strict boolean default: true Option to disable strict validation of the tool parameters.

[](#param-lifecycle) lifecycle Lifecycle Lifecycle hooks that can intercept and modify inputs and outputs throughout the stages of tool execution.

### [ Handler Function](#handler-function)

The handler function receives two arguments:

1. `input` : The validated parameters matching your schema definition
2. `context` : An object containing:
    - `agent` : The Agent instance that called the tool
    - `network` : The network instance, providing access to the [`network.state`](\reference\state) .

Example handler with full type annotations:

Copy Ask AI

```
import { createTool } from '@inngest/agent-kit' ;

const tool = createTool ({
name: 'write-file' ,
description: 'Write a file to disk with the given contents' ,
parameters: {
type: 'object' ,
properties: {
path: { type: 'string' },
contents: { type: 'string' },
},
},
handler : async ({ path , contents }, { agent , network }) => {
await fs . writeFile ( path , contents );
network . state . fileWritten = true ;
return { success: true };
},
});
```

### [ lifecycle](#lifecycle)

[](#param-on-start) onStart function

Called before the tool handler is executed. The `onStart` hook can be used to:

- Modify input parameters before they are passed to the handler
- Prevent the tool from being called by throwing an error

[](#param-on-finish) onFinish function

Called after the tool handler has completed. The `onFinish` hook can be used to:

- Modify the result before it is returned to the agent
- Perform cleanup operations

onStart onFinish Copy Ask AI

```
const tool = createTool ({
name: 'write-file' ,
lifecycle: {
onStart : ({ parameters }) => {
// Validate or modify parameters before execution
return parameters ;
},
},
});
```

[createAgent Previous](\reference\create-agent) [createNetwork Next](\reference\create-network)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.