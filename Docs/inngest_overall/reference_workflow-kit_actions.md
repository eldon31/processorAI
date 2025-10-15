#### On this page

- [Creating workflow actions](\docs\reference\workflow-kit\actions#creating-workflow-actions)
- [Passing actions to the React components: PublicEngineAction[]](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action)
- [Passing actions to the Workflow Engine: EngineAction[]](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action)
- [handler() function argument properties](\docs\reference\workflow-kit\actions#handler-function-argument-properties)

References [Workflow Kit](\docs\reference\workflow-kit)

# Creating workflow actions

The [`@inngest/workflow-kit`](https://npmjs.com/package/@inngest/workflow-kit) package provides a [workflow engine](\docs\reference\workflow-kit\engine) , enabling you to create workflow actions on the back end. These actions are later provided to the front end so end-users can build their own workflow instance using the [`<Editor />`](\docs\reference\workflow-kit\components-api) .

Workflow actions are defined as two objects using the [`EngineAction`](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action) (for the back-end) and [`PublicEngineAction`](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action) (for the front-end) types.

src/inngest/actions-definition.ts src/inngest/actions.ts

Copy Copied

```
import { type PublicEngineAction } from "@inngest/workflow-kit" ;

export const actionsDefinition : PublicEngineAction [] = [
{
kind : "grammar_review" ,
name : "Perform a grammar review" ,
description : "Use OpenAI for grammar fixes" ,
} ,
];
```

In the example above, the `actionsDefinition` array would be passed via props to the [`<Provider />`](\docs\reference\workflow-kit\components-api) while the `actions` are passed to the [`Engine`](\docs\reference\workflow-kit\engine) .

**Why do I need two types of actions?**

The actions need to be separated into 2 distinct objects to avoid leaking the action handler implementations and dependencies into the front end:

## [Passing actions to the React components: PublicEngineAction[]](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action)

- Name `kind` Type string Required required Description Kind is an enum representing the action's ID. This is not named as "id" so that we can keep consistency with the WorkflowAction type.
- Name `name` Type string Required required Description Name is the human-readable name of the action.
- Name `description` Type string Required optional Description Description is a short description of the action.
- Name `icon` Type string Required optional Description Icon is the name of the icon to use for the action. This may be an URL, or an SVG directly.

## [Passing actions to the Workflow Engine: EngineAction[]](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action)

**Note** : Inherits `PublicEngineAction` properties.

- Name `handler` Type function Required optional Description The handler is your code that runs whenever the action occurs. Every function handler receives a single object argument which can be deconstructed. The key arguments are `event` and `step` .

### src/inngest/actions.ts

Copy Copied

```
import { type EngineAction } from "@inngest/workflow-kit" ;

import { actionsDefinition } from "./actions-definition" ;

export const actions : EngineAction [] = [
{
// Add a Table of Contents
... actionsDefinition[ 0 ] ,
handler : async ({ event , step , workflow , workflowAction , state }) => {
// ...
}
} ,
];
```

The details of the `handler()` **unique argument's properties** can be found below:

### [handler() function argument properties](\docs\reference\workflow-kit\actions#handler-function-argument-properties)

- Name `event` Type TriggerEvent Required optional Description See the Inngest Function handler [`event`](\docs\reference\functions\create#event) [argument property definition](\docs\reference\functions\create#event) .
- Name `step` Type Step Required optional Description See the Inngest Function handler [`step`](\docs\reference\functions\create#step) [argument property definition](\docs\reference\functions\create#step) .
- Name `workflow` Type Workflow Required optional Description See the [Workflow instance format](\docs\reference\workflow-kit\workflow-instance) .
- Name `workflowAction` Type WorkflowAction Required optional Description WorkflowAction is the action being executed, with fully interpolated inputs. Key properties are:
- Name `state` Type object Required optional Description State represents the current state of the workflow, with previous action's outputs recorded as key-value pairs.