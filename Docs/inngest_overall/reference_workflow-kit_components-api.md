#### On this page

- [Components API (React)](\docs\reference\workflow-kit\components-api#components-api-react)
- [Usage](\docs\reference\workflow-kit\components-api#usage)
- [Reference](\docs\reference\workflow-kit\components-api#reference)
- [&lt;Provider&gt;](\docs\reference\workflow-kit\components-api#provider)

References [Workflow Kit](\docs\reference\workflow-kit)

# Components API (React)

The [`@inngest/workflow-kit`](https://npmjs.com/package/@inngest/workflow-kit) package provides a set of React components, enabling you to build a workflow editor UI in no time!

workflow-kit-announcement-video-loop.gif

<!-- image -->

## [Usage](\docs\reference\workflow-kit\components-api#usage)

### src/components/my-workflow-editor.ts

Copy Copied

```
import { useState } from "react" ;
import { Editor , Provider , Sidebar , type Workflow } from "@inngest/workflow-kit/ui" ;

// import `PublicEngineAction[]`
import { actionsDefinitions } from "@/inngest/actions-definitions" ;

// NOTE - Importing CSS from JavaScript requires a bundler plugin like PostCSS or CSS Modules
import "@inngest/workflow-kit/ui/ui.css" ;
import "@xyflow/react/dist/style.css" ;

export const MyWorkflowEditor = ({ workflow } : { workflow : Workflow }) => {
const [ workflowDraft , updateWorkflowDraft ] =
useState < typeof workflow>(workflow);

return (
< Provider
workflow = {workflowDraft}
trigger = {{ event : { name : 'blog-post.updated' } }}
availableActions = {actionsDefinitions}
onChange = {updateWorkflowDraft}
>
< Editor >
< Sidebar position = "right" ></ Sidebar >
</ Editor >
</ Provider >
);
};
```

## [Reference](\docs\reference\workflow-kit\components-api#reference)

### [&lt;Provider&gt;](\docs\reference\workflow-kit\components-api#provider)

`<Provider>` is a [Controlled Component](https://react.dev/learn/sharing-state-between-components#controlled-and-uncontrolled-components) , watching the `workflow={}` to update.

Make sure to updated `workflow={}` based on the updates received via `onChange={}` .

- Name `workflow` Type Workflow Required required Description A [Workflow instance object](\docs\reference\workflow-kit\workflow-instance) .
- Name `trigger` Type object Required required Description An object with a `name: string` property [representing an event name](\docs\reference\functions\create#trigger) .
- Name `availableActions` Type PublicEngineAction[] Required optional Description See [the](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action) [`PublicEngineActionEngineAction[]`](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action) [reference](\docs\reference\workflow-kit\actions#passing-actions-to-the-react-components-public-engine-action) .
- Name `onChange` Type function Required required Description A callback function, called after each `workflow` changes.
- Name `{children}` Type React.ReactNode Required required Description The `<Provider>` component should always get the following tree as children:

Copy Copied

```
< Editor >
< Sidebar position = "right" ></ Sidebar >
</ Editor >
```