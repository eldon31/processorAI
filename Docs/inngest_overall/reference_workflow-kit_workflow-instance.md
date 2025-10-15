#### On this page

- [Workflow instance](\docs\reference\workflow-kit\workflow-instance#workflow-instance)
- [Workflow](\docs\reference\workflow-kit\workflow-instance#workflow)
- [WorkflowAction](\docs\reference\workflow-kit\workflow-instance#workflow-action)
- [WorkflowEdge](\docs\reference\workflow-kit\workflow-instance#workflow-edge)

References [Workflow Kit](\docs\reference\workflow-kit)

# Workflow instance

A workflow instance represents a user configuration of a sequence of [workflow actions](\docs\reference\workflow-kit\actions) , later provided to the [workflow engine](\docs\reference\workflow-kit\engine) for execution.

Example of a workflow instance object:

Copy Copied

```
{
"name" : "Generate social posts" ,
"edges" : [
{
"to" : "1" ,
"from" : "$source"
} ,
{
"to" : "2" ,
"from" : "1"
}
] ,
"actions" : [
{
"id" : "1" ,
"kind" : "generate_tweet_posts" ,
"name" : "Generate Twitter posts"
} ,
{
"id" : "2" ,
"kind" : "generate_linkedin_posts" ,
"name" : "Generate LinkedIn posts"
}
]
}
```

**How to use the workflow instance object**

Workflow instance objects are meant to be retrieved from the [`<Provider>`](\docs\reference\workflow-kit\components-api) Editor, stored in database and loaded into the [Workflow Engine](\docs\reference\workflow-kit\engine) using a loader.

Use this reference if you need to update the workflow instance between these steps.

## [Workflow](\docs\reference\workflow-kit\workflow-instance#workflow)

A Workflow instance in an object with the following properties:

- Name `name` Type string Required optional Description Name of the worklow configuration, provided by the end-user.
- Name `description` Type string Required optional Description description of the worklow configuration, provided by the end-user.
- Name `actions` Type WorkflowAction[] Required required Description See the [`WorkflowAction`](\docs\reference\workflow-kit\workflow-instance#workflow-action) reference below.
- Name `edges` Type WorkflowEdge[] Required required Description See the [`WorkflowEdge`](\docs\reference\workflow-kit\workflow-instance#workflow-edge) reference below.

## [WorkflowAction](\docs\reference\workflow-kit\workflow-instance#workflow-action)

`WorkflowAction` represent a step of the workflow instance linked to an defined [`EngineAction`](\docs\reference\workflow-kit\actions) .

- Name `id` Type string Required optional Description The ID of the action within the workflow instance. This is used as a reference and must be unique within the Instance itself.
- Name `kind` Type string Required required Description The action kind, used to look up the `EngineAction` definition.
- Name `name` Type string Required required Description Name is the human-readable name of the action.
- Name `description` Type string Required optional Description Description is a short description of the action.
- Name `inputs` Type object Required optional Description Inputs is a list of configured inputs for the EngineAction. The record key is the key of the EngineAction input name, and the value is the variable's value. This will be type checked to match the EngineAction type before save and before execution. Ref inputs for interpolation are `"!ref($.<path>)"` , eg. `"!ref($.event.data.email)"`

## [WorkflowEdge](\docs\reference\workflow-kit\workflow-instance#workflow-edge)

A `WorkflowEdge` represents the link between two `WorkflowAction` .

- Name `from` Type string Required required Description The `WorkflowAction.id` of the source action. `"$source"` is a reserved value used as the starting point of the worklow instance.
- Name `to` Type string Required required Description The `WorkflowAction.id` of the next action.