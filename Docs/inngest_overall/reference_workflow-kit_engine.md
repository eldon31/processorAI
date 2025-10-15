#### On this page

- [Using the workflow engine](\docs\reference\workflow-kit\engine#using-the-workflow-engine)
- [Configure](\docs\reference\workflow-kit\engine#configure)

References [Workflow Kit](\docs\reference\workflow-kit)

# Using the workflow engine

The workflow `Engine` is used to run a given [workflow instance](\docs\reference\workflow-kit\workflow-instance) within an Inngest Function:

### src/inngest/workflow.ts

Copy Copied

```
import { Engine , type Workflow } from "@inngest/workflow-kit" ;

import { inngest } from "./client" ;
import { actions } from "./actions" ;
import { loadWorkflowInstanceFromEvent } from "./loaders" ;

const workflowEngine = new Engine ({
actions : actionsWithHandlers ,
loader : (event) => {
return loadWorkflowInstanceFromEvent (event);
} ,
});

export default inngest .createFunction (
{ id : "blog-post-workflow" } ,
{ event : "blog-post.updated" } ,
async ({ event , step }) => {
// When `run` is called,
//  the loader function is called with access to the event
await workflowEngine .run ({ event , step });
}
);
```

## [Configure](\docs\reference\workflow-kit\engine#configure)

- Name `actions` Type EngineAction[] Required optional Description See [the](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action) [`EngineAction[]`](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action) [reference](\docs\reference\workflow-kit\actions#passing-actions-to-the-workflow-engine-engine-action) .
- Name `loader` Type function Required optional Description An async function receiving the [`event`](\docs\reference\functions\create#event) as unique argument and returning a valid [`Workflow`](\docs\reference\workflow-kit\workflow-instance) [instance](\docs\reference\workflow-kit\workflow-instance) object.
- Name `disableBuiltinActions` Type boolean Required optional Description For selectively adding built-in actions, set this to true and expose the actions you want via the [`<Provider>`](\docs\reference\workflow-kit\components-api) `availableActions` prop.