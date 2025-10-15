#### On this page

- [Python middleware lifecycle](\docs\reference\python\middleware\lifecycle#python-middleware-lifecycle)
- [Hook reference](\docs\reference\python\middleware\lifecycle#hook-reference)
- [transform\_input](\docs\reference\python\middleware\lifecycle#transform-input)
- [before\_memoization](\docs\reference\python\middleware\lifecycle#before-memoization)
- [after\_memoization](\docs\reference\python\middleware\lifecycle#after-memoization)
- [before\_execution](\docs\reference\python\middleware\lifecycle#before-execution)
- [after\_execution](\docs\reference\python\middleware\lifecycle#after-execution)
- [transform\_output](\docs\reference\python\middleware\lifecycle#transform-output)
- [before\_response](\docs\reference\python\middleware\lifecycle#before-response)
- [before\_send\_events](\docs\reference\python\middleware\lifecycle#before-send-events)
- [after\_send\_events](\docs\reference\python\middleware\lifecycle#after-send-events)

References [Python SDK](\docs\reference\python) [Middleware](\docs\reference\python\middleware\overview)

# Python middleware lifecycle

The order of middleware lifecycle hooks is as follows:

1. [transform\_input](\docs\reference\python\middleware\lifecycle#transform-input)
2. [before\_memoization](\docs\reference\python\middleware\lifecycle#before-memoization)
3. [after\_memoization](\docs\reference\python\middleware\lifecycle#after-memoization)
4. [before\_execution](\docs\reference\python\middleware\lifecycle#before-execution)
5. [after\_execution](\docs\reference\python\middleware\lifecycle#after-execution)
6. [transform\_output](\docs\reference\python\middleware\lifecycle#transform-output)
7. [before\_response](\docs\reference\python\middleware\lifecycle#before-response)

All of these functions may be called multiple times in a single function run. For example, if your function has 2 steps then all of the hooks will run 3 times (once for each step and once for the function).

Additionally, there are two hooks when sending events:

1. [before\_send\_events](\docs\reference\python\middleware\lifecycle#before-send-events)
2. [after\_send\_events](\docs\reference\python\middleware\lifecycle#after-send-events)

## [Hook reference](\docs\reference\python\middleware\lifecycle#hook-reference)

### [transform\_input](\docs\reference\python\middleware\lifecycle#transform-input)

Called when receiving a request from Inngest and before running any functions. Commonly used to mutate data sent by Inngest, like decryption.

Arguments

- Name `ctx` Type Context Required required Description `ctx` argument passed to Inngest functions.
- Name `function` Type Function Required required Description Inngest function object.
- Name `steps` Type StepMemos Required required Description Memoized step data.

### [before\_memoization](\docs\reference\python\middleware\lifecycle#before-memoization)

Called before checking memoized step data.

### [after\_memoization](\docs\reference\python\middleware\lifecycle#after-memoization)

Called after exhausting memoized step data.

### [before\_execution](\docs\reference\python\middleware\lifecycle#before-execution)

Called before executing "new code". For example, `before_execution` is called after returning the last memoized step data, since function-level code after that step is "new".

### [after\_execution](\docs\reference\python\middleware\lifecycle#after-execution)

Called after executing "new code".

### [transform\_output](\docs\reference\python\middleware\lifecycle#transform-output)

Called after a step or function returns. Commonly used to mutate data before sending it back to Inngest, like encryption.

Arguments

- Name `result` Type TransformOutputResult Required required Description Show nested properties

### [before\_response](\docs\reference\python\middleware\lifecycle#before-response)

Called before sending a response back to Inngest.

### [before\_send\_events](\docs\reference\python\middleware\lifecycle#before-send-events)

Called before sending events to Inngest.

Arguments

- Name `events` Type list[Event] Required required Description Events to send.

### [after\_send\_events](\docs\reference\python\middleware\lifecycle#after-send-events)

Called after sending events to Inngest.

Arguments

- Name `result` Type SendEventsResult Required required Description Show nested properties