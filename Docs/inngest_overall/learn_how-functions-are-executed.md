#### On this page

- [How Inngest functions are executed: Durable Execution](\docs\learn\how-functions-are-executed#how-inngest-functions-are-executed-durable-execution)
- [What is Durable Execution?](\docs\learn\how-functions-are-executed#what-is-durable-execution)
- [How Inngest functions work](\docs\learn\how-functions-are-executed#how-inngest-functions-work)
- [How steps are executed](\docs\learn\how-functions-are-executed#how-steps-are-executed)
- [Initial execution](\docs\learn\how-functions-are-executed#initial-execution)
- [Secondary executions - Memoization of steps](\docs\learn\how-functions-are-executed#secondary-executions-memoization-of-steps)
- [Error handling](\docs\learn\how-functions-are-executed#error-handling)
- [Conclusion](\docs\learn\how-functions-are-executed#conclusion)
- [Further reading](\docs\learn\how-functions-are-executed#further-reading)

Features [Inngest Functions](\docs\features\inngest-functions) [Steps &amp; Workflows](\docs\features\inngest-functions\steps-workflows)

# How Inngest functions are executed: Durable Execution

One of the core features of Inngest is Durable Execution. Durable Execution allows your functions to be fault-tolerant and resilient to failures. The end result is that your code, and therefore, your overall application, is more reliable.

This page covers what Durable Execution is, how it works, and how it works with Inngest functions.

## [What is Durable Execution?](\docs\learn\how-functions-are-executed#what-is-durable-execution)

Durable Execution is a fault-tolerant approach to executing code that is achieved by handling failures and interruptions gracefully with automatic retries and state persistence. This means that your code can continue to run even if there are issues like network failures, timeouts, infrastructure outages, and other transient errors.

Key aspects of Durable Execution include:

- **State persistance** - Function state is persisted outside of the function execution context. This enables function execution to be resumed from the point of failure on the same *or* different infrastructure.
- **Fault-tolerance** - Errors or exceptions are caught by the execution layer and are automatically retried. Retry behavior can be customized to handle the accepted number of retries and handle different types of errors.

In practice, Durable Execution is implemented in the form of "durable functions," sometimes also called "durable workflows." Durable functions can throw errors or exceptions and automatically retry, resuming execution from the point of failure. Durable functions are designed to be long-running and stateful, meaning that they can persist state across function invocations and retries.

## [How Inngest functions work](\docs\learn\how-functions-are-executed#how-inngest-functions-work)

Inngest functions are durable: they throw errors or exceptions, automatically retry from the point of failure, and can be stateful and long-running.

Inngest functions use " **Steps** " to define the execution flow of a function. Each step:

- Is a unit of work that can be run and retried independently.
- Captures any error or exception thrown within it.
- Will not be re-executed if it has already been successfully executed.
- Returns state ( *data* ) that can be used by subsequent steps.
- Can be executed in parallel or sequentially, depending on the function's configuration.

Complex functions can consist of many steps. This allows a long-running function to be broken down into smaller, more manageable units of work. As each step is retried independently, and the function can be resumed from the point of failure, avoiding unnecessary re-execution of work.

In comparison, some Durable Execution systems modify the runtime environment to persist state or interrupt errors or exceptions. Inngest SDKs are written using standard language primitives, which enables Inngest functions to run in any environment or runtime - including serverless environments - without modification.

### [How steps are executed](\docs\learn\how-functions-are-executed#how-steps-are-executed)

Inngest functions are defined with a series of steps that define the execution flow of the function. Each step is defined with a unique ID and a function that defines the work to be done. The data returned can be used by subsequent steps.

Inngest functions execute incrementally, *step by step* . As a function is executed, the results of each step are returned to Inngest and persisted in a managed function state store. The steps that successfully executed are [*memoized*](https://en.wikipedia.org/wiki/Memoization) . The function then resumes, skipping any steps that have already been completed and the SDK injects the data returned by the previous step into the function.

Each step in your function is executed as **a separate HTTP request** . Any non-deterministic logic (such as DB calls or API calls) must be placed within a `step.run()` call to ensure it executes efficiently and correctly in the context of the execution model.

Let's look at an example of a function and walk through how it is executed:

Copy Copied

```
const fn = inngest .createFunction (
{ id : "import-contacts" } ,
{ event : "contacts/csv.uploaded" } ,
// The function handler:
async ({ event , step }) => {
const rows = await step .run ( "parse-csv" , async () => {
return await parseCsv ( event . data .fileURI);
});

const normalizedRows = await step .run ( "normalize-raw-csv" , async () => {
const normalizedColumnMapping = getNormalizedColumnNames ();
return normalizeRows (rows , normalizedColumnMapping);
});

const results = await step .run ( "input-contacts" , async () => {
return await importContacts (normalizedRows);
});

return { results };
}
);
```

### [Initial execution](\docs\learn\how-functions-are-executed#initial-execution)

1. When the function is first called, the *function handler* is called with only the `event` payload data sent.
2. When the first step is discovered, the `"parse-csv"` step is run. As the step has not been executed before, the step's code (the callback function) is run and the result is captured.
3. The function does not continue executing beyond this step. Each SDK uses a different method to interrupt the function execution before running any more code in your function handler.
4. Internally, the step's ID ( `"parse-csv"` ) is hashed as the state identifier to be used in future executions. Additionally, the steps' index ( `0` in this case) is also included in the result.
5. The result is sent back to Inngest and persisted in the function state store.

### [Secondary executions - Memoization of steps](\docs\learn\how-functions-are-executed#secondary-executions-memoization-of-steps)

Each of the subsequent steps leverages the state of previous executions and memoization. Here's how it works:

6. The function is re-executed, this time with the `event` payload data and the state of the previous execution in JSON.
7. The next step is discovered ( `"parse-csv"` ).
8. The previous result is found in the state of previous executions. Internally, the SDK uses the hash of the step name to look up the result in the state data.
9. The step's code is not executed, instead the SDK injects the result into the return value of `step.run` , (in this example, the data will be returned as `rows` ).
10. The function continues execution until the next step is discovered ( `"normalize-raw-csv"` ).
11. The step's code is executed and the result is returned to Inngest (in the same approach as steps 2-5 above).

### [Error handling](\docs\learn\how-functions-are-executed#error-handling)

Some steps may throw errors or exceptions during execution. Here's how error handling works within function execution:

12. If an error occurs during the execution of a step (for example, `"input-contacts"` ), the function is interrupted and the error is caught by the SDK.
13. The error is serialized and returned to Inngest. The number of attempts are logged and the error is persisted in the function state store.
14. Depending on the number of attempts configured for the function, the function may be retried (see: [Error handling](\docs\guides\error-handling) ):
    - If the the function *has not* exhausted the number of attempts, the function is re-executed from the point of failure with the state of all previous step executions. The step is re-executed and follows the same process as above (see: steps 6-11).
    - If the function *has* exhausted the number of attempts, the function is re-executed with the error thrown. The function can then catch and handle the error as desired (see: [Handling a failing step](\docs\guides\error-handling#handling-a-failing-step) ).

To learn about how determinism is handled and how you can version functions, read the [Versioning long running functions](\docs\learn\versioning) guide.

## [Conclusion](\docs\learn\how-functions-are-executed#conclusion)

Inngest functions use steps and memoization to execute functions incrementally and durably. This approach ensures that functions are fault-tolerant and resilient to failures. By breaking down functions into steps, Inngest functions can be retried and resumed from the point of failure. This approach ensures that your code is more reliable and can handle transient errors gracefully.

## [Further reading](\docs\learn\how-functions-are-executed#further-reading)

More information on Durable Execution in Inngest:

- Blog post: ["How we built a fair multi-tenant queuing system"](\blog\building-the-inngest-queue-pt-i-fairness-multi-tenancy)
- Blog post: ["Debouncing in Queueing Systems: Optimizing Efficiency in Asynchronous Workflows"](\blog\debouncing-in-queuing-systems-optimizing-efficiency-in-async-workflows)
- Blog post: ["Accidentally Quadratic: Evaluating trillions of event matches in real-time"](\blog\accidentally-quadratic-evaluating-trillions-of-event-matches-in-real-time)
- Blog post: ["Queues aren't the right abstraction"](\blog\queues-are-no-longer-the-right-abstraction)